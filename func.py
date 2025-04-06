from flask import Flask, jsonify
import cv2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time


def filto_exames_confirmado(email, password):
    # Configura o modo headless no Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executa sem interface gráfica
    chrome_options.add_argument("--no-sandbox")  # Recomendado para ambientes como VMs
    chrome_options.add_argument("--disable-dev-shm-usage")  # Evita problemas de memória compartilhada
    chrome_options.add_argument("--disable-gpu")  # Desativa GPU (apenas para precaução em alguns sistemas)

    # Inicializa o driver com as opções configuradas
    navegador = webdriver.Chrome(options=chrome_options)
    
    try:
        # Abre a página de login
        navegador.get('https://akin-lis-app-web.vercel.app/')

        # Preenche as abas de login
        navegador.find_element("id", "email").send_keys(email)
        navegador.find_element("id", "password").send_keys(password)

        # Clica no botão de login
        wait = WebDriverWait(navegador, 30)
        element = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/section/div/div/div[2]/form/button')))
        element.click()

        # Espera até que o botão "Agendamentos" esteja presente
        agendamentos_button = WebDriverWait(navegador, 10000).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[2]/div/div[2]/div/ul/li[1]/button"))
    )
    # Clique no botão "Agendamentos" ou faça outra ação necessária
        print("Apareceu")
        # Captura uma captura de tela da página
        navegador.save_screenshot('screenshot.png')

        # Carrega a captura de tela e a imagem do elemento
        screenshot = cv2.imread('screenshot.png')
        element_image = cv2.imread('ct.png')

        # Usa OpenCV para localizar a posição do elemento na captura de tela
        result = cv2.matchTemplate(screenshot, element_image, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Desenha um retângulo ao redor do elemento encontrado
        top_left = max_loc
        bottom_right = (top_left[0] + element_image.shape[1], top_left[1] + element_image.shape[0])
        cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)
        click_script = f"document.elementFromPoint({bottom_right[0]}, {bottom_right[1]}).click();"
        navegador.execute_script(click_script)
        #time.sleep(20)
        #navegador.find_element(By.XPATH, '//*[@id="radix-:ri:"]/ul/li[3]/a/span').click()

        navegador.save_screenshot('screenshot.png')

        # Carrega a captura de tela e a imagem do elemento
        screenshot = cv2.imread('screenshot.png')
        element_image = cv2.imread('confirmados.png')

        # Usa OpenCV para localizar a posição do elemento na captura de tela
        result = cv2.matchTemplate(screenshot, element_image, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Desenha um retângulo ao redor do elemento encontrado
        top_left = max_loc
        bottom_right = (top_left[0] + element_image.shape[1], top_left[1] + element_image.shape[0])
        cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)
        click_script = f"document.elementFromPoint({bottom_right[0]}, {bottom_right[1]}).click();"
        navegador.execute_script(click_script)

        # Salva a imagem resultante
        cv2.imwrite('resultado.png', screenshot)
        time.sleep(1)
        # Retorna a URL atual como resposta
        current_url = navegador.current_url
        print("URL atual da aba:", current_url)
        return current_url

    except TimeoutException:
        print("O botão 'Agendamentos' não apareceu a tempo.")
        return jsonify({"status": "erro", "mensagem": "O botão não apareceu a tempo"})

    finally:
        # Garante que o navegador seja fechado
        navegador.quit()

def filtro_pacientes():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executa sem interface gráfica
    chrome_options.add_argument("--no-sandbox")  # Recomendado para ambientes como VMs
    chrome_options.add_argument("--disable-dev-shm-usage")  # Evita problemas de memória compartilhada
    chrome_options.add_argument("--disable-gpu")  # Desativa GPU (apenas para precaução em alguns sistemas)

    # Inicializa o driver com as opções configuradas
    navegador = webdriver.Chrome(options=chrome_options)
    

    # Abre a página de login
    navegador = webdriver.Chrome()

# Abre a página de login
    navegador.get('https://akin-lis-app-web.vercel.app/')
    navegador.maximize_window()
# Preenche as abas de login (substitua 'username_field', 'password_field' e 'login_button' pelos seletores corretos)
    navegador.find_element("id", "email").send_keys("jpedro@gmail.com")
    navegador.find_element("id", "password").send_keys("jpe2024")
# Identificar o botão usando uma parte da classe e o tipo
#navegador.find_element(By.CSS_SELECTOR, 'button.bg-blue-600[type="submit"]').click()
    wait = WebDriverWait(navegador, 30)
    element = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/section/div/div/div[2]/form/button')))
    element.click()

    wait = WebDriverWait(navegador, 30000)
    element = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/div[2]/div/div[2]/div/ul/li[2]/button/a[2]/span')))
    element.click()

    wait = WebDriverWait(navegador, 30000)
    element = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/main/div/div/div[1]/div/div/div[1]/div[2]/input')))
    element.send_keys("júlio césar")

    wait = WebDriverWait(navegador, 30000)
    element = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/main/div/div/div[1]/div/div/div[2]/table/tbody/tr/td[6]/a')))
    element.click()

    time.sleep(1)
# Obter a URL da aba atual
    current_url = navegador.current_url

    return  current_url

def ola1():
    return "Mas uma vez"
