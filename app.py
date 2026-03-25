from flask import Flask, request, jsonify
import pdfplumber
import os
from anthropic import Anthropic

app = Flask(__name__)

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

@app.route("/")
def home():
    return "Agente regulatorio activo 🚀"

@app.route("/analizar", methods=["POST"])
def analizar():
    file = request.files["file"]

    texto = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            texto += page.extract_text() or ""

    respuesta = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": f"Analiza este documento regulatorio:\n\n{texto}"
            }
        ]
    )

    return jsonify({"resultado": respuesta.content[0].text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
