# Decisiones del proyecto — Construction Plan Reviewer

## Producto
- La base de la revisión es la lista de chequeo del Comité de Construcción.
  El reglamento del condominio respalda los criterios, pero no agrega
  criterios que el comité no revisa.
- App de doble uso: la IA propone un resultado por criterio y el revisor
  humano confirma o corrige TODOS los criterios antes de exportar.
- Entregable final: PDF con el formato del checklist del comité, resultado
  por criterio, observaciones, logo del condominio, nombre del revisor y
  fecha.
- Los criterios asistidos por IA se marcan discretamente en el PDF.
- Fase 1 con 5 criterios: sello digital CFIA, hidrosanitarios, retiro
  frontal, altura máxima y dimensiones de dormitorios.
- Fases: 1) llamada simple al LLM, 2) RAG del reglamento, 3) agente,
  4) servidor MCP, 5) evaluación con métricas.

## Interfaz
- Botón "Revisar con IA" por criterio (para re-ejecutar uno solo) y botón
  general "Revisar todo con IA" (ahorra llamadas al agrupar criterios que
  usan las mismas láminas).
- Cada criterio muestra una caja de texto con lo que la IA encontró y lo
  que le faltó.
- El texto de esa caja es la propuesta para la columna Observaciones del
  checklist del comité.
- La exportación del PDF se habilita solo cuando todos los criterios están
  confirmados.

## Stack y arquitectura
- Frontend: Angular. Backend: Python + FastAPI.
- Base de datos y archivos: Supabase (PostgreSQL + pgvector + Storage).
- Revisiones asíncronas: jobs con estado (pendiente, procesando, listo).
- El motor de revisión y el proveedor de LLM viven detrás de interfaces
  intercambiables, para comparar enfoques y proveedores.
- LLMs: Gemini Flash para visión, Groq para tareas de texto.
  Opción futura: modelo local con Ollama.

## Documentos y láminas
- Un proyecto se sube como varios archivos (láminas), no un solo PDF.
- Se clasifican VISTAS, no láminas: una página puede tener varias.
- Clasificador en cascada: título → índice de láminas → LLM con visión
  → confirmación humana.
- Normalizar texto (mayúsculas, tildes) y usar diccionario de sinónimos.
- Números: aceptar coma y punto decimal.
- El texto extraído sirve para clasificar; para medir se necesita visión.
- El sello digital del CFIA está en una franja lateral de la lámina, no en
  el cajetín. Se trata como una vista propia (SELLOS) y puede requerir
  visión, porque a veces se inserta como imagen.
- Documentos externos (carta de cumplimiento, uso de suelo, plan de
  residuos) se manejan aparte de las láminas.

## Evaluación de criterios
- La IA extrae hechos; el código Python aplica las reglas.
- Datos completos → el código decide (cumple o no cumple) y la IA lo
  propone. Datos incompletos → se muestra lo encontrado y lo faltante, y
  el criterio pasa a revisión manual.
- La IA puede confirmar lo malo, pero no garantizar lo bueno: encontrar
  evidencia de incumplimiento permite proponer "No cumple"; no encontrarla
  no prueba que se cumpla.
- Los umbrales son datos: cada criterio tiene una lista de reglas con
  condición opcional. Se aplican todas las reglas cuya condición se cumple.
- Tipos de verificación: presencia, medición, cálculo, condicional,
  documento, lista negra y manual.
- Toda propuesta de la IA incluye evidencia (lámina, página) y el valor
  leído.
- "Información insuficiente" es un resultado válido; la IA no inventa.
- Resultado (cumple / no cumple / no aplica) y estado (propuesto por IA /
  revisión manual / confirmado) son dimensiones separadas.
- Si falta un documento requerido, el criterio pasa a revisión manual.
- Se guarda lo que propuso la IA y lo que decidió el humano: es el set de
  evaluación.
- Se guardan resultado_ia y resultado_final por separado; resultado_ia nunca se modifica.

## Materiales y estética
- La lista negra de materiales (Reglamento, Art. 14a) pertenece al criterio
  "Materiales de construcción".
- Si la IA encuentra un material prohibido → propone "No cumple" con la
  evidencia en Observaciones. El revisor confirma.
- Si encuentra un material similar a uno prohibido → alerta y revisión
  manual.
- Si no encuentra ninguno → revisión manual con la nota "no se detectaron
  materiales prohibidos".
- Los prefabricados con baldosas van en la lista negra (detección por
  texto); estética los evalúa visualmente.
- "Estética y alineamiento con la normativa" es manual y se revisa sobre
  las elevaciones (fachadas) y el cuadro de acabados.

## Privacidad
- Las carpetas planos/ y reglamento/ nunca van a Git.
- El tier gratuito de Gemini no se usa con planos reales de terceros.

## Forma de trabajo
- Escribo yo: modelos de datos, reglas de evaluación y lógica de IA.
- Asistido por un agente de código (OpenCode, pendiente de instalar): UI,
  endpoints, configuración, tests y PDF.

## Pendientes
- Mover los criterios de checklist.py a un archivo JSON versionado.
- Modelar la excepción de retiros (pared incombustible sin ventanas).
- Cobertura máxima variable según el lote.
- Lista negra con sinónimos agrupados (de list[str] a dict).
- Reglas condicionales de materiales: techo de zinc debe ir pintado
  (Art. 14b) y requisitos para contenedores (Art. 14d).
- Mostrar como información de contexto los permisos municipales y visados
  que vengan en las láminas (el comité no los revisa hoy).
- Fase 3: herramienta del agente para verificar el código del sello CFIA.
- Mover docs/ a la raíz del repositorio.