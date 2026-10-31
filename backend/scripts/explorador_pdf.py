import sys
import pymupdf  # PyMuPDF

ruta = sys.argv[1]
pdf = pymupdf.open(ruta)

for numero, pagina in enumerate(pdf, start=1):
    texto = pagina.get_text()
    print(f"--- Página {numero} ---")
    print(texto)