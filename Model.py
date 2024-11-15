def adivinar_numero(numero_objetivo, rango_min=10, rango_max=1000):
    intentos = 0
    while rango_min <= rango_max:
        intentos += 1
        punto_medio = (rango_min + rango_max) // 2
        print(f"Intento {intentos}: ¿Es el número {punto_medio}?")

        if punto_medio == numero_objetivo:
            print(f"¡Número encontrado! El número es {punto_medio}.")
            return punto_medio
        elif punto_medio < numero_objetivo:
            rango_min = punto_medio + 1
        else:
            rango_max = punto_medio - 1
        
        if intentos >= 10:
            print("Límite de intentos alcanzado sin éxito.")
            return None

# Ejemplo de uso
numero_secreto = 200 
# Este sería el número que el programa intenta adivinar
adivinar_numero(numero_secreto)

# Bomba Cuando Esta en la Posición Correcta
# Misil Cuando el Número es correcto pero no está en la posición correcta
# No Se puede repetir el digitos es decir 200 no puede ser 220 y tampoco 200
# Suposición: 200


