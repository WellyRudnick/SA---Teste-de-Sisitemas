<h1 align="center">Teste Unitário</h1>

O grupo foi designado a realizar um trabalho de operações aritméticas para validar o software. Embarcado da empresa de calculadora Techpoint, responsável pelo desenvolvimento de calculadoras portáteis. O time reunido por Paulo Ricardo, Bruno Ducka, Wellison, Lucas e Vinicius Ângelo é responsável por garantir que o módulo de operações básicas funcione corretamente antes de ser entregue a produção final. Desta forma é solicitado que o time realize testes unitários com rigor para as operações de soma, subtração, divisão e multiplicação prevendo
falhas comuns como estouro de valores e entradas inválidas.

## 1- Introduzindo o Selenium:

Para poder executar e codificar as dentro da página webp e automatiza, é nescessário puxar a biblioteca do selenium:

 ```python
# webdriver permite controlar navegadores
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
```
Com isso, código tem ligação com navegador

## 2- Configurando a página:

Para poder configurar a página, é utilizado o Options, service e driver, que configura o navegador para permitir a automatização:

```python
options = Options()

options.add_argument("--disable-blink-features=AutomationControlled")
#Esconde a informção de que o navegador está sendo controlado por automação
options.add_argument("start-maximized")
#abre o navegador já maximizado
options.add_argument("--log-level=3")
#Reduz a quantidade de logs no terminal
options.add_argument("--disable-features=MediaSessionService VoiceTranscriptionCapability")
#Desabilita serviços de mídia e transcrição de voz
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
#Faz o navegador a se identificar como usuário comum do Chrome.
service = Service(ChromeDriverManager().install(), log_level="OFF")
#Baixa a versão correta e compátivel do ChromerDriver, e inicia com os logs preparativos desligados para deixar o código mais limpo
driver = webdriver.Chrome(service=service, options=options)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """Object.defineProperty(navigator, 'webdriver', { get: () => undefined });"""
)
#Driver cria uma janela do Chrome, aplicando as configurações definidas no options e utilizando o service;


```

## 3- Criando as função de rotas do teste:

A proxima parte do código foca na criação de funções para verificação e interação das informações, as funções interagem com a calculadora, verificam os resultados esperados com os obtidos, também é criado variaveis e um array para armazenar os teste falhos e quantidade acertos e erros.

```python
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
        #armazena o nome do teste, o resultado esperado e o que foi obtido


def clicar_botao(id_botao):
    botao = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, id_botao)))
    time.sleep(random.uniform(0.2, 0.5))
    botao.click()
    # procura o botão na página

def obter_resultado():
    resultado_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "display")))
    time.sleep(0.3)
    return resultado_div.text.strip()

```
## 4- Execução do teste e exibição dos resultados:
A parte do código foca na verificação e interação das informações, o código interage com a calculadora para criar cenários de resultados, após concluir a interação, verifica os resultados esperados com os obtidos, se o teste foi bem sucedido, é adicionado 1 ponto de acerto, se o teste foi mal sucedio, é adicionado 1 ponto de erro e este teste falho é armazenado e só revelado no final da execução, mostrando os resultados obtidos com os esperados, após isso, o navegador é fechado.

```python
try:
    driver.get("file:///C:/Users/vinicius_alves9/Documents/the%20one/Calculadora.html")
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

```

## Membros do grupo:
<table style="background-color:blue"> <tr> <td align="center"> <a href="https://github.com/dutkabruno" target="_blank"> <img src="https://github.com/dutkabruno.png" width="100px" style="border-radius:50%"/><br/> <b>@Bruno</b> </a> </td> <td align="center"> <a href="https://github.com/luc4as-calixto" target="_blank"> <img src="https://github.com/luc4as-calixto.png" width="100px" style="border-radius:50%"/><br/> <b>@Lucas</b> </a> </td> <td align="center"> <a href="https://github.com/WellyRudnick" target="_blank"> <img src="https://github.com/WellyRudnick.png" width="100px" style="border-radius:50%"/><br/> <b>@Welly</b> </a> </td> <td align="center"> <a href="https://github.com/Paulo-r-joao" target="_blank"> <img src="https://github.com/Paulo-r-joao.png" width="100px" style="border-radius:50%"/><br/> <b>@Paulo</b> </a> </td> <td align="center"> <a href="https://github.com/vinicius835" target="_blank"> <img src="https://github.com/vinicius835.png" width="100px" style="border-radius:50%"/><br/> <b>@Vinicius.A</b> </a> </td> </tr> </table>
