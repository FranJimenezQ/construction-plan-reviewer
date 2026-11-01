from app.engine.clasificador import normalizar, clasificar_texto
from app.models.checklist import TipoVista


def test_quita_tildes_y_pasa_a_mayusculas():
    assert normalizar("Distribución Eléctrica") == "DISTRIBUCION ELECTRICA"

def test_colapsa_espacios_dobles():
    assert normalizar("UBICACIÓN  GEOGRAFICA") == "UBICACION GEOGRAFICA"

def test_une_saltos_de_linea():
    assert normalizar("Planta de\nTechos") == "PLANTA DE TECHOS"

def test_detecta_vista_mecanica():
    texto = "PLANTA DE\nDISTRIBUCION MECANICA\nTANQUE SEPTICO"
    assert clasificar_texto(texto) == {TipoVista.MECANICA}

def test_detecta_varias_vistas():
    texto = "PLANTA LOCALIZACION ... PLANTA DE TECHOS ... ACABADOS GENERALES"
    assert clasificar_texto(texto) == {
        TipoVista.LOCALIZACION, TipoVista.TECHOS, TipoVista.ACABADOS
    }

def test_tildes_y_minusculas_no_importan():
    texto = "Planta de Distribución Eléctrica"
    assert clasificar_texto(texto) == {TipoVista.ELECTRICA}

def test_simbologia_no_es_elevacion():
    texto = "ELEVACION Y CORTE\nINDICA LA LAMINA DONDE SE VA A UBICAR EL CORTE"
    assert clasificar_texto(texto) == set()

def test_detecta_corte_real():
    assert TipoVista.CORTES in clasificar_texto("CORTE A-A")

def test_detalle_de_corte_no_es_corte():
    assert TipoVista.CORTES not in clasificar_texto("Detalle de corte tipico")

def test_corte_de_tuberia_no_es_corte():
    assert TipoVista.CORTES not in clasificar_texto("CORTE 45º")