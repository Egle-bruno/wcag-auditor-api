from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import re
import time

# 1. Configuración inicial
app = Flask(__name__)
CORS(app)

# 2. El "Cerebro" de la auditoría
def realizar_auditoria(html_codigo):
    inicio_ia = time.time()
    errores = []
    
    # Detección de errores WCAG (Imágenes y Lenguaje)
    if re.search(r'<img(?!.*?alt=)', html_codigo):
        errores.append({"error": "[ALTA] Falta atributo ALT en imágenes."})
    
    if 'lang=' not in html_codigo.lower():
        errores.append({"error": "[BAJA] Falta atributo 'lang' en <html>."})

    tiempo_ia = round(time.time() - inicio_ia, 4)
    ahorro = len(errores) * 5

    return {
        "resumen_ejecutivo": {
            "estado": "Finalizado con éxito",
            "total_errores": len(errores),
            "tiempo_ia": f"{tiempo_ia}s",
            "tiempo_humano_ahorrado": f"{ahorro} min"
        },
        "detalles_tecnicos": errores,
        "codigo_limpio": html_codigo.replace("<html>", "<html lang='es'>")
    }

# 3. RUTA VISUAL (La cara del proyecto en la nube)
@app.route('/')
def home():
    # Esta línea busca el archivo index.html dentro de la carpeta /templates
    return render_template('index.html')

# 4. RUTA TÉCNICA (La que procesa los datos)
@app.route('/audit', methods=['POST'])
def audit_endpoint():
    data = request.get_json()
    
    # Validamos que el paquete traiga la etiqueta 'html_content'
    if not data or 'html_content' not in data:
        return jsonify({"error": "No se recibió contenido HTML"}), 400
    
    resultado = realizar_auditoria(data['html_content'])
    return jsonify(resultado)

# 5. Encendido del servidor
if __name__ == '__main__':
    app.run(debug=True, port=5000)