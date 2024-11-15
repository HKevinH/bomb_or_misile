import pandas as pd
import numpy as np
import random

def generar_datos_mejorados(n_muestras=10000):
    entradas = []
    for _ in range(n_muestras):
        # Selecciona un número objetivo al azar para cada muestra
        numero_objetivo = np.random.randint(0, 1001)
        suposicion_actual = np.random.randint(0, 1001)
        distancia = abs(numero_objetivo - suposicion_actual)

        # Determina el número de bombas basado en la distancia
        if distancia < 10:
            bombas = 3
        elif distancia < 50:
            bombas = 2
        elif distancia < 100:
            bombas = 1
        else:
            bombas = 0

        # Ajusta la lógica para determinar el número de misiles, permitiendo hasta 3 misiles
        if distancia <= 100:
            misiles = 0
        else:
          misiles = min(7, 1 + distancia // 150)

        # Calcula el ajuste necesario para alcanzar el número objetivo
        ajuste_necesario = numero_objetivo - suposicion_actual

        # Agrega los datos de la muestra actual a la lista de entradas
        entradas.append([suposicion_actual, bombas, misiles, numero_objetivo, ajuste_necesario])

    # Crea un DataFrame de pandas con las entradas y asigna nombres a las columnas
    return pd.DataFrame(entradas, columns=['suposicion_actual', 'bombas', 'misiles', 'numero_objetivo', 'ajuste_necesario'])

# Genera los datos mejorados
df = generar_datos_mejorados()

# Guarda los datos en un archivo CSV sin incluir el índice
df.to_csv('./Dataset/datos_entrenamiento.csv', index=False)
