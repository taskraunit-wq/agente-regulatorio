from flask import Flask, request, jsonify
import pdfplumber

app = Flask(__name__)

@app.route("/")
def home():
    return "Agente regulatorio activo 🚀"

@app.route("/analizar", methods=["POST"])
def analizar():
    file = request.files["file"]

    texto = ""
    with pdfplumber.open(file) as pdf:
        for pagina in pdf.pages:
            texto += pagina.extract_text() or ""

    return jsonify({
        "resultado": texto[:1000]  # solo muestra parte
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
