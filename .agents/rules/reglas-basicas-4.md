---
trigger: always_on
---

# FASE 3 — ESPECIFICACIÓN TÉCNICA (BLUEPRINT) — v1
## Reto 2 — Educación: Detección Temprana de Riesgo Escolar
### Hackathon EPIS XXI · Categoría B — Vanguardia IA Generativa

**Basado en:** Fase 1 (Intent v2) + Fase 2 (Constitución v2.1)
**Regla de oro de esta fase:** todo lo aquí definido es lo que se programa. Si algo no está en este documento, no se improvisa en código — se vuelve a este documento y se cierra primero.

---

## 0. Trazabilidad Constitución → Especificación

| Artículo Constitución | Cómo se traduce en esta Especificación |
|---|---|
| Art. I (Propósito/Alcance) | §3 Esquema de datos, §7 API, límites explícitos en §12 |
| Art. II (IA real, trazabilidad visible) | §5 Motor de IA (contrato I/O), §8 Dashboard (bloque de trazabilidad) |
| Art. III (Clasificación, 3.2.1, 3.3) | §4 Lógica de clasificación (pseudocódigo exacto) |
| Art. IV (Dignidad) | §5.2 Prompt del sistema (reglas de lenguaje) |
| Art. V (Privacidad/datos ficticios) | §3.4 Dataset sintético |
| Art. VI (Accesibilidad) | §8 Dashboard (nota quechua), §2 Stack (offline-friendly) |
| Art. VII (Stack/tiempo) | §2 Stack tecnológico congelado |
| Art. VIII (Resiliencia/fallback) | §6 Modo de respaldo |
| Art. IX (Datos incompletos, 9.3) | §4.4 Reglas de datos faltantes/insuficientes |
| Art. X (Aceptación) | §10 Casos de prueba |
| Art. XI (Roles) | §11 Plan de implementación (asigna orden, no personas — ver pendiente) |

---

## 1. Arquitectura general

```
┌─────────────────────┐      ┌──────────────────────────┐      ┌───────────────────┐
│  Dataset ficticio    │      │   Backend (FastAPI)       │      │   Dashboard web    │
│  data/estudiantes    │─────▶│   1. Motor de reglas      │─────▶│   (HTML+JS+Tailwind)│
│  .json (15-20 regs)  │      │      (clasificación)      │      │                     │
└─────────────────────┘      │   2. Cliente IA generativa│      │  Tabla + detalle    │
                              │      (Anthropic API)      │      │  por estudiante     │
                              │   3. Módulo de fallback   │      └───────────────────┘
                              │      (cache/*.json)       │
                              └──────────────────────────┘
```

**Flujo end-to-end por estudiante:**
1. El backend lee el registro del estudiante desde el dataset.
2. El **motor de reglas** (determinista, sin IA) calcula el nivel de riesgo y las variables que lo motivaron (Art. III).
3. El backend arma un **prompt estructurado** con esos datos + nivel de riesgo y llama a la API de IA generativa para obtener explicación + recomendación.
4. Si la llamada falla o tarda > 6 s → se activa el **fallback** (Art. VIII) y se marca visiblemente.
5. El frontend consulta un único endpoint (`GET /api/estudiantes`) y renderiza la tabla + panel de detalle.

---

## 2. Stack tecnológico (congelado para Fase 3 — cierra el pendiente del Art. VII §7.3)

| Capa | Decisión | Justificación |
|---|---|---|
| Backend | **Python 3.11 + FastAPI** | Rápido de escribir, tipado con Pydantic (fuerza el contrato de datos), server async nativo para llamadas a la API de IA sin bloquear. |
| Almacenamiento dataset | **Archivo JSON local** (`data/estudiantes.json`) | No se requiere BD (Art. VII §7.2). JSON permite `null`/"N/D" nativos para Art. IX. |
| Cache de fallback | **Archivo JSON local** (`cache/respuestas_ia.json`), clave = `id_estudiante` | Persistente entre reinicios, cero infraestructura extra. |
| Proveedor de IA generativa | **API de Anthropic (Claude)**, modelo `claude-haiku-4-5` para la demo (rápido y barato); `claude-sonnet-5` como respaldo de calidad si hay tiempo | Ya usado por el equipo (Claude Code); latencia baja es crítica en demo en vivo. |
| Frontend | **HTML + JS vanilla + Tailwind (CDN)** | Cero build step, cero framework que pueda fallar en vivo. Un solo archivo `index.html`. |
| Autenticación | **Ninguna** (Art. VII §7.2 lo prohíbe explícitamente para este MVP) | — |

> Nota: si el equipo prefiere Streamlit en vez de HTML+JS por velocidad de desarrollo, es intercambiable sin afectar §3–§6 de este documento — solo cambia §8.

---

## 3. Esquema de datos

### 3.1 Estructura de un registro (`Estudiante`)

```json
{
  "id": "EST-001",
  "nombre": "María Quispe H.",
  "grado": "3ro de secundaria",
  "asistencia_pct": 82,
  "notas_promedio": 11.5,
  "participacion": "baja",
  "lengua_materna": "quechua",
  "observaciones": null
}
```

### 3.2 Definición de campos

| Campo | Tipo | Rango/valores válidos | Faltante se representa como |
|---|---|---|---|
| `id` | string | `EST-001` … `EST-020` | — (obligatorio, nunca falta) |
| `nombre` | string | nombre ficticio | — (obligatorio) |
| `grado` | string | libre, ej. "1ro secundaria" | — (informativo, no entra en clasificación) |
| `asistencia_pct` | number \| null | 0–100 | `null` |
| `notas_promedio` | number \| null | 0–20 (escala vigesimal) | `null` |
| `participacion` | string \| null | `"baja"` \| `"media"` \| `"alta"` | `null` |
| `lengua_materna` | string | informativo, ej. `"quechua"` / `"castellano"` | no afecta clasificación (Art. VI) |
| `observaciones` | string \| null | libre, opcional | `null` |

**Definición técnica de dato faltante (cierra Art. IX §9.3.3):** un campo se considera faltante si su valor JSON es `null`. **No se usará el string `"N/D"` en el JSON** — se estandariza a `null` para evitar dos representaciones distintas del mismo caso (la Constitución permitía ambas; esta Especificación elige una sola para evitar bugs de parsing).

### 3.3 Reglas de validación al cargar el dataset
- `asistencia_pct` fuera de 0–100 → se trata como dato inválido = `null` (se registra advertencia en consola, no rompe la demo).
- `notas_promedio` fuera de 0–20 → mismo tratamiento.
- `participacion` con valor distinto a los 3 permitidos → se trata como `null`.

### 3.4 Dataset ficticio (Art. V)
- 15–20 registros generados sintéticamente por el equipo, cubriendo **obligatoriamente** al menos un caso de cada escenario del §10 (casos de prueba), incluyendo mínimo 2 registros con datos faltantes parciales y 1 registro con las 3 variables faltantes.
- Nombres ficticios, sin relación con personas reales identificables (Art. V §5.1).

---

## 4. Módulo 1 — Lógica de clasificación de riesgo (determinista, sin IA)

### 4.1 Umbrales congelados para Fase 3 (calibrables en Fase 4 sin romper estructura — Art. III §3.4)

| Variable | 🟢 Bajo | 🟡 Medio | 🔴 Alto |
|---|---|---|---|
| Asistencia | ≥ 90% | 75–89% | < 75% |
| Notas | ≥ 13 | 11–12 | < 11 |
| Participación | alta / media | baja | *(participación nunca es 🔴 por sí sola — ver 4.2)* |

**Nota de calibración:** participación solo tiene 2 estados de riesgo (🟢 si media/alta, 🟡 si baja) porque es ordinal-categórica, no numérica; no puede "romperse" hacia 🔴 de forma aislada. Esto es una decisión de diseño explícita, no una omisión.

### 4.2 Pseudocódigo del motor de reglas

```
función clasificar_estudiante(estudiante):
    variables_presentes = []
    variables_faltantes = []
    nivel_por_variable = {}

    # Paso 1: evaluar cada variable de forma aislada
    si estudiante.asistencia_pct no es null:
        nivel_por_variable["asistencia"] = evaluar_asistencia(estudiante.asistencia_pct)
        variables_presentes.append("asistencia")
    sino:
        variables_faltantes.append("asistencia")

    si estudiante.notas_promedio no es null:
        nivel_por_variable["notas"] = evaluar_notas(estudiante.notas_promedio)
        variables_presentes.append("notas")
    sino:
        variables_faltantes.append("notas")

    si estudiante.participacion no es null:
        nivel_por_variable["participacion"] = evaluar_participacion(estudiante.participacion)
        variables_presentes.append("participacion")
    sino:
        variables_faltantes.append("participacion")

    # Paso 2: Art. IX §9.3.2 — sin ninguna variable disponible
    si len(variables_presentes) == 0:
        retornar {
            nivel: "⚪ Dato insuficiente",
            motivo: "Las 3 variables carecen de dato — requiere revisión manual del docente",
            variables_faltantes: variables_faltantes
        }

    # Paso 3: Art. III §3.2.1 — regla del peor caso directo
    si "🔴" in nivel_por_variable.values():
        nivel_global = "🔴"
    sino:
        # contar señales negativas aisladas (variables en 🟡)
        señales_negativas = contar(nivel_por_variable.values() == "🟡")
        si señales_negativas == 0:
            nivel_global = "🟢"
        sino si señales_negativas == 1:
            nivel_global = "🟡"
        sino:  # 2 o más
            nivel_global = "🔴"

    retornar {
        nivel: nivel_global,
        motivo: construir_motivo(nivel_por_variable, variables_faltantes),
        variables_faltantes: variables_faltantes
    }


función evaluar_asistencia(valor):
    si valor >= 90: retornar "🟢"
    sino si valor >= 75: retornar "🟡"
    sino: retornar "🔴"

función evaluar_notas(valor):
    si valor >= 13: retornar "🟢"
    sino si valor >= 11: retornar "🟡"
    sino: retornar "🔴"

función evaluar_participacion(valor):
    si valor en ["alta", "media"]: retornar "🟢"
    sino: retornar "🟡"   # "baja" — nunca 🔴 de forma aislada
```

### 4.3 `construir_motivo()` — trazabilidad visible (Art. II §2.3)
Genera una lista de strings cortos, uno por variable evaluada, ej.:
```
["Asistencia: 82% — nivel 🟡 (umbral 🟢 es ≥90%)",
 "Notas: 11.5 — nivel 🟡 (umbral 🟢 es ≥13)",
 "Participación: sin dato — evaluado solo con asistencia y notas"]
```
Este arreglo se muestra en el dashboard **antes o junto con** el texto de IA (obligatorio, no opcional).

### 4.4 Reglas de datos faltantes/insuficientes (Art. IX §9.3, resumen operativo)
| Variables con dato | Comportamiento |
|---|---|
| 3 de 3 | Clasificación normal (§4.2) |
| 1 o 2 de 3 | Se clasifica solo con las disponibles + se listan explícitamente las faltantes en `motivo` |
| 0 de 3 | Estado `⚪ Dato insuficiente`, no se fuerza 🟢/🟡/🔴 |

---

## 5. Módulo 2 — Motor de IA generativa

### 5.1 Contrato de entrada (lo que el backend envía al modelo)

```json
{
  "estudiante": {
    "nombre": "María Quispe H.",
    "grado": "3ro de secundaria"
  },
  "nivel_riesgo": "🟡",
  "motivos": [
    "Asistencia: 82% — nivel 🟡 (umbral 🟢 es ≥90%)",
    "Notas: 11.5 — nivel 🟡 (umbral 🟢 es ≥13)"
  ],
  "variables_faltantes": ["participacion"]
}
```

### 5.2 System prompt (fijo, no cambia por estudiante)

```
Eres un asistente que ayuda a docentes de instituciones educativas rurales del Perú
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
```

### 5.3 User prompt (dinámico, por estudiante)
```
Nivel de riesgo detectado: {nivel_riesgo}
Motivos de la clasificación: {motivos, uno por línea}
Variables sin dato: {variables_faltantes, o "ninguna"}
Grado del estudiante: {grado}

Genera la explicación y recomendación según las reglas del sistema.
```

