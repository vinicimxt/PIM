import os
import json
import hashlib

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

def carregar_dados_usuario():
    return carregar_json(DADOS_FILE)

def salvar_dados_usuario(dados):
    salvar_json(DADOS_FILE, dados)

def carregar_trilhas():
    if not os.path.exists(TRILHAS_FILE):
        print("⚠️ Arquivo trilhas.json não encontrado na pasta /data.")
        return []
    return carregar_json(TRILHAS_FILE)

def carregar_modulos(trilha_nome_snake):
    path = os.path.join(DATA_DIR, 'modules', f"{trilha_nome_snake}.json")
    return carregar_json(path)

def carregar_conteudo(trilha_nome_snake, id_modulo):
    path = os.path.join(DATA_DIR, 'contents', trilha_nome_snake, f"module_{id_modulo}_content.json")
    return carregar_json(path)

def carregar_questoes(trilha_nome_snake, id_modulo):
    path = os.path.join(DATA_DIR, 'questions', trilha_nome_snake, f"{trilha_nome_snake}_module{id_modulo}_questions.json")
    return carregar_json(path)

def snake_case(nome):
    return nome.lower().replace(' ', '_').replace(':', '').replace(',', '').replace('-', '').replace('__', '_')

def criptografar_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def cadastrar_usuario():
    dados = carregar_dados_usuario()
    print("\n--- Cadastro de Novo Usuário ---")
    nome = input("Nome completo: ").strip()
    idade = input("Idade: ").strip()
    login = input("Login desejado: ").strip()

    if any(a['login'] == login for a in dados.get('aluno', [])):
        print("⚠️  Login já em uso.")
        return

    senha = input("Senha: ").strip()
    hash_senha = criptografar_senha(senha)

    novo_id = (dados['aluno'][-1]['id'] if dados.get('aluno') else 0) + 1
    aluno = {
        "id": novo_id,
        "nome": nome,
        "login": login,
        "senha": hash_senha,
        "idade": idade,
        "trilha_atual": 1,
        "modulos_concluidos": {},
        "projetos_concluidos": [],
        "desafios_concluidos": [],
        "notas": {}
    }
    dados.setdefault('aluno', []).append(aluno)
    salvar_dados_usuario(dados)
    print("✅ Usuário cadastrado com sucesso!")

def login_usuario():
    dados = carregar_dados_usuario()
    print("\n--- Login ---")
    login = input("Login: ").strip()
    senha = input("Senha: ").strip()
    hash_senha = criptografar_senha(senha)

    for aluno in dados.get('aluno', []):
        if aluno['login'] == login and aluno['senha'] == hash_senha:
            print(f"\n🎉 Bem‐vindo(a), {aluno['nome']}!")
            return aluno
    print("⚠️  Login ou senha inválidos.")
    return None

def calcular_mediana(lista):
    lista_ordenada = sorted(lista)
    n = len(lista_ordenada)
    if n % 2:
        return lista_ordenada[n // 2]
    return (lista_ordenada[n//2 - 1] + lista_ordenada[n//2]) / 2

def mostrar_estatisticas():
    dados = carregar_dados_usuario()
    trilhas = carregar_trilhas()

    if not dados.get('aluno'):
        print("Nenhum aluno cadastrado.")
        return

    print("\n--- Estatísticas de Progresso ---")
    for trilha in trilhas:
        id_trilha = str(trilha['id_trilha'])
        nome_trilha = trilha['nome']

        conclusoes_trilha = [
            len(aluno.get('modulos_concluidos', {}).get(id_trilha, []))
            for aluno in dados['aluno']
        ]

        if not any(conclusoes_trilha):
            print(f"\n📚 {nome_trilha}: Nenhum módulo concluído ainda.")
            continue

        media = sum(conclusoes_trilha) / len(conclusoes_trilha)
        moda = max(set(conclusoes_trilha), key=conclusoes_trilha.count)
        mediana = calcular_mediana(conclusoes_trilha)

        print(f"\n📚 {nome_trilha}")
        print(f" - Média de módulos concluídos: {media:.2f}")
        print(f" - Moda de módulos concluídos: {moda}")
        print(f" - Mediana de módulos concluídos: {mediana}")

def fazer_quiz(aluno, questoes, trilha_nome_snake, id_trilha, id_modulo):
    if not questoes:
        print("\n⚠️  Este módulo não possui questionário.")
        return

    print("\n🧠 Quiz iniciado!")
    acertos = 0

    for q in questoes:
        print(f"\n{q['pergunta']}")
        for alt in q['alternativas']:
            print(f"  {alt}")
        resp = input("Resposta (letra): ").strip().upper()
        if resp == q['resposta'].upper():
            print("✅ Correto!")
            acertos += 1
        else:
            print(f"❌ Incorreto! Resposta certa: {q['resposta']}")

    total = len(questoes)
    nota = round((acertos / total) * 100, 2)
    print(f"\n📊 Você acertou {acertos} de {total} → Nota: {nota}%")

    if nota == 100:
        aluno.setdefault('modulos_concluidos', {}).setdefault(str(id_trilha), []).append(id_modulo)
        print(f"🎉 Parabéns! Módulo {id_modulo} concluído!")

    aluno.setdefault('notas', {}).setdefault(str(id_trilha), []).append(nota)

    dados = carregar_dados_usuario()
    for i, a in enumerate(dados.get('aluno', [])):
        if a['login'] == aluno['login']:
            dados['aluno'][i] = aluno
            break
    salvar_dados_usuario(dados)

def menu_modulo(aluno, trilha_nome, id_trilha, modulo):
    trilha_snake = snake_case(trilha_nome)
    conteudo = carregar_conteudo(trilha_snake, modulo['id_modulo'])
    questoes = carregar_questoes(trilha_snake, modulo['id_modulo'])

    while True:
        print(f"\n--- Módulo: {modulo['nome']} ---")
        print("1. Ver Conteúdo")
        print("2. Fazer Quiz")
        print("0. Voltar")
        op = input("Opção: ").strip()

        if op == "1":
            print(f"\n📚 Conteúdo: {conteudo.get('descricao', 'Sem descrição disponível.')}")
            input("\nPressione Enter para continuar.")
        elif op == "2":
            fazer_quiz(aluno, questoes, trilha_snake, id_trilha, modulo['id_modulo'])
        elif op == "0":
            break
        else:
            print("⚠️ Opção inválida.")

def menu_trilhas(aluno):
    trilhas = carregar_trilhas()
    print(trilhas)
    while True:
        print("\n--- Trilhas Disponíveis ---")
        for t in trilhas:
            print(f"{t['id_trilha']}. {t['nome']}")
        print("0. Voltar")

        op = input("Escolha: ").strip()
        if op == "0":
            break
        if not op.isdigit():
            print("⚠️ Opção inválida.")
            continue

        id_trilha = int(op)
        trilha = next((t for t in trilhas if t['id_trilha'] == id_trilha), None)
        if not trilha:
            print("⚠️ Trilha inválida.")
            continue

        trilha_snake = snake_case(trilha['nome'])
        modulos = carregar_modulos(trilha_snake)

        while True:
            print(f"\n--- {trilha['nome']} ---")
            for m in modulos:
                concluido = aluno.get('modulos_concluidos', {}).get(str(id_trilha), [])
                status = "✅" if m['id_modulo'] in concluido else "🔒"
                print(f"{m['id_modulo']}. {m['nome']} {status}")
            print("0. Voltar")

            escolha = input("Escolha o módulo: ").strip()
            if escolha == "0":
                break
            if escolha.isdigit():
                mid = int(escolha)
                modulo = next((x for x in modulos if x['id_modulo'] == mid), None)
                if modulo:
                    menu_modulo(aluno, trilha['nome'], id_trilha, modulo)
                else:
                    print("⚠️ Módulo inválido.")
            else:
                print("⚠️ Opção inválida.")

def menu_principal(aluno):
    while True:
        print("\n--- Menu Principal ---")
        print("1. Trilhas de Conhecimento")
        print("2. Estatísticas")
        print("0. Sair")
        op = input("Escolha: ").strip()

        if op == "1":
            menu_trilhas(aluno)
        elif op == "2":
            mostrar_estatisticas()
        elif op == "0":
            break
        else:
            print("⚠️ Opção inválida.")

def menu_inicial():
    while True:
        print("\n=== Plataforma Educação Digital Segura ===")
        print("1. Cadastrar")
        print("2. Login")
        print("0. Sair")
        op = input("Escolha: ").strip()

        if op == "1":
            cadastrar_usuario()
        elif op == "2":
            aluno = login_usuario()
            if aluno:
                menu_principal(aluno)
        elif op == "0":
            break
        else:
            print("⚠️ Opção inválida.")

if __name__ == "__main__":
    menu_inicial()
