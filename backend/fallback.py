"""
Módulo de modo de respaldo (fallback).
Implementa el Artículo VIII §6 de la Especificación Técnica.

El cache se genera previamente con scripts/generar_cache.py.
Nunca contiene texto redactado manualmente — siempre proviene del modelo IA.
"""

import json
import os
from pathlib import Path

CACHE_PATH = Path(__file__).parent.parent / "cache" / "respuestas_ia.json"

_cache: dict = {}
_cache_cargado = False


def _cargar_cache() -> dict:
    """Carga el cache desde disco (lazy loading)."""
    global _cache, _cache_cargado
    if _cache_cargado:
        return _cache

    if CACHE_PATH.exists():
        try:
            with open(CACHE_PATH, "r", encoding="utf-8") as f:
                _cache = json.load(f)
            print(f"[Fallback] Cache cargado: {len(_cache)} entradas desde {CACHE_PATH}")
        except (json.JSONDecodeError, IOError) as e:
            print(f"[Fallback] Error al cargar cache: {e}")
            _cache = {}
    else:
        print(f"[Fallback] Cache no encontrado en {CACHE_PATH} — se generará en la primera ejecución con conexión.")
        _cache = {}

    _cache_cargado = True
    return _cache


def guardar_en_cache(id_estudiante: str, explicacion: str, recomendacion: str) -> None:
    """Guarda una respuesta en el cache local (la usa generar_cache.py)."""
    from datetime import datetime, timezone

    cache = _cargar_cache()
    cache[id_estudiante] = {
        "explicacion": explicacion,
        "recomendacion": recomendacion,
        "generado_en": datetime.now(timezone.utc).isoformat(),
    }

    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

    # Actualizar el cache en memoria
    global _cache
    _cache = cache


def obtener_fallback(id_estudiante: str) -> dict | None:
    """
    Intenta obtener respuesta cacheada para un estudiante.
    
    Returns:
        dict con explicacion, recomendacion y origen="fallback"
        None si no hay cache para ese estudiante
    """
    cache = _cargar_cache()
    entrada = cache.get(id_estudiante)

    if entrada:
        return {
            "explicacion": entrada["explicacion"],
            "recomendacion": entrada["recomendacion"],
            "origen_ia": "fallback",
            "generado_en": entrada.get("generado_en"),
        }
    return None


def respuesta_error_sin_cache() -> dict:
    """
    Respuesta de último recurso cuando no hay API ni cache.
    Art. VIII §6.2 — nunca se muestra un error crudo al docente.
    """
    return {
        "explicacion": "No se pudo generar la explicación en este momento.",
        "recomendacion": "Por favor, reintente más tarde o contacte al soporte técnico para revisión manual.",
        "origen_ia": "error_sin_cache",
    }
