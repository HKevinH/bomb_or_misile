import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor

def cargar_datos(csv_path='./Dataset/datos_entrenamiento.csv'):
    datos = pd.read_csv(csv_path)
    X = datos[['suposicion_actual', 'bombas', 'misiles']].values
    y = datos['ajuste_necesario'].values.reshape(-1, 1)
    return X, y

def definir_modelo():
    modelo = DecisionTreeRegressor(random_state=42)
    return modelo

def entrenar_modelo(modelo, X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler_x = StandardScaler().fit(X_train)
    X_train_scaled = scaler_x.transform(X_train)
    modelo.fit(X_train_scaled, y_train)
    return modelo, scaler_x

def juego(modelo, scaler_x):
    rango_min, rango_max = 0, 1000
    suposicion_actual = (rango_min + rango_max) // 2
    print("Intentaré adivinar el número en el que estás pensando entre 0 y 1000.")

    while True:
        print(f"Mi suposición es {suposicion_actual}")
        respuesta = input("¿He adivinado tu número? (sí/no): ").lower().strip()
        if respuesta == 'sí':
            print(f"¡He adivinado tu número! Era {suposicion_actual}.")
            break

        bombas = int(input("Número de bombas: "))
        misiles = int(input("Número de misiles: "))
        entrada = scaler_x.transform([[suposicion_actual, bombas, misiles]])
        ajuste_predicho = modelo.predict(entrada)[0]

        # Ajuste del rango en función de las pistas de bombas y misiles
        if bombas > 0:
            rango_max = suposicion_actual  # Estrechar el rango superior
        if misiles > 0:
            rango_min = suposicion_actual  # Estrechar el rango inferior

        # Ajuste de la próxima suposición
        if bombas > misiles:
            paso = max(1, (rango_max - rango_min) // (bombas + 2))  # Ajuste más fino si hay más bombas
            suposicion_actual -= paso
        else:
            paso = max(10, (rango_max - rango_min) // (misiles + 2))  # Ajuste más grande si hay más misiles
            suposicion_actual += paso

        suposicion_actual = max(rango_min, min(suposicion_actual, rango_max))

# Cargar datos y definir el modelo
X, y = cargar_datos()
modelo = definir_modelo()

# Entrenar el modelo y obtener el escalador
modelo, scaler_x = entrenar_modelo(modelo, X, y)

# Jugar
juego(modelo, scaler_x)
