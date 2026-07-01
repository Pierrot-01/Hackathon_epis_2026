---
trigger: always_on
---

# FASE 1 — CAPTURA DE INTENCIÓN (SSD) — v2
## Reto 2 — Educación: Detección Temprana de Riesgo Escolar

---

## 1. Enunciado del reto (¿Cómo podríamos…?)
¿Cómo podríamos ayudar a docentes y tutores a detectar a tiempo a los estudiantes en riesgo de bajo rendimiento o deserción, y ofrecerles un apoyo pertinente?

---

## 2. Problema
Los docentes identifican el bajo rendimiento y la deserción cuando el problema ya está avanzado (el estudiante ya faltó mucho o bajó notablemente sus notas). No existe una forma sencilla de detectar señales tempranas ni de personalizar el apoyo según el caso.

---

## 3. Usuarios
- Docentes
- Tutores
- Directores

## 4. Beneficiarios
- Estudiantes de zonas rurales y urbano-marginales del Perú, de menor nivel socioeconómico.
- Docentes de dichas instituciones educativas (usan la herramienta y reciben las alertas/recomendaciones).

---

## 5. Dónde ocurre (contexto geográfico y social)
- Instituciones educativas rurales y urbano-marginales del Perú.
- Muchas comunidades tienen el quechua como lengua materna.
- 6 de cada 10 estudiantes de menor nivel socioeconómico no tienen internet en casa (BID, 2024).

---

## 6. Contexto clave (cifras que justifican el problema)
- Solo el **16.7%** de estudiantes rurales de 2.º de primaria alcanza el nivel esperado en comprensión lectora, frente al **49.7%** en zonas urbanas (ECE, MINEDU).
- La deserción en secundaria rural llega al **5.2%** (hasta **8.6%** en mujeres) (MINEDU).

---

## 7. Situación actual vs. situación deseada
| Situación hoy | Situación deseada |
|---|---|
| El riesgo se detecta tarde, cuando ya hay ausentismo o notas muy bajas. | A partir de datos de seguimiento (asistencia, notas, participación) se identifican niveles de riesgo tempranamente. |
| No hay forma sencilla de personalizar el apoyo. | Se sugiere un apoyo pertinente, personalizado y distinto según el caso. |

---

## 8. Objetivo
Detectar tempranamente a los estudiantes en riesgo (bajo rendimiento o deserción) utilizando datos de seguimiento académico, y generar recomendaciones de apoyo personalizadas y explicables.

---

## 9. Datos disponibles y su definición operacional
| Variable | Tipo de dato | Rango / formato propuesto |
|---|---|---|
| Asistencia | Numérico | % de asistencia mensual o N.º de inasistencias consecutivas |
| Notas | Numérico | Escala vigesimal (0–20), por curso o promedio general |
| Participación | Categórico u ordinal | Ej. Baja / Media / Alta, o puntaje 1–5 |

*(Datos ficticios; no se usan datos reales de estudiantes menores de edad. Esta estructura es una propuesta base — debe cerrarse en Fase 2 antes de construir el dataset de 15–20 registros.)*

---

## 10. Nivel de riesgo — definición operacional propuesta
Para evitar interpretaciones distintas entre miembros del equipo, se propone un esquema de **3 niveles**:

| Nivel | Criterio orientativo (a ajustar en Fase 2) |
|---|---|
| 🟢 Bajo | Asistencia ≥ 90%, notas ≥ 13, participación media/alta |
| 🟡 Medio | Asistencia 75–89% o notas 11–12 o participación baja de forma aislada |
| 🔴 Alto | Asistencia < 75% o notas < 11 o combinación de 2+ señales negativas |

*Esta tabla es un punto de partida, no un cierre definitivo — el equipo debe validarla o ajustarla al inicio de la Fase 2, pero ya no debe quedar abierta como pregunta sin dueño.*

---

## 11. Resultado esperado de la solución
La solución debe:
1. Procesar datos de seguimiento de un estudiante.
2. Identificar el **nivel de riesgo** (según el esquema de la sección 10).
3. Generar una **explicación del riesgo**: en lenguaje natural, señalando qué variables y valores concretos motivaron la clasificación (ej. "3 inasistencias seguidas y promedio de 10 en Matemática").
4. Entregar una **recomendación o intervención personalizada**, no un mensaje genérico, coherente con el nivel de riesgo y el motivo detectado.
5. Demostrarse con un conjunto ficticio de **al menos 15–20 registros** de estudiantes.

---

## 12. Rol específico de la IA generativa (requisito no negociable) ⚠️
**La IA generativa debe ser un componente real de la solución**, no un adorno. Definición de su rol dentro de la arquitectura:
- La **clasificación del nivel de riesgo** puede apoyarse en reglas/lógica (sección 10) para asegurar consistencia y trazabilidad.
- La **generación de la explicación y la recomendación personalizada** debe hacerse mediante IA generativa (modelo de lenguaje), tomando como entrada los datos del estudiante y el nivel de riesgo detectado.
- Esto garantiza explicabilidad (la lógica de clasificación es auditable) y personalización real (el texto no es una plantilla fija).

*Nota: esta división de responsabilidades es la propuesta de base; el equipo puede ajustarla en Fase 2, pero debe quedar explícita antes de programar.*

---

## 13. Formato de salida / interfaz esperada
- Salida mínima viable: **tabla o dashboard simple** que liste a los estudiantes con su nivel de riesgo, explicación y recomendación.
- No se requiere una app compleja ni integración con sistemas externos — prioridad en velocidad de desarrollo dado el límite de 3 horas.
- El acceso está pensado para el **docente/tutor desde la institución educativa**, no para que el estudiante lo use desde casa (dado el bajo acceso a internet en el hogar reportado por BID 2024).

---

## 14. Alcance excluido (fuera del scope)
- No se espera integración con el SIAGIE ni con sistemas oficiales del MINEDU.
- No se deben usar datos reales de estudiantes (menores de edad).
- No se busca resolver toda la política de permanencia escolar, solo la detección + recomendación de apoyo.
- No se requiere una interfaz para uso directo del estudiante o su familia en esta versión del prototipo.

---

## 15. Restricciones y consideraciones
- Uso obligatorio de datos ficticios (no datos reales de menores).
- Las recomendaciones deben ser **respetuosas y no estigmatizantes** hacia el estudiante (evitar lenguaje que etiquete o culpabilice).
- La solución no debe depender de que el estudiante tenga conectividad; el punto de uso es el docente en la institución.
- Considerar diversidad lingüística/cultural (comunidades quechuahablantes) al redactar recomendaciones — al menos como nota de diseño, aunque no se implemente traducción en el MVP.

---

## 16. Nivel de madurez esperado (restricción de tiempo)
**Prototipo funcional (MVP)** demostrable en vivo, alcanzable dentro de las **3 horas** de la categoría.

---

## 17. Métrica de éxito y criterios de aceptación
El prototipo se considera exitoso si:
- Procesa correctamente un dataset ficticio de **15–20 registros** con la estructura de la sección 9.
- Clasifica el nivel de riesgo de cada estudiante de forma **consistente** con las reglas definidas (sección 10).
- Genera, mediante IA generativa, una explicación y recomendación **distinta para cada caso** (no una plantilla repetida) en al menos el 90% de los registros.
- Las recomendaciones no contienen lenguaje estigmatizante (validación manual del equipo antes de la demo).

---

## 18. Decisiones cerradas vs. pendientes para Fase 2

**Cerradas en esta versión:**
- Estructura de datos de entrada.
- Esquema de niveles de riesgo (versión inicial).
- Rol de la IA generativa dentro de la arquitectura.
- Punto de acceso/usuario final de la interfaz.

**Pendientes a resolver al iniciar Fase 2 (diseño de solución):**
- Ajuste fino de los umbrales de riesgo (sección 10) con el equipo completo.
- Prompt/modelo específico de IA generativa a usar y su formato de entrada/salida.
- Diseño visual final del dashboard (wireframe).
- Guion de la demo en vivo para sustentación.
