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


# Pendiente: combina regla_aplica y cumple_regla.
# def evaluar(item: ChecklistItem, hechos: dict) -> Evaluacion:
#     ...