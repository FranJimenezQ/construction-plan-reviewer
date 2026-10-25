from pydantic import BaseModel

from app.models.checklist import ChecklistItem, Regla
from app.models.result import Resultado


class Evaluacion(BaseModel):
    resultado: Resultado | None   # None = no se pudo decidir
    faltantes: list[str] = []
    detalles: list[str] = []


# ¿El valor respeta el mínimo y el máximo de la regla?
def cumple_regla(regla: Regla, valor: float) -> bool:
    if regla.minimo is not None and valor < regla.minimo:
        return False
    if regla.maximo is not None and valor > regla.maximo:
        return False
    return True


# ¿Esta regla le corresponde al proyecto? Solo mira la condición
# (plantas, tapia...), nunca el valor medido.
def regla_aplica(regla: Regla, hechos: dict) -> bool:
    if regla.condicion is None:
        return True
    for clave, valor_esperado in regla.condicion.items():
        if hechos.get(clave) != valor_esperado:
            return False
    return True


# Decide si el proyecto cumple el criterio. None = faltan datos.
def evaluar(item: ChecklistItem, hechos: dict) -> Evaluacion:
    faltantes = []
    detalles = []

    # 1: filtrar solo las reglas que aplican
    aplicables = []
    for regla in item.reglas:
        if regla_aplica(regla, hechos):
            aplicables.append(regla)
        else:
            detalles.append(f"Regla {regla.magnitud} no aplica (condición no cumplida).")

    if len(aplicables) == 0:
        faltantes.append("No se pudo determinar ninguna regla aplicable. (revisar condiciones)")
        return Evaluacion(resultado=None, faltantes=faltantes, detalles=detalles)

    # 2: Estan todos los datos necesarios para evaluar las reglas aplicables? Agrega regla magnitud
         # a la lista de faltantes.
         #Al terminar, si hay faltantes, devuelve resultado=None
    for regla in aplicables:
        if regla.magnitud not in hechos:
            faltantes.append(regla.magnitud)
            detalles.append(f"Falta el dato {regla.magnitud} para evaluar la regla.")

    if len(faltantes) > 0:
        return Evaluacion(resultado=None, faltantes=faltantes, detalles=detalles)

    # Pasada 3: ¿cumplen todas?
    #   empieza con todas_cumplen = True
    #   para cada regla aplicable: si no cumple, todas_cumplen = False
    #   agrega un texto a detalles en cada vuelta
    #   al terminar el for, decide CUMPLE o NO_CUMPLE según todas_cumplen
    todas_cumplen = True
    for regla in aplicables:
        valor = hechos.get(regla.magnitud)
        if cumple_regla(regla, valor):
            detalles.append(f"Regla {regla.magnitud} cumple (valor={valor}).")
        else:
            todas_cumplen = False
            detalles.append(f"Regla {regla.magnitud} NO cumple (valor={valor}).")

    if todas_cumplen:
        return Evaluacion(resultado=Resultado.CUMPLE, faltantes=faltantes, detalles=detalles)
    else:
        return Evaluacion(resultado=Resultado.NO_CUMPLE, faltantes=faltantes, detalles=detalles)