import csv
import json
import re
import time
from datetime import datetime
from pathlib import Path


class Assistente:
    """Conduz o atendimento, registra o histórico e calcula indicadores."""

    AVISO = "este assistente não é um canal oficial"

    def __init__(self, nome, base, pasta_dados="data"):
        self.nome = nome
        self.base = base
        self.pasta_dados = Path(pasta_dados)
        self.pasta_dados.mkdir(parents=True, exist_ok=True)
        self.caminho_historico = self.pasta_dados / "historico.json"
        self.caminho_csv = self.pasta_dados / "atendimentos.csv"
        self.historico = self._carregar_historico()
        self.facilidades = []

    def _carregar_historico(self):
        """Carrega o histórico anterior; se estiver ausente ou inválido, inicia vazio."""
        if not self.caminho_historico.exists():
            return []

        try:
            with self.caminho_historico.open("r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            return dados if isinstance(dados, list) else []
        except (json.JSONDecodeError, OSError):
            print("Aviso: histórico ausente ou corrompido. Um novo será criado.")
            return []

    @staticmethod
    def _contem_dado_pessoal(texto):
        """Bloqueia entradas com arroba ou sequência de 8 ou mais dígitos."""
        return "@" in texto or re.search(r"\d{8,}", texto) is not None

    @staticmethod
    def _ler_sim_nao(mensagem):
        while True:
            resposta = input(mensagem).strip().lower()
            if resposta in ("s", "sim"):
                return True
            if resposta in ("n", "nao", "não"):
                return False
            print("Entrada inválida. Digite s para sim ou n para não.")

    @staticmethod
    def _ler_opcao(mensagem, minimo, maximo):
        while True:
            entrada = input(mensagem).strip()
            if entrada == "0":
                return 0
            try:
                opcao = int(entrada)
                if minimo <= opcao <= maximo:
                    return opcao
            except ValueError:
                pass
            print(f"Opção inválida. Digite um número entre {minimo} e {maximo}, ou 0 para voltar.")

    def registrar(self, origem, pergunta, id_orientacao, encontrou,
                  ajudou, tentativas, tempo):
        registro = {
            "data": datetime.now().isoformat(timespec="seconds"),
            "origem": origem,
            "pergunta": pergunta,
            "id_orientacao": id_orientacao,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": tentativas,
            "tempo_segundos": tempo
        }
        self.historico.append(registro)
        self._salvar_historico()

    def _salvar_historico(self):
        try:
            with self.caminho_historico.open("w", encoding="utf-8") as arquivo:
                json.dump(self.historico, arquivo, ensure_ascii=False, indent=4)
        except OSError as erro:
            print(f"Não foi possível salvar o histórico: {erro}")

    def exportar_csv(self):
        """Exporta todos os atendimentos para data/atendimentos.csv."""
        campos = [
            "data", "origem", "pergunta", "id_orientacao", "encontrou",
            "ajudou", "tentativas", "tempo_segundos"
        ]
        try:
            with self.caminho_csv.open("w", newline="", encoding="utf-8-sig") as arquivo:
                escritor = csv.DictWriter(arquivo, fieldnames=campos)
                escritor.writeheader()
                escritor.writerows(self.historico)
            print(f"Atendimentos exportados para: {self.caminho_csv}")
        except OSError as erro:
            print(f"Erro ao exportar CSV: {erro}")

    def indicadores(self):
        """Calcula e apresenta os indicadores do histórico."""
        total = len(self.historico)
        if total == 0:
            print("\nAinda não há atendimentos registrados.")
            return

        encontrados = sum(1 for item in self.historico if item["encontrou"])
        ajudaram = sum(1 for item in self.historico if item["ajudou"] is True)
        tempo_medio = sum(item["tempo_segundos"] for item in self.historico) / total
        tentativas_media = sum(item["tentativas"] for item in self.historico) / total

        respondidos = [item for item in self.historico if item["ajudou"] is not None]
        taxa_acerto = (
            100 * sum(1 for item in respondidos if item["ajudou"]) / len(respondidos)
            if respondidos else 0
        )

        print("\n========== INDICADORES ==========")
        print(f"Total de atendimentos: {total}")
        print(f"Resposta encontrada: {encontrados / total * 100:.1f}%")
        print(f"Taxa de acerto (ajudou): {taxa_acerto:.1f}%")
        print(f"Tempo médio para encontrar: {tempo_medio:.1f} segundos")
        print(f"Tentativas por atendimento: {tentativas_media:.1f}")
        if self.facilidades:
            media_facilidade = sum(self.facilidades) / len(self.facilidades)
            print(f"Facilidade de uso (1 a 5): {media_facilidade:.1f}")
        else:
            print("Facilidade de uso: ainda sem avaliações nesta execução.")

        sem_solucao = [
            item for item in self.historico
            if not item["encontrou"] or item["ajudou"] is False
        ]
        print("\nDúvidas sem solução:")
        if sem_solucao:
            for item in sem_solucao:
                print(f"  - {item['pergunta']}")
        else:
            print("  Nenhuma registrada.")

    def perguntar(self):
        """Recebe uma pergunta livre e apresenta a melhor orientação encontrada."""
        inicio = time.time()
        tentativas = 0

        while True:
            pergunta = input("\nDigite sua dúvida (0 para voltar): ").strip()

            if pergunta == "0":
                return

            if not pergunta:
                print("A pergunta não pode ficar vazia.")
                continue

            if self._contem_dado_pessoal(pergunta):
                print("Atenção: não digite CPF, telefone, e-mail ou outros dados pessoais. Reescreva.")
                continue

            tentativas += 1
            resultados = self.base.buscar(pergunta)

            if not resultados or resultados[0][0] < 3:
                print("\nNão encontrei uma orientação com confiança suficiente.")
                print("Tente usar outras palavras ou navegar pelas categorias.")
                if resultados:
                    alternativas = [item for item in resultados if item[0] > 0][:2]
                    if alternativas:
                        print("\nTalvez você esteja procurando por:")
                        for pontos, orientacao in alternativas:
                            print(f"  - {orientacao.titulo} ({pontos} pontos)")
                self.registrar(
                    "pergunta", pergunta, None, False, None,
                    tentativas, round(time.time() - inicio, 1)
                )
                continue

            pontos, orientacao = resultados[0]
            if pontos >= 6:
                confianca = "ALTA"
            else:
                confianca = "MÉDIA"

            print(f"\nConfiança da resposta: {confianca} ({pontos} pontos)")
            orientacao.exibir()

            alternativas = [item for item in resultados[1:3] if item[0] >= 3]
            if alternativas:
                print("\nOutras orientações relacionadas:")
                for pontos_alt, orientacao_alt in alternativas:
                    print(f"  - {orientacao_alt.titulo} ({pontos_alt} pontos)")

            ajudou = self._ler_sim_nao("\nEssa orientação respondeu sua dúvida? (s/n): ")
            self.registrar(
                "pergunta", pergunta, orientacao.id, True, ajudou,
                tentativas, round(time.time() - inicio, 1)
            )
            return

    def navegar(self):
        """Permite escolher uma categoria e consultar suas orientações."""
        categorias = self.base.categorias()
        if not categorias:
            print("Não há categorias disponíveis.")
            return

        while True:
            print("\n========== CATEGORIAS ==========")
            for indice, categoria in enumerate(categorias, start=1):
                print(f"{indice}. {categoria}")
            print("0. Voltar")

            opcao = self._ler_opcao("Escolha uma categoria: ", 1, len(categorias))
            if opcao == 0:
                return

            categoria = categorias[opcao - 1]
            orientacoes = self.base.por_categoria(categoria)

            while True:
                print(f"\n--- {categoria} ---")
                for indice, orientacao in enumerate(orientacoes, start=1):
                    print(f"{indice}. {orientacao.titulo}")
                print("0. Voltar")

                escolha = self._ler_opcao("Escolha uma orientação: ", 1, len(orientacoes))
                if escolha == 0:
                    break

                inicio = time.time()
                orientacao = orientacoes[escolha - 1]
                orientacao.exibir()
                ajudou = self._ler_sim_nao("\nEssa orientação respondeu sua dúvida? (s/n): ")
                self.registrar(
                    "categoria", orientacao.titulo, orientacao.id, True, ajudou,
                    1, round(time.time() - inicio, 1)
                )

    def avaliar_facilidade(self):
        """Solicita uma nota de facilidade entre 1 e 5."""
        while True:
            entrada = input("\nDe 1 a 5, quão fácil foi usar o assistente? (0 para pular): ").strip()
            if entrada == "0":
                return
            try:
                nota = int(entrada)
                if 1 <= nota <= 5:
                    self.facilidades.append(nota)
                    return
            except ValueError:
                pass
            print("Nota inválida. Digite um número de 1 a 5 ou 0 para pular.")

    def executar(self):
        """Exibe o menu principal até o usuário escolher sair."""
        print(f"\n===== {self.nome} =====")
        print("Orientações para jovens em busca do primeiro emprego.")
        print("Não informe dados pessoais durante o atendimento.")

        while True:
            print("\n1. Fazer uma pergunta")
            print("2. Navegar por categorias")
            print("3. Ver indicadores")
            print("0. Sair")

            opcao = self._ler_opcao("Escolha uma opção: ", 1, 3)

            if opcao == 0:
                break
            elif opcao == 1:
                self.perguntar()
            elif opcao == 2:
                self.navegar()
            elif opcao == 3:
                self.indicadores()

        self.avaliar_facilidade()
        self.indicadores()
        self.exportar_csv()
        print("\nObrigado por utilizar o Citizen Assist AI!")
