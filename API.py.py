from flask import Flask, jsonify, request
import random
from sinais import calcular_probabilidade, rodadas_anteriores, adicionar_resultado

app = Flask(__name__)

@app.route('/')
def home():
    return "API de Sinais Bac Bo rodando!"

@app.route('/rodadas', methods=['GET'])
def get_rodadas():
    return jsonify({"rodadas": rodadas_anteriores})

@app.route('/probabilidades', methods=['GET'])
def get_probabilidades():
    probabilidades = calcular_probabilidade(rodadas_anteriores)
    return jsonify({"probabilidades": probabilidades})

@app.route('/adicionar_resultado', methods=['POST'])
def adicionar_resultado_endpoint():
    return adicionar_resultado(request.get_json())

@app.route('/forcar_sinal', methods=['GET'])
def forcar_sinal():
    probabilidades = calcular_probabilidade(rodadas_anteriores)
    proxima_aposta = max(probabilidades, key=probabilidades.get)
    
    if proxima_aposta == "🟧":
        proxima_aposta = random.choice(["🔴", "🔵"])
    
    mensagem_sinal = f"Entrar na cor {proxima_aposta} Proteção no empate 🟧 5% do valor da sua aposta"
    return jsonify({"sinal": mensagem_sinal})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
