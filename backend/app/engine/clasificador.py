import unicodedata
from pydantic import BaseModel
import pymupdf
from app.models.checklist import TipoVista
from app.data.sinonimos import SINONIMOS
import re
import os

# Modelo para clasificar_pdf . PaginaClasificada, contiene archivo, pagina y vistas
class PaginaClasificada(BaseModel):
    archivo: str
    pagina: int
    vistas: set[TipoVista]

# Deja un texto listo para comparar con el diccionario de sinónimos:
# mayúsculas, sin tildes y con un solo espacio entre palabras.
# Ej: "Distribución  Eléctrica" -> "DISTRIBUCION ELECTRICA"
def normalizar(texto: str) -> str:
    # Quitar tildes y pasar a mayúsculas
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8').upper()
    
    # Separar el texto en palabras
    palabras = texto.split()
        
    # split() separa por cualquier espacio o salto de línea;
    # join() vuelve a unir con un solo espacio    
    texto_normalizado = ' '.join(palabras)
    
    return texto_normalizado


# Funcion clasificar_texto Normalizar el texto de entrada.
#Crear un conjunto vacío de vistas encontradas.
#Para cada vista y su lista de frases en SINONIMOS: si alguna frase aparece dentro del texto normalizado, agregar la vista al conjunto.
#Devolver el conjunto.

def clasificar_texto(texto: str) -> set[TipoVista]:
    texto_normalizado = normalizar(texto)
    vistas_encontradas = set()
    for vista, frases in SINONIMOS.items():
        if any(frase in texto_normalizado for frase in frases):
            vistas_encontradas.add(vista)
    if re.search(r"CORTE [A-Z]-[A-Z]", texto_normalizado):
        vistas_encontradas.add(TipoVista.CORTES)
    return vistas_encontradas

# Busca el cuadro del índice: el rectángulo dibujado más pequeño
# que contiene el texto "INDICE". Devuelve None si no hay índice.
def encontrar_zona_indice(pagina) -> pymupdf.Rect | None:
    for bloque in pagina.get_text("blocks"):
        if normalizar(bloque[4]) == "INDICE":
            rect_indice = pymupdf.Rect(bloque[:4])
            marcos = [d["rect"] for d in pagina.get_drawings()
                      if d["rect"].contains(rect_indice)]
            if marcos:
                return min(marcos, key=lambda r: r.get_area())
    return None

# Abre un PDF y clasifica cada página bloque por bloque,
# ignorando el texto que está dentro del cuadro del índice.
# Ej: "Lam-02.pdf" -> [PaginaClasificada(archivo="Lam-02.pdf", pagina=1, vistas={ELEVACIONES, CORTES})]

def clasificar_pdf(ruta: str) -> list[PaginaClasificada]:
    pdf = pymupdf.open(ruta)
    resultados = []
    for numero, pagina in enumerate(pdf, start=1):
        zona_indice = encontrar_zona_indice(pagina)
        vistas = set()
        for bloque in pagina.get_text("blocks"):
            rect_bloque = pymupdf.Rect(bloque[:4])
            if zona_indice and zona_indice.contains(rect_bloque):
                continue
            vistas.update(clasificar_texto(bloque[4]))
        resultados.append(PaginaClasificada(archivo=os.path.basename(ruta), pagina=numero, vistas=vistas))
    return resultados