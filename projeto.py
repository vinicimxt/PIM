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
        "modulos_concluidos": [],
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
def fazer_quiz(aluno, modulo, dados):
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
        if modulo['id'] not in aluno['modulos_concluidos']:
            aluno['modulos_concluidos'].append(modulo['id'])
            print(f"🎉 Parabéns! Etapa '{modulo['nome']}' concluída com sucesso!")

    # Armazena a nota no perfil do aluno
    aluno.setdefault('notas', {})[modulo['id']] = nota

    # Atualiza o aluno na lista e salva tudo
    for i, a in enumerate(dados['aluno']):
        if a['login'] == aluno['login']:
            dados['aluno'][i] = aluno
            break
    salvar_dados(dados)

# ---------------------------------------------------
# Mini-menu de Módulo
# ---------------------------------------------------
def menu_modulo(aluno, modulo, dados):
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
            fazer_quiz(aluno, modulo, dados)
        elif op == "0":
            break
        else:
            print("⚠️  Opção inválida.")

# ---------------------------------------------------
# Aulas / Módulos
# ---------------------------------------------------
def aulas_programacao(aluno):
    dados = carregar_dados()
    trilha = dados['trilhas'][aluno['trilha_atual'] - 1]
    while True:
        print(f"\n--- {trilha['nome']} ---")
        for m in trilha['modulos']:
            if m['id'] in aluno.get('modulos_concluidos', []):
                status = "✅"
            else:
                status = "⏳" if m["id"] == 1 or m["id"] - 1 in aluno.get('modulos_concluidos', []) else "🔒"
            print(f"{m['id']}. {m['nome']} {status}")
        print("0. Voltar")
        escolha = input("Escolha o módulo: ").strip()
        if escolha == "0":
            break
        if escolha.isdigit():
            mid = int(escolha)
            mod = next((x for x in trilha['modulos'] if x['id']==mid), None)
            if mod:
                if mod['id'] in aluno.get('modulos_concluidos', []) or mod['id'] == 1 or mod['id'] - 1 in aluno.get('modulos_concluidos', []):
                    menu_modulo(aluno, mod, dados)
                else:
                    print("❌ Módulo bloqueado! Complete os anteriores para liberar.")
                continue
        print("⚠️  Módulo inválido.")

def simulacao_robotica(aluno):
    print("\n--- Simulação de Projetos de Robótica ---")
    print("""
1. Conecte um LED ao pino GPIO 17 (resistor 220Ω).
2. Código exemplo com RPi.GPIO:
   import RPi.GPIO as GPIO
   import time
   GPIO.setmode(GPIO.BCM)
   GPIO.setup(17, GPIO.OUT)
   try:
       while True:
           GPIO.output(17, GPIO.HIGH)
           time.sleep(1)
           GPIO.output(17, GPIO.LOW)
           time.sleep(1)
   except KeyboardInterrupt:
       GPIO.cleanup()
""")
    input("Pressione Enter para voltar ao menu.")

def dicas_seguranca():
    print("\n--- Dicas de Segurança Digital ---")
    print("""
1. Nunca compartilhe sua senha.
2. Use autenticação de dois fatores.
3. Desconfie de links suspeitos.
4. Faça backups regulares.
5. Mantenha sistemas e antivírus atualizados.
""")
    input("Pressione Enter para voltar ao menu.")

# ---------------------------------------------------
# Menus de Fluxo
# ---------------------------------------------------
def menu_principal(aluno):
    while True:
        print("\n--- Menu Principal ---")
        print("1. Aulas de Programação Básica")
        print("2. Simulação Robótica")
        print("3. Dicas de Segurança")
        print("4. Estatísticas")
        print("5. Sair")
        op = input("Escolha: ").strip()
        if op == "1":
            aulas_programacao(aluno)
        elif op == "2":
            simulacao_robotica(aluno)
        elif op == "3":
            dicas_seguranca()
        elif op == "4":
            mostrar_estatisticas()
        elif op == "5":
            break
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
