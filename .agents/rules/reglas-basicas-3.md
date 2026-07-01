---
trigger: always_on
---

## ARTÍCULO IX — Manejo de Datos Incompletos o Ambiguos

**Sección 9.1**
Si un registro del dataset ficticio tiene un dato faltante (ej. participación no registrada), el sistema no debe fallar ni excluir silenciosamente al estudiante. Debe clasificarlo con la información disponible y señalar explícitamente qué dato faltó (ej. "Participación: sin datos — evaluado solo con asistencia y notas").

**Sección 9.2**
Ver Artículo III, Sección 3.3, para el criterio de desempate cuando las variables disponibles apuntan a niveles de riesgo distintos.

**Sección 9.3 — Regla de datos insuficientes (cierre de vacío)**
La Sección 9.1 cubre el caso de un dato faltante; esta sección cubre los casos no contemplados de ausencia parcial o total:

1. **Si al menos 1 de las 3 variables tiene dato disponible:** se clasifica al estudiante usando únicamente las variables disponibles, aplicando el Artículo III completo (incluida la regla de desempate del peor caso, Sección 3.3, y la definición de señal negativa, Sección 3.2.1, evaluada solo sobre las variables presentes). Se debe señalar explícitamente en el dashboard cuáles variables faltaron, como ya exige la Sección 9.1.
2. **Si las 3 variables carecen de dato:** el registro **no se clasifica** en 🟢/🟡/🔴. En su lugar, se muestra un estado distinto: **"⚪ Dato insuficiente — requiere revisión manual del docente"**. Forzar una clasificación de riesgo sin ninguna evidencia disponible violaría el principio de dignidad del Artículo IV, al etiquetar a un estudiante sin base real.
3. **Definición técnica de "dato faltante":** para efectos de esta Constitución, se considera dato faltante cualquier celda vacía, valor `null`, o valor explícitamente marcado como "N/D" en el dataset ficticio. El formato exacto de representación se define en la Fase 3 (esquema de datos).

---

## ARTÍCULO X — Estándares de Calidad y Aceptación

**Sección 10.1 — Criterios de éxito del MVP**
El sistema se considera aceptable si:
1. Procesa correctamente los 15–20 registros ficticios definidos.
2. Clasifica el riesgo de forma consistente con las reglas del Artículo III (incluyendo desempate y definición de señal negativa, Sección 3.2.1).
3. Genera explicaciones y recomendaciones distintas para al menos el 90% de los registros (no plantillas repetidas), entendiendo como válidas tanto las generadas en vivo como las de respaldo cacheadas conforme al Artículo VIII, Sección 8.1.
4. No contiene lenguaje estigmatizante en ninguna salida (Artículo IV).
5. Muestra la trazabilidad de la clasificación de forma visible (Artículo II, Sección 2.3), incluyendo cuándo una explicación proviene del modo de respaldo (Art. VIII, 8.1.3).
6. Sobrevive una falla simulada de la API de IA sin romper la demo (Artículo VIII).
7. Maneja correctamente los registros con datos insuficientes según el Artículo IX, Sección 9.3, sin fallar ni forzar una clasificación sin evidencia.

**Sección 10.2 — Formato de salida**
Tabla o dashboard simple, legible por un docente sin conocimientos técnicos, mostrando: estudiante, nivel de riesgo (o estado "⚪ Dato insuficiente"), variable(s) que lo motivaron, explicación, recomendación.

---

## ARTÍCULO XI — Roles y Responsabilidades

**Sección 11.1**
Antes de iniciar la Fase 3, el equipo debe asignar un responsable (dueño) por cada módulo, usando esta plantilla:

| Módulo | Responsable | Notas |
|---|---|---|
| Dataset ficticio (15-20 registros) | *(por asignar)* | |
| Lógica de clasificación de riesgo (Art. III, incl. 3.2.1 y 3.3) | *(por asignar)* | |
| Integración con IA generativa (prompt + llamada API) | *(por asignar)* | |
| Modo de respaldo / cacheo de respuestas (Art. VIII, 8.1) | *(por asignar)* | |
| Dashboard / interfaz | *(por asignar)* | |
| Manejo de datos insuficientes (Art. IX, 9.3) | *(por asignar)* | |
| Revisión de lenguaje no estigmatizante (Art. IV) | *(por asignar)* | |

**Sección 11.2**
Un responsable no trabaja aislado — cada módulo depende de que los otros respeten esta Constitución (ej. quien programe el dashboard necesita el formato exacto que entregue quien programe la clasificación).

---

## ARTÍCULO XII — Gobernanza y Enmiendas

**Sección 12.1**
Cualquier cambio a los Artículos II, IV o V (IA generativa real, no estigmatización, privacidad de datos) requiere que el equipo completo esté de acuerdo y quede documentado como una enmienda explícita, incrementando la versión de este documento (v2 → v3, etc.) — no pueden modificarse implícitamente durante la programación.

**Sección 12.2**
Los Artículos III, VI, VII, VIII y IX (umbrales de riesgo, accesibilidad, stack técnico, resiliencia, manejo de datos incompletos) pueden calibrarse libremente en las Fases 3 y 4, siempre que respeten el espíritu del artículo. Se recomienda anotar los cambios al pie de este documento con fecha/hora, dado el contexto de hackathon de 3 horas.

**Sección 12.3**
Ante cualquier ambigüedad no cubierta por esta Constitución, el equipo debe resolverla priorizando: 1) dignidad del estudiante, 2) veracidad/explicabilidad, 3) viabilidad en el tiempo disponible.

---

## Trazabilidad respecto a la Fase 1
Esta Constitución traduce en principios de gobierno las definiciones ya cerradas en la Fase 1 (Intent v2): estructura de datos, niveles de riesgo, rol de la IA generativa, interfaz y criterios de aceptación. No introduce alcance nuevo — formaliza lo ya acordado como reglas que ninguna decisión técnica posterior puede violar sin enmienda.

---

## Pendiente inmediato antes de Fase 3
1. Completar la tabla de stack técnico (Art. VII, Sección 7.3) con los valores reales que el equipo elija.
2. Completar la tabla de responsables (Art. XI).
Ambos son de rápida resolución (minutos), no bloquean el contenido de esta Constitución, pero sí deben cerrarse antes de escribir la Especificación técnica.

---

## Registro de Enmiendas (Art. XII, Sección 12.2)

| Fecha/Hora | Artículo/Sección afectada | Cambio | Tipo |
|---|---|---|---|
| *(completar)* | Art. II — nueva Sección 2.4 | Aclara que "IA real" se refiere al origen del texto, no al momento de la llamada; remite al Art. VIII para el modo de respaldo. | Aclaración, no enmienda protegida |
| *(completar)* | Art. III — nueva Sección 3.2.1 | Define operacionalmente "señal negativa" y la regla de conteo/resolución para clasificación global. | Calibración libre (12.2) |
| *(completar)* | Art. VIII — Sección 8.1 reescrita | El modo de respaldo debe usar respuestas cacheadas generadas previamente por el mismo modelo de IA, nunca texto redactado manualmente por el equipo. Exige indicador visible cuando el fallback está activo. | Calibración libre (12.2) |
| *(completar)* | Art. IX — nueva Sección 9.3 | Define qué hacer cuando faltan 2 o 3 variables, y qué se considera "dato faltante" técnicamente. Introduce el estado "⚪ Dato insuficiente". | Calibración libre (12.2) |
| *(completar)* | Art. X — Sección 10.1 ajustada (puntos 3, 5, 7) | Aclara que las respuestas de respaldo cuentan como generadas por IA; añade criterio de aceptación para manejo de datos insuficientes. | Consecuencia directa de los cambios anteriores |

*Ninguno de estos cambios modifica el contenido protegido de los Artículos II, IV o V — solo aclara la interacción entre artículos y cierra ambigüedades operativas. Por eso no requieren el proceso de acuerdo unánime documentado de la Sección 12.1.*

---

## Siguiente paso sugerido
**Fase 3 — Especificación (Spec):** traducir estos artículos en especificaciones técnicas concretas: esquema de datos exacto (incluyendo representación de valores faltantes según Art. IX, 9.3.3), contrato de entrada/salida del modelo de IA generativa, wireframe del dashboard (incluyendo el estado "⚪ Dato insuficiente" y el indicador de modo de respaldo), casos de prueba para calibrar los umbrales de riesgo y validar la regla de señal negativa (Art. III, 3.2.1), y el diseño del mecanismo de fallback con cacheo real (Art. VIII, 8.1).
