from modules.utils import carregar_json, salvar_json, criptografar_senha, DADOS_FILE

def carregar_dados_usuario():
    return carregar_json(DADOS_FILE)

def salvar_dados_usuario(dados):
    salvar_json(DADOS_FILE, dados)
    
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