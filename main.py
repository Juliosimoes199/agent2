  GNU nano 4.8                          /home/akin_osapicare/agent2/main.py                                     
import func
from flask import Flask, jsonify, request
import sys
print(f"Python executável: {sys.executable}")



app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Olá do Flask!'

@app.route('/chefe_laboratorio', methods=['GET'])
def tecnico_laboratorio():
    return 'Mais'

@app.route('/ver', methods=['GET'])
def ver_rota():
    s = func.ola1()  # Supondo que func.ola() retorne uma string
    return s

# Executa o servidor Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Permite acesso externo
