---
trigger: always_on
---

### 5.4 Contrato de salida esperado
```json
{
  "explicacion": "María mantiene una asistencia moderada (82%) y un promedio cercano al límite (11.5), lo que sugiere una atención temprana antes de que la tendencia baje más.",
  "recomendacion": "Se sugiere una conversación breve de seguimiento con María y, si es posible, con su familia, para identificar si hay alguna dificultad puntual que esté afectando su asistencia."
}
```

### 5.5 Parámetros de la llamada API
- `model`: `claude-haiku-4-5` (latencia baja, prioridad en demo)
- `max_tokens`: 300
- `timeout` aplicado por el backend: **6 segundos** → si se excede, dispara fallback (Art. VIII)
- Parseo: extraer JSON de la respuesta; si el parseo falla, tratar como fallo de llamada → fallback también.

---

## 6. Módulo 3 — Modo de respaldo (fallback) — Art. VIII

### 6.1 Generación previa del cache (se hace **antes** de la demo, durante desarrollo)
Un script (`scripts/generar_cache.py`) recorre los 15–20 registros, llama a la API real una vez por estudiante, y guarda el resultado en `cache/respuestas_ia.json`:
```json
{
  "EST-001": {
    "explicacion": "...",
    "recomendacion": "...",
    "generado_en": "2026-06-30T22:10:00"
  }
}
```
Esto cumple Art. VIII §8.1.1: el fallback **siempre** es texto de origen genuino del modelo, nunca redactado a mano.

### 6.2 Lógica de activación en tiempo real
```
función obtener_explicacion(estudiante_id, payload):
    intentar:
        respuesta = llamar_api_ia(payload, timeout=6s)
        retornar { ...respuesta, origen: "vivo" }
    si_falla_o_timeout:
        respuesta_cache = cache[estudiante_id]
        si respuesta_cache existe:
            retornar { ...respuesta_cache, origen: "fallback" }
        sino:
            retornar {
                explicacion: "No se pudo generar la explicación en este momento.",
                recomendacion: "Reintentar más tarde o revisar manualmente.",
                origen: "error_sin_cache"
            }
```

### 6.3 Indicador visible obligatorio (Art. VIII §8.1.3)
Cuando `origen == "fallback"`, el dashboard muestra:
> ⚠️ *Explicación generada previamente — modo de respaldo activo*

**Nunca** se muestra un stack trace, código HTTP, ni mensaje técnico crudo al docente.

---

## 7. Módulo 4 — API Backend (contrato FastAPI)

| Endpoint | Método | Descripción | Respuesta |
|---|---|---|---|
| `/api/estudiantes` | GET | Lista los N estudiantes ya clasificados y con explicación/recomendación (llama a §4 + §5/§6 internamente, con cache en memoria por sesión de demo) | `200` array de `EstudianteResultado` |
| `/api/estudiantes/{id}` | GET | Detalle de un estudiante puntual (útil para refrescar uno solo sin recargar todo) | `200` `EstudianteResultado` o `404` |
| `/api/health` | GET | Chequeo simple de que el backend está vivo | `200 {"status": "ok"}` |

### 7.1 Modelo de respuesta `EstudianteResultado`
```json
{
  "id": "EST-001",
  "nombre": "María Quispe H.",
  "grado": "3ro de secundaria",
  "nivel_riesgo": "🟡",
  "motivos": ["Asistencia: 82% — nivel 🟡 (umbral 🟢 es ≥90%)", "..."],
  "variables_faltantes": ["participacion"],
  "explicacion": "...",
  "recomendacion": "...",
  "origen_ia": "vivo"
}
```
Para el caso `⚪ Dato insuficiente`, `explicacion` y `recomendacion` se omiten (o van `null`) y `nivel_riesgo` = `"⚪ Dato insuficiente"`.

---

## 8. Módulo 5 — Dashboard (wireframe funcional)

### 8.1 Vista principal — tabla
```
┌────────────────────────────────────────────────────────────────────────┐
│  Detección Temprana de Riesgo Escolar                    [🔄 Actualizar]│
├────┬──────────────────┬────────┬────────────┬──────────────────────────┤
│ ID │ Estudiante        │ Riesgo │ Grado       │ Motivo principal          │
├────┼──────────────────┼────────┼────────────┼──────────────────────────┤
│ 01 │ María Quispe H.   │ 🟡     │ 3ro sec.    │ Asistencia 82%, notas 11.5│
│ 02 │ Jhon Huamán T.    │ 🔴     │ 2do sec.    │ Asistencia 60%            │
│ 03 │ Rosa Sulca P.     │ 🟢     │ 1ro sec.    │ Todo dentro de rango      │
│ 04 │ Luis Ccorahua R.  │ ⚪     │ 4to sec.    │ Sin datos disponibles     │
└────┴──────────────────┴────────┴────────────┴──────────────────────────┘
```
Filas coloreadas suavemente según nivel (verde/ámbar/rojo/gris) — sin iconografía alarmante.

### 8.2 Panel de detalle (al hacer clic en una fila)
```
┌──────────────────────────────────────────────────┐
│ María Quispe H. — 3ro de secundaria     🟡 Medio  │
├──────────────────────────────────────────────────┤
│ Variables que motivaron la clasificación:         │
│  • Asistencia: 82% (umbral 🟢 ≥90%)               │
│  • Notas: 11.5 (umbral 🟢 ≥13)                    │
│  • Participación: sin dato                        │
│                                                    │
│ ⚠️ Explicación generada previamente — modo de      │
│    respaldo activo               (si aplica)      │
│                                                    │
│ Explicación:                                      │
│  María mantiene una asistencia moderada...        │
│                                                    │
│ Recomendación:                                    │
│  Se sugiere una conversación breve de seguimiento │
└──────────────────────────────────────────────────┘
```

### 8.3 Estado `⚪ Dato insuficiente`
El panel de detalle reemplaza explicación/recomendación por:
> "⚪ No hay datos suficientes para clasificar a este estudiante. Se recomienda revisión manual del docente."

### 8.4 Nota de diseño lingüístico-cultural (Art. VI §6.2 — no implementado en MVP)
Se deja constancia documental: el dashboard debería, en una versión futura, permitir alternar textos generados al quechua o incluir apoyo bilingüe. **No se implementa en esta versión**, solo se declara como decisión de diseño pendiente.

---

## 9. Manejo de errores (resumen operativo)

| Escenario | Comportamiento esperado |
|---|---|
| API de IA no responde / timeout | Fallback automático (§6), indicador visible |
| Dataset con valor fuera de rango | Se normaliza a `null`, no rompe carga (§3.3) |
| Estudiante con 0 variables | Estado `⚪ Dato insuficiente` (§4.4) |
| JSON de la IA mal formado | Se trata como fallo de llamada → fallback |
| Endpoint `/api/estudiantes/{id}` con id inexistente | `404` con mensaje claro, sin stack trace |

---

## 10. Casos de prueba (validan Art. III y Art. IX — deben pasar todos antes de la demo)

| # | Caso | Asistencia | Notas | Participación | Resultado esperado |
|---|---|---|---|---|---|
| 1 | Todo bien | 95% | 15 | alta | 🟢 |
| 2 | Una señal 🟡 aislada | 80% | 15 | alta | 🟡 (1 señal negativa) |
| 3 | Dos señales 🟡 | 80% | 11.5 | alta | 🔴 (2+ señales negativas, ninguna 🔴 individual) |
| 4 | Una variable 🔴 directa | 60% | 15 | alta | 🔴 (peor caso directo, Art. III §3.2.1.1) |
| 5 | Desempate | 95% (🟢) | 9 (🔴) | alta (🟢) | 🔴 (prevalece el peor nivel) |
| 6 | Falta 1 variable | 95% | 15 | `null` | Clasifica con 2 variables, señala participación faltante |
| 7 | Faltan 2 variables | `null` | 15 | `null` | Clasifica solo con notas, señala 2 faltantes |
| 8 | Faltan las 3 | `null` | `null` | `null` | `⚪ Dato insuficiente` |
| 9 | Límite exacto asistencia | 90% | 15 | alta | 🟢 (90 es ≥90, no 🟡) |
| 10 | Límite exacto notas | 95% | 13 | alta | 🟢 (13 es ≥13) |
| 11 | Fallback forzado | (cualquiera) | — | — | API simulada caída → se usa cache, indicador visible, sin stack trace |
| 12 | Lenguaje no estigmatizante | (cualquier caso 🔴) | — | — | Revisión manual confirma ausencia de palabras prohibidas (Art. IV §4.1) |

---

## 11. Plan de implementación sugerido (orden para 3 horas)

| Bloque | Tiempo aprox. | Entregable |
|---|---|---|
| 1. Dataset + motor de reglas (§3, §4) | 40 min | `data/estudiantes.json` + función `clasificar_estudiante()` probada con los 12 casos de §10 |
| 2. Integración IA + prompt (§5) | 35 min | Llamada real funcionando para 1 estudiante, JSON parseado correctamente |
| 3. Generación de cache de fallback (§6.1) | 15 min | `cache/respuestas_ia.json` generado para los 15-20 registros |
| 4. Endpoints FastAPI (§7) | 25 min | `/api/estudiantes` responde con datos reales |
| 5. Dashboard (§8) | 40 min | Tabla + panel de detalle funcionando contra el backend real |
| 6. Prueba end-to-end + fallback forzado | 15 min | Flujo completo probado 1 vez con conexión real (Art. VIII §8.2) |
| Buffer | 10 min | Ajustes de último minuto, revisión de lenguaje (Art. IV §4.3) |

---

## 12. Checklist pre-demo (derivado de Art. X §10.1)

- [ ] Los 15–20 registros cargan sin error.
- [ ] Clasificación consistente en los 12 casos de prueba (§10).
- [ ] ≥90% de explicaciones/recomendaciones son distintas entre sí (no plantilla repetida).
- [ ] Ninguna salida contiene lenguaje estigmatizante (revisión manual hecha).
- [ ] Trazabilidad de variables visible en el dashboard antes/junto al texto de IA.
- [ ] Fallback probado manualmente (desconectar internet o forzar timeout) y el indicador aparece correctamente.
- [ ] Caso `⚪ Dato insuficiente` probado y visible en la demo.
- [ ] Ningún error crudo (stack trace / código HTTP) se muestra en pantalla.

---

## 13. Pendientes explícitos para Fase 4 (Plan) y Fase 5 (Tareas)

Estos NO se resuelven en esta Especificación — quedan abiertos intencionalmente:
1. **Asignación real de responsables por módulo** (Art. XI, tabla de la Constitución) — nombres del equipo.
2. Guion exacto de la demo en vivo (qué estudiantes mostrar, en qué orden, qué fallback forzar).
3. Ajuste fino de los 12 casos de prueba si el equipo decide calibrar umbrales (Art. III §3.4 lo permite).
4. Decisión final entre `claude-haiku-4-5` vs `claude-sonnet-5` según latencia real observada en pruebas.

---

*Fin de la Especificación técnica — Fase 3. Este documento es la única fuente de verdad para la implementación (Fase 5). Cualquier cambio de fondo durante la programación debe reflejarse aquí primero, no solo en el código.*
