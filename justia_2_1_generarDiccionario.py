import json
import pandas as pd

# 1. Definición del Diccionario Técnico de Características Jurídicas (Features)
# Se recopilan conceptos claves o palabras comunes relacionados con cada rama del derecho
# y luego se genera ell archivo en formatos json y csv.
diccionario_juridico = {
    "Derecho de Familia": [
        "alimento", "cuota", "menor", "hijo", "patria", "potestad", "custodia", "parentesco", 
        "cónyuge", "matrimonio", "divorcio", "paternidad", "adn", "conciliación", "adopción",
        "icbf", "compañero", "permanente", "unión", "marital", "violencia", "económica"
    ],
    "Derecho Laboral": [
        "trabajador", "empleador", "contrato", "realidad", "subordinación", "salario", "prestación", 
        "cesantía", "vacación", "despido", "justa", "causa", "embarazo", "maternidad", "fuero", 
        "sindical", "acoso", "laboral", "pensión", "vejez", "invalidez", "colpensiones", "huelga", "ugpp"
    ],
    "Derecho Civil": [
        "rescisión", "lesión", "enorme", "perjuicio", "material", "daño", "emergente", "lucro", 
        "cesante", "prescripción", "adquisitiva", "dominio", "bien", "inmueble", "posesión", 
        "contrato", "compraventa", "incumplimiento", "póliza", "aseguradora", "nulidad", "letra", "cambio"
    ],
    "Derecho Penal": [
        "fiscalía", "imputación", "delito", "hurto", "agravado", "juez", "garantías", "aseguramiento", 
        "cárcel", "detención", "preventiva", "preclusión", "atipicidad", "sentencia", "condenatoria", 
        "inocencia", "concusión", "concierto", "delinquir", "custodia", "evidencia", "imputado"
    ],
    "Derecho Constitucional": [
        "tutela", "fundamental", "derecho", "constitución", "bloque", "constitucionalidad", 
        "vulneración", "amparo", "corte", "constitucional", "dignidad", "humana", "igualdad", 
        "discriminación", "debido", "proceso", "precedente", "sentencia", "unificación", "su"
    ]
}

# 2. Guardar el diccionario en formato JSON
json_path = "diccionario_justia_features.json"
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(diccionario_juridico, f, ensure_ascii=False, indent=4)

# 3. Guardar el diccionario en formato CSV 
filas = []
for categoria, palabras in diccionario_juridico.items():
    for palabra in palabras:
        filas.append({"categoria": categoria, "keyword": palabra})
df_dict = pd.DataFrame(filas)
csv_path = "diccionario_justia_features.csv"
df_dict.to_csv(csv_path, index=False, encoding='utf-8')

# 4. Fin del proceso de generación 
print("Archivos del diccionario jurídico de JustIA generados con éxito.")
