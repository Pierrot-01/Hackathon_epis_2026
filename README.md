# 🏫 Vanguardia EPIS — Detección Temprana de Riesgo Escolar

Sistema de alerta temprana y recomendación pedagógica personalizada para docentes y tutores de instituciones rurales y urbano-marginales de Perú, diseñado para operar bajo condiciones de conectividad limitada.

---

## 🛠️ Metodología SDD (Spec-Driven Development) Aplicada

Este proyecto se ha desarrollado bajo la metodología **SDD (Desarrollo Guiado por Especificación)**, estructurado en tres fases estratégicas antes de escribir la primera línea de código:

1. **Captura de Intención (Fase 1 - SSD):** Definición del problema, usuarios (docentes/tutores) y limitaciones de infraestructura (falta de conectividad recurrente en el hogar).
2. **Constitución del Proyecto (Fase 2):** Establecimiento de reglas de negocio inmutables (Artículos I a XII), destacando la no estigmatización del estudiante (Art. IV) y la división estricta de responsabilidades (Art. II).
3. **Especificación Técnica y Blueprint (Fase 3):** Congelación del diseño del motor de reglas, prompts del sistema, contratos de datos (JSON schemas), casos de prueba y mecanismo de fallback.

### Ventajas de SDD en este MVP:
* **Separación de Responsabilidades:** La clasificación de riesgo (🟢/🟡/🔴/⚪) es **100% determinista e idéntica en cualquier ejecución** (motor de reglas auditable), mientras que la IA Generativa se limita exclusivamente a redactar la explicación contextualizada y recomendaciones de apoyo pedagógico.
* **Resiliencia Predictiva:** Se especificó un mecanismo de caché offline obligatorio (Art. VIII) antes de codificar, asegurando que si la API Key falla o excede la cuota de peticiones (Rate Limits), el sistema siga operativo mostrando respuestas previamente validadas.
* **Calidad de Datos:** Manejo preciso de datos ausentes parciales o totales (Art. IX), definiendo el estado de `⚪ Dato insuficiente` para evitar estigmatizar al estudiante si no hay variables registradas.

---

## 🏗️ Estructura del Proyecto

```
proyecto/
├── backend/
│   ├── main.py            # API REST (FastAPI) y servicio de archivos estáticos
│   ├── classifier.py      # Lógica determinista de clasificación de riesgo (Art. III)
│   ├── ia_client.py       # Conector con Google Gemini API (gemini-2.0-flash)
│   ├── fallback.py        # Módulo de gestión de caché local
│   ├── requirements.txt   # Dependencias de Python
│   └── .env.example       # Plantilla de variables de entorno
├── data/
│   └── estudiantes.json   # Dataset ficticio de 20 estudiantes de prueba
├── cache/
│   └── respuestas_ia.json # Explicaciones de IA cacheadas
├── frontend/              # Interfaz de usuario (HTML5/Vanilla JS/Tailwind CSS)
│   ├── index.html         # Pantalla de Login
│   ├── monitoreo.html     # Panel de Monitoreo Interactivo
│   ├── admin.html         # Métricas y Distribución Global
│   └── reportes.html      # Reportes analíticos y listados completos
├── start.sh               # Script de inicio automatizado para Linux/macOS
└── generar_cache.py       # Script utilitario para pre-generar el caché de la IA
```

---

## 🚀 Guía de Instalación y Despliegue

Sigue estos pasos para desplegar el proyecto en cualquier dispositivo:

### 1. Requisitos Previos
* **Python 3.11 o superior** instalado.
* Gestor de paquetes **pip**.
* Una cuenta de desarrollo y **Gemini API Key** (puedes obtenerla gratis en [Google AI Studio](https://aistudio.google.com/app/apikey)).

### 2. Clonar el Repositorio
```bash
git clone https://github.com/Pierrot-01/Hackathon_epis_2026.git
cd Hackathon_epis_2026
```

### 3. Instalar Dependencias
Instala los paquetes necesarios en el entorno global (o en tu entorno virtual):
```bash
pip install -r backend/requirements.txt
```
*(Nota: Si usas distribuciones Linux basadas en Debian/Arch que restringen instalaciones globales, puedes añadir la bandera `--break-system-packages` o crear un entorno virtual virtualenv)*.

### 4. Configurar Variables de Entorno
Crea el archivo `.env` dentro del directorio `backend/`:
```bash
cp backend/.env.example backend/.env
```
Edita `backend/.env` e introduce tu clave:
```env
GEMINI_API_KEY=tu-api-key-de-gemini-aqui
```

### 5. Pre-generar el Caché (Recomendado para la demo / Sin conexión)
Para evitar rate-limits durante la demo, o para trabajar completamente offline, pre-carga las respuestas de la IA ejecutando:
```bash
export GEMINI_API_KEY=tu-api-key-de-gemini-aqui
python3 generar_cache.py
```
Este script evaluará los estudiantes e invocará la API de Gemini para guardar las explicaciones en `cache/respuestas_ia.json`.

### 6. Ejecutar el Servidor
Puedes iniciar el proyecto con el script automatizado:
```bash
./start.sh
```
O ejecutando FastAPI directamente:
```bash
cd backend
python3 main.py
```

El servidor estará escuchando en **`http://localhost:8000`**.

---

## 🎯 Verificación e Integridad
Para validar el correcto funcionamiento del motor de reglas determinista y asegurar el cumplimiento del Artículo III de la Constitución, ejecuta la suite de pruebas unitarias locales:
```bash
python3 backend/classifier.py
```
*Salida esperada: `✅ Todos los tests pasaron! (10/10)`*
