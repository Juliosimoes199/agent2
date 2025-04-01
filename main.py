from flask import Flask, jsonify, request
import func
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Olá do Flask!'

@app.route('/tecnico_laboratorio', methods=['POST', 'GET'])
def tecnico_laboratorio():
    if request.method == 'POST':
        question = request.form['question']
        lista_de_frases = [
            "Filtragem de Exames Confirmados.",
            "Alocação de Técnicos de Laboratório nos Exames Confirmados.",
            "Filtragem dos Perfis dos Pacientes.",
            "Edição de Dados dos Perfis dos Pacientes.",
            "Filtragem de Histórico de Exames.",
            "Filtragem de Próximos Exames.",
            "Inicializar Análise de Imagens Microscópicas Automatizada.",
            "Inicializar Análise de Imagens Microscópicas Manual.",
            "Geração de Laudo Laboratorial.",
            "Envio de Laudo Laboratorial.",
            "Filtragem de Perfis de Técnicos de Laboratórios.",
            "Remover Perfis de Técnicos de Laboratório.",
            "Editar Perfis de Técnicos de Laboratório.",
            "Monitoramento de Actividades de Técnicos de Laboratórios."
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
            return jsonify({"status": "sucesso", "frase": correspondente, "indice": v})
        else:
            return jsonify({"status": "erro", "mensagem": "Permissão negada para essa funcionalidade."}), 403

    
   # v = func.filto_exames_confirmado()
   # return v
    

@app.route('/ver', methods=['GET'])
def ver():
    s = func.ola()
    return s



# Executa o servidor Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Permite acesso externo
