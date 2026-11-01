import unicodedata
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