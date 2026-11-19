# Citizen Assist AI

Assistente de orientação ao cidadão executado no terminal.

## Público e tema
Projeto de exemplo direcionado a jovens em busca do primeiro emprego, com orientações sobre documentos, trabalho e qualificação profissional.

## Como executar
É necessário ter Python 3 instalado. Não são necessárias bibliotecas externas.

```bash
python main.py
```

## Estrutura
- `main.py`: inicializa o sistema.
- `orientacao.py`: classe Orientacao.
- `base_conhecimento.py`: carrega JSON, normaliza e pontua perguntas.
- `assistente.py`: atendimento, navegação, histórico, indicadores e CSV.
- `data/base_conhecimento.json`: base com 10 orientações de exemplo.
- `data/historico.json`: histórico persistente.
- `data/atendimentos.csv`: exportação dos atendimentos.

## Regra de pontuação
- +3 pontos por palavra-chave encontrada na pergunta.
- +1 ponto por palavra da pergunta com 4 ou mais letras encontrada no título.
- 6 pontos ou mais: confiança ALTA.
- 3 a 5 pontos: confiança MÉDIA.
- Menos de 3 pontos: orientação não encontrada.

## Teste com usuários
Preencher após testar com pelo menos 3 pessoas de fora da equipe e somar 10 ou mais atendimentos. Não registrar nomes nem dados pessoais.

## Integrantes
- Victor Hugo Lavaqui - RM: 573838