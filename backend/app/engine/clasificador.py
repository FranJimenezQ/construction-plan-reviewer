import unicodedata
from pydantic import BaseModel
import pymupdf
from app.models.checklist import TipoVista
from app.data.sinonimos import SINONIMOS
import re

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


# Modelo para clasificar_pdf . PaginaClasificada, contiene archivo, pagina y vistas

class PaginaClasificada(BaseModel):
    archivo: str
    pagina: int
    vistas: set[TipoVista]

# Abre un PDF y clasifica cada página.
# Ej: "Lam-02.pdf" -> [PaginaClasificada(archivo="Lam-02.pdf", pagina=1, vistas={ELEVACIONES, CORTES})]
    # Paso 1: abrir el PDF con pymupdf.open(ruta)
    # Paso 2: lista vacía de resultados
    # Paso 3: recorrer las páginas con enumerate(..., start=1)
    #         (igual que en tu explorador_pdf.py)
    #         para cada página: extraer el texto, clasificarlo
    #         y agregar un PaginaClasificada a la lista
    # Paso 4: devolver la lista

def clasificar_pdf(ruta: str) -> list[PaginaClasificada]:
    pdf = pymupdf.open(ruta)
    resultados = []
    for numero, pagina in enumerate(pdf, start=1):
        texto = pagina.get_text()
        vistas = clasificar_texto(texto)
        resultados.append(PaginaClasificada(archivo=ruta, pagina=numero, vistas=vistas))
    return resultados