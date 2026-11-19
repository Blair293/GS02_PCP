import json
import unicodedata
from pathlib import Path

from orientacao import Orientacao


class BaseConhecimento:
    """Carrega, organiza e pesquisa as orientações cadastradas em JSON."""

    def __init__(self, caminho):
        self.caminho = Path(caminho)
        self.orientacoes = []

    @staticmethod
    def normalizar(texto):
        """Remove acentos e pontuação e converte o texto para minúsculas."""
        texto = str(texto).lower().strip()
        texto = unicodedata.normalize("NFD", texto)
        texto = "".join(
            caractere for caractere in texto
            if unicodedata.category(caractere) != "Mn"
        )

        for sinal in "?!.,;:()[]{}'\"":
            texto = texto.replace(sinal, " ")

        return " " + " ".join(texto.split()) + " "

    def carregar(self):
        """Lê o arquivo JSON e transforma cada registro em um objeto Orientacao."""
        try:
            if not self.caminho.exists():
                print(f"Aviso: arquivo não encontrado: {self.caminho}")
                self.orientacoes = []
                return False

            with self.caminho.open("r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

            if not isinstance(dados, list):
                raise ValueError("O JSON deve conter uma lista de orientações.")

            orientacoes_carregadas = []
            campos_obrigatorios = {
                "id", "categoria", "titulo", "palavras_chave", "resposta",
                "documentos", "onde", "fonte", "verificado_em"
            }

            for indice, item in enumerate(dados, start=1):
                if not isinstance(item, dict):
                    raise ValueError(f"Registro {indice} não é um objeto JSON.")

                faltantes = campos_obrigatorios - item.keys()
                if faltantes:
                    raise ValueError(
                        f"Registro {indice} sem os campos: {', '.join(sorted(faltantes))}"
                    )

                if len(item["palavras_chave"]) < 3:
                    raise ValueError(
                        f"A orientação {item['id']} precisa de pelo menos 3 palavras-chave."
                    )

                orientacoes_carregadas.append(Orientacao(**item))

            self.orientacoes = orientacoes_carregadas
            return True

        except (json.JSONDecodeError, OSError, TypeError, ValueError) as erro:
            print(f"Não foi possível carregar a base de conhecimento: {erro}")
            self.orientacoes = []
            return False

    def categorias(self):
        """Retorna as categorias sem repetição, em ordem alfabética."""
        return sorted({orientacao.categoria for orientacao in self.orientacoes})

    def por_categoria(self, categoria):
        """Retorna as orientações pertencentes à categoria escolhida."""
        return [
            orientacao for orientacao in self.orientacoes
            if self.normalizar(orientacao.categoria) == self.normalizar(categoria)
        ]

    def pontuar(self, pergunta, orientacao):
        """
        Calcula a pontuação:
        +3 para cada palavra-chave encontrada na pergunta;
        +1 para cada palavra da pergunta (4 ou mais letras) encontrada no título.
        """
        pergunta_normalizada = self.normalizar(pergunta)
        titulo_normalizado = self.normalizar(orientacao.titulo)

        pontos = 0

        for palavra_chave in orientacao.palavras_chave:
            chave_normalizada = self.normalizar(palavra_chave).strip()
            if chave_normalizada and f" {chave_normalizada} " in pergunta_normalizada:
                pontos += 3

        palavras_pergunta = set(pergunta_normalizada.split())
        palavras_titulo = set(titulo_normalizado.split())

        for palavra in palavras_pergunta:
            if len(palavra) >= 4 and palavra in palavras_titulo:
                pontos += 1

        return pontos

    def buscar(self, pergunta):
        """Devolve tuplas (pontos, orientação), da maior para a menor pontuação."""
        resultados = [
            (self.pontuar(pergunta, orientacao), orientacao)
            for orientacao in self.orientacoes
        ]
        resultados.sort(key=lambda item: item[0], reverse=True)
        return resultados
