import os
import platform
import subprocess
import webbrowser

def abrir_link(caminho_relativo):
    caminho_completo = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", caminho_relativo))

    # Debug
    print(f"[DEBUG] Caminho final esperado: {caminho_completo}")

    if not os.path.exists(caminho_completo):
        print(f"Arquivo não encontrado: {caminho_completo}")
        print("Tentando abrir como link no navegador...")
        webbrowser.open(caminho_relativo)
        return

    sistema = platform.system()
    if sistema == "Darwin":
        subprocess.run(["open", caminho_completo])
    elif sistema == "Linux":
        subprocess.run(["xdg-open", caminho_completo])
    elif sistema == "Windows":
        subprocess.run(["start", caminho_completo], shell=True)
    else:
        print(f"Sistema {sistema} não suportado. Tentando abrir como link.")
        webbrowser.open(caminho_relativo)

abrir_link("assets/pdf/fundamentos_de_python/fundamentos_de_python_modulo_1.pdf")