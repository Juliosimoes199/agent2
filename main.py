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
    # Inicializa o driver (substitua 'your_driver_path' pelo caminho do seu driver)
    navegador = webdriver.Chrome()

    # Abre a página de login
    navegador.get('https://akin-lis-app-web.vercel.app/')
    navegador.maximize_window()
    # Preenche as abas de login (substitua 'username_field', 'password_field' e 'login_button' pelos seletores corretos)
    navegador.find_element("id", "email").send_keys("jpedro@gmail.com")
    navegador.find_element("id", "password").send_keys("jpe2024")
    # Identificar o botão usando uma parte da classe e o tipo
    # navegador.find_element(By.CSS_SELECTOR, 'button.bg-blue-600[type="submit"]').click()
    # click_script = f"document.elementFromPoint({x}, {y}).click();"
    # navegador.execute_script(click_script)

    wait = WebDriverWait(navegador, 30)
    element = wait.until(EC.visibility_of_element_located(
        (By.XPATH, '/html/body/section/div/div/div[2]/form/button')))
    element.click()

    # Espera até que o botão "Agendamentos" esteja presente
    try:
        agendamentos_button = WebDriverWait(navegador, 10000).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div/div/div[2]/div/div[2]/div/ul/li[1]/button"))
        )
        # Clique no botão "Agendamentos" ou faça outra ação necessária
        print("Apareceu")
        # Captura uma captura de tela da página
        navegador.save_screenshot('screenshot.png')

        # Carrega a captura de tela e a imagem do elemento
        screenshot = cv2.imread('screenshot.png')
        element_image = cv2.imread('ct.png')

        # Usa OpenCV para localizar a posição do elemento na captura de tela
        result = cv2.matchTemplate(
            screenshot, element_image, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Desenha um retângulo ao redor do elemento encontrado
        top_left = max_loc
        bottom_right = (top_left[0] + element_image.shape[1],
                        top_left[1] + element_image.shape[0])
        cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)
        click_script = f"document.elementFromPoint({bottom_right[0]}, {bottom_right[1]}).click();"
        navegador.execute_script(click_script)
        # time.sleep(20)
        # navegador.find_element(By.XPATH, '//*[@id="radix-:ri:"]/ul/li[3]/a/span').click()

        navegador.save_screenshot('screenshot.png')

        # Carrega a captura de tela e a imagem do elemento
        screenshot = cv2.imread('screenshot.png')
        element_image = cv2.imread('confirmados.png')

        # Usa OpenCV para localizar a posição do elemento na captura de tela
        result = cv2.matchTemplate(
            screenshot, element_image, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Desenha um retângulo ao redor do elemento encontrado
        top_left = max_loc
        bottom_right = (top_left[0] + element_image.shape[1],
                        top_left[1] + element_image.shape[0])
        cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)
        click_script = f"document.elementFromPoint({bottom_right[0]}, {bottom_right[1]}).click();"
        navegador.execute_script(click_script)

        # Salva a imagem resultante
        cv2.imwrite('resultado.png', screenshot)
        time.sleep(1)
        current_url = navegador.current_url

        print("URL atual da aba:", current_url)

    except TimeoutException:
        print("O botão 'Agendamentos' não apareceu a tempo.")
    time.sleep(3)


app.run(host="0.0.0.0", port=8000)
