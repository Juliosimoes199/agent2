import spacy
from fuzzywuzzy import fuzz
from flask import Flask, jsonify, request
import sys
import re
import func

app = Flask(__name__)
nlp = spacy.load("pt_core_news_md")  # Carrega o modelo Spacy uma vez

@app.route('/')
def hello_world():
    return 'Olá do Flask!'

@app.route('/chefe_laboratorio', methods=['POST'])
def tecnico_laboratorio():
    texto = request.form['texto']
    email = request.form['email']
    password = request.form['password']
    def analisar_texto(texto, palavras_chave):
        resultados = []
        doc = nlp(texto)

        for palavra in palavras_chave:
            palavra_doc = nlp(palavra)
            for token in doc:
                similaridade_semantica = token.similarity(palavra_doc) >= 0.75
                similaridade_textual = fuzz.ratio(token.text.lower(), palavra.lower()) >= 75

                if similaridade_semantica or similaridade_textual:
                    resultados.append(palavra)
        return list(set(resultados)) # Retorna apenas palavras-chave únicas encontradas

    palavras_chave = ["filtro", "exames", "confirmados",
                      "alocação", "técnico", "laboratório", "Aloque",
                      "perfis", "pacientes",
                      "editar", "edição", "dados", "informação",
                      "histórico", "próximos",
                      "inicializar", "análise", "imagens",
                      "microscópica", "automatizada", "manual",
                      "manualmente",
                      "geração", "gerar", "laudo",
                      "envio", "remover", "eliminar",
                      "monitorar", "monitoramento", "actividades",
                      "Acção", "movimento", "trabalho", "faça"]

    #texto = "Analise manual mais exames e exames laboratorias tambem"
    resultados = analisar_texto(texto, palavras_chave)
    if ("filtro" in resultados) & ("exames" in resultados):
        url = func.filto_exames_confirmado(email, password)
        return jsonify({"status": resultados, "url": url})

    elif ("filtro" in resultados) & (("perfis" in resultados) or ("pacientes" in resultados)):

        def extrair_informacoes_pessoais(texto):
            doc = nlp(texto)
            informacoes_pessoais = {
            "nomes": [],
            "emails": [],
            "telefones": [],
            }
            outras_entidades = []

    # Extrai entidades nomeadas e organiza por tipos
            for ent in doc.ents:
                if ent.label_ == "PER":  # Nome de pessoas
                    informacoes_pessoais["nomes"].append(ent.text)
                else:
                    outras_entidades.append({"texto": ent.text, "tipo": ent.label_})

    # Busca por e-mails no texto usando regex
            emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", texto)
            informacoes_pessoais["emails"].extend(emails)

    # Busca por números de telefone no texto usando regex
            telefones = re.findall(r"\b\d{8,11}\b", texto)
            informacoes_pessoais["telefones"].extend(telefones)


            return informacoes_pessoais, outras_entidades


        informacoes, outras_entidades = extrair_informacoes_pessoais("Jesus esta aqui")
        nomes = informacoes['nomes']
        nomes= nomes[0]
        
        nome = "Kuenda"
        url = func.filtro_pacientes(nome, password, email)
        return jsonify({"status": resultados, "url":url, "nomes":nomes})
    else:
        return "Não tem"
        
    #return jsonify({"status": resultados})

@app.route('/ver', methods=['GET'])
def ver_rota():
    # s = func.ola1()  # Remova se não estiver usando func
    return "Rota /ver" # Adicione um retorno padrão

# Executa o servidor Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Permite acesso externo
