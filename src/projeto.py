import json
import hashlib
import os

DADOS_FILE = 'alunos.json'

def carregar_dados():
    if os.path.exists(DADOS_FILE):
        with open(DADOS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"aluno": [], "trilhas": []}

def salvar_dados(dados):
    with open(DADOS_FILE, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def criptografar_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# ---------------------------------------------------
# Cadastro / Login
# ---------------------------------------------------
def cadastrar_usuario():
    dados = carregar_dados()
    print("\n--- Cadastro de Novo Usuário ---")
    nome = input("Nome completo: ").strip()
    idade = input("Idade: ").strip()
    login = input("Login desejado: ").strip()

    if any(a['login'] == login for a in dados['aluno']):
        print("⚠️  Login já em uso.")
        return

    senha = input("Senha: ").strip()
    hash_senha = criptografar_senha(senha)

    novo_id = (dados['aluno'][-1]['id'] if dados['aluno'] else 0) + 1
    dados['aluno'].append({
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
    })
    salvar_dados(dados)
    print("✅ Usuário cadastrado com sucesso!")

def login_usuario():
    dados = carregar_dados()
    print("\n--- Login ---")
    login = input("Login: ").strip()
    senha = input("Senha: ").strip()
    hash_senha = criptografar_senha(senha)
    for aluno in dados['aluno']:
        if aluno['login'] == login and aluno['senha'] == hash_senha:
            print(f"\n🎉 Bem‐vindo(a), {aluno['nome']}!")
            return aluno
    print("⚠️  Login ou senha inválidos.")
    return None

# ---------------------------------------------------
# Estatísticas de Progresso
# ---------------------------------------------------
def calcular_mediana(lista):
    lista_ordenada = sorted(lista)
    n = len(lista_ordenada)
    if n % 2:
        return lista_ordenada[n // 2]
    return (lista_ordenada[n//2 - 1] + lista_ordenada[n//2]) / 2

def mostrar_estatisticas():
    dados = carregar_dados()
    conclusoes = [len(a.get('modulos_concluidos', [])) for a in dados['aluno']]
    if not conclusoes:
        print("Nenhum dado de progresso disponível.")
        return
    media = sum(conclusoes) / len(conclusoes)
    moda = max(set(conclusoes), key=conclusoes.count)
    mediana = calcular_mediana(conclusoes)
    print(f"\n--- Estatísticas de Progresso ---")
    print(f"Média de módulos concluídos: {media:.2f}")
    print(f"Moda de módulos concluídos: {moda}")
    print(f"Mediana de módulos concluídos: {mediana}")

# ---------------------------------------------------
# Quiz e avaliações
# ---------------------------------------------------
def fazer_quiz(aluno, modulo, dados, id_trilha):
    questoes = modulo.get('questoes', [])
    if not questoes:
        print("\n⚠️  Este módulo não possui questionário.")
        return

    print(f"\n🧠 Quiz: {modulo['nome']}")
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

    # Se acertou todas as questões (nota 100), marca módulo como concluído
    if nota == 100:
        if modulo['id'] not in aluno['modulos_concluidos'].get(id_trilha, []):
            aluno['modulos_concluidos'].setdefault(id_trilha, []).append(modulo['id'])
            print(f"🎉 Parabéns! Etapa '{modulo['nome']}' concluída com sucesso!")

    # Armazena a nota no perfil do aluno
    aluno.setdefault('notas', {}).setdefault(id_trilha, []).append(nota)

    # Atualiza o aluno na lista e salva tudo
    for i, a in enumerate(dados['aluno']):
        if a['login'] == aluno['login']:
            dados['aluno'][i] = aluno
            break
    salvar_dados(dados)

# ---------------------------------------------------
# Mini-menu de Módulo
# ---------------------------------------------------
def menu_modulo(aluno, modulo, dados, trilha_id):
    while True:
        print(f"\n--- Módulo: {modulo['nome']} ---")
        print("1. Ver Conteúdo")
        print("2. Fazer Quiz")
        print("0. Voltar")
        op = input("Opção: ").strip()
        if op == "1":
            print(f"\nObjetivo: {modulo.get('objetivo','')}")
            print(f"Conteúdo: {modulo.get('conteudo','')}")
            if modulo.get('topicos'):
                print("Tópicos:")
                for t in modulo['topicos']:
                    print(f"  - {t}")
            if modulo.get('desafios'):
                print("Desafios:")
                for d in modulo['desafios']:
                    print(f"  - {d}")
            if modulo.get('projetos'):
                print("Projetos:")
                for p in modulo['projetos']:
                    print(f"  - {p}")
            input("\nPressione Enter para continuar.")
        elif op == "2":
            fazer_quiz(aluno, modulo, dados, trilha_id)
        elif op == "0":
            break
        else:
            print("⚠️  Opção inválida.")

# ---------------------------------------------------
# Aulas / Módulos
# ---------------------------------------------------
def menu_trilhas(aluno, trilha):
    dados = carregar_dados()  # Carrega os dados das trilhas
    
    if not trilha:
        print("⚠️ Trilha não encontrada.")
        return
    
    while True:
        print(f"\n--- {trilha['nome']} ---")
        
        # Exibe os módulos da trilha escolhida
        for m in trilha['modulos']:
            modulos_concluidos = aluno.get('modulos_concluidos', {}).get(trilha['id'], [])
            if m['id'] in modulos_concluidos:
                status = "✅"  # Módulo concluído
            else:
                # Módulo em progresso ou bloqueado
                status = "⏳" if m["id"] == 1 or m["id"] - 1 in modulos_concluidos else "🔒"
            print(f"{m['id']}. {m['nome']} {status}")
        
        print("0. Voltar")
        escolha = input("Escolha o módulo: ").strip()
        
        # Opção para voltar
        if escolha == "0":
            break
        
        # Verificação da escolha
        if escolha.isdigit():
            mid = int(escolha)
            mod = next((x for x in trilha['modulos'] if x['id'] == mid), None)
            if mod:
                if mod['id'] in modulos_concluidos or mod['id'] == 1 or mod['id'] - 1 in modulos_concluidos:
                    menu_modulo(aluno, mod, dados, trilha['id'])  # Chama o menu do módulo escolhido
                else:
                    print("❌ Módulo bloqueado! Complete os anteriores para liberar.")
            else:
                print("⚠️ Módulo inválido.")
        else:
            print("⚠️ Módulo inválido.")


# ---------------------------------------------------
# Menus de Fluxo
# ---------------------------------------------------
def menu_principal(aluno):
    while True:
        dados = carregar_dados()
        ultimo_id_trilha = max(t['id'] for t in dados['trilhas']) # pega o maior ID de trilha (logo, ultima op)
        op_estatisticas = ultimo_id_trilha + 1
        print("\n--- Menu Principal ---")
        
        for trilha in dados['trilhas']:
            print(f"{trilha['id']}. {trilha['nome']}")

        # Exibe as outras opções    
        print(f"{op_estatisticas}. Estatísticas")
        print("0. Sair")

        op = input("Escolha: ").strip()
        
        if op.isdigit():
            op = int(op)
            if op == 0:
                break
            elif op == op_estatisticas:
                mostrar_estatisticas()
            else:
                trilha = next((t for t in dados['trilhas'] if t['id'] == op), None)
                if trilha:
                    menu_trilhas(aluno, trilha)
                else:
                    print("⚠️ Trilha inválida.")
        else:
            print("⚠️  Opção inválida.")

def menu_inicial():
    while True:
        print("\n=== Plataforma Educação Digital Segura ===")
        print("1. Cadastrar")
        print("2. Login")
        print("3. Sair")
        escolha = input("Opção: ").strip()
        if escolha == "1":
            cadastrar_usuario()
        elif escolha == "2":
            aluno = login_usuario()
            if aluno:
                menu_principal(aluno)
        elif escolha == "3":
            break
        else:
            print("⚠️  Inválido. Tente novamente.")

if __name__ == "__main__":
    menu_inicial()
