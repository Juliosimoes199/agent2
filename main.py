from flask import Flask, jsonify
import cv2
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time

# Configura logs globais
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.route('/')
def hello_world():
    logging.info("Rota '/' foi acessada.")
    return 'Olá do Flask!'

@app.route('/filtros', methods=['GET'])
def filtros():
    logging.info("Rota '/filtros' foi acessada.")
    
    # Configura o modo headless no Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executa sem interface gráfica
    chrome_options.add_argument("--no-sandbox")  # Recomendado para ambientes como VMs
    chrome_options.add_argument("--disable-dev-shm-usage")  # Evita problemas de memória compartilhada
    chrome_options.add_argument("--disable-gpu")  # Desativa GPU (apenas para precaução em alguns sistemas)
    logging.info("Opções do Chrome configuradas.")

    # Inicializa o driver com as opções configuradas
    navegador = webdriver.Chrome(options=chrome_options)
    logging.info("Navegador inicializado.")
    
    try:
        # Abre a página de login
        navegador.get('https://akin-lis-app-web.vercel.app/')
        logging.info("Página de login acessada.")

        # Preenche as abas de login
        navegador.find_element("id", "email").send_keys("jpedro@gmail.com")
        logging.info("Campo de email preenchido.")
        navegador.find_element("id", "password").send_keys("jpe2024")
        logging.info("Campo de senha preenchido.")

        # Clica no botão de login
        wait = WebDriverWait(navegador, 30)
        element = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/section/div/div/div[2]/form/button')))
        element.click()
        logging.info("Botão de login clicado.")

        # Espera até que o botão "Agendamentos" esteja presente
        agendamentos_button = WebDriverWait(navegador, 30).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[2]/div/div[2]/div/ul/li[1]/button"))
        )
        logging.info("Botão 'Agendamentos' encontrado.")

        # Captura uma captura de tela da página
        navegador.save_screenshot('screenshot.png')
        logging.info("Captura de tela salva.")

        # Carrega a captura de tela e a imagem do elemento
        screenshot = cv2.imread('screenshot.png')
        element_image = cv2.imread('ct.png')
        logging.info("Imagens carregadas para análise.")

        # Usa OpenCV para localizar a posição do elemento na captura de tela
        result = cv2.matchTemplate(screenshot, element_image, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Desenha um retângulo ao redor do elemento encontrado
        top_left = max_loc
        bottom_right = (top_left[0] + element_image.shape[1], top_left[1] + element_image.shape[0])
        cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)
        logging.info("Retângulo desenhado ao redor do elemento encontrado.")

        click_script = f"document.elementFromPoint({bottom_right[0]}, {bottom_right[1]}).click();"
        navegador.execute_script(click_script)
        logging.info("Elemento clicado via script executado.")

        # Salva a imagem resultante
        cv2.imwrite('resultado.png', screenshot)
        logging.info("Imagem resultante salva.")
        
        # Retorna a URL atual como resposta
        current_url = navegador.current_url
        logging.info(f"URL atual da aba: {current_url}")
        return jsonify({"status": "sucesso", "url_atual": current_url})

    except TimeoutException:
        logging.error("O botão 'Agendamentos' não apareceu a tempo.")
        return jsonify({"status": "erro", "mensagem": "O botão não apareceu a tempo"})

    finally:
        # Garante que o navegador seja fechado
        navegador.quit()
        logging.info("Navegador fechado.")

# Executa o servidor Flask
if __name__ == '__main__':
    try:
        logging.info("Iniciando servidor Flask.")
        app.run(host="0.0.0.0", port=5000)
    except Exception as e:
        logging.error(f"Erro ao iniciar o servidor Flask: {e}")
