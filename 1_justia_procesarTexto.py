import json
import re
import unicodedata
import pandas as pd
import spacy

# ======================================================================
# 1. SIMULACIÓN DEL CORPUS JURÍDICO 
# Se quiso manejar un rango de 60 textos que tomen casos de las áreas
# más comunues con base en lo encontrado en otras fuentes(familia,
# laboral, penal, civil)
# ======================================================================


datos = [
    # --- ÁREA: FAMILIA (Casos de violencia, alimentos, custodia, etc.) ---
    {"id": 1, "area": "Familia", "texto": "El demandado incumplió de manera reiterada con la obligación alimentaria fijada a favor de sus hijos menores de edad."},
    {"id": 2, "area": "Familia", "texto": "Se configura violencia económica cuando el cónyuge ejerce un control restrictivo y arbitrario sobre los recursos financieros del hogar."},
    {"id": 3, "area": "Familia", "texto": "La actora solicita la cesación de efectos civiles de matrimonio católico por la causal de relaciones sexuales extramatrimoniales."},
    {"id": 4, "area": "Familia", "texto": "El principio del interés superior del menor obliga al juez a tomar medidas cautelares urgentes para proteger su integridad física y psicológica."},
    {"id": 5, "area": "Familia", "texto": "La violencia patrimonial se evidenció al destruir los títulos de propiedad y enajenar los bienes de la sociedad conyugal sin autorización."},
    {"id": 6, "area": "Familia", "texto": "Se interpone demanda de impugnación de la paternidad debido a pruebas de ADN que descartan el vínculo biológico."},
    {"id": 7, "area": "Familia", "texto": "La custodia y cuidado personal de la menor será ejercida de forma compartida por ambos progenitores según el acuerdo conciliatorio."},
    {"id": 8, "area": "Familia", "texto": "El ICBF intervino en el proceso para restablecer los derechos de los niños que se encontraban en situación de abandono decretada."},
    {"id": 9, "area": "Familia", "texto": "Se solicita la liquidación de la sociedad patrimonial de hecho entre compañeros permanentes tras una convivencia mayor a dos años."},
    {"id": 10, "area": "Familia", "texto": "El juzgado de familia decretó la privación de la patria potestad del progenitor por maltrato habitual comprobado."},
    {"id": 11, "area": "Familia", "texto": "La fijación de la cuota alimentaria provisional debe tasarse conforme a la capacidad económica del alimentante y la necesidad del menor."},
    {"id": 12, "area": "Familia", "texto": "Existe una delgada línea entre la violencia económica y la patrimonial, por lo que el despacho analizará el dolo en la privación de recursos."},
    {"id": 13, "area": "Familia", "texto": "Se solicita la homologación del fallo de adopción consentida emitido por la defensoría de familia para garantizar el estado civil del menor."},
    {"id": 14, "area": "Familia", "texto": "La demandante exige la declaración judicial de la unión marital de hecho tras la separación definitiva de la pareja de compañeros."},
    {"id": 15, "area": "Familia", "texto": "Se interpone recurso de apelación contra la providencia que tasó de forma desproporcionada los gastos de educación y recreación del menor."},

    # --- ÁREA: LABORAL (Contratos, despidos, fueros, pensiones) ---
    {"id": 16, "area": "Laboral", "texto": "El trabajador demanda el reconocimiento del contrato de realidad tras haber prestado servicios bajo continuada subordinación laboral."},
    {"id": 17, "area": "Laboral", "texto": "Se produjo un despido sin justa causa encontrándose la trabajadora en estado de embarazo, vulnerando el fuero de maternidad."},
    {"id": 18, "area": "Laboral", "texto": "La empresa omitió el pago de las acreencias laborales correspondientes a cesantías, intereses a las cesantías y vacaciones devengadas."},
    {"id": 19, "area": "Laboral", "texto": "El actor argumenta acoso laboral por parte de su superior jerárquico mediante la asignación de cargas de trabajo desproporcionadas."},
    {"id": 20, "area": "Laboral", "texto": "Se solicita la indexación de la primera mesada pensional debido a la pérdida del poder adquisitivo de la moneda a lo largo del tiempo."},
    {"id": 21, "area": "Laboral", "texto": "La administradora de fondos de pensiones Colpensiones negó el reconocimiento de la pensión de invalidez argumentando falta de semanas."},
    {"id": 22, "area": "Laboral", "texto": "El fuero sindical protege a los miembros de la junta directiva de ser despedidos o desmejorados en sus condiciones sin previa calificación judicial."},
    {"id": 23, "area": "Laboral", "texto": "Se demostró el nexo causal entre la enfermedad degenerativa del operario y las funciones físicas ejecutadas en la planta de producción."},
    {"id": 24, "area": "Laboral", "texto": "La UGPP impuso una sanción pecuniaria a la empresa por la inexactitud en los aportes al sistema de seguridad social integral."},
    {"id": 25, "area": "Laboral", "texto": "El contrato de prestación de servicios civiles desnaturalizó la relación de trabajo genuina, configurando un claro contrato realidad."},
    {"id": 26, "area": "Laboral", "texto": "El trabajador reclama el pago de horas extras dominicales y festivos que fueron laborados y no reportados en las planillas oficiales."},
    {"id": 27, "area": "Laboral", "texto": "La terminación unilateral del vínculo laboral por mutuo acuerdo se encuentra viciada por coacción del empleador bajo amenaza de despido."},
    {"id": 28, "area": "Laboral", "texto": "Se solicita la reliquidación pensional incluyendo los factores salariales devengados en el último año de servicios del servidor público."},
    {"id": 29, "area": "Laboral", "texto": "La parte demandada exceptúa falta de legitimación en la causa por pasiva al no haber sido el empleador directo del accionante."},
    {"id": 30, "area": "Laboral", "texto": "El sindicato convoca a huelga imputable al empleador debido a los reiterados incumplimientos en la convención colectiva de trabajo vigente."},

    # --- ÁREA: CIVIL (Contratos, responsabilidad, bienes, obligaciones) ---
    {"id": 31, "area": "Civil", "texto": "Se interpone acción de rescisión por lesión enorme al haberse enajenado el inmueble por menos de la mitad de su justo precio."},
    {"id": 32, "area": "Civil", "texto": "La parte demandante exige el pago de los perjuicios materiales en sus modalidades de daño emergente y lucro cesante por accidente de tránsito."},
    {"id": 33, "area": "Civil", "texto": "Se solicita la declaración de prescripción extraordinaria adquisitiva de dominio sobre el bien inmueble que ha poseído por más de diez años."},
    {"id": 34, "area": "Civil", "texto": "Incumplimiento contractual derivado de la falta de entrega de la maquinaria industrial en la fecha estipulada en la promesa de compraventa."},
    {"id": 35, "area": "Civil", "texto": "La aseguradora objetó la reclamación civil argumentando que el siniestro ocurrió bajo una de las causales de exclusión expresa de la póliza."},
    {"id": 36, "area": "Civil", "texto": "Se demanda la nulidad absoluta del contrato de donación por carecer de la insinuación notarial exigida por la legislación vigente."},
    {"id": 37, "area": "Civil", "texto": "Proceso ejecutivo singular para el cobro judicial de una letra de cambio cuyo plazo de exigibilidad se encuentra plenamente vencido."},
    {"id": 38, "area": "Civil", "texto": "Se alega la responsabilidad civil extracontractual del propietario del vehículo automotor considerado una actividad peligrosa por el ordenamiento."},
    {"id": 39, "area": "Civil", "texto": "Demanda de restitución de inmueble arrendado por la causal de mora en el pago de los cánones de arrendamiento mensuales."},
    {"id": 40, "area": "Civil", "texto": "La servidumbre de tránsito debe constituirse de forma forzosa dado que el predio sirviente es la única vía de acceso al camino público."},
    {"id": 41, "area": "Civil", "texto": "Se solicita el levantamiento del patrimonio de familia inembargable para proceder con la venta comercial del apartamento adquirido."},
    {"id": 42, "area": "Civil", "texto": "La teoría de la imprevisión contractual aplica debido al aumento desmesurado de los costos por una devaluación abrupta de la moneda nacional."},
    {"id": 43, "area": "Civil", "texto": "Se instaura acción reivindicatoria de dominio para recuperar la posesión material de un lote invadido de manera violenta por terceros."},
    {"id": 44, "area": "Civil", "texto": "Se solicita la resolución del contrato de permuta comercial ante el vicio oculto detectado en los automotores entregados como parte de pago."},
    {"id": 45, "area": "Civil", "texto": "La hipoteca abierta sin límite de cuantía debe ser cancelada formalmente al haberse extinguido la obligación principal garantizada."},

    # --- ÁREA: PENAL (Delitos, debido proceso, medidas cautelares) ---
    {"id": 46, "area": "Penal", "texto": "La Fiscalía General de la Nación formuló imputación por el delito de hurto calificado y agravado en concurso heterogéneo."},
    {"id": 47, "area": "Penal", "texto": "El juez de control de garantías impuso medida de aseguramiento de detención preventiva en establecimiento carcelario contra el procesado."},
    {"id": 48, "area": "Penal", "texto": "La defensa solicita la preclusión de la investigación penal aduciendo la atipicidad absoluta de la conducta desplegada por su representado."},
    {"id": 49, "area": "Penal", "texto": "Se apela la sentencia condenatoria argumentando la violación al principio de presunción de inocencia y la falta de pruebas de cargo."},
    {"id": 50, "area": "Penal", "texto": "El procesado cometió el delito de concusión al exigir dinero en su calidad de servidor público para agilizar un trámite administrativo."},
    {"id": 51, "area": "Penal", "texto": "Se investiga la comisión del delito de concierto para delinquir con fines de tráfico de estupefacientes a nivel intermunicipal."},
    {"id": 52, "area": "Penal", "texto": "La cadena de custodia de los elementos materiales probatorios se vio comprometida al no registrarse las firmas en el acta de recolección."},
    {"id": 53, "area": "Penal", "texto": "Se configura la legítima defensa al demostrarse una agresión actual, inminente e injustificada contra la vida del imputado."},
    {"id": 54, "area": "Penal", "texto": "La víctima de violencia de género solicita medidas de protección frente a las amenazas de muerte proferidas por el presunto agresor."},
    {"id": 55, "area": "Penal", "texto": "El peritaje de medicina legal determinó una incapacidad médico-legal definitiva de cuarenta días por lesiones personales graves."},
    {"id": 56, "area": "Penal", "texto": "Se solicita la libertad por vencimiento de términos procesales al haber transcurrido el tiempo legal sin que se radicara el escrito de acusación."},
    {"id": 57, "area": "Penal", "texto": "La conducta penal analizada encaja en el tipo penal de fraude procesal al haber inducido en error a un servidor público con documentos falsos."},
    {"id": 58, "area": "Penal", "texto": "El indiciado se allanó a los cargos de peculado por apropiación buscando obtener una rebaja sustancial de la pena en la dosificación punitiva."},

    # --- CASOS COMPLEJOS / BORDES (Términos sensibles y debates éticos) ---
    {"id": 59, "area": "Familia", "texto": "La violencia patrimonial y la violencia económica vulneran la dignidad de la mujer, requiriendo un enfoque interseccional en el juzgado civil."},
    {"id": 60, "area": "Laboral", "texto": "Un despido discriminatorio motivado por la orientación sexual del trabajador activa de inmediato la protección constitucional vía acción de tutela."}
]


# =====================================================================
# 2. CONFIGURACIÓN DEL MODELO DE NLP (spaCy)
# =====================================================================
try:
    nlp = spacy.load("es_core_news_sm")
except OSError:
    raise OSError("Por favor instala el modelo de español ejecutando: python -m spacy download es_core_news_sm")


# =====================================================================
# 3. FUNCIONES DE PREPROCESAMIENTO NLP.
# Son las funciones que se utilzarán para limpiar las cadenas y poderla
# manejar para poder crear la familiaridad con el lenguaje natural
# =====================================================================

def limpiar_texto(texto: str) -> str:
    """
    Convierte a minúsculas, remueve caracteres especiales y elimina las tildes/acentos.
    """
    # Se pasa el texto a minúsculas
    texto = texto.lower()
    
    # Se normaliza para extraer acentos y diéresis de forma limpia
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    
    # Se aplica una expresión regular para mantener solo caracteres alfanuméricos y espacios, removiendo la puntuación
    texto = re.sub(r'[^a-z0-9\s]', '', texto)
    
    # 4. Quita los espacios que se generen luego del proceso anterior
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    return texto


def preprocesar_corpus_juridico(texto_original: str) -> str:
    """
    Tokeniza, filtra palabras vacías (stopwords tradicionales y procedimentales)
    y genera el lema morfológico oficial en español utilizando spaCy.
    """    
    texto_limpio = limpiar_texto(texto_original)
        
    # Se aplica(nlp) sobre el texto para convertirlo en un objeto con información detallada
    # como lemas, entidades o gramática mediante el pipeline de spaCy.
    doc = nlp(texto_limpio)
    
    # Se crea un arreglo de stop words en español, apra así reducir el costo computacional.
    # Aplican artículos, preposiciones, conjunciones, adejtivos demostrativos, interjecciones y algunos términos
    # comunes a todos los textos legales. La idea es que se pula lo más posible el diccionario para facilitar el 
    # NPL y poderle brindar mayor especificidad en el proceso
    stopwords_ext = {
        "el", "la", "los", "las", "un", "una", "unos", "unas", "de", "del", "a", "al", "en", "y", "o", "u", "bajo",
        "para", "por", "con", "sin", "sobre", "tras", "durante", "mediante", "este", "esta", "estos", "estas",
        "ese", "esa", "esos", "esas", "aquel", "aquella", "se", "lo", "su", "sus", "como", "mas", "pero", 
        "algun", "alguna", "cada", "cual", "cuyo", "cuya", "haber", "ser", "estar", "hacer", "tener", "caso", 
        "proceso", "demandado", "demandante", "solicita", "articulo", "codigo", "ley", "parte", "surgir", "instaura"
    }
    
    tokens_procesados = []
    
    # Se recorre cada palabra del texto que se procesó y con la ayuda del módulo de spaCy
    # que se agregó, se extrae el lema y se agrega cada una de esas palabras
    
    for token in doc:
        # Excluir palabras vacías por defecto de spaCy y nuestro diccionario personalizado
        if not token.is_stop and token.text not in stopwords_ext:
            # Obtener la raíz del diccionario (lema) de la palabra
            # Ej: "incumplieron" -> "incumplir", "bienes" -> "bien", "punitiva" -> "punitivo"
            lema = token.lemma_
            tokens_procesados.append(lema)
            
    # Retornar el string normalizado unificado
    return " ".join(tokens_procesados)


# =====================================================================
# 4. EJECUCIÓN DEL PIPELINE Y APLICAR LA FUNCIÓN DE PREPROCESO
# =====================================================================

print(f"Iniciando el pipeline de NLP para los {len(datos)} fragmentos de JustIA...\n")

# Construcción de la estructura de datos tabular
df = pd.DataFrame(datos)

# Aplicar la función de NLP elemento a elemento
df['texto_limpio_nlp'] = df['texto'].apply(preprocesar_corpus_juridico)


# =====================================================================
# 5. GENERAR LOS ARCHIVOS SOLICITADOS (.CSV y .JSON)
# =====================================================================

csv_filename = "justia_corpus.csv"
df.to_csv(csv_filename, index=False, encoding='utf-8')
print(f"✔ Se genera archivo CSV: '{csv_filename}'")

json_filename = "justia_corpus.json"
df.to_json(json_filename, orient='records', force_ascii=False, indent=4)
print(f"✔ Se genera archivo JSON: '{json_filename}'")


# =====================================================================
# 6. AUDITORÍA 
# =====================================================================
print("\n" + "="*70)
print("AUDITORÍA Y REVISIÓN DE TEXTOS")
print("="*70)

# Pruebas con algunos textos
arr_auditoria = [4, 10, 24, 30, 37, 44, 60]
for cid in arr_auditoria:
    fila = df[df['id'] == cid].iloc[0]
    print(f"\n[ID {fila['id']} | Categoría: {fila['area']}]")
    print(f"  📝 Texto Base: {fila['texto']}")
    print(f"  ⚙ Procesdo:  {fila['texto_limpio_nlp']}")
