import telebot
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

TOKEN = "SEU_TOKEN"
CHAT_ID = "SEU_CHAT_ID"
bot = telebot.TeleBot(TOKEN)

# Link camuflado
LINK_PLATAFORMA = "[Apostar agora](https://www.estrelabet.bet.br/pb/jogos)"

# Configuração do Selenium
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
except Exception as e:
    print(f"Erro ao iniciar o WebDriver: {e}")
    exit(1)

rodadas_anteriores = []
contador_empate = 0

def obter_resultados_bacbo():
    global rodadas_anteriores
    url = "https://historicbet.com/cataloguer/bacbo/"
    driver.get(url)
    time.sleep(5)

    try:
        elemento = driver.find_element(By.XPATH, "/html/body/div[4]/main/div[9]")
        resultados = elemento.text.split(" ")
        rodadas_anteriores = resultados[-50:]
        print("Rodadas atualizadas:", rodadas_anteriores)
    except Exception as e:
        print("Erro ao obter resultados:", e)

def calcular_probabilidade(rodadas):
    total = len(rodadas)
    if total == 0:
        return {"🔴": 0.33, "🔵": 0.33, "🟧": 0.34}

    contagens = {"🔴": 0, "🔵": 0, "🟧": 0}
    for resultado in rodadas:
        if resultado in contagens:
            contagens[resultado] += 1

    return {chave: contagens[chave] / total for chave in contagens}

def adicionar_resultado(dados):
    global contador_empate
    if not dados or "resultado" not in dados:
        return jsonify({"erro": "Envie um JSON com a chave 'resultado'"}), 400

    resultado_real = dados["resultado"]
    if resultado_real not in ["🔴", "🔵", "🟧"]:
        return jsonify({"erro": "Resultado inválido. Use 🔴, 🔵 ou 🟧"}), 400

    rodadas_anteriores.append(resultado_real)

    if resultado_real == "🟧":
        contador_empate = 0
    else:
        contador_empate += 1

    return jsonify({"mensagem": "Resultado adicionado com sucesso!", "rodadas": rodadas_anteriores})

def enviar_sinal():
    global contador_empate
    while True:
        obter_resultados_bacbo()
        probabilidades = calcular_probabilidade(rodadas_anteriores)
        proxima_aposta = max(probabilidades, key=probabilidades.get)

        if proxima_aposta == "🟧" and contador_empate < 26:
            proxima_aposta = random.choice(["🔴", "🔵"])

        mensagem_sinal = f"{LINK_PLATAFORMA}\n\nEntrar na cor {proxima_aposta} Proteção no empate 🟧 5% do valor da sua aposta"
        bot.send_message(CHAT_ID, mensagem_sinal, parse_mode="Markdown")
        print(f"Sinal enviado: {mensagem_sinal}")

        time.sleep(60)

if __name__ == '__main__':
    enviar_sinal()
