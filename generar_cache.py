#!/usr/bin/env python3
"""
Script para generar el cache de respaldo — ejecutar desde la raíz del proyecto.
"""
import sys
from pathlib import Path

# Agregar el directorio backend al path para que los imports internos funcionen
sys.path.insert(0, str(Path(__file__).parent / "backend"))

# Ahora importar directamente (sin prefijo backend.)
from classifier import clasificar_estudiante
from ia_client import generar_explicacion
from fallback import guardar_en_cache

import asyncio
import json
import os

DATA_PATH = Path(__file__).parent / "data" / "estudiantes.json"
CACHE_PATH = Path(__file__).parent / "cache" / "respuestas_ia.json"


async def main():
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        print("❌ GEMINI_API_KEY no configurada.")
        print("   Obtén una gratis en: https://aistudio.google.com/app/apikey")
        print("   export GEMINI_API_KEY=tu-key-aqui")
        sys.exit(1)

    print(f"\n🚀 Generando cache de fallback (Art. VIII §6.1)")
    print(f"   Dataset: {DATA_PATH}")
    print(f"   Cache: {CACHE_PATH}")
    print("-" * 60)

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    ok = 0
    for est in dataset:
        clasificacion = clasificar_estudiante(est)
        nivel = clasificacion["nivel"]

        if nivel == "⚪":
            print(f"  ⚪ {est['id']} — {est['nombre']}: Sin datos → omitido.")
            continue

        print(f"  ⏳ {est['id']} — {est['nombre']} ({nivel})...", end=" ", flush=True)

        resultado = await generar_explicacion(
            id_estudiante=est["id"],
            nombre=est["nombre"],
            grado=est["grado"],
            nivel_riesgo=nivel,
            motivos=clasificacion["motivos"],
            variables_faltantes=clasificacion["variables_faltantes"],
        )

        if resultado.get("origen_ia") == "vivo":
            guardar_en_cache(est["id"], resultado["explicacion"], resultado["recomendacion"])
            print("✅")
            ok += 1
        else:
            print(f"❌ {resultado.get('origen_ia')}")

        await asyncio.sleep(0.5)

    print(f"\n✅ Cache generado: {ok} entradas.")
    print(f"   Archivo: {CACHE_PATH}")


if __name__ == "__main__":
    asyncio.run(main())
