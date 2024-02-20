

import math
from matplotlib.typing import ColorType
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



#input("Introduzca el archivo .csv: ")

def calcular_medias(archivo_path):
    df = pd.read_csv(archivo_path)
    years = pd.to_datetime(df['Fecha']).dt.year.unique()
    total_list = [] # Lista para almacenar las medias de consumo por hora para cada año y mes
    # Iterar sobre los años
    for j in years:
        #print(j)
        # Iterar sobre los meses
        for k in range(1, 13):
            # Filtrar el DataFrame por año y mes
            tmp = df[(pd.to_datetime(df['Fecha']).dt.year == j) & (pd.to_datetime(df['Fecha']).dt.month == k)]
            # Calcular las medias de consumo por hora para este DataFrame filtrado y añadirlo a total_list
            total_list.append(mean_per_hours(tmp))
    return total_list

def mean_per_hours(current_df):
    
    # Lista para almacenar las medias de consumo por hora
    mean_list = []
    # Iterar sobre las horas del día (1 a 24)
    for i in range(1, 25):
        # Filtrar el DataFrame por la hora actual
        aux = current_df[current_df['Hora'] == i]
        # Calcular la media de consumo para esa hora y añadirla a la lista
        mean_list.append(aux['Consumo'].mean())
    return mean_list





def guardar_grafica(total_list):
   
    flat_list = [item for sublist in total_list for item in sublist]
    
    x_axis = [i for i in range(1, 865)]

    plt.figure(figsize=(20,10))
    plt.bar(x_axis, flat_list, width=1.0)

    plt.ylim(0,1)

    plt.title('Average consumption per hour', fontsize=25)
    plt.xlabel('Month hour')
    plt.ylabel('consumption 0-1')

    plt.savefig('static/image.png')

def mean(serie):
    sumador=0
    length=serie.size
    for i in range(length):
        sumador+=serie[i]
    return sumador/length
    
    
def var(serie):
    sumador=0
    length=serie.size
    Mean=mean(serie)
    for i in range(length):
        sumador+=(serie[i]-Mean)**2
    return sumador/length

def std(serie):
    return math.sqrt(var(serie))

def price_per_hour(archivo_path,preciokwh_path):
    list = []
    list2 = []
    res = []
    df = pd.read_csv(archivo_path)
    df2 = pd.read_csv(preciokwh_path, header=0)
    serie= df2['Precio']
    for i in range(1,25):
        aux=df[(df['Hora'])==i]
        list.append(aux['Consumo'].mean())
        list2.append(serie[i-1])
    for k in range(24):
        res.append(list[k]*list2[k])
    return res

def guardar_precio(precio):
    plt.figure(figsize=(20,10))
    plt.hist(precio, bins=24, color='red', edgecolor='black', alpha=0.7)
    media=sum(precio)/len(precio)
    plt.axvline(x=media, color='green', linestyle='--', label='Media')
    plt.title('Average prize per hour', fontsize=25)
    plt.savefig('static/image1.png')