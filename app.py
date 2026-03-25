from flask import Flask, request, jsonify
import pdfplumber

app = Flask(__name__)

@app.route("/")
def home():
    return "Agente regulatorio activo 🚀"

@app.route("/analizar", methods=["POST"])
def analizar():
    print("HEADERS:", request.headers)
    print("FILES:", request.files)

    if 'file' not in request.files:
        return jsonify({
            "error": "No se recibió archivo",
            "debug_files": str(request.files)
        }), 400

    file = request.files['file']

    texto = ""

    try:
        with pdfplumber.open(file) as pdf:
            for pagina in pdf.pages:
                texto += pagina.extract_text() or ""

        return jsonify({
            "mensaje": "OK",
            "preview": texto[:500]
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
