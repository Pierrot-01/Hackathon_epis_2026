"""
Cliente de IA Generativa — Google Gemini.
Implementa §5 de la Especificación Técnica (Art. II §2.2 y Art. IV).

División de responsabilidades:
  - La clasificación de riesgo la hace classifier.py (determinista, sin IA)
  - La explicación y recomendación la genera este módulo (IA generativa real)
"""

import json
import os
import asyncio
from typing import Optional

from google import genai
from google.genai import types

from fallback import obtener_fallback, respuesta_error_sin_cache, guardar_en_cache

# --- Configuración ---
MODEL = "gemini-2.0-flash"          # Rápido y gratuito para demo
MAX_TOKENS = 300
TIMEOUT_SEGUNDOS = 10.0             # Gemini es más rápido, ampliamos a 10s

# --- System Prompt fijo (§5.2) — Reglas de lenguaje (Art. IV) ---
SYSTEM_PROMPT = """Eres un asistente que ayuda a docentes de instituciones educativas rurales del Perú
a redactar explicaciones y recomendaciones de apoyo para estudiantes según su nivel
de riesgo académico.

Reglas obligatorias (no negociables):
1. NUNCA uses lenguaje que etiquete, culpabilice o estigmatice al estudiante.
   Prohibido: "problemático", "flojo", "en riesgo de fracaso", "mal alumno", etc.
2. El tono debe ser constructivo y orientado a una acción concreta del docente.
3. La explicación debe basarse ÚNICAMENTE en los motivos y datos entregados —
   no inventes datos que no se te dieron.
4. Si falta alguna variable, puedes mencionarlo con naturalidad, sin dramatizar.
5. La recomendación debe ser específica al caso, no un mensaje genérico.
6. Responde ÚNICAMENTE en JSON válido, sin texto adicional ni markdown,
   con este formato exacto:
   {"explicacion": "...", "recomendacion": "..."}
7. Cada campo debe tener máximo 2-3 frases.
8. Escribe en español peruano, con respeto y dignidad hacia el estudiante."""


def construir_user_prompt(
    nombre: str,
    grado: str,
    nivel_riesgo: str,
    motivos: list[str],
    variables_faltantes: list[str],
) -> str:
    """Construye el prompt dinámico por estudiante (§5.3)."""
    motivos_txt = "\n".join(f"- {m}" for m in motivos)
    faltantes_txt = ", ".join(variables_faltantes) if variables_faltantes else "ninguna"

    return f"""Nombre del estudiante: {nombre}
Grado: {grado}
Nivel de riesgo detectado: {nivel_riesgo}
Motivos de la clasificación:
{motivos_txt}
Variables sin dato: {faltantes_txt}

Genera la explicación y recomendación según las reglas del sistema."""


async def generar_explicacion(
    id_estudiante: str,
    nombre: str,
    grado: str,
    nivel_riesgo: str,
    motivos: list[str],
    variables_faltantes: list[str],
) -> dict:
    """
    Genera explicación y recomendación vía Google Gemini.

    Lógica de resiliencia (§6.2):
    1. Intenta llamada real con timeout.
    2. Si falla o timeout → activa fallback desde cache.
    3. Si tampoco hay cache → retorna mensaje de error sin stack trace.
    """
    # El estado ⚪ no requiere explicación de IA
    if nivel_riesgo == "⚪":
        return {
            "explicacion": None,
            "recomendacion": None,
            "origen_ia": "no_aplica",
        }

    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        print(f"[IA] GEMINI_API_KEY no configurada → fallback para {id_estudiante}")
        fallback = obtener_fallback(id_estudiante)
        if fallback:
            return fallback
        return respuesta_error_sin_cache()

    user_prompt = construir_user_prompt(nombre, grado, nivel_riesgo, motivos, variables_faltantes)

    try:
        client = genai.Client(api_key=api_key)

        # Llamada con timeout estricto
        response = await asyncio.wait_for(
            asyncio.get_event_loop().run_in_executor(
                None,
                lambda: client.models.generate_content(
                    model=MODEL,
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        max_output_tokens=MAX_TOKENS,
                        temperature=0.7,
                    ),
                )
            ),
            timeout=TIMEOUT_SEGUNDOS,
        )

        texto = response.text.strip()

        # Limpiar posible markdown de código que Gemini a veces añade
        if texto.startswith("```"):
            texto = texto.split("```")[1]
            if texto.startswith("json"):
                texto = texto[4:]
            texto = texto.strip()

        # Parseo JSON de la respuesta
        datos = json.loads(texto)
        explicacion = datos.get("explicacion", "")
        recomendacion = datos.get("recomendacion", "")

        if not explicacion or not recomendacion:
            raise ValueError("Campos vacíos en respuesta de IA")

        return {
            "explicacion": explicacion,
            "recomendacion": recomendacion,
            "origen_ia": "vivo",
        }

    except (asyncio.TimeoutError, Exception) as e:
        print(f"[IA] Fallo en llamada API para {id_estudiante}: {type(e).__name__}: {e}")
        print(f"[IA] Activando fallback para {id_estudiante}")

        fallback = obtener_fallback(id_estudiante)
        if fallback:
            return fallback

        return respuesta_error_sin_cache()
