# 🔍 FisiChecker — Sistema Unificado de Auditoría de Accesibilidad Web (WCAG 2.1)

**FisiChecker** es una plataforma integral desarrollada en **Python & Django** para la evaluación, diagnóstico y reporte automático de accesibilidad web bajo el estándar internacional **WCAG 2.1 (Niveles A, AA y AAA)**.

El sistema integra interfaz web completa (HTML5 + CSS con soporte para tema oscuro + JavaScript nativo), motor de scraping y análisis de los 78 criterios de éxito WCAG, exportación multiformato (CSV y Excel) y API REST.

---

## 🚀 Características Principales

* **Auditoría Integral de 78 Criterios WCAG 2.1**:
  * **Principio 1: Perceptible** (29 criterios) — Contraste de color, alternativas de texto (alt), jerarquía semántica, subtítulos, redimensionamiento de texto y diseño adaptable (reflow).
  * **Principio 2: Operable** (29 criterios) — Accesibilidad completa por teclado, sin trampas de foco, enlaces y botones descriptivos, skip-links, páginas tituladas y control de movimiento.
  * **Principio 3: Comprensible** (17 criterios) — Idioma de la página y partes, prevención e identificación de errores en formularios, etiquetas claras e instrucciones.
  * **Principio 4: Robusto** (3 criterios) — Análisis sintáctico (parsing sin IDs duplicados), nombre/rol/valor en componentes ARIA y regiones de estado.

* **Frontend Unificado (Sin dependencias de Node.js)**:
  * Renderizado directo con Django Templates y estilos CSS modernos.
  * Selector de tema Claro / Oscuro con persistencia en navegador.
  * Filtrado interactivo en vivo por Principio, Nivel (A/AA/AAA) y Veredicto (*Cumple, No Cumple, Parcial, N/A*).
  * Desglose con explicaciones pedagógicas: *"¿Qué evalúa este criterio?"* y *"¿Qué se detectó en el código?"*.

* **Métricas y Análisis Avanzado**:
  * Puntuación de conformidad global calculada según la fórmula de **Hilera et al.** (excluyendo criterios no aplicables).
  * Clasificación de accesibilidad: *Alto, Moderado, Deficiente, Muy deficiente*.
  * Script integrado para análisis y generación de gráficos en **Google Colab**.

* **Exportación y Gestión de Reportes**:
  * Exportación en **Excel (.xlsx)** con hojas separadas de *Resumen* y *Detalles de Criterios*.
  * Exportación en **CSV** con soporte de codificación UTF-8 BOM.
  * Historial de auditorías persistido por usuario en base de datos.

---

## 🛠️ Requisitos del Sistema

* **Python 3.10 o superior**
* **pip** (gestor de paquetes de Python)
* **SQLite** (incluido por defecto) o **MySQL / PostgreSQL**

---

## 📦 Instalación y Puesta en Marcha

### 1. Clonar el repositorio
```bash
git clone https://github.com/JhosepSF/FisiChecker.git
cd FisiChecker/Back
```

### 2. Crear y activar entorno virtual
```bash
# En Windows (PowerShell):
python -m venv .venv
.venv\Scripts\activate

# En Linux / macOS:
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Base de Datos y Migraciones
```bash
python manage.py migrate
```

### 5. Crear usuario administrador (Opcional pero recomendado)
```bash
python manage.py createsuperuser
```

### 6. Iniciar el Servidor de Aplicación
```bash
python manage.py runserver
```

La aplicación estará lista y accesible en tu navegador en:
👉 **`http://127.0.0.1:8000/`**

---

## 📁 Estructura del Proyecto

```
FisiChecker/
└── Back/
    ├── FisiChecker/              # Configuración global del proyecto Django
    │   ├── settings.py           # Configuración de base de datos, sesiones y static
    │   ├── urls.py               # Enrutamiento de vistas web y API REST
    │   └── wsgi.py               # Entrada WSGI para producción
    │
    ├── audits/                   # Módulo central de auditorías WCAG
    │   ├── models.py             # Modelos WebsiteAudit y WebsiteAuditResult
    │   ├── views.py              # Vistas HTML y controladores de API REST
    │   ├── audit.py              # Motor de orquestación de auditorías
    │   ├── statistics.py         # Métricas Hilera et al. y reportes estadísticos
    │   │
    │   ├── checks/criteria/      # Implementación individual de los 78 criterios WCAG
    │   │   ├── p1/               # Criterios del Principio 1 (Perceptible)
    │   │   ├── p2/               # Criterios del Principio 2 (Operable)
    │   │   ├── p3/               # Criterios del Principio 3 (Comprensible)
    │   │   └── p4/               # Criterios del Principio 4 (Robusto)
    │   │
    │   ├── wcag/                 # Utilidades WCAG y analizador profundo (enricher)
    │   │   ├── context.py        # Extractor del DOM y árbol de elementos
    │   │   ├── enricher.py       # Enriquecimiento semántico y detección de evidencias
    │   │   └── constants.py      # Metadatos oficiales WCAG 2.1
    │   │
    │   ├── templates/audits/     # Plantillas HTML del Frontend
    │   │   ├── base.html         # Layout base con header, usuario y tema
    │   │   ├── login.html        # Formulario de autenticación
    │   │   ├── panel.html        # Panel de control y auditoría en tiempo real
    │   │   ├── audit_detail.html # Reporte completo e imprimible
    │   │   └── colab.html        # Script para Google Colab
    │   │
    │   └── static/audits/        # Archivos estáticos CSS y JS
    │       ├── css/login.css     # Estilos de inicio de sesión
    │       ├── css/panel.css     # Sistema de diseño con modo oscuro
    │       └── js/panel.js       # Interactividad, filtros y cliente de auditoría
    │
    ├── manage.py                 # CLI de gestión Django
    ├── requirements.txt          # Dependencias Python del proyecto
    └── db.sqlite3                # Base de datos local
```

---

## 🔌 Rutas y Endpoints Disponibles

### Vistas Web (Frontend)
| Ruta | Descripción |
| :--- | :--- |
| **`/` o `/panel/`** | Panel Principal: Buscador de URLs, ejecución de auditoría y filtros interactivos. |
| **`/login/`** | Pantalla de inicio de sesión de usuarios y auditores. |
| **`/logout/`** | Cierre seguro de sesión. |
| **`/audits/<id>/`** | Vista detallada e imprimible del reporte de una auditoría guardada. |
| **`/colab/`** | Cuaderno de análisis con script en Python para Google Colab. |
| **`/admin/`** | Panel de administración de Django (gestión de usuarios y registros). |

### Exportación de Datos
| Endpoint | Formato | Descripción |
| :--- | :--- | :--- |
| **`GET /api/export/excel`** | `.xlsx` | Libro Excel con hojas de *Resumen* y *Criterios WCAG*. |
| **`GET /api/export/csv`** | `.csv` | Archivo CSV detallado de las auditorías del usuario. |

### API REST
| Endpoint | Método | Descripción |
| :--- | :--- | :--- |
| **`/api/audit`** | `POST` | Ejecuta una nueva auditoría enviando `{"url": "https://..."}`. |
| **`/api/audits`** | `GET` | Lista las auditorías del usuario autenticado. |
| **`/api/audits/<id>`** | `GET` | Obtiene el JSON completo con resultados de una auditoría. |
| **`/api/audits/<id>/delete/`** | `DELETE` | Elimina una auditoría y sus registros vinculados. |
| **`/api/statistics/report/`** | `GET` | Reporte consolidado de métricas y estadísticas globales. |

---

## 📄 Licencia

Este proyecto se distribuye bajo la **Licencia MIT**.

```
MIT License

Copyright (c) 2026 JhosepSF - FisiChecker (UNMSM - FISI)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🎓 Créditos y Contexto Académico

Desarrollado como proyecto de investigación y desarrollo en la **Facultad de Ingeniería de Sistemas e Informática (FISI)** de la **Universidad Nacional Mayor de San Marcos (UNMSM)**, Lima, Perú.
