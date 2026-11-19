class Orientacao:
    """Representa uma orientação da base de conhecimento."""

    def __init__(
        self, id, categoria, titulo, palavras_chave, resposta,
        documentos, onde, fonte, verificado_em
    ):
        self.id = id
        self.categoria = categoria
        self.titulo = titulo
        self.palavras_chave = palavras_chave
        self.resposta = resposta
        self.documentos = documentos
        self.onde = onde
        self.fonte = fonte
        self.verificado_em = verificado_em

    def exibir(self):
        """Exibe a orientação completa no terminal."""
        print(f"\n>> {self.titulo} [{self.categoria}]")
        print(self.resposta)

        print("\nDocumentos/informações que podem ser necessários:")
        if self.documentos:
            for documento in self.documentos:
                print(f"  - {documento}")
        else:
            print("  - Consulte a fonte oficial para confirmar.")

        print(f"\nOnde: {self.onde}")
        print(f"Fonte: {self.fonte} (data informada na base: {self.verificado_em})")
        print("Aviso: este assistente NÃO é um canal oficial.")
