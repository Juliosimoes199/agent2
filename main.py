import func
import time
from flask import Flask, jsonify, request
import sys


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Olá do Flask!'

@app.route('/chefe_laboratorio', methods=['GET'])
def tecnico_laboratorio():
        def analisar_texto(texto, palavras_chave):
        def analisar_texto(texto, palavras_chave):
        # Carregando o modelo de linguagem
        nlp = spacy.load("pt_core_news_md")
        resultados = []

        # Processando o texto
        doc = nlp(texto)

        for palavra in palavras_chave:
            palavra_doc = nlp(palavra)
            for token in doc:
                # Verifica similaridade semântica com Spacy
                similaridade_semantica = token.similarity(palavra_doc) >= 0.75

                # Verifica similaridade textual usando fuzzywuzzy
                similaridade_textual = fuzz.ratio(token.text.lower(), palavra.lower()) >= 75

                #if similaridade_semantica or similaridade_textual:
                    #resultados.append((token.text, palavra))

                if similaridade_semantica or similaridade_textual:
                    resultados.append(palavra)

        return resultados

    # Exemplo de uso
    #texto = "faça a edição os perfis dos pacientes de tecnicos exame monitoramento envie"                                          
    palavras_chave = ["filtro", "exames", "confirmados",
                      "alocação", "técnico", "laboratório", "Aloque",
                      "perfis", "pacientes",
                      "editar", "edição", "dados", "informação",
                      "histórico", "próximos","",
                      "inicializar", "análise", "imagens",
                      "microscópica", "automatizada", "manual",
                      "manualmente", "", "",
                      "geração", "gerar", "laudo",
                      "envio", "remover", "eliminar",
                      "monitorar", "monitoramento", "actividades",
                      "Acção", "movimento", "trabalho"

                     ]
    #while True:
    texto = "Analise manual mais exames"
     #   if texto == 'sair':
    #        break
    resultados = analisar_texto(texto, palavras_chave)
    #for token, palavra in resultados:
    #    print(f"'{token}' corresponde à palavra-chave '{palavra}'")

        #print(resultados)


    return jsonify({"status": resultados})

@app.route('/ver', methods=['GET'])
def ver_rota():
    s = func.ola1()  # Supondo que func.ola() retorne uma string
    return s

# Executa o servidor Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Permite acesso externo
