from flask import Flask, jsonify, request, session
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from itertools import permutations

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'
CORS(app, supports_credentials=True, origins=["http://localhost:3000"])  
auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("secret")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

def generar_numeros():
    return [''.join(p) for p in permutations('0123456789', 3) if len(set(p)) == 3]

@app.route('/api/nuevo-juego', methods=['GET'])
@auth.login_required
def nuevo_juego():
    session['candidatos'] = generar_numeros()
    session['intentos'] = 0
    return jsonify({'candidatos': session['candidatos'], 'intentos': session['intentos']})

@app.route('/api/enviar-intento', methods=['POST'])
@auth.login_required
def enviar_intento():
    data = request.json
    suposicion = data.get('suposicion')
    bombas = data.get('bombas')
    misiles = data.get('misiles')
    respuesta_nada = data.get('nada', False)
    
    if not all([suposicion, bombas is not None, misiles is not None]):
        return jsonify({"error": "Faltan datos necesarios"}), 400

    candidatos = session.get('candidatos', [])
    if respuesta_nada:
        digitos_descartados = set(suposicion)
        candidatos = descartar_digitos(candidatos, digitos_descartados)
    else:
        candidatos = actualizar_candidatos(candidatos, suposicion, bombas, misiles)

    session['candidatos'] = candidatos
    session['intentos'] += 1
    return jsonify({'candidatos': candidatos, 'intentos': session['intentos']})

def descartar_digitos(candidatos, digitos_descartados):
    return [num for num in candidatos if all(d not in num for d in digitos_descartados)]

def actualizar_candidatos(candidatos, suposicion, bombas, misiles):
    nuevos_candidatos = []
    for candidato in candidatos:
        b, m = evaluar_suposicion(suposicion, candidato)
        if b == bombas and m == misiles:
            nuevos_candidatos.append(candidato)
    return nuevos_candidatos

def evaluar_suposicion(suposicion, secreto):
    bombas = sum(s == p for s, p in zip(suposicion, secreto))
    print(bombas)
    misiles = sum(min(suposicion.count(x), secreto.count(x)) for x in set(suposicion)) - bombas
    print(misiles)
    return bombas, misiles

if __name__ == '__main__':
    app.run(debug=True)
