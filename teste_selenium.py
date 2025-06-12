from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("start-maximized")
options.add_argument("--log-level=3")
options.add_argument("--disable-features=MediaSessionService,VoiceTranscriptionCapability")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

service = Service(ChromeDriverManager().install(), log_level="OFF")
driver = webdriver.Chrome(service=service, options=options)

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """Object.defineProperty(navigator, 'webdriver', { get: () => undefined });"""
})

testes_certos = 0
testes_errados = 0
falhas = []


def verificar_resultado(esperado, obtido, nome_teste):
    global testes_certos, testes_errados, falhas
    print(f"🧮 Resultado obtido: {obtido}")
    if obtido == esperado:
        print("✅ Resultado correto!")
        testes_certos += 1
    else:
        print("❌ Resultado incorreto!")
        testes_errados += 1
        falhas.append(f"{nome_teste} (esperado: {esperado}, obtido: {obtido})")



def clicar_botao(id_botao):
    botao = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, id_botao)))
    time.sleep(random.uniform(0.2, 0.5))
    botao.click()


def obter_resultado():
    resultado_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "display")))
    time.sleep(0.3)
    return resultado_div.text.strip()


try:
    driver.get("http://127.0.0.1:5500/Calculadora.html")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body")))

    def testar(nome_teste, botoes, resultado_esperado):
        print(f"\n🔹 {nome_teste}")
        for b in botoes:
            clicar_botao(b)
        resultado = obter_resultado()
        verificar_resultado(resultado_esperado, resultado, nome_teste)
        clicar_botao("C")

    print("\n\033[92mTESTES DE SOMA\033[0m")
    testar("Soma 1", ["1", "+", "2", "="], "3")
    testar("Soma 2", ["5", "-", "3", "+", "0", "="], "2")
    testar("Soma 3", ["1", ".", "7", "+", "0", ".", "3", "="], "2")

    print("\n\033[92mTESTES DE SUBTRAÇÃO\033[0m")
    testar("Subtração 1", ["8", "-", "4", "="], "4")
    testar("Subtração 2", ["9", "-", "3", "-", "3", ".", "4", "="], "2.6")
    testar("Subtração 3", ["5", "-", "2", "5", "="], "-20")

    print("\n\033[92mTESTES DE MULTIPLICAÇÃO\033[0m")
    testar("Multiplicação 1", ["3", "*", "2", "="], "6")
    testar("Multiplicação 2", ["2", ".", "5", "*", "2", "="], "5")
    testar("Multiplicação 3", ["4", "0", "*", "2", "="], "80")

    print("\n\033[92mTESTES DE DIVISÃO\033[0m")
    testar("Divisão 1", ["8", "/", "2", "="], "4")
    testar("Divisão 2", ["5", "/", "2", ".", "5", "="], "2")
    testar("Divisão 3", ["9", "/", "4", ".", "5", "/", "2", "="], "1")

    print("\n\033[94m========== RESUMO DOS TESTES ==========\033[0m")
    print(f"✔️ Testes corretos: {testes_certos}")
    print(f"❌ Testes incorretos: {testes_errados}")

    if falhas:
        print("\n❗ Testes com falha:")
        for falha in falhas:
            print(f" - {falha}")
    else:
        print("\n🎉 Todos os testes passaram!")

finally:
    driver.quit()
    print("\n\033[93mNavegador fechado.\033[0m")