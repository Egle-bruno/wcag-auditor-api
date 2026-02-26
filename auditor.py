from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import time

# 1. Inicializamos la aplicación y activamos CORS
# CORS es necesario para que Microsoft pueda enviarnos datos sin bloqueos de seguridad
app = Flask(__name__)
CORS(app)

# 2. La lógica de auditoría (El "Cerebro")
def realizar_auditoria(html_codigo):
    inicio_ia = time.time()
    errores = []
    
    # Detección de errores (WCAG)
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

# 3. Creamos la "puerta" o Endpoint de la API
# Aquí es donde Power Automate enviará el HTML sucio
@app.route('/audit', methods=['POST'])
def audit_endpoint():
    # Recibimos el JSON que envía el bot
    data = request.get_json()
    
    # Validamos que nos hayan enviado la variable 'html_content'
    if not data or 'html_content' not in data:
        return jsonify({"error": "No se recibió contenido"}), 400
    
    # Procesamos y devolvemos la respuesta en formato JSON
    resultado = realizar_auditoria(data['html_content'])
    return jsonify(resultado)

# 4. Arrancamos el servidor en tu computadora
if __name__ == '__main__':
    app.run(debug=True, port=5000)