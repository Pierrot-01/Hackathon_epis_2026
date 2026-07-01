"""
API Backend — FastAPI.
Implementa §7 de la Especificación Técnica.

Endpoints:
  GET /api/estudiantes          → Lista todos los estudiantes clasificados
  GET /api/estudiantes/{id}     → Detalle de un estudiante
  GET /api/health               → Estado del servidor
"""

import json
import os
import asyncio
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

from classifier import clasificar_estudiante
from ia_client import generar_explicacion

# --- Rutas ---
BASE_DIR = Path(__file__).parent.parent
DATA_PATH = BASE_DIR / "data" / "estudiantes.json"
FRONTEND_DIR = BASE_DIR / "frontend"

# --- App ---
app = FastAPI(
    title="Vanguardia EPIS — API de Detección de Riesgo Escolar",
    version="1.0.0",
    description="Backend para detección temprana de riesgo académico. Constitución v2.1.",
)

# CORS: permite acceso desde el frontend servido como archivo local o desde el mismo servidor
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Modelos Pydantic (§7.1) ---
class EstudianteResultado(BaseModel):
    id: str
    nombre: str
    grado: str
    nivel_riesgo: str
    motivos: list[str]
    variables_faltantes: list[str]
    explicacion: Optional[str]
    recomendacion: Optional[str]
    origen_ia: str  # "vivo" | "fallback" | "error_sin_cache" | "no_aplica"

    # Campos originales del dataset (útiles para el frontend)
    asistencia_pct: Optional[float]
    notas_promedio: Optional[float]
    participacion: Optional[str]
    lengua_materna: Optional[str]
    observaciones: Optional[str]


# --- Cache en memoria por sesión (evita llamadas repetidas a la API durante la demo) ---
_resultados_cache: dict[str, EstudianteResultado] = {}


def cargar_dataset() -> list[dict]:
    """Carga y valida el dataset de estudiantes."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset no encontrado en {DATA_PATH}")

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


async def procesar_estudiante(est: dict) -> EstudianteResultado:
    """Clasifica un estudiante y obtiene su explicación de IA."""
    clasificacion = clasificar_estudiante(est)

    ia_result = await generar_explicacion(
        id_estudiante=est["id"],
        nombre=est["nombre"],
        grado=est["grado"],
        nivel_riesgo=clasificacion["nivel"],
        motivos=clasificacion["motivos"],
        variables_faltantes=clasificacion["variables_faltantes"],
    )

    return EstudianteResultado(
        id=est["id"],
        nombre=est["nombre"],
        grado=est["grado"],
        nivel_riesgo=clasificacion["nivel"],
        motivos=clasificacion["motivos"],
        variables_faltantes=clasificacion["variables_faltantes"],
        explicacion=ia_result.get("explicacion"),
        recomendacion=ia_result.get("recomendacion"),
        origen_ia=ia_result.get("origen_ia", "desconocido"),
        asistencia_pct=est.get("asistencia_pct"),
        notas_promedio=est.get("notas_promedio"),
        participacion=est.get("participacion"),
        lengua_materna=est.get("lengua_materna"),
        observaciones=est.get("observaciones"),
    )


# --- Endpoints ---

@app.get("/api/health")
def health_check():
    """Chequeo de estado del servidor."""
    return {"status": "ok", "version": "1.0.0"}


@app.get("/api/estudiantes", response_model=list[EstudianteResultado])
async def listar_estudiantes(force_refresh: bool = False):
    """
    Lista todos los estudiantes con su clasificación de riesgo y explicación de IA.
    
    - Primer llamado: procesa todos los estudiantes (llama a clasificador + IA).
    - Llamadas siguientes: retorna desde cache en memoria (a menos que force_refresh=True).
    """
    global _resultados_cache

    if _resultados_cache and not force_refresh:
        return list(_resultados_cache.values())

    dataset = cargar_dataset()

    # Procesar todos los estudiantes en paralelo
    tareas = [procesar_estudiante(est) for est in dataset]
    resultados = await asyncio.gather(*tareas)

    # Guardar en cache en memoria
    _resultados_cache = {r.id: r for r in resultados}

    return resultados


@app.get("/api/estudiantes/{id_estudiante}", response_model=EstudianteResultado)
async def obtener_estudiante(id_estudiante: str, force_refresh: bool = False):
    """
    Retorna el detalle de un estudiante específico.
    Si no está en cache, lo procesa individualmente.
    """
    global _resultados_cache

    if id_estudiante in _resultados_cache and not force_refresh:
        return _resultados_cache[id_estudiante]

    dataset = cargar_dataset()
    est = next((e for e in dataset if e["id"] == id_estudiante), None)

    if est is None:
        raise HTTPException(
            status_code=404,
            detail=f"Estudiante '{id_estudiante}' no encontrado en el dataset."
        )

    resultado = await procesar_estudiante(est)
    _resultados_cache[id_estudiante] = resultado
    return resultado


@app.get("/api/stats")
async def estadisticas():
    """Retorna estadísticas globales para el dashboard de administración."""
    global _resultados_cache

    if not _resultados_cache:
        # Si no hay cache, cargar sin IA para rapidez
        dataset = cargar_dataset()
        resultados_temp = []
        for est in dataset:
            clasificacion = clasificar_estudiante(est)
            resultados_temp.append(clasificacion["nivel"])
        niveles = resultados_temp
    else:
        niveles = [r.nivel_riesgo for r in _resultados_cache.values()]

    total = len(niveles)
    alto = niveles.count("🔴")
    medio = niveles.count("🟡")
    bajo = niveles.count("🟢")
    insuficiente = niveles.count("⚪")

    return {
        "total": total,
        "alto": alto,
        "medio": medio,
        "bajo": bajo,
        "insuficiente": insuficiente,
        "pct_alto": round(alto / total * 100, 1) if total > 0 else 0,
        "pct_medio": round(medio / total * 100, 1) if total > 0 else 0,
        "pct_bajo": round(bajo / total * 100, 1) if total > 0 else 0,
    }


# --- Servir el frontend como archivos estáticos ---
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

    @app.get("/")
    def root():
        return FileResponse(str(FRONTEND_DIR / "index.html"))

    @app.get("/{page}.html")
    def pagina(page: str):
        filepath = FRONTEND_DIR / f"{page}.html"
        if filepath.exists():
            return FileResponse(str(filepath))
        raise HTTPException(status_code=404, detail="Página no encontrada")


# --- Punto de entrada ---
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
