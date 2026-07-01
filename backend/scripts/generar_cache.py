"""
Script de generación de cache de fallback.
Implementa §6.1 de la Especificación Técnica (Art. VIII §8.1).

Ejecutar ANTES de la demo con conexión real a la API:
    python scripts/generar_cache.py

Este script:
1. Carga los 15-20 estudiantes del dataset.
2. Clasifica cada uno con el motor de reglas.
3. Llama a la API de Anthropic para cada estudiante.
4. Guarda las respuestas en cache/respuestas_ia.json.

Las respuestas cacheadas son genuinamente generadas por el modelo IA
(no redactadas a mano), cumpliendo Art. VIII §8.1.1 y §8.1.2.
"""

import asyncio
import json
import sys
import os
from pathlib import Path

# Agregar el directorio backend al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.classifier import clasificar_estudiante
from backend.ia_client import generar_explicacion, SYSTEM_PROMPT
from backend.fallback import guardar_en_cache

DATA_PATH = Path(__file__).parent.parent / "data" / "estudiantes.json"
CACHE_PATH = Path(__file__).parent.parent / "cache" / "respuestas_ia.json"


async def generar_cache():
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print("❌ ERROR: ANTHROPIC_API_KEY no está configurada.")
        print("   Configura la variable de entorno antes de ejecutar este script:")
        print("   export ANTHROPIC_API_KEY=sk-ant-...")
        sys.exit(1)

    print(f"\n🚀 Iniciando generación de cache de fallback")
    print(f"   Dataset: {DATA_PATH}")
    print(f"   Cache destino: {CACHE_PATH}")
    print(f"   Modelo: claude-haiku-4-5")
    print("-" * 60)

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    ok = 0
    errores = 0

    for est in dataset:
        clasificacion = clasificar_estudiante(est)
        nivel = clasificacion["nivel"]

        # Los estudiantes con ⚪ no necesitan explicación de IA
        if nivel == "⚪":
            print(f"  ⚪ {est['id']} — {est['nombre']}: Dato insuficiente, se omite llamada a IA.")
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
            guardar_en_cache(
                est["id"],
                resultado["explicacion"],
                resultado["recomendacion"],
            )
            print(f"✅ Guardado.")
            ok += 1
        else:
            print(f"❌ Error: {resultado.get('origen_ia')}")
            errores += 1

        # Pequeña pausa para no saturar la API
        await asyncio.sleep(0.5)

    print("-" * 60)
    print(f"\n✅ Cache generado: {ok} entradas exitosas, {errores} errores.")
    print(f"   Archivo: {CACHE_PATH}")

    if errores > 0:
        print(f"\n⚠️  Hay {errores} estudiantes sin cache. Revisa tu API key y conexión.")


if __name__ == "__main__":
    asyncio.run(generar_cache())
