from pathlib import Path

from assistente import Assistente
from base_conhecimento import BaseConhecimento


def main():
    pasta_projeto = Path(__file__).resolve().parent
    caminho_json = pasta_projeto / "data" / "base_conhecimento.json"
    pasta_dados = pasta_projeto / "data"

    base = BaseConhecimento(caminho_json)
    base.carregar()

    if not base.orientacoes:
        print("A base de conhecimento está vazia ou não pôde ser carregada.")
        print("Verifique o arquivo data/base_conhecimento.json.")
        return

    assistente = Assistente("Citizen Assist AI", base, pasta_dados)
    assistente.executar()


if __name__ == "__main__":
    main()
