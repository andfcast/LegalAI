import json
import re
import unicodedata

def limpiar_y_dividir_texto(texto: str) -> list:
    """
    Convierte a minúsculas, remueve caracteres especiales y elimina las tildes/acentos.
    Finalmente separa el texto por espacios para obtener cada palabra en un listado.
    """
    texto = texto.lower()
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    texto = re.sub(r'[^a-z0-9\s]', '', texto)
    return texto.split()

def predecir_area_juridica(texto_usuario: str, ruta_diccionario: str = "diccionario_justia_features.json") -> dict:
    """
    Recibe un texto en lenguaje natural y obtiene la categoría jurídica más probable,
    detallando información en forma de reporte
    """
    # Se carga el diccionario generado en la rutina 2_1_justia_generarDiccionario.py
    with open(ruta_diccionario, 'r', encoding='utf-8') as f:
        diccionario = json.load(f)
        
    # Se obtiene las palabras del texto de entrada
    tokens = limpiar_y_dividir_texto(texto_usuario)
    
    # Conteo de coincidencias y registro de evidencias para trazabilidad
    cont_categorias = {cat: 0 for cat in diccionario.keys()}
    coincidencias = {cat: [] for cat in diccionario.keys()}
    
    for token in tokens:
        for categoria, palabras_clave in diccionario.items():
            if token in palabras_clave:
                cont_categorias[categoria] += 1
                if token not in coincidencias[categoria]:
                    coincidencias[categoria].append(token)
                    
    # Determina la categoría con mayor puntaje
    max_num_coincidencias = max(cont_categorias.values())
    
    # Se determinan los casos en que no hayan coincidencias de categorías o haya más de una que aplique y cumpla los criterios
    if max_num_coincidencias == 0:
        cat_asignada = "Indeterminado / Requiere Asignación Manual"
    else:        
        cat_opciones = [cat for cat, votos in cont_categorias.items() if votos == max_num_coincidencias]
        cat_asignada = cat_opciones[0] if len(cat_opciones) == 1 else "Ambivalente (Revisión Docente Requerida)"
        
    # Detallar el reporte de la información encontrada
    reporte = {
        "categoria": cat_asignada,
        "score": max_num_coincidencias,
        "matriz_categorias": cont_categorias,
        "listado_evidencias": {cat: evs for cat, evs in coincidencias.items() if len(evs) > 0},
        "nota": "Sugerencia automatizada de apoyo. Sometida a revisión de auditoría antes de ratificar el área."
    }
    
    return reporte

# =====================================================================
# PRUEBAS APLICADAS
# =====================================================================
if __name__ == "__main__":
    print("--- PRUEBAS DE CLASIFICACIÓN DEJUSTIA ---")
    
    caso1 = "Necesito fijar con urgencia la cuota de alimentos de mi hijo menor de edad porque el papá se niega a pagar."
    resultado1 = predecir_area_juridica(caso1)
    print(f"\nCaso 1 Texto: '{caso1}'")
    print(json.dumps(resultado1, ensure_ascii=False, indent=2))
        
    caso2 = "Interpongo una acción de tutela por la vulneración flagrante a mi derecho fundamental al debido proceso y la igualdad."
    resultado2 = predecir_area_juridica(caso2)
    print(f"\nCaso 2 Texto: '{caso2}'")
    print(json.dumps(resultado2, ensure_ascii=False, indent=2))
