from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import re
import time

app = Flask(__name__)
CORS(app)

def realizar_auditoria(html_codigo):
    inicio_ia = time.time()
    errores = []
    
    # 1. Validación de Imágenes
    if re.search(r'<img(?!.*?alt=)', html_codigo):
        errores.append({"prioridad": "ALTA", "error": "Falta atributo ALT en imágenes."})
    
    # 2. Validación de Idioma
    if 'lang=' not in html_codigo.lower():
        errores.append({"prioridad": "MEDIA", "error": "Falta atributo 'lang' en la etiqueta <html>."})

    # 3. Validación de Títulos (Nueva Regla)
    if not re.search(r'<h1', html_codigo.lower()):
        errores.append({"prioridad": "ALTA", "error": "No se encontró un título principal (<h1>)."})

    tiempo_ia = round(time.time() - inicio_ia, 4)
    
    # Generar código corregido básico
    codigo_limpio = html_codigo
    if 'lang=' not in codigo_limpio.lower():
        codigo_limpio = codigo_limpio.replace("<html>", "<html lang='es'>")

    return {
        "resumen": {
            "total_errores": len(errores),
            "tiempo": f"{tiempo_ia}s",
            "ahorro_estimado": f"{len(errores) * 5} min"
        },
        "detalles": errores,
        "codigo_corregido": codigo_limpio
    }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/audit', methods=['POST'])
def audit_endpoint():
    data = request.get_json()
    if not data or 'html_content' not in data:
        return jsonify({"error": "Contenido no recibido"}), 400
    return jsonify(realizar_auditoria(data['html_content']))

if __name__ == '__main__':
    app.run(debug=True)