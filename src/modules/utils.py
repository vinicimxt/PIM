import os
import json
import hashlib
import subprocess, platform

DATA_DIR = 'src/data'
DADOS_FILE = os.path.join(DATA_DIR, 'user.json')
TRILHAS_FILE = os.path.join(DATA_DIR, 'trilhas.json')

def carregar_json(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                return data if isinstance(data, (list, dict)) else {}
            except json.JSONDecodeError as e:
                print(f"⚠️ Erro ao carregar JSON em {path}: {e}")
                return {}
    return {}

def salvar_json(path, dados):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def carregar_modulos(trilha_nome_snake):
    path = os.path.join(DATA_DIR, 'modules', f"{trilha_nome_snake}.json")
    return carregar_json(path)

def carregar_modulos_por_caminho(caminho_relativo):
    path = os.path.join(DATA_DIR, caminho_relativo)
    return carregar_json(path)



def carregar_conteudo( ):
    path = os.path.join(DATA_DIR, 'contents', "contents.json")
    return carregar_json(path)

def carregar_questoes(trilha_nome_snake, id_modulo):
    path = os.path.join(DATA_DIR, 'questions', trilha_nome_snake, f"{trilha_nome_snake}_module{id_modulo}_questions.json")
    return carregar_json(path)

def snake_case(nome):
    return nome.lower().replace(' ', '_').replace(':', '').replace(',', '').replace('-', '').replace('__', '_')

def criptografar_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def abrir_link(caminho_relativo):
    raiz_projeto = os.path.abspath(os.path.join(os.path.dirname(__file__), ""))
    
    caminho_completo = os.path.normpath(os.path.join(raiz_projeto, caminho_relativo))


    if not os.path.exists(caminho_completo):
        print(f"❌ Arquivo não encontrado: {caminho_completo}")
        return

    sistema = platform.system()
    try:
        if sistema == "Darwin":  # macOS
            subprocess.run(["open", caminho_completo])
        elif sistema == "Linux":
            subprocess.run(["xdg-open", caminho_completo])
        elif sistema == "Windows":
            subprocess.run(["start", caminho_completo], shell=True)
        else:
            print(f"⚠️ Sistema {sistema} não suportado.")
    except Exception as e:
        print(f"❌ Erro ao tentar abrir o arquivo: {e}")