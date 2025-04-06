# baixar antes de usar o spacy=  python -m spacy download pt_core_news_md
import spacy
import re

# Carrega o modelo de linguagem do spaCy
nlp = spacy.load("pt_core_news_sm")

def extraor_nomes(texto):
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

# Texto de exemplo
    texto = """O cliente com sexo feminino, julio cesar . entre em contato pelo e-mail maria.silva@example.com ou pelo telefone 999887766."""

# Extrai informações pessoais
    informacoes, outras_entidades = extrair_informacoes_pessoais(texto)


#print("Outras Entidades Encontradas:", outras_entidades)
    nome = informacoes['nomes']
    return nome[0]