from enum import Enum
from pydantic import BaseModel

# ============================================================
# CRITERIOS DEL COMITÉ — Revisión de Anteproyectos
# Formato: [tipo] Aspecto: criterio resumido   (★ = fase 1)
# ============================================================
#
# [presencia]   Identificación: propietario, cédula y n.º de lote en planos
# [presencia] ★ Documentación: planos firmados por profesional del CFIA
# [documento]   Documentación: carta de cumplimiento del reglamento
# [documento]   Uso de suelo: compatible con uso residencial (certificación)
# [medicion]  ★ Altura máxima: 1 planta máx. 7 m / 2 plantas máx. 10 m
# [medicion]  ★ Retiro frontal: mínimo 2 m desde la línea de propiedad
# [condicional] Retiros laterales (1 planta): no se exige si pared
#               incombustible sin ventana/linternilla; 1.5 m con tapia;
#               3 m sin tapia
# [condicional] Retiros laterales (2 plantas): misma excepción;
#               2 m con tapia; 3 m sin tapia
# [condicional] Retiro posterior (1 planta): misma excepción;
#               3 m; 1.5 m con tapia
# [condicional] Retiro posterior (2 plantas): misma excepción;
#               4 m; 3 m con tapia
# [calculo]     Cobertura: máx. 40% del lote (o según lote en reglamento)
# [medicion]  ★ Dormitorios: área mín. 9 m², lado mín. 2.70 m
# [medicion]    Baños: área mín. 3 m², lado mín. 1.20 m
# [medicion]    Cocina: área mín. 5 m², ancho mín. 2 m
#               (puede ser menor si está integrada a sala/comedor)
# [medicion]    Sala-comedor: mín. 10 m² y 2.50 m de ancho;
#               si son independientes: sala 6.50 m², comedor 7.50 m²
# [calculo]     Ventanas en dormitorios: ≥ 10% del área del dormitorio
# [manual]      Ventilación e iluminación adecuadas en áreas habitables
# [medicion]    Puertas: alto mín. 2.10 m; ancho mín. 0.90 m libre
#               (0.80 m en piezas no habitables)
# [manual]      Circulación: espacios amplios, seguros y accesibles
# [presencia] ★ Hidrosanitarios: tratamiento de aguas residuales
#               y abastecimiento de agua potable
# [documento]   Residuos: plan de manejo durante la construcción
# [manual]      Protección de áreas comunes durante la construcción
# [manual]      Estética y lineamientos del condominio
# [manual]      Materiales según lineamientos de la comisión
class TipoVerificacion(str, Enum):
    PRESENCIA = "presencia"
    MEDICION = "medicion"
    CALCULO = "calculo"
    CONDICIONAL = "condicional"
    DOCUMENTO = "documento"
    LISTA_NEGRA = "lista_negra"
    MANUAL = "manual"

class TipoVista(str, Enum):
    CAJETIN = "cajetin"
    DISTRIBUCION_ARQUITECTONICA = "distribucion_arquitectonica"
    UBICACION = "ubicacion"
    LOCALIZACION = "localizacion"
    TECHOS = "techos"
    ACABADOS = "acabados"
    ELEVACIONES = "elevaciones"
    CORTES = "cortes"
    ESTRUCTURAL = "estructural"
    MECANICA = "mecanica"
    ELECTRICA = "electrica"
    SELLOS = "sellos"

class TipoDocumento(str, Enum):
    CARTA_CUMPLIMIENTO = "carta_cumplimiento"
    CERTIFICACION_USO_SUELO = "certificacion_uso_suelo"
    PLAN_RESIDUOS = "plan_residuos"

class Regla(BaseModel):
    magnitud: str                  # "area", "lado_menor", "altura"...
    minimo: float | None = None
    maximo: float | None = None
    unidad: str
    condicion: dict[str, int | bool] | None = None  # None = siempre aplica

class ChecklistItem(BaseModel):
    id: str
    aspecto: str
    criterio: str
    tipo_verificacion: TipoVerificacion
    vistas_requeridas: list[TipoVista] = []
    documentos_requeridos: list[TipoDocumento] = []
    reglas: list[Regla] = []
    lista_materiales_no_permitidos: list[str] = []

identificacion_propietario = ChecklistItem(
    id="identificacion-propietario",
    aspecto="Identificación del propietario y lote",
    criterio="Propietario, cédula y número de lote en planos.",
    tipo_verificacion=TipoVerificacion.PRESENCIA,
    vistas_requeridas=[TipoVista.CAJETIN],
)
firma_cfia = ChecklistItem(
    id="firma-cfia",
    aspecto="Documentación completa",
    criterio="Planos con sello digital del CFIA.",
    tipo_verificacion=TipoVerificacion.PRESENCIA,
    vistas_requeridas=[TipoVista.SELLOS],
)
carta_cumplimiento = ChecklistItem(
    id="carta-cumplimiento",
    aspecto="Documentación completa",
    criterio="Se requiere la carta de cumplimiento del reglamento.",
    tipo_verificacion=TipoVerificacion.DOCUMENTO,
    documentos_requeridos=[TipoDocumento.CARTA_CUMPLIMIENTO],
)
uso_suelo = ChecklistItem(
    id="uso-suelo",
    aspecto="Uso de suelo",
    criterio="Uso de suelo compatible con uso residencial (certificación).",
    tipo_verificacion=TipoVerificacion.DOCUMENTO,
    documentos_requeridos=[TipoDocumento.CERTIFICACION_USO_SUELO],
)
altura_maxima = ChecklistItem(
    id="altura-maxima",
    aspecto="Altura máxima de la edificación",
    criterio="Altura máxima: 1 planta 7 m / 2 plantas 10 m.",
    tipo_verificacion=TipoVerificacion.MEDICION,
    vistas_requeridas=[TipoVista.ELEVACIONES, TipoVista.CORTES],
    reglas=[
        Regla(magnitud="altura", maximo=7.0, unidad="m", condicion={"plantas": 1}),
        Regla(magnitud="altura", maximo=10.0, unidad="m" , condicion={"plantas": 2})
    ],
)
retiro_frontal = ChecklistItem(
    id="retiro-frontal",
    aspecto="Retiros frontales",
    criterio="Retiro mínimo de 2 m desde la línea de propiedad.",
    tipo_verificacion=TipoVerificacion.MEDICION,
    vistas_requeridas=[TipoVista.LOCALIZACION],
    reglas=[
        Regla(magnitud="distancia", minimo=2.0, unidad="m")
    ],
)
retiros_laterales_1_planta = ChecklistItem(
    id="retiros-laterales-1-planta",
    aspecto="Retiros laterales (una planta)",
    criterio="No se exige si pared incombustible sin ventana/linternilla; 1.5 m con tapia; 3 m sin tapia.",
    tipo_verificacion=TipoVerificacion.CONDICIONAL,
    vistas_requeridas=[TipoVista.LOCALIZACION],
    reglas=[
        Regla(magnitud="distancia", minimo=1.5, unidad="m", condicion={"tapia": True}),
        Regla(magnitud="distancia", minimo=3.0, unidad="m", condicion={"tapia": False})
    ],
)
retiros_laterales_2_plantas = ChecklistItem(
    id="retiros-laterales-2-plantas",
    aspecto="Retiros laterales (dos plantas)",
    criterio="No se exige si pared incombustible sin ventana/linternilla; 2 m con tapia; 3 m sin tapia.",
    tipo_verificacion=TipoVerificacion.CONDICIONAL,
    vistas_requeridas=[TipoVista.LOCALIZACION],
    reglas=[
        Regla(magnitud="distancia", minimo=2.0, unidad="m", condicion={"tapia": True}),
        Regla(magnitud="distancia", minimo=3.0, unidad="m", condicion={"tapia": False})
    ],
)
retiro_posterior_1_planta = ChecklistItem(
    id="retiro-posterior-1-planta",
    aspecto="Retiros posteriores (una planta)",
    criterio="No se exige si pared incombustible sin ventana/linternilla; 3 m; 1.5 m con tapia.",
    tipo_verificacion=TipoVerificacion.CONDICIONAL,
    vistas_requeridas=[TipoVista.LOCALIZACION],
    reglas=[
        Regla(magnitud="distancia", minimo=1.5, unidad="m", condicion={"tapia": True}),
        Regla(magnitud="distancia", minimo=3.0, unidad="m", condicion={"tapia": False})
    ],
)
retiro_posterior_2_plantas = ChecklistItem(
    id="retiro-posterior-2-plantas",
    aspecto="Retiros posteriores (dos plantas)",
    criterio="No se exige si pared incombustible sin ventana/linternilla; 4 m; 3 m con tapia.",    
    tipo_verificacion=TipoVerificacion.CONDICIONAL,
    vistas_requeridas=[TipoVista.LOCALIZACION],    
    reglas=[
        Regla(magnitud="distancia", minimo=3.0, unidad="m", condicion={"tapia": True}),
        Regla(magnitud="distancia", minimo=4.0, unidad="m", condicion={"tapia": False})
    ],
)
cobertura_maxima = ChecklistItem(
    id="cobertura-maxima",
    aspecto="Cobertura máxima de construcción",
    criterio="Máximo 40% del lote (o según lote en reglamento).",
    tipo_verificacion=TipoVerificacion.CALCULO,
    vistas_requeridas=[TipoVista.LOCALIZACION],
    reglas=[
        Regla(magnitud="porcentaje_cobertura", maximo=40.0, unidad="%")
        ],
)
dormitorios = ChecklistItem(
    id="dormitorios",
    aspecto="Dimensiones mínimas de dormitorios",
    criterio="Área mínima de 9 m² con un lado no menor de 2.70 m.",
    tipo_verificacion=TipoVerificacion.MEDICION,
    vistas_requeridas=[TipoVista.DISTRIBUCION_ARQUITECTONICA],
    reglas=[
        Regla(magnitud="area", minimo=9.0, unidad="m²"),
        Regla(magnitud="lado_menor", minimo=2.70, unidad="m")
    ]
)
area_minima_bano = ChecklistItem(
    id="area-minima-bano",
    aspecto="Dimensiones mínimas de baños",
    criterio="Área mínima de 3 m², lado mínimo de 1.20 m.",
    tipo_verificacion=TipoVerificacion.MEDICION,
    vistas_requeridas=[TipoVista.DISTRIBUCION_ARQUITECTONICA],
    reglas=[
        Regla(magnitud="area", minimo=3.0, unidad="m²"),
        Regla(magnitud="lado_menor", minimo=1.20, unidad="m")
    ],
)
area_minima_cocina = ChecklistItem(
    id="area-minima-cocina",
    aspecto="Dimensiones mínimas de cocina",
    criterio="Área mínima de 5 m², ancho mínimo de 2 m (puede ser menor si está integrada a sala/comedor).",
    tipo_verificacion=TipoVerificacion.MEDICION,
    vistas_requeridas=[TipoVista.DISTRIBUCION_ARQUITECTONICA],
    reglas=[
        Regla(magnitud="area", minimo=5.0, unidad="m²"),
        Regla(magnitud="lado_menor", minimo=2.0, unidad="m")
    ],
)
area_minima_sala_comedor = ChecklistItem(
    id="area-minima-sala-comedor",
    aspecto="Dimensiones mínimas de Sala-comedor",
    criterio="Mínimo 10 m² y 2.50 m de ancho; si son independientes: sala 6.50 m², comedor 7.50 m.",
    tipo_verificacion=TipoVerificacion.MEDICION,
    vistas_requeridas=[TipoVista.DISTRIBUCION_ARQUITECTONICA],
    reglas=[
        Regla(magnitud="area", minimo=10.0, unidad="m²"),
        Regla(magnitud="lado_menor", minimo=2.50, unidad="m")
    ],
)
area_minima_ventanas_dormitorio = ChecklistItem(
    id="area-minima-ventanas-dormitorio",
    aspecto="Ventanas en dormitorios",
    criterio="Área mínima de ventanas en dormitorios: ≥ 10% del área del dormitorio.",
    tipo_verificacion=TipoVerificacion.CALCULO,
    vistas_requeridas=[TipoVista.DISTRIBUCION_ARQUITECTONICA, TipoVista.ELEVACIONES],
    reglas=[
        Regla(magnitud="porcentaje", minimo=10.0, unidad="%")
    ],
)
ventilacion_iluminacion_adecuadas = ChecklistItem(
    id="ventilacion-iluminacion-adecuadas",
    aspecto="Ventilación e iluminación",
    criterio="Ventilación e iluminación adecuadas en áreas habitables.",
    tipo_verificacion=TipoVerificacion.MANUAL,
    vistas_requeridas=[TipoVista.DISTRIBUCION_ARQUITECTONICA],
)
medidas_puertas = ChecklistItem(
    id="medidas-puertas",
    aspecto="Dimensiones mínimas de puertas",
    criterio="Alto mínimo de 2.10 m; ancho mínimo de 0.90 m libre (0.80 m en piezas no habitables).",
    tipo_verificacion=TipoVerificacion.MEDICION,
    vistas_requeridas=[TipoVista.DISTRIBUCION_ARQUITECTONICA],
    reglas=[
        Regla(magnitud="alto", minimo=2.10, unidad="m"),
        Regla(magnitud="ancho", minimo=0.90, unidad="m")
    ],
)
areas_circulacion = ChecklistItem(
    id="areas-circulacion",
    aspecto="Espacios de circulación",
    criterio="Espacios amplios, seguros y accesibles.",
    tipo_verificacion=TipoVerificacion.MANUAL,
    vistas_requeridas=[TipoVista.DISTRIBUCION_ARQUITECTONICA],
)
sistemas_hidrosanitarios = ChecklistItem(
    id="sistemas-hidrosanitarios",
    aspecto="Servicios básicos hidrosanitarios",
    criterio="Tratamiento de aguas residuales y abastecimiento de agua potable.",
    tipo_verificacion=TipoVerificacion.PRESENCIA,
    vistas_requeridas=[TipoVista.MECANICA],
)
documento_residuos = ChecklistItem(
    id="documento-residuos",
    aspecto="Gestión de residuos durante la construcción",
    criterio="Plan de manejo de residuos durante la construcción.",
    tipo_verificacion=TipoVerificacion.DOCUMENTO,
    documentos_requeridos=[TipoDocumento.PLAN_RESIDUOS],
)
proteccion_areas_comunes = ChecklistItem(
    id="proteccion-areas-comunes",
    aspecto="Protección de áreas comunes",
    criterio="Protección de áreas comunes durante la construcción.",
    tipo_verificacion=TipoVerificacion.MANUAL,
    vistas_requeridas=[TipoVista.DISTRIBUCION_ARQUITECTONICA],
)
estetica_lineamientos = ChecklistItem(
    id="estetica-lineamientos", 
    aspecto="Estética y alineamiento con la normativa",
    criterio="Estética y lineamientos del condominio.", 
    tipo_verificacion=TipoVerificacion.MANUAL,
    vistas_requeridas=[TipoVista.DISTRIBUCION_ARQUITECTONICA, TipoVista.ELEVACIONES, TipoVista.ACABADOS],
)
materiales_lineamientos = ChecklistItem(
    id="materiales-lineamientos",
    aspecto="Materiales de construcción",
    criterio="Respeta los lineamientos del condominio establecidos por la comisión.",
    tipo_verificacion=TipoVerificacion.LISTA_NEGRA,
    vistas_requeridas=[TipoVista.ACABADOS, TipoVista.ELEVACIONES, TipoVista.ESTRUCTURAL],
    lista_materiales_no_permitidos=[
        "columnas prefabricadas con acabado de baldosas horizontales o verticales",
        "paredes de lámina de zinc ondulado (permitido solo en bodega temporal)",
        "plywood o madera contrachapada",
        "lámina Plycem Fibrolit",
    ],
)

if __name__ == "__main__":
    print(identificacion_propietario.model_dump_json(indent=2))
    print(retiro_frontal.model_dump_json(indent=2))
    print(firma_cfia.model_dump_json(indent=2))
    print(altura_maxima.model_dump_json(indent=2))