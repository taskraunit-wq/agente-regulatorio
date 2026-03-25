from anthropic import Anthropic
import pdfplumber

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def extraer_texto_pdf(ruta):
    texto = ""
    with pdfplumber.open(ruta) as pdf:
        for pagina in pdf.pages:
            texto += pagina.extract_text() or ""
    return texto

def revisar(arte, marbete):
    prompt = f"""
Actúas como experto regulatorio.

MARBETE APROBADO:
{marbete}

ARTE NUEVO:
{arte}

Dime:
1. Diferencias
2. Riesgos
3. Recomendaciones
"""
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

arte = extraer_texto_pdf("arte.pdf")
marbete = extraer_texto_pdf("marbete.pdf")

print(revisar(arte, marbete))