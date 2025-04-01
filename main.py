from flask import Flask, jsonify
import func
import cv2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Olá do Flask!'

@app.route('/tecnico_laboratorio', methods=['GET'])
def tecnico_laboratorio():
    return func.filto_exames_confirmado()
    

@app.route('/ver', methods=['GET'])
def ver():
    s = func.ola()
    return s



# Executa o servidor Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Permite acesso externo
