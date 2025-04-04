import func
from flask import Flask, jsonify, request
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('rslp')
nltk.download('punkt_tab')

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Olá do Flask!'

@app.route('/chefe_laboratorio', methods=['POST'])
def tecnico_laboratorio():
    try:
        if request.method == 'POST':
            question = request.form['question'] #
            email = request.form['email']
            password = request.form['password']
            
            lista_de_frases = [
                "Filtragem de Exames Confirmados.",
                "Filtre Exames Confirmados",
                "Alocação de Técnicos de Laboratorio nos Exames Confirmados.",
                "Filtragem dos Perfis dos Pacientes.",
                "Edição de Dados dos Perfis dos Pacientes.",
                "Filtragem de Historico de Exames.",
                "Filtragem de Proximos Exames.",
                "Inicializar Analise de Imagens Microscopicas Automatizada.",
                "Inicializar Analise de Imagens Microscopicas Manual.",
                "Geração de Laudo Laboratorial.",
                "Envio de Laudo Laboratorial.",
                "Filtragem de Perfis de Técnicos de Laboratorios.",
                "Remover Perfis de Técnicos de Laboratorio.",
                "Editar Perfis de Técnicos de Laboratorio.",
                "Monitoramento de Actividades de Tecnicos de Laboratorios."
            ]

            def ver(frase, lista):
                for i, c in enumerate(lista):
                    if frase in c:
                        return i
                return None

            # Adiciona lista de palavras supérfluas para remover
            PALAVRAS_SUPERFLUAS = ["por mim", "por favor", "agora"]

            # Função para remover palavras ou expressões irrelevantes
            def limpar_frase(frase):
                for palavra in PALAVRAS_SUPERFLUAS:
                    frase = frase.replace(palavra, "")
                return frase.strip()

            # Função para normalizar frases e extrair palavras-chave
            def normalizar_frase(frase):
                stemmer = RSLPStemmer()  # Stemmer para Português
                stop_words = set(stopwords.words('portuguese'))  # Remove palavras irrelevantes
                palavras = word_tokenize(frase.lower())
                palavras_normalizadas = [stemmer.stem(p) for p in palavras if p not in stop_words and re.match(r'\w+', p)]
                return " ".join(palavras_normalizadas)

            # Função para verificar correspondência de frases normalizadas
            def verificar_correspondencia(frase, lista):
                frase_limpa = limpar_frase(frase)  # Remove palavras supérfluas
                frase_normalizada = normalizar_frase(frase_limpa)
                for item in lista:
                    if frase_normalizada in normalizar_frase(item):
                        return item
                return None

            # Verifica correspondência direta com base em normalização
            correspondente = verificar_correspondencia(question, lista_de_frases)
            if correspondente:
                indice = ver(correspondente, lista_de_frases)
                url = None
                if indice is not None:
                    if (indice == 0) or (indice == 1):
                        url = func.filto_exames_confirmado(email, password)
                    return jsonify({"status": "sucesso", "frase": correspondente, "indice": indice, "url":url})
                else:
                    return jsonify({"status": "erro", "mensagem": "Índice não encontrado."}), 500
            else:
                return jsonify({"status": "erro", "mensagem": "Permissão negada para essa funcionalidade."}), 403

    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

@app.route('/ver', methods=['GET'])
def ver_rota():
    s = func.ola1()  # Supondo que func.ola() retorne uma string
    return s

# Executa o servidor Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Permite acesso externo
