from datos import lectura_datos
from algoritmos import greedy, grasp, enfriamientosimulado, algoritmogenetico, algoritmomemetico
from datos import visualizacion
import pandas as pd
import time


def mostrar_resultados(ruta_solucion, tiempo_total, distancia_total, beneficio, tiempo_max, es_ciclica, tiempo_ejecucion):
        """Mostrar resultados de forma interactiva.

        Esta función recoge los datos que devuelve la ejecución de los algoritmos y los muestra.

        Args:
            ruta_solucion (array): Array de números con los nodos de la ruta solución
            tiempo_total (float): Número que representa el tiempo total de la ruta solución.
            distancia_total (float): Número que representa la distancia total de la ruta solución.
            beneficio (int): Número que representa el interés total de la ruta solución.
            tiempo_max (float): Número que representa el tiempo total máximo del que se dispone para hacer la ruta.
            es_ciclica (bool): Booleano que representa si la ruta es cíclica o no.
            tiempo_ejecucion (float): Tiempo de ejecución del algoritmo. 

        Returns:
            void: Prints con la información generada de la ruta solución.
        """
        print("Tiempo ejecucion algoritmo:", tiempo_ejecucion, "segundos")
        print("Ruta solución:", ruta_solucion)
        print("Tiempo total:", tiempo_total)   
        print("Distancia total:", distancia_total) 
        print("Interes total:", beneficio) 
        print("Margen:", tiempo_max - tiempo_total)
        if(es_ciclica):
            
            if(len(ruta_solucion)>1):
                print("Porcentaje interes: ",(beneficio/(len(ruta_solucion)-1))*10)
                print("Numero de nodos visitados:", len(ruta_solucion)-1)
            else:
                print("Porcentaje interes: ",(beneficio/(len(ruta_solucion)))*10)
                print("Numero de nodos visitados:", len(ruta_solucion))
           
        else:
            print("Numero de nodos visitados:", len(ruta_solucion))
            print("Porcentaje interes: ",(beneficio/len(ruta_solucion))*10)
            
        print("Ruta ciclica:", es_ciclica)

def main(numero_ejecuciones):
    
    # Leer los archivos correspondientes 
    ruta_archivo_nodos = 'data/pois_158.csv'
    ruta_archivo_distancias = 'data/distancias_158.csv'
    ruta_archivo_tiempos = 'data/tiempos_158.csv'
    ruta_archivo_edad_velocidad = 'data/edadvelocidad.csv'
    edad_velocidad_df = pd.read_csv(ruta_archivo_edad_velocidad)
    
    # DataFrame para almacenar los resultados
    resultados_df = pd.DataFrame(columns=['ALGORITMO', 'POIS VISITADOS', 'INTERÉS','DISTANCIA TOTAL', 'TIEMPO RUTA', 'MARGEN'])


    # Cargar datos
    datos = lectura_datos.Datos(ruta_archivo_nodos, ruta_archivo_distancias, ruta_archivo_tiempos)
    nodos_df = datos.cargar_nodos()
    distancias_df = datos.cargar_distancias()
    tiempos_df = datos.cargar_tiempos()
    
    # Solicitar la edad (para obtener la velocidad correspondiente) y el tiempo máximo al usuario
    edad = int(input("Introduce la edad (entre 0 y 99): "))
    velocidad = edad_velocidad_df[(edad_velocidad_df['Edad_inicio'] <= edad) & (edad_velocidad_df['Edad_fin'] >= edad)]['Velocidad(m/min)'].iloc[0]
    print("Velocidad correspondiente a la edad:", velocidad)

    tiempo_max = int(input("Introduce el tiempo máximo: "))
    print("Tiempo máximo:", tiempo_max)
    
  
       
    # Solicitamos al usuario que algoritmo desea ejecutar  
    print("¿Qué algoritmo(s) deseas ejecutar?")
    print("1. Greedy")
    print("2. GRASP")
    print("3. Enfriamiento Simulado")
    print("4. Algoritmo Genético")
    print("5. Algoritmo Memético")
    print("6. Todos")
    eleccion = input("Introduce el número correspondiente a tu elección, separados por coma si son varios (ejemplo: 1,2): ")

    elecciones = [int(e.strip()) for e in eleccion.split(",")]

    # Preguntamos si la ruta es cíclica, en caso afirmativo se decide el nodo cíclico
    es_ciclica = input("¿Deseas que la ruta sea cíclica? (si/no): ").strip().lower() == 'si'
    nodo_origen = None
    if es_ciclica:
        print("Lista de POIs:")
        for nodo, row in nodos_df.iterrows():
            print(f"{nodo}: {row['name']}")
        nodo_origen = int(input("Selecciona el número de nodo para el punto de origen: "))

    for i in range(numero_ejecuciones):
        # Ejecutamos los algoritmos
        if 1 in elecciones or 6 in elecciones: #greedy
            if(es_ciclica):
                print("\nALGORITMO GREEDY")
                print(f"Ejecución {i+1}:")
                alg_greedy = greedy.Greedy(nodos_df, distancias_df, tiempos_df, tiempo_max, velocidad=velocidad) 
                tiempo_ini = time.time()
                ruta_solucion, tiempo_total, distancia_total, beneficio = alg_greedy.aplicar_greedy_ciclico(nodo_ciclico=nodo_origen)
                tiempo_fin = time.time()
                tiempo_ejecucion = tiempo_fin - tiempo_ini
                mostrar_resultados(ruta_solucion, tiempo_total, distancia_total, beneficio, tiempo_max, es_ciclica, tiempo_ejecucion)
                  # Agregar resultados al DataFrame
                margen = tiempo_max - tiempo_total
                nuevo_df = pd.DataFrame({
                    'ALGORITMO': ["GREEDY"],
                    'POIS VISITADOS': [ruta_solucion],
                    'INTERÉS': [beneficio],
                    'DISTANCIA TOTAL': [distancia_total],
                    'TIEMPO RUTA': [tiempo_total],
                    'MARGEN': [margen]
                })

                # Concatenar el nuevo DataFrame con resultados_df
                resultados_df = pd.concat([resultados_df, nuevo_df], ignore_index=True)

            else:
                print("\nALGORITMO GREEDY")
                print(f"Ejecución {i+1}:")
                alg_greedy = greedy.Greedy(nodos_df, distancias_df, tiempos_df, tiempo_max, velocidad=velocidad) 
                tiempo_ini = time.time()
                ruta_solucion, tiempo_total, distancia_total, beneficio = alg_greedy.aplicar_greedy()
                tiempo_fin = time.time()
                tiempo_ejecucion = tiempo_fin - tiempo_ini
                mostrar_resultados(ruta_solucion, tiempo_total, distancia_total, beneficio, tiempo_max, es_ciclica, tiempo_ejecucion)
                margen = tiempo_max - tiempo_total
                nuevo_df = pd.DataFrame({
                    'ALGORITMO': ["GREEDY"],
                    'POIS VISITADOS': [ruta_solucion],
                    'INTERÉS': [beneficio],
                    'DISTANCIA TOTAL': [distancia_total],
                    'TIEMPO RUTA': [tiempo_total],
                    'MARGEN': [margen]
                })

                # Concatenar el nuevo DataFrame con resultados_df
                resultados_df = pd.concat([resultados_df, nuevo_df], ignore_index=True)

        if 2 in elecciones or 6 in elecciones: #grasp
           
            if(es_ciclica):
                print("\nALGORITMO GRASP")
                print(f"Ejecución {i+1}:")
                alg_grasp = grasp.Grasp(nodos_df, distancias_df, tiempos_df, tiempo_max, velocidad=velocidad)
                tiempo_ini = time.time() 
                ruta_solucion, tiempo_total, distancia_total, beneficio = alg_grasp.aplicar_grasp_ciclico(nodo_ciclico=nodo_origen)
                tiempo_fin = time.time()
                tiempo_ejecucion = tiempo_fin - tiempo_ini
                mostrar_resultados(ruta_solucion, tiempo_total, distancia_total, beneficio, tiempo_max, es_ciclica, tiempo_ejecucion)
                margen = tiempo_max - tiempo_total
                nuevo_df = pd.DataFrame({
                    'ALGORITMO': ["GRASP"],
                    'POIS VISITADOS': [ruta_solucion],
                    'INTERÉS': [beneficio],
                    'DISTANCIA TOTAL': [distancia_total],
                    'TIEMPO RUTA': [tiempo_total],
                    'MARGEN': [margen]
                })

                # Concatenar el nuevo DataFrame con resultados_df
                resultados_df = pd.concat([resultados_df, nuevo_df], ignore_index=True)

            else:
                print("\nALGORITMO GRASP")
                print(f"Ejecución {i+1}:")
                alg_grasp = grasp.Grasp(nodos_df, distancias_df, tiempos_df, tiempo_max, velocidad=velocidad)
                tiempo_ini = time.time()
                ruta_solucion, tiempo_total, distancia_total, beneficio = alg_grasp.aplicar_grasp()
                tiempo_fin = time.time()
                tiempo_ejecucion = tiempo_fin - tiempo_ini
                mostrar_resultados(ruta_solucion, tiempo_total, distancia_total, beneficio, tiempo_max, es_ciclica, tiempo_ejecucion)
                margen = tiempo_max - tiempo_total
                nuevo_df = pd.DataFrame({
                    'ALGORITMO': ["GRASP"],
                    'POIS VISITADOS': [ruta_solucion],
                    'INTERÉS': [beneficio],
                    'DISTANCIA TOTAL': [distancia_total],
                    'TIEMPO RUTA': [tiempo_total],
                    'MARGEN': [margen]
                })

                # Concatenar el nuevo DataFrame con resultados_df
                resultados_df = pd.concat([resultados_df, nuevo_df], ignore_index=True)

        if 3 in elecciones or 6 in elecciones: #es
            if(es_ciclica):
                print("\nALGORITMO ENFRIAMIENTO SIMULADO")
                print(f"Ejecución {i+1}:")
                alg_es = enfriamientosimulado.EnfriamientoSimulado(nodos_df, distancias_df, tiempos_df, tiempo_max, velocidad=velocidad)
                tiempo_ini = time.time()
                ruta_solucion, tiempo_total, distancia_total, beneficio = alg_es.aplicar_enfriamiento_simulado_ciclico(nodo_ciclico=nodo_origen)
                tiempo_fin = time.time()
                tiempo_ejecucion = tiempo_fin - tiempo_ini
                mostrar_resultados(ruta_solucion, tiempo_total, distancia_total, beneficio, tiempo_max, es_ciclica, tiempo_ejecucion)
                margen = tiempo_max - tiempo_total
                nuevo_df = pd.DataFrame({
                    'ALGORITMO': ["ENFRIAMIENTO SIMULADO"],
                    'POIS VISITADOS': [ruta_solucion],
                    'INTERÉS': [beneficio],
                    'DISTANCIA TOTAL': [distancia_total],
                    'TIEMPO RUTA': [tiempo_total],
                    'MARGEN': [margen]
                })

                # Concatenar el nuevo DataFrame con resultados_df
                resultados_df = pd.concat([resultados_df, nuevo_df], ignore_index=True)
            else:
                print("\nALGORITMO ENFRIAMIENTO SIMULADO")
                print(f"Ejecución {i+1}:")
                alg_es = enfriamientosimulado.EnfriamientoSimulado(nodos_df, distancias_df, tiempos_df, tiempo_max, velocidad=velocidad)
                tiempo_ini = time.time()
                ruta_solucion, tiempo_total, distancia_total, beneficio = alg_es.aplicar_enfriamiento_simulado()
                tiempo_fin = time.time()
                tiempo_ejecucion = tiempo_fin - tiempo_ini
                mostrar_resultados(ruta_solucion, tiempo_total, distancia_total, beneficio, tiempo_max, es_ciclica, tiempo_ejecucion)
                margen = tiempo_max - tiempo_total
                nuevo_df = pd.DataFrame({
                    'ALGORITMO': ["ENFRIAMIENTO SIMULADO"],
                    'POIS VISITADOS': [ruta_solucion],
                    'INTERÉS': [beneficio],
                    'DISTANCIA TOTAL': [distancia_total],
                    'TIEMPO RUTA': [tiempo_total],
                    'MARGEN': [margen]
                })

                # Concatenar el nuevo DataFrame con resultados_df
                resultados_df = pd.concat([resultados_df, nuevo_df], ignore_index=True)

        if 4 in elecciones or 6 in elecciones: #genetico
            if(es_ciclica):
                print("\nALGORITMO GENETICO")
                print(f"Ejecución {i+1}:")
                alg_ag = algoritmogenetico.AlgoritmoGeneticoEstacionario(nodos_df, distancias_df, tiempos_df, tiempo_max, velocidad=velocidad)
                tiempo_ini = time.time()
                ruta_solucion, tiempo_total, distancia_total, beneficio = alg_ag.aplicar_algoritmo_genetico_ciclico(nodo_ciclico=nodo_origen)
                tiempo_fin = time.time()
                tiempo_ejecucion = tiempo_fin - tiempo_ini
                mostrar_resultados(ruta_solucion, tiempo_total, distancia_total, beneficio, tiempo_max, es_ciclica, tiempo_ejecucion)
                margen = tiempo_max - tiempo_total
                nuevo_df = pd.DataFrame({
                    'ALGORITMO': ["GENETICO"],
                    'POIS VISITADOS': [ruta_solucion],
                    'INTERÉS': [beneficio],
                    'DISTANCIA TOTAL': [distancia_total],
                    'TIEMPO RUTA': [tiempo_total],
                    'MARGEN': [margen]
                })

                # Concatenar el nuevo DataFrame con resultados_df
                resultados_df = pd.concat([resultados_df, nuevo_df], ignore_index=True)

            else:
                print("\nALGORITMO GENETICO")
                print(f"Ejecución {i+1}:")
                alg_ag = algoritmogenetico.AlgoritmoGeneticoEstacionario(nodos_df, distancias_df, tiempos_df, tiempo_max, velocidad=velocidad)
                tiempo_ini = time.time()
                ruta_solucion, tiempo_total, distancia_total, beneficio = alg_ag.aplicar_algoritmo_genetico()
                tiempo_fin = time.time()
                tiempo_ejecucion = tiempo_fin - tiempo_ini
                mostrar_resultados(ruta_solucion, tiempo_total, distancia_total, beneficio, tiempo_max, es_ciclica, tiempo_ejecucion)
                margen = tiempo_max - tiempo_total
                nuevo_df = pd.DataFrame({
                    'ALGORITMO': ["GENETICO"],
                    'POIS VISITADOS': [ruta_solucion],
                    'INTERÉS': [beneficio],
                    'DISTANCIA TOTAL': [distancia_total],
                    'TIEMPO RUTA': [tiempo_total],
                    'MARGEN': [margen]
                })

                # Concatenar el nuevo DataFrame con resultados_df
                resultados_df = pd.concat([resultados_df, nuevo_df], ignore_index=True)

        if 5 in elecciones or 6 in elecciones: #memetico
            if(es_ciclica):
                tiempo_ini = time.time()
                print("\nALGORITMO MEMETICO")
                print(f"Ejecución {i+1}:")
                alg_mm = algoritmomemetico.AlgoritmoMemetico(nodos_df, distancias_df, tiempos_df, tiempo_max, velocidad=velocidad)
                ruta_solucion, tiempo_total, distancia_total, beneficio = alg_mm.aplicar_algoritmo_memetico_ciclico(nodo_ciclico=nodo_origen)
                tiempo_fin = time.time()
                tiempo_ejecucion = tiempo_fin - tiempo_ini
                mostrar_resultados(ruta_solucion, tiempo_total, distancia_total, beneficio, tiempo_max, es_ciclica, tiempo_ejecucion)
                margen = tiempo_max - tiempo_total
                nuevo_df = pd.DataFrame({
                    'ALGORITMO': ["MEMETICO"],
                    'POIS VISITADOS': [ruta_solucion],
                    'INTERÉS': [beneficio],
                    'DISTANCIA TOTAL': [distancia_total],
                    'TIEMPO RUTA': [tiempo_total],
                    'MARGEN': [margen]
                })

                # Concatenar el nuevo DataFrame con resultados_df
                resultados_df = pd.concat([resultados_df, nuevo_df], ignore_index=True)

            else:
                print("\nALGORITMO MEMETICO")
                print(f"Ejecución {i+1}:")
                alg_mm = algoritmomemetico.AlgoritmoMemetico(nodos_df, distancias_df, tiempos_df, tiempo_max, velocidad=velocidad)
                tiempo_ini = time.time()
                ruta_solucion, tiempo_total, distancia_total, beneficio = alg_mm.aplicar_algoritmo_memetico()
                tiempo_fin = time.time()
                tiempo_ejecucion = tiempo_fin - tiempo_ini
                mostrar_resultados(ruta_solucion, tiempo_total, distancia_total, beneficio, tiempo_max, es_ciclica, tiempo_ejecucion)
                margen = tiempo_max - tiempo_total
                nuevo_df = pd.DataFrame({
                    'ALGORITMO': ["MEMETICO"],
                    'POIS VISITADOS': [ruta_solucion],
                    'INTERÉS': [beneficio],
                    'DISTANCIA TOTAL': [distancia_total],
                    'TIEMPO RUTA': [tiempo_total],
                    'MARGEN': [margen]
                })

                # Concatenar el nuevo DataFrame con resultados_df
                resultados_df = pd.concat([resultados_df, nuevo_df], ignore_index=True)

    
    
    vista = visualizacion.Visualizacion(nodos_df)
    if nodos_df is not None:
        vista.visualizar_varias_rutas(nodos_df, resultados_df, "mapa_main_interactivo.html")

    


if __name__ == "__main__":
    numero_ejecuciones = int(input("Introduce el número de ejecuciones para cada algoritmo: "))
    main(numero_ejecuciones)
