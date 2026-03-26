from flask import Flask, request, jsonify
import os
from flask_cors import CORS
from openai import OpenAI
import PyPDF2

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/analizar", methods=["POST"])
def analizar():
    if 'file' not in request.files:
        return jsonify({"error": "No se recibió archivo"}), 400

    file = request.files['file']

    # Leer PDF
    reader = PyPDF2.PdfReader(file)
    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

    # 🔥 AQUÍ entra la IA
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un experto en regulación sanitaria y etiquetado."},
            {"role": "user", "content": f"Analiza este documento y detecta riesgos regulatorios:\n{text[:3000]}"}
        ]
    )

    resultado = response.choices[0].message.content

    return jsonify({
        "mensaje": "OK",
        "analisis": resultado
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
