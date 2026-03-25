from flask import Flask, request, jsonify
import pdfplumber

app = Flask(__name__)

@app.route("/")
def home():
    return "Agente regulatorio activo 🚀"

@app.route("/analizar", methods=["POST"])
def analizar():
    try:
        # Verificar si viene archivo
        if 'file' not in request.files:
            return jsonify({"error": "No se encontró el archivo"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "Archivo vacío"}), 400

        texto = ""

        with pdfplumber.open(file) as pdf:
            for pagina in pdf.pages:
                texto += pagina.extract_text() or ""

        return jsonify({
            "mensaje": "PDF procesado correctamente",
            "preview": texto[:500]
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
