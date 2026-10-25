from app.engine.evaluador import evaluar
from app.engine.evaluador import cumple_regla, regla_aplica
from app.models.checklist import Regla, altura_maxima, dormitorios
from app.models.result import Resultado


# ---------- cumple_regla ----------

def test_altura_dentro_del_maximo():
    regla = Regla(magnitud="altura", maximo=7.0, unidad="m")
    assert cumple_regla(regla, 4.98) is True


def test_altura_sobre_el_maximo():
    regla = Regla(magnitud="altura", maximo=7.0, unidad="m")
    assert cumple_regla(regla, 8.5) is False


# ---------- regla_aplica ----------

def test_regla_sin_condicion_siempre_aplica():
    regla = Regla(magnitud="area", minimo=9.0, unidad="m²")
    hechos = {"area": 8.39, "lado_menor": 2.80}
    assert regla_aplica(regla, hechos) is True


def test_regla_aplica_si_coincide_condicion():
    regla = Regla(magnitud="altura", maximo=7.0, unidad="m", condicion={"plantas": 1})
    hechos = {"altura": 8.5, "plantas": 1}
    assert regla_aplica(regla, hechos) is True


def test_regla_no_aplica_si_no_coincide():
    regla = Regla(magnitud="altura", maximo=10.0, unidad="m", condicion={"plantas": 2})
    hechos = {"altura": 8.5, "plantas": 1}
    assert regla_aplica(regla, hechos) is False

def test_dormitorio_angosto_no_cumple():
    hechos = {"area": 9.5, "lado_menor": 2.0}
    assert evaluar(dormitorios, hechos).resultado == Resultado.NO_CUMPLE


def test_altura_sin_plantas_no_decide():
    hechos = {"altura": 4.98}
    assert evaluar(altura_maxima, hechos).resultado is None

def test_dormitorio_sin_lado_no_decide():
    hechos = {"area": 9.5}
    resultado = evaluar(dormitorios, hechos)
    assert resultado.resultado is None
    assert "lado_menor" in resultado.faltantes