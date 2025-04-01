from flask import Flask, jsonify
import func

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Olá do Flask!'

@app.route('/tecnico_laboratorio', methods=['GET'])
def tecnico_laboratorio():
    v = func.filto_exames_confirmado()
    return v
    

@app.route('/ver', methods=['GET'])
def ver():
    s = func.ola()
    return s



# Executa o servidor Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Permite acesso externo
