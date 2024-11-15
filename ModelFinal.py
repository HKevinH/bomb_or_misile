import csv
from itertools import permutations
import random

def generar_numeros():
    # Genera todos los números posibles de tres dígitos sin repetición.
    return [''.join(p) for p in permutations('0123456789', 3)]

def leer_candidatos(archivo):
    with open(archivo, mode='r', newline='') as file:
        lector = csv.reader(file)
        return [fila[0] for fila in lector]

def escribir_candidatos(candidatos, archivo):
    with open(archivo, mode='w', newline='') as file:
        escritor = csv.writer(file)
        for num in candidatos:
            escritor.writerow([num])

def evaluar_suposicion(suposicion, secreto):
    bombas = sum(s == p for s, p in zip(suposicion, secreto))
    misiles = sum(min(suposicion.count(x), secreto.count(x)) for x in set(suposicion)) - bombas
    return bombas, misiles

def descartar_digitos(candidatos, digitos_descartados):
    return [num for num in candidatos if all(d not in num for d in digitos_descartados)]

def actualizar_candidatos(candidatos, suposicion, bombas, misiles, respuesta_nada):
    if respuesta_nada:
        digitos_descartados = set(suposicion)
        return descartar_digitos(candidatos, digitos_descartados)
    else:
        nuevos_candidatos = []
        for candidato in candidatos:
            b, m = evaluar_suposicion(suposicion, candidato)
            if b == bombas and m == misiles:
                nuevos_candidatos.append(candidato)
        return nuevos_candidatos

def main():
    archivo_candidatos = './Dataset/candidatos.csv'
    candidatos = generar_numeros()
    escribir_candidatos(candidatos, archivo_candidatos)
    intentos = 0
    
    while True:
        if len(candidatos) <= 3:
            sugerencias = candidatos
        else:
            sugerencias = random.sample(candidatos, 3)
        
        intentos += 1
        print(f"Intento #{intentos} - Sugerencias actuales: {', '.join(sugerencias)}")
        for suposicion in sugerencias:
            print(f"Sugerencia: {suposicion}")
            respuesta = input("¿Bombas, Misiles, o Nada? (Ejemplo: 1,0 o nada), o es tu número (escribe 'correcto'): ")
            if respuesta.lower() == "correcto":
                print(f"¡Número correcto! El número es {suposicion}")
                return
            elif respuesta.lower() == "nada":
                bombas = 0
                misiles = 0
                respuesta_nada = True
            else:
                bombas, misiles = map(int, respuesta.split(','))
                respuesta_nada = False
            
            candidatos = actualizar_candidatos(candidatos, suposicion, bombas, misiles, respuesta_nada)
            escribir_candidatos(candidatos, archivo_candidatos)
            print(f"Candidatos restantes: {len(candidatos)}")
            
            if len(candidatos) == 1:  
                print(f"¡Número correcto! El número es {candidatos[0]}")
                return
            
            if bombas == 3:
                print(f"¡Número correcto! El número es {suposicion}")
                return
       
        
        if not candidatos:
            print("No hay más candidatos. Juego terminado.")
            break

if __name__ == '__main__':
    main()

