import os
import time
from justia_2_2_predecirCategoria import predecir_area_juridica  # Logíca ejercicio 2

def mostrar_header():    
    print("\n" + "="*70)
    print("        SISTEMA JUSTIA - CONSULTORIO JURÍDICO VIRTUAL  ")    
    print("="*70)
    print("   Esta es una herramienta automatizada de apoyo preliminar.")
    print("   No reemplaza la asesoría jurídica de un abogado calificado.")
    print("="*70)

def menu_principal():    
    print("\n[ MENÚ DE OPERACIONES ]")
    print("1. Ingresar consulta legal en lenguaje natural (Clasificación Automatizada)")
    print("2. Cargar documento de entrada (PDF, Escaneados o Texto sin formato)")
    print("3. Simular una clasificación")
    print("4. Salir del sistema")
    return input("\nSeleccione una opción (1-4): ").strip()

def flujo_consulta_legal():
    """Canaliza las preguntas de los usuarios y ejecuta el predictor con trazabilidad."""
    print("\n--- 1. INGRESO DE CONSULTA LEGAL ---")
    print("Describa su situación de forma clara (mencione hechos, personas involucradas y su petición):")
    consulta = input("\n Su consulta > ").strip()
    
    if len(consulta) < 15:
        print("\n Error: La descripción es demasiado corta para realizar un análisis semántico fiable.")
        return

    print("\n Procesando texto mediante el pipeline NLP de JustIA...")
    time.sleep(1)
    
    # Ejecutamos la función de predicción construida en la Actividad 2
    resultado = predecir_area_juridica(consulta)
    
    print("\n" + "-"*50)
    print("RESULTADOS")
    print("-"*50)
    print(f" Área Sugerida: {resultado['categoria'].upper()}")
    print(f" Palabras clave halladas: {resultado['score']}")
    
    if "listado_evidencias" in resultado and resultado["listado_evidencias"]:
        print("\n Evidencia encontrada:")
        for cat, evs in resultado["listado_evidencias"].items():
            print(f"   • En [{cat}]: Términos detectados -> {', '.join(evs)}")
    
    print(f"\n Nota: {resultado['nota']}")
    print("-"*50)

def flujo_carga_documentos():
    """Simula la extracción de información desde archivos externos, aplicando filtros éticos."""
    print("\n--- 2. CARGA DE DOCUMENTOS ---")
    print("Soportados: .pdf, .txt, .png, .jpeg (Imágenes escaneadas)")
    ruta_archivo = input("Ingrese el nombre o ruta simulada del archivo: ").strip()
        
    _, ext = os.path.splitext(ruta_archivo.lower())
    if ext not in ['.pdf', '.txt', '.png', '.jpeg', '.jpg']:
        print("\n Formato de archivo no soportado.")
        return

    print(f"\n Leyendo '{ruta_archivo}'...")
    time.sleep(1.5)    
    if ext in ['.png', '.jpeg', '.jpg']:
        print("  [BLOQUEO ÉTICO] Se detectó un archivo de imagen.")
        print("                  El sistema ha desactivado los módulos de Reconocimiento Facial.")
        print("                  Razón: Alto riesgo de estigmatización y vigilancia excesiva.")
        print("                  Acción: Solo se extraerá texto mediante OCR plano.")
    
    print("\n Extracción completada con éxito.")
    print(" Contenido preliminar extraído (Simulado):")
    print("   '...vulneración flagrante de derechos, se solicita amparo constitucional inmediato...'")

def mostrar_clasificacion_simulada():
    """Simula una clasificación"""
    print("\n" + "="*70)
    print("Clasificación")
    print("="*70)
    texto_prueba = "Fui despedida de mi trabajo en la empresa de calzado justo después de informar a mi jefe que me encontraba en estado de embarazo de tres meses."
    print("\n Analizando el texto en el entorno de pruebas éticas...")
    time.sleep(1.2)
    resultado = predecir_area_juridica(texto_prueba);
    print("\nRESULTADO SIMULADO:")
    print(f"   • Texto evaluado: \"{texto_prueba}\"")
    print("   • Categoría detectada por el modelo: " + resultado["categoria"] + " (Simulado)")        
    print("\n Clasificación completada: No se detectaron anomalías éticas en la consulta.")
    print("="*70)

def ejecutar():
    """Bucle de consola."""
    while True:
        mostrar_header()
        opcion = menu_principal()
        
        if opcion == "1":
            flujo_consulta_legal()
        elif opcion == "2":
            flujo_carga_documentos()
        elif opcion == "3":
            mostrar_clasificacion_simulada()
        elif opcion == "4":
            print("\n Acceso cerrado de forma segura.\n")
            break
        else:
            print("\n Opción inválida. Por favor, digite un número del 1 al 4.")
            
        input("\nPresione ENTER para regresar al menú principal...")
        # Limpieza de pantalla básica para simular refresco de interfaz
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    ejecutar()
