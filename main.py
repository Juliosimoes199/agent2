from flask import Flask, request, jsonify
import cv2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Olá do Flask!'

@app.route('/filtros', methods=['GET'])
def filtros():
    # Inicializa o driver
    navegador = webdriver.Chrome()
    
    try:
        # Abre a página de login
        navegador.get('https://akin-lis-app-web.vercel.app/')
        navegador.maximize_window()

        # Preenche as abas de login
        navegador.find_element("id", "email").send_keys("jpedro@gmail.com")
        navegador.find_element("id", "password").send_keys("jpe2024")

        # Clica no botão de login
        wait = WebDriverWait(navegador, 30)
        element = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/section/div/div/div[2]/form/button')))
        element.click()

        # Espera até que o botão "Agendamentos" esteja presente
        agendamentos_button = WebDriverWait(navegador, 10000).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[2]/div/div[2]/div/ul/li[1]/button"))
        )

        # Realiza ações na página
        print("Apareceu")
        navegador.save_screenshot('screenshot.png')

        # Processa imagens usando OpenCV
        screenshot = cv2.imread('screenshot.png')
        element_image = cv2.imread('ct.png')
        result = cv2.matchTemplate(screenshot, element_image, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        
        # Desenha retângulo no elemento encontrado
        top_left = max_loc
        bottom_right = (top_left[0] + element_image.shape[1], top_left[1] + element_image.shape[0])
        cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)
        navegador.save_screenshot('resultado.png')
        
        # Retorna a URL atual como resposta
        current_url = navegador.current_url
        print("URL atual da aba:", current_url)
        return jsonify({"status": "sucesso", "url_atual": current_url})

    except TimeoutException:
        print("O botão 'Agendamentos' não apareceu a tempo.")
        return jsonify({"status": "erro", "mensagem": "O botão não apareceu a tempo"})

    finally:
        # Garante que o navegador seja fechado
        navegador.quit()

# Executa o servidor Flask
if __name__ == '__main__':
    app.run()
