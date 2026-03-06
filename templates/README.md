# 🔍 Auditor de Accesibilidad WCAG (API & Web)

Esta es una herramienta profesional para la detección automática de errores de accesibilidad web, diseñada para ayudar a desarrolladores a cumplir con las normativas internacionales de inclusión digital.

## ✨ Funciones principales
- **Detección de Imágenes:** Identifica la falta de atributos `alt` para lectores de pantalla.
- **Validación de Idioma:** Verifica que la etiqueta `<html>` tenga el atributo `lang`.
- **Estructura Semántica:** Asegura que exista al menos un título principal `<h1>`.
- **Corrección Automática:** Genera una propuesta de código limpio y corregido.

## 🛠️ Tecnologías utilizadas
- **Backend:** Python 3.10 + Flask.
- **Deployment:** Render (PaaS).
- **Frontend:** HTML5, CSS3 y JavaScript moderno (Fetch API).
- **Seguridad:** CORS habilitado para conexiones remotas.

## 🚀 Cómo usar la API
Puedes enviar una petición POST a la siguiente URL:
`https://wcag-auditor-api.onrender.com/audit`

Con el siguiente cuerpo JSON:
{ "html_content": "tu código html aquí" }