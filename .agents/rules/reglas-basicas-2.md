---
trigger: always_on
---

# CONSTITUCIÓN DEL PROYECTO — v2.1
## Fase 2 — SDD (Spec-Driven Development)
## Proyecto: Detección Temprana de Riesgo Escolar — Reto 2 (Educación)

**Versión:** 2.1 | **Estado:** Vigente para Fase 3 en adelante
**Cambios respecto a v2:** cierre de 3 brechas detectadas en revisión de Fase 2 (ver *Registro de Enmiendas* al pie). No se modifica el espíritu de ningún artículo protegido (II, IV, V).

> Esta Constitución establece los principios rectores, no negociables y reglas de gobierno que guiarán todas las decisiones técnicas y de diseño en las fases siguientes (Especificación, Plan, Tareas e Implementación). Ninguna decisión posterior puede contradecir lo establecido aquí sin una enmienda explícita y justificada.

## PREÁMBULO
Este proyecto nace para ayudar a docentes y tutores de instituciones educativas rurales y urbano-marginales del Perú a detectar tempranamente a estudiantes en riesgo de bajo rendimiento o deserción, mediante una solución que combina lógica de clasificación auditable con IA generativa real, priorizando la dignidad del estudiante, la explicabilidad y la viabilidad técnica dentro de un tiempo de desarrollo de 3 horas.

## ARTÍCULO I — Propósito y Alcance

**Sección 1.1 — Propósito**
La solución debe procesar datos de seguimiento académico ficticios (asistencia, notas, participación) para identificar niveles de riesgo estudiantil y generar explicaciones y recomendaciones personalizadas.

**Sección 1.2 — Alcance permitido**
- Procesamiento de datos ficticios de 15–20 estudiantes.
- Clasificación de nivel de riesgo.
- Generación de explicación y recomendación vía IA generativa.
- Visualización en tabla/dashboard para uso docente.

**Sección 1.3 — Alcance prohibido (fuera de todo debate)**
- ❌ No integración con SIAGIE ni sistemas oficiales del MINEDU.
- ❌ No uso de datos reales de estudiantes o menores de edad, bajo ninguna circunstancia.
- ❌ No se intentará resolver la política de permanencia escolar en su totalidad.
- ❌ No se construirá una interfaz para uso directo del estudiante/familia en esta versión.

---

## ARTÍCULO II — Principio No Negociable: IA Generativa Real

**Sección 2.1**
La IA generativa **no es un accesorio decorativo**; es un componente funcional obligatorio del sistema. Ninguna implementación que reemplace este componente por plantillas estáticas o lógica if/else disfrazada de "IA" será válida.

**Sección 2.2 — División de responsabilidades (arquitectura obligatoria)**
1. La **clasificación del nivel de riesgo** se basa en reglas auditables y trazables (ver Artículo III).
2. La **explicación y la recomendación personalizada** se generan mediante un modelo de lenguaje (IA generativa), a partir de los datos del estudiante y su nivel de riesgo.

**Sección 2.3 — Trazabilidad visible (no solo interna)**
La trazabilidad no puede quedar solo en logs técnicos. El dashboard debe mostrar al docente, junto al nivel de riesgo, **qué variable(s) concreta(s)** lo motivaron (ej. "Asistencia: 68% — por debajo del umbral de 75%"), antes o junto con el texto generado por IA.

**Sección 2.4 — Origen legítimo del texto generado (aclaración, ver Art. VIII)**
El requisito de "IA generativa real" no exige que la llamada al modelo ocurra necesariamente en el instante de la demo. Lo que no se negocia es el **origen** del texto: debe haber sido producido por el modelo de lenguaje en algún momento del desarrollo, nunca redactado manualmente por el equipo simulando ser salida de IA. El Artículo VIII, Sección 8.1, define cómo esto opera en el modo de respaldo.

---

## ARTÍCULO III — Principio de Clasificación de Riesgo

**Sección 3.1 — Niveles**
El sistema reconocerá tres niveles de riesgo: 🟢 Bajo, 🟡 Medio, 🔴 Alto.

**Sección 3.2 — Criterios base (sujetos a calibración, no a eliminación)**
| Nivel | Criterio orientativo |
|---|---|
| 🟢 Bajo | Asistencia ≥ 90%, notas ≥ 13, participación media/alta |
| 🟡 Medio | Asistencia 75–89% o notas 11–12, o una señal negativa aislada |
| 🔴 Alto | Asistencia < 75% o notas < 11, o combinación de 2+ señales negativas |

**Sección 3.2.1 — Definición operacional de "señal negativa" (cierre de ambigüedad)**
Se define **señal negativa** como cualquier variable individual del estudiante (asistencia, notas o participación) cuyo valor, evaluado de forma aislada, cae fuera del rango 🟢 Bajo correspondiente a esa variable — es decir, cae en su propio rango 🟡 o 🔴, **antes** de aplicar la regla de desempate de la Sección 3.3.

Regla de conteo y resolución:
1. Si **alguna variable individual**, evaluada por sí sola, alcanza el rango 🔴 → se aplica directamente la regla del peor caso (Sección 3.3): la clasificación global es 🔴, sin necesidad de contar señales adicionales.
2. Si **ninguna variable individual** alcanza por sí sola el rango 🔴 → se cuenta cuántas variables caen en rango 🟡 (señales negativas aisladas):
   - **Cero** señales negativas → clasificación global 🟢.
   - **Una** señal negativa → clasificación global 🟡.
   - **Dos o más** señales negativas → clasificación global 🔴 (acumulación de riesgo, aunque ninguna variable por sí sola llegue a 🔴).

Esta regla es determinista y auditable: dos personas distintas, con los mismos tres valores de un estudiante, deben llegar siempre a la misma clasificación.

**Sección 3.3 — Regla de desempate (principio del peor caso)**
Cuando las variables de un estudiante caen en niveles distintos entre sí (ej. asistencia en nivel Bajo pero notas en nivel Alto), **prevalece el nivel de riesgo más alto detectado entre las variables evaluadas**. Esto es una decisión de seguridad: es preferible una falsa alerta que dejar pasar un caso real.

**Sección 3.4**
Los umbrales numéricos pueden ajustarse durante la Fase 3 (Especificación) tras validarlos con casos de prueba, pero la **estructura de 3 niveles, el principio de reglas auditables, la regla de desempate y la definición operacional de señal negativa (3.2.1)** no pueden eliminarse.

---

## ARTÍCULO IV — Principio de Dignidad y No Estigmatización

**Sección 4.1**
Ninguna explicación o recomendación generada podrá usar lenguaje que etiquete, culpabilice o estigmatice al estudiante (ej. prohibido: "estudiante problemático", "flojo", "en riesgo de fracaso").

**Sección 4.2**
El lenguaje debe ser constructivo y orientado a la acción del docente (ej. "se recomienda una conversación de seguimiento con el estudiante y su familia").

**Sección 4.3**
Toda salida generada por IA debe pasar una revisión manual del equipo antes de la demo, verificando el cumplimiento de este artículo.

---

## ARTÍCULO V — Principio de Privacidad y Datos Ficticios

**Sección 5.1**
Está terminantemente prohibido usar datos reales de estudiantes menores de edad, incluso como referencia o inspiración directa de un caso real identificable.

**Sección 5.2**
Todo el dataset de demostración (15–20 registros) debe ser generado de forma sintética, con nombres y datos ficticios.

**Sección 5.3**
Esta regla no admite excepciones ni siquiera "solo para pruebas internas".

---

## ARTÍCULO VI — Principio de Accesibilidad y Contexto

**Sección 6.1**
La solución se diseña asumiendo que el estudiante puede no tener conectividad a internet en casa; por lo tanto, el punto de acceso del sistema es el **docente/tutor desde la institución educativa**, no el hogar del estudiante.

**Sección 6.2**
Se debe dejar constancia de diseño (aunque no se implemente en el MVP) de la consideración lingüística/cultural de comunidades quechuahablantes.

---

## ARTÍCULO VII — Principio de Simplicidad, Tiempo y Stack Técnico

**Sección 7.1 — Restricción de tiempo**
El proyecto es un **MVP demostrable en vivo dentro de 3 horas**. Toda decisión de diseño debe evaluarse primero bajo el criterio: *"¿esto es indispensable para demostrar el flujo completo end-to-end?"*

**Sección 7.2 — Prohibición de sobreingeniería**
Se prohíbe construir autenticación de usuarios, bases de datos persistentes complejas, ni integraciones externas no mencionadas en el Artículo I, salvo que sean estrictamente necesarias para el flujo mínimo.

**Sección 7.3 — Stack tecnológico (a fijar antes de Fase 3)**
El equipo debe definir y congelar, antes de iniciar la Especificación (Fase 3):
- Lenguaje/framework de backend (ej. Python + Flask/FastAPI, o Node.js).
- Forma de almacenamiento del dataset ficticio (ej. archivo CSV/JSON local — **no se requiere base de datos** dado el alcance).
- Proveedor y modelo de IA generativa a usar (ej. API de Claude, OpenAI, u otro disponible para el equipo).
- Tecnología de frontend/dashboard (ej. HTML+JS simple, Streamlit, o similar de bajo esfuerzo).

*Nota: esta sección se completa como parte del entregable de Fase 2, con los valores concretos que el equipo decida — ver plantilla al final de este documento.*

**Sección 7.4 — Prevalencia de lo funcional**
Ante un conflicto entre "hacerlo perfecto" y "hacerlo funcional a tiempo", prevalece lo funcional, siempre que no viole los Artículos II a VI.

---

## ARTÍCULO VIII — Principio de Resiliencia en la Demo

**Sección 8.1 — Modo de respaldo (fallback) [revisado — cierre de contradicción con Art. II y Art. X]**
Dado que la IA generativa depende de una API externa, el equipo debe prever un **modo de respaldo (fallback)** para la demo en vivo. Este modo de respaldo debe cumplir estrictamente lo siguiente:

1. Las respuestas de respaldo deben ser **explicaciones y recomendaciones generadas previamente por el mismo modelo de IA generativa** del proyecto (durante desarrollo o pruebas, con conexión real a la API), y luego **cacheadas localmente** para los casos clave del dataset de demo.
2. Bajo ninguna circunstancia el modo de respaldo consistirá en texto **redactado manualmente por el equipo** simulando ser salida de IA generativa, ni en plantillas fijas de tipo if/else. Esto violaría el Artículo II, Sección 2.1.
3. Si la llamada en vivo a la IA falla o tarda más de lo esperado, el sistema debe activar el modo de respaldo automáticamente y mostrar al docente un indicador visible y honesto (ej. "⚠️ Explicación generada previamente — modo de respaldo activo"), preservando la trazabilidad exigida en el Artículo II, Sección 2.3. Nunca se debe mostrar un error crudo (stack trace, código HTTP, etc.).
4. Estas respuestas de respaldo cacheadas **sí cuentan** como explicaciones "generadas por IA" a efectos del criterio de aceptación del Artículo X, Sección 10.1.3, porque su origen es genuinamente el modelo de lenguaje.

**Sección 8.2**
Se recomienda probar el flujo completo al menos una vez de principio a fin, con conexión real, antes de la sustentación — no solo probar componentes por separado.

