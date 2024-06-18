import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse  # Importa argparse
import ast
from math import pi
import numpy as np


def cargar_datos(ruta_archivo):
    """Carga los datos desde un archivo CSV.

    Args:
        ruta_archivo (str): La ruta del archivo CSV.

    Returns:
        pandas.DataFrame: Los datos cargados desde el archivo CSV.
    """
    return pd.read_csv(ruta_archivo)

def escribir_resultados_a_archivo_df(ruta_archivo, resultados_df):
    resultados_df.to_csv(ruta_archivo, index=False)

def graficar_dispersion(resultados, x, y, titulo_comun="", hue='ALGORITMO'):
    """Genera un gráfico de dispersión.

       Args:
        resultados (pandas.DataFrame): El DataFrame que contiene los datos.
        x (str): El nombre de la columna para el eje x.
        y (str): El nombre de la columna para el eje y.
        titulo_comun (str): El título común para el gráfico.
        hue (str): El nombre de la columna para agrupar colores. 
    """
    plt.figure(figsize=(10, 8))
    ax = sns.scatterplot(data=resultados, x=x, y=y, hue=hue, style=hue, s=100)

    plt.title(f'{titulo_comun}\nDispersión de {x} vs {y}', fontsize=14, fontweight='bold') 
    plt.xlabel(x, fontsize=13) 
    plt.ylabel(y, fontsize=13) 
    plt.legend(loc='best', title='Algoritmo', frameon=False, fontsize=12, title_fontsize=13)
    
    annot = ax.annotate("", xy=(0,0), xytext=(20,20), textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    def update_annot(ind, ax, annot, scatter):
        pos = scatter.get_offsets()[ind["ind"][0]]
        row_id = ind["ind"][0]
        x_val, y_val = pos
        algo_name = resultados.iloc[row_id][hue]  # Acceso al nombre del algoritmo
        annot.xy = pos
        text = f"Algoritmo: {algo_name}\n{x}: {x_val:.2f}, {y}: {y_val:.2f}"
        annot.set_text(text)
        annot.get_bbox_patch().set_alpha(0.4)

    def hover(event):
        vis = annot.get_visible()
        if event.inaxes == ax:
            cont, ind = scatter.contains(event)
            if cont:
                update_annot(ind, ax, annot, scatter)
                annot.set_visible(True)
                plt.draw()
            else:
                if vis:
                    annot.set_visible(False)
                    plt.draw()

    scatter = ax.collections[0]  # Acceso a la colección de puntos creada por sns.scatterplot
    plt.gcf().canvas.mpl_connect("motion_notify_event", hover)


def graficar_bigotes(resultados, y, x='ALGORITMO', titulo_comun=""):
    """Genera un diagrama de caja.

    Args:
        resultados (pandas.DataFrame): El DataFrame que contiene los datos.
        y (str): El nombre de la columna para el eje y.
        x (str): El nombre de la columna para agrupar en el eje x.
        titulo_comun (str): El título común para el gráfico.
    """
    plt.figure(figsize=(10, 8))
   
    paleta_colores = sns.color_palette("viridis", n_colors=len(resultados[x].unique()))  
    
    sns.boxplot(x=x, y=y, data=resultados, palette=paleta_colores)
    plt.title(f'{titulo_comun}\nDiagrama de caja de {y}', fontsize=14, fontweight='bold')
    plt.xticks(fontsize=13) 
    plt.yticks(fontsize=13)  
    plt.xlabel('')  
    plt.ylabel(y, fontsize=13) 
    plt.grid(True, linestyle='--', alpha=0.6) 

    plt.tight_layout()  
    
def graficar_diagrama_araña(resultados, titulo_comun=""):
    """Genera un diagrama de araña.

    Args:
        resultados (pandas.DataFrame): El DataFrame que contiene los datos.
        titulo_comun (str): El título común para el gráfico. 
    """
    categorias = ['INTERÉS', 'DISTANCIA TOTAL', 'TIEMPO RUTA', 'MARGEN','NUMERO DE POIS VISITADOS']
    N = len(categorias)
    
    valores_maximos = resultados[categorias].max()
    resultados_normalizados = resultados[categorias] / valores_maximos
    
    promedios_por_algoritmo = resultados_normalizados.groupby(resultados['ALGORITMO']).mean().reset_index()
    
    angulos = [n / float(N) * 2 * pi for n in range(N)]
    angulos += angulos[:1]
    
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    
    for index, row in promedios_por_algoritmo.iterrows():
        valores = row.drop('ALGORITMO').values.flatten().tolist()
        valores += valores[:1]
        ax.plot(angulos, valores, linewidth=2, linestyle='-', marker='o', markersize=8, label=row['ALGORITMO'])
        ax.fill(angulos, valores, alpha=0.1)
    
    ax.set_thetagrids([n * 360.0 / N for n in range(N)], categorias, fontsize=12)  
    ax.tick_params(axis='y', labelsize=12)  
    plt.title(titulo_comun + '\nDiagrama de Araña por Algoritmo', fontsize=14, fontweight='bold', pad=30) 
    plt.legend(loc='upper left', bbox_to_anchor=(1.0, 0.9), fontsize=12)  

    # Mover las etiquetas fuera del círculo
    for i, label in enumerate(ax.get_xticklabels()):
        label.set_position((-0.1,-0.1))
        

  

def graficar_matriz_pois(resultados, tamaño_bbdd, titulo_comun=""):
    """Genera una matriz de POIs visitados.

    Args:
        resultados (pandas.DataFrame): El DataFrame que contiene los datos.
        tamaño_bbdd (int): El tamaño de la base de datos de POIs.
        titulo_comun (str): El título común para el gráfico. 
    """
    plt.figure(figsize=(10, 8))
    max_pois_visitados = resultados['POIS VISITADOS'].apply(lambda x: len(ast.literal_eval(x))).max()

    pois = range(1, tamaño_bbdd + 1)
    matriz_pois = pd.DataFrame(0, index=pois, columns=range(1, max_pois_visitados + 1))
    
    for index, row in resultados.iterrows():
        pois_visitados = ast.literal_eval(row['POIS VISITADOS'])
        for idx, poi in enumerate(pois_visitados, start=1):
            if poi in pois:
                matriz_pois.loc[poi, idx] += 1

    ax = sns.heatmap(matriz_pois, cmap='Greys', cbar=True)
    plt.title(titulo_comun + '\nMatriz de POIs Visitados', fontsize=14, fontweight='bold', pad=30)
    plt.xlabel('Posición en la Solución', fontsize=12)
    plt.ylabel('ID del POI', fontsize=12)

    annot = ax.annotate("", xy=(0,0), xytext=(10,10), textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="white", ec="black"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    def hover(event):
        if event.inaxes == ax:
            # Convertir las coordenadas del evento a ubicación de celda
            col, row = int(event.xdata + 0.5), int(event.ydata + 0.5)
            if row > 0 and row <= tamaño_bbdd and col > 0 and col <= max_pois_visitados:
                # Ajustar la posición de la anotación y actualizar su texto
                annot.xy = (col - 1, row - 1)
                poi_id = row
                visit_count = matriz_pois.iloc[row-1, col-1]
                if(visit_count > 0):
                    annot.set_text(f"POI {poi_id}\nPosición: {col}\nVisitas: {visit_count}")
                    annot.set_visible(True)
                    plt.draw()
            else:
                if annot.get_visible():
                    annot.set_visible(False)
                    plt.draw()
        else:
            if annot.get_visible():
                annot.set_visible(False)
                plt.draw()

    plt.gcf().canvas.mpl_connect("motion_notify_event", hover)


def tabla_ordenada_por_interes(resultados):
    """Ordena y muestra una tabla basada en el nivel de interés.
    
    Args:
        resultados (pandas.DataFrame): DataFrame con los datos de los algoritmos.

    Returns:
        pandas.DataFrame: DataFrame ordenado por nivel de interés.
    """
    return resultados.sort_values(by='INTERÉS', ascending=False)

def mejor_solucion_por_algoritmo(resultados):
    """Encuentra la mejor solución por cada algoritmo con respecto al interes, en caso de empate el siguiente factor 
    es el tiempo de ruta. 

    Args:
        resultados (pandas.DataFrame): DataFrame con los datos de los algoritmos.

    Returns:
        pandas.DataFrame: DataFrame con la mejor solución de cada algoritmo.
    """
    # Primero ordenamos los resultados por INTERÉS y luego por DISTANCIA TOTAL
    resultados = resultados.sort_values(by=['INTERÉS', 'TIEMPO RUTA'], ascending=[False, True])
    # Agrupamos por ALGORITMO y tomamos la primera ocurrencia que será la mejor en INTERÉS y menor en DISTANCIA TOTAL
    resultados = resultados.loc[resultados.groupby('ALGORITMO')['INTERÉS'].idxmax()]
    return resultados.sort_values(by='INTERÉS', ascending=False)

        
    
# Función para calcular ROC
def calcular_roc(resultados, criterios):
    # Normalizar cada criterio para que todos tengan igual importancia
    for criterio in criterios:
        max_value = resultados[criterio].max()
        resultados[criterio] = resultados[criterio] / max_value

    # Calcular ROC como el promedio de los criterios normalizados
    resultados['ROC'] = resultados[criterios].mean(axis=1)
    return resultados.sort_values(by='ROC', ascending=False)



def main(ruta_archivo):
    """Función principal para el análisis de resultados de algoritmos.

    Args:
        ruta_archivo (str): La ruta del archivo CSV con los resultados para análisis.
    """
    resultados = cargar_datos(ruta_archivo)
    tamaño_bbdd = resultados['TAMAÑO BBDD'].iloc[0] if 'TAMAÑO BBDD' in resultados.columns else 'Desconocido'
    tiempo_max = resultados['TIEMPO MAX'].iloc[0] if 'TIEMPO MAX' in resultados.columns else 'Desconocido'
    ciclica = resultados['RUTA CICLICA'].iloc[0] if 'RUTA CICLICA' in resultados.columns else 'Desconocido'
    edad = resultados['EDAD'].iloc[0] if 'EDAD' in resultados.columns else 'Desconocido'
    titulo_comun = f'BASE DE DATOS: {tamaño_bbdd} POIS. TIEMPO MAXIMO: {tiempo_max}. CICLICA: {ciclica}. EDAD: {edad}'

   
    graficar_dispersion(resultados, 'DISTANCIA TOTAL', 'INTERÉS', titulo_comun)
    graficar_dispersion(resultados, 'MARGEN', 'INTERÉS', titulo_comun)
    graficar_dispersion(resultados, 'TIEMPO RUTA', 'INTERÉS', titulo_comun)
    graficar_dispersion(resultados, 'TIEMPO RUTA', 'DISTANCIA TOTAL', titulo_comun)
    graficar_dispersion(resultados, 'MARGEN', 'NUMERO DE POIS VISITADOS', titulo_comun)
    
    
    graficar_bigotes(resultados, 'TIEMPO RUTA', 'ALGORITMO', titulo_comun)
   
    graficar_bigotes(resultados, 'INTERÉS', 'ALGORITMO', titulo_comun)
    graficar_bigotes(resultados, 'DISTANCIA TOTAL', 'ALGORITMO', titulo_comun)
    graficar_bigotes(resultados, 'MARGEN', 'ALGORITMO', titulo_comun)
    graficar_bigotes(resultados, 'NUMERO DE POIS VISITADOS', 'ALGORITMO', titulo_comun)
    
    graficar_diagrama_araña(resultados, titulo_comun)
    
    graficar_matriz_pois(resultados, int(tamaño_bbdd), titulo_comun)
    
    resultados_roc = resultados[:]
    criterios = ['INTERÉS', 'DISTANCIA TOTAL', 'TIEMPO RUTA', 'MARGEN', 'NUMERO DE POIS VISITADOS'] 
    resultados_roc = calcular_roc(resultados_roc, criterios)
    escribir_resultados_a_archivo_df('tabla_roc.csv', resultados_roc)
    
    resultados_ordenados = resultados[:]
    resultados_ordenados = tabla_ordenada_por_interes(resultados_ordenados)
    escribir_resultados_a_archivo_df('tabla_ordenada.csv', resultados_ordenados)
   
    mejores = f'MEJORES 5 RESULTADOS\n BASE DE DATOS: {tamaño_bbdd} POIS. TIEMPO MAXIMO: {tiempo_max}. CICLICA: {ciclica}. EDAD: {edad}'
    resultados_mejores = resultados[:]
    resultados_mejores = mejor_solucion_por_algoritmo(resultados_mejores)
    escribir_resultados_a_archivo_df('tabla_mejores.csv', resultados_mejores)
    graficar_diagrama_araña(resultados_mejores, mejores)
    
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Análisis de resultados de algoritmos.")
    parser.add_argument('ruta_archivo', type=str, help='Ruta del archivo CSV con los resultados para análisis.')

    args = parser.parse_args()
    main(args.ruta_archivo)
