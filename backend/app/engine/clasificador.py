import unicodedata

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