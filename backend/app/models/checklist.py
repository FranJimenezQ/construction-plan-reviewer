from enum import Enum
from pydantic import BaseModel

class TipoVerificacion(str, Enum):
    PRESENCIA = "presencia"
    MEDICION = "medicion"
    CALCULO = "calculo"
    CONDICIONAL = "condicional"
    DOCUMENTO = "documento"
    MANUAL = "manual"

class TipoLamina(str, Enum):
    LOCALIZACION = "localizacion"
    DISTRIBUCION = "distribucion"
    ELEVACIONES = "elevaciones"
    # ... tú completas el resto

class ChecklistItem(BaseModel):
    id: str
    aspecto: str
    criterio: str
    tipo_verificacion: TipoVerificacion
    laminas_requeridas: list[TipoLamina]
    umbral_minimo: float | None = None   # None = no aplica
    umbral_maximo: float | None = None
    unidad: str | None = None

retiro_frontal = ChecklistItem(
    id="retiro-frontal",
    aspecto="Retiros frontales",
    criterio="Retiro mínimo de 2 m desde la línea de propiedad.",
    tipo_verificacion=TipoVerificacion.MEDICION,
    laminas_requeridas=[TipoLamina.LOCALIZACION],
    umbral_minimo=2.0,
    unidad="m",
)

if __name__ == "__main__":
    print(retiro_frontal.model_dump_json(indent=2))