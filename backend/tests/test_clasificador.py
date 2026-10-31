from app.engine.clasificador import normalizar

def test_quita_tildes_y_pasa_a_mayusculas():
    assert normalizar("Distribución Eléctrica") == "DISTRIBUCION ELECTRICA"

def test_colapsa_espacios_dobles():
    assert normalizar("UBICACIÓN  GEOGRAFICA") == "UBICACION GEOGRAFICA"

def test_une_saltos_de_linea():
    assert normalizar("Planta de\nTechos") == "PLANTA DE TECHOS"