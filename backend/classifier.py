"""
Motor de clasificación de riesgo determinista.
Implementa el Artículo III de la Constitución y §4 de la Especificación Técnica.
"""

from typing import Optional

# --- Umbrales congelados (§4.1) ---
UMBRAL_ASISTENCIA_BAJO = 90    # >= 90 → 🟢
UMBRAL_ASISTENCIA_MEDIO = 75   # 75-89 → 🟡, <75 → 🔴

UMBRAL_NOTAS_BAJO = 13         # >= 13 → 🟢
UMBRAL_NOTAS_MEDIO = 11        # 11-12 → 🟡, <11 → 🔴

NIVEL_BAJO = "🟢"
NIVEL_MEDIO = "🟡"
NIVEL_ALTO = "🔴"
NIVEL_INSUFICIENTE = "⚪"

PARTICIPACION_VALIDAS = {"alta", "media", "baja"}


def evaluar_asistencia(valor: float) -> str:
    """Evalúa la asistencia porcentual y retorna el nivel de riesgo."""
    if valor >= UMBRAL_ASISTENCIA_BAJO:
        return NIVEL_BAJO
    elif valor >= UMBRAL_ASISTENCIA_MEDIO:
        return NIVEL_MEDIO
    else:
        return NIVEL_ALTO


def evaluar_notas(valor: float) -> str:
    """Evalúa el promedio de notas (escala vigesimal) y retorna el nivel de riesgo."""
    if valor >= UMBRAL_NOTAS_BAJO:
        return NIVEL_BAJO
    elif valor >= UMBRAL_NOTAS_MEDIO:
        return NIVEL_MEDIO
    else:
        return NIVEL_ALTO


def evaluar_participacion(valor: str) -> str:
    """
    Evalúa la participación cualitativa.
    Nota de diseño §4.1: participación nunca alcanza 🔴 de forma aislada.
    """
    if valor in ("alta", "media"):
        return NIVEL_BAJO
    else:  # "baja"
        return NIVEL_MEDIO


def construir_motivo(
    nivel_por_variable: dict,
    variables_faltantes: list,
    estudiante: dict
) -> list[str]:
    """
    Genera la lista de strings de trazabilidad visible (Art. II §2.3).
    Retorna una lista de mensajes cortos, uno por variable evaluada.
    """
    motivos = []

    if "asistencia" in nivel_por_variable:
        val = estudiante["asistencia_pct"]
        nivel = nivel_por_variable["asistencia"]
        umbral_txt = f"≥{UMBRAL_ASISTENCIA_BAJO}% para 🟢, ≥{UMBRAL_ASISTENCIA_MEDIO}% para 🟡"
        motivos.append(
            f"Asistencia: {val}% — nivel {nivel} (umbral 🟢 es ≥{UMBRAL_ASISTENCIA_BAJO}%)"
        )

    if "notas" in nivel_por_variable:
        val = estudiante["notas_promedio"]
        nivel = nivel_por_variable["notas"]
        motivos.append(
            f"Notas: {val} — nivel {nivel} (umbral 🟢 es ≥{UMBRAL_NOTAS_BAJO})"
        )

    if "participacion" in nivel_por_variable:
        val = estudiante["participacion"]
        nivel = nivel_por_variable["participacion"]
        motivos.append(
            f"Participación: {val} — nivel {nivel}"
        )

    for var in variables_faltantes:
        nombre_var = {
            "asistencia": "Asistencia",
            "notas": "Notas",
            "participacion": "Participación"
        }.get(var, var)
        motivos.append(f"{nombre_var}: sin dato — evaluado sin esta variable")

    return motivos


def normalizar_campo(estudiante: dict) -> dict:
    """
    Normaliza valores inválidos a None según §3.3.
    - asistencia_pct fuera de 0-100 → None
    - notas_promedio fuera de 0-20 → None
    - participacion con valor distinto a los 3 permitidos → None
    """
    e = dict(estudiante)

    if e.get("asistencia_pct") is not None:
        try:
            val = float(e["asistencia_pct"])
            if not (0 <= val <= 100):
                print(f"[WARN] {e['id']}: asistencia_pct={val} fuera de rango → se trata como None")
                e["asistencia_pct"] = None
            else:
                e["asistencia_pct"] = val
        except (TypeError, ValueError):
            e["asistencia_pct"] = None

    if e.get("notas_promedio") is not None:
        try:
            val = float(e["notas_promedio"])
            if not (0 <= val <= 20):
                print(f"[WARN] {e['id']}: notas_promedio={val} fuera de rango → se trata como None")
                e["notas_promedio"] = None
            else:
                e["notas_promedio"] = val
        except (TypeError, ValueError):
            e["notas_promedio"] = None

    if e.get("participacion") is not None:
        if e["participacion"] not in PARTICIPACION_VALIDAS:
            print(f"[WARN] {e['id']}: participacion='{e['participacion']}' inválida → se trata como None")
            e["participacion"] = None

    return e


def clasificar_estudiante(estudiante: dict) -> dict:
    """
    Clasifica el nivel de riesgo de un estudiante.
    Implementa el pseudocódigo del §4.2 (Art. III §3.2.1 y §3.3).

    Retorna dict con:
        - nivel: str (🟢 / 🟡 / 🔴 / ⚪)
        - motivos: list[str]  ← trazabilidad visible (Art. II §2.3)
        - variables_faltantes: list[str]
    """
    e = normalizar_campo(estudiante)

    variables_presentes = []
    variables_faltantes = []
    nivel_por_variable = {}

    # Paso 1: evaluar cada variable de forma aislada
    if e["asistencia_pct"] is not None:
        nivel_por_variable["asistencia"] = evaluar_asistencia(e["asistencia_pct"])
        variables_presentes.append("asistencia")
    else:
        variables_faltantes.append("asistencia")

    if e["notas_promedio"] is not None:
        nivel_por_variable["notas"] = evaluar_notas(e["notas_promedio"])
        variables_presentes.append("notas")
    else:
        variables_faltantes.append("notas")

    if e["participacion"] is not None:
        nivel_por_variable["participacion"] = evaluar_participacion(e["participacion"])
        variables_presentes.append("participacion")
    else:
        variables_faltantes.append("participacion")

    # Paso 2: sin ninguna variable disponible → ⚪ (Art. IX §9.3.2)
    if len(variables_presentes) == 0:
        return {
            "nivel": NIVEL_INSUFICIENTE,
            "motivos": ["Las 3 variables carecen de dato — requiere revisión manual del docente"],
            "variables_faltantes": variables_faltantes,
        }

    # Paso 3: regla del peor caso (Art. III §3.2.1)
    valores = list(nivel_por_variable.values())

    if NIVEL_ALTO in valores:
        # Alguna variable individual alcanza 🔴 → clasificación directa
        nivel_global = NIVEL_ALTO
    else:
        # Contar señales negativas (variables en 🟡)
        señales_negativas = sum(1 for v in valores if v == NIVEL_MEDIO)
        if señales_negativas == 0:
            nivel_global = NIVEL_BAJO
        elif señales_negativas == 1:
            nivel_global = NIVEL_MEDIO
        else:
            # 2+ señales negativas → 🔴 por acumulación
            nivel_global = NIVEL_ALTO

    motivos = construir_motivo(nivel_por_variable, variables_faltantes, e)

    return {
        "nivel": nivel_global,
        "motivos": motivos,
        "variables_faltantes": variables_faltantes,
    }


# --- Tests rápidos (ejecutar directamente para verificar) ---
if __name__ == "__main__":
    casos_prueba = [
        # (id, asistencia, notas, participacion, esperado)
        ("Caso 1 — Todo bien", 95, 15, "alta", "🟢"),
        ("Caso 2 — 1 señal 🟡", 80, 15, "alta", "🟡"),
        ("Caso 3 — 2 señales 🟡 → 🔴", 80, 11.5, "alta", "🔴"),
        ("Caso 4 — 1 var 🔴 directa", 60, 15, "alta", "🔴"),
        ("Caso 5 — Desempate peor caso", 95, 9, "alta", "🔴"),
        ("Caso 9 — Límite exacto asist", 90, 15, "alta", "🟢"),
        ("Caso 10 — Límite exacto notas", 95, 13, "alta", "🟢"),
    ]

    print("\n=== Tests Clasificador ===\n")
    todos_ok = True
    for nombre, asis, notas, partic, esperado in casos_prueba:
        est = {
            "id": "TEST",
            "asistencia_pct": asis,
            "notas_promedio": notas,
            "participacion": partic,
        }
        resultado = clasificar_estudiante(est)
        ok = resultado["nivel"] == esperado
        estado = "✅" if ok else "❌"
        print(f"{estado} {nombre}: {resultado['nivel']} (esperado {esperado})")
        if not ok:
            todos_ok = False
            print(f"   Motivos: {resultado['motivos']}")

    # Casos con datos faltantes
    est_falta1 = {"id": "T6", "asistencia_pct": 95, "notas_promedio": 15, "participacion": None}
    r6 = clasificar_estudiante(est_falta1)
    print(f"{'✅' if r6['nivel'] == '🟢' else '❌'} Caso 6 — Falta participacion: {r6['nivel']} (esperado 🟢)")
    print(f"   Faltantes: {r6['variables_faltantes']}")

    est_falta2 = {"id": "T7", "asistencia_pct": None, "notas_promedio": 15, "participacion": None}
    r7 = clasificar_estudiante(est_falta2)
    print(f"{'✅' if r7['nivel'] == '🟢' else '❌'} Caso 7 — Faltan 2 vars: {r7['nivel']} (esperado 🟢)")
    print(f"   Faltantes: {r7['variables_faltantes']}")

    est_falta3 = {"id": "T8", "asistencia_pct": None, "notas_promedio": None, "participacion": None}
    r8 = clasificar_estudiante(est_falta3)
    print(f"{'✅' if r8['nivel'] == '⚪' else '❌'} Caso 8 — Faltan 3 vars: {r8['nivel']} (esperado ⚪)")

    print(f"\n{'✅ Todos los tests pasaron!' if todos_ok else '❌ Hay fallos — revisar lógica'}")
