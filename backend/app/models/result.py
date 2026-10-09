from enum import Enum
from typing import List, Optional
from pydantic import BaseModel
from app.models.checklist import TipoVista

class EstadoRevision(str, Enum):
    PENDIENTE = "pendiente"
    PROPUESTO_POR_IA = "propuesto por IA"
    REVISION_MANUAL = "revisión manual"
    CONFIRMADO = "confirmado"

class Resultado(str, Enum):
    CUMPLE = "cumple"
    NO_CUMPLE = "no cumple"
    NO_APLICA = "no aplica"

class Evidencia(BaseModel):
    archivo: str | None = None
    lamina: str
    pagina: int | None = None
    vista: TipoVista | None = None
    descripcion: str
    valor_leido: str | None = None

class ItemResult(BaseModel):
    criterio_id: str
    estado: EstadoRevision = EstadoRevision.PENDIENTE
    resultado_ia: Resultado | None = None
    resultado_final: Resultado | None = None
    hechos: dict[str, float | int | bool | str] = {}
    datos_faltantes: List[str] = []
    evidencias: List[Evidencia] = []
    observaciones: str | None = None
    revisado_por: str | None = None


 
# ============================================================
# CASOS DE PRUEBA (basados en las láminas de mi casa)
# ============================================================
 
# Caso 1: la IA encuentra todo, el código decide "cumple"
# y el revisor confirma sin cambios.
caso_altura = ItemResult(
    criterio_id="altura-maxima",
    estado=EstadoRevision.CONFIRMADO,
    resultado_ia=Resultado.CUMPLE,
    resultado_final=Resultado.CUMPLE,
    hechos={"altura": 4.98, "plantas": 1},
    evidencias=[
        Evidencia(
            lamina="Lam-02",
            pagina=1,
            vista=TipoVista.ELEVACIONES,
            descripcion="Nivel superior 0+4.98 en elevación principal",
            valor_leido="0+4.98",
        )
    ],
    observaciones="Altura 4.98 m en edificación de 1 planta (máx. 7 m).",
    revisado_por="Francisco Jiménez",
)
 
# Caso 2: la IA NO encuentra el sello. Un hecho también puede ser
# "no está" (False). La evidencia indica dónde buscó.
# Todavía no hay resultado_final: falta que el revisor confirme.
caso_sello_cfia = ItemResult(
    criterio_id="firma-cfia",
    estado=EstadoRevision.PROPUESTO_POR_IA,
    resultado_ia=Resultado.NO_CUMPLE,
    hechos={"sello_cfia_presente": False},
    evidencias=[
        Evidencia(
            lamina="Lam-01",
            pagina=1,
            vista=TipoVista.SELLOS,
            descripcion="Franja lateral sin sello digital del CFIA",
        )
    ],
    observaciones="No se encontró el sello digital del CFIA en las láminas.",
)
 
# Caso 3: faltan datos. La IA no puede decidir, así que NO propone
# resultado (None) y el criterio pasa a revisión manual.
# Lo que sí encontró queda en hechos; lo que no, en datos_faltantes.
caso_retiro_lateral = ItemResult(
    criterio_id="retiros-laterales-1-planta",
    estado=EstadoRevision.REVISION_MANUAL,
    resultado_ia=None,
    hechos={"tapia": True},
    datos_faltantes=[
        "Elevación lateral izquierda (para verificar ventanas en esa fachada)",
    ],
    evidencias=[
        Evidencia(
            lamina="Lam-02",
            pagina=1,
            vista=TipoVista.ELEVACIONES,
            descripcion="Solo hay elevación principal, posterior y lateral derecha",
        )
    ],
    observaciones="Falta la elevación lateral izquierda. Revisar manualmente.",
)
 
# Caso 4: la IA se equivoca y el revisor la corrige.
# resultado_ia y resultado_final son distintos: esta diferencia
# es un dato para la evaluación de la fase 5.
caso_dormitorio = ItemResult(
    criterio_id="dormitorios",
    estado=EstadoRevision.CONFIRMADO,
    resultado_ia=Resultado.NO_CUMPLE,
    resultado_final=Resultado.CUMPLE,
    hechos={"area": 8.39, "lado_menor": 2.80},
    evidencias=[
        Evidencia(
            lamina="Lam-03",  # verificar en qué lámina aparece el área
            pagina=1,
            vista=TipoVista.ESTRUCTURAL,
            descripcion="Área de aposento indicada en la lámina estructural",
            valor_leido="8,39 m2",
        )
    ],
    observaciones=(
        "La IA tomó el área de la lámina estructural. Según la planta de "
        "distribución, el dormitorio mide más de 9 m². Cumple."
    ),
    revisado_por="Francisco Jiménez",
)
 
 
if __name__ == "__main__":
    for caso in [caso_altura, caso_sello_cfia, caso_retiro_lateral, caso_dormitorio]:
        print(caso.model_dump_json(indent=2))
        print()
 