from modules.usuario import carregar_dados_usuario
from modules.trilhas import carregar_trilhas

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
