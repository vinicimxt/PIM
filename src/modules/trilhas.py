from modules.utils import carregar_json, TRILHAS_FILE, carregar_modulos, carregar_conteudo, carregar_questoes, snake_case
from modules.usuario import carregar_dados_usuario, salvar_dados_usuario
import os

def carregar_trilhas():
    if not os.path.exists(TRILHAS_FILE):
        print("⚠️ Arquivo trilhas.json não encontrado na pasta /data.")
        return []
    return carregar_json(TRILHAS_FILE)

def fazer_quiz(aluno, questoes, id_trilha, id_modulo):
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
    conteudo_lista = carregar_conteudo()
    
    descricao = "Sem descrição disponível."
    for trilha_conteudo in conteudo_lista:
        if trilha_conteudo.get("id_trilha") == id_trilha:
            chave = f"descricao_modulo_{modulo['id_modulo']}"
            descricao = trilha_conteudo.get(chave, descricao)
            break
    
    questoes = carregar_questoes(trilha_snake, modulo['id_modulo'])

    while True:
        print(f"\n--- Módulo: {modulo['nome']} ---")
        print("1. Ver Conteúdo")
        print("2. Fazer Quiz")
        print("0. Voltar")
        op = input("Opção: ").strip()

        if op == "1":
            print(f"\n📚 Conteúdo: {descricao}")
            input("\nPressione Enter para continuar.")
        elif op == "2":
            fazer_quiz(aluno, questoes, id_trilha, modulo['id_modulo'])
        elif op == "0":
            break
        else:
            print("⚠️ Opção inválida.")

def menu_trilhas(aluno):
    trilhas = carregar_trilhas()
    
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