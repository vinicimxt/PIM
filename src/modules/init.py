from modules.trilhas import menu_trilhas
from modules.estatisticas import mostrar_estatisticas
from modules.usuario import cadastrar_usuario, login_usuario

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