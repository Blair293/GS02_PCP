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
- Código: P1
- Data: 13/11/2026
- Tarefa: Perguntar como economizar energia com LED.
- Concluiu? Sim.
- Dificuldade observada: Não apresentou dificuldades.
- Comentário: Achou interessante descobrir quanto poderia economizar substituindo lâmpadas antigas por LED.
- Ajuste realizado: Nenhum ajuste necessário.
---
- Código: P2
- Data: 13/11/2026
- Tarefa: Consultar a comparação entre LED e energia solar.
- Concluiu? Parcialmente.
- Dificuldade observada: Teve dificuldade para entender o tempo de retorno do investimento.
- Comentário: Gostaria de uma explicação mais simples sobre o retorno financeiro.
- Ajuste realizado: Adicionar uma explicação sobre o tempo necessário para recuperar o investimento.
---
- Código: P3
- Data: 18/11/2026
- Tarefa: Perguntar ao assistente qual alternativa é mais econômica entre lâmpadas LED e energia solar.
- Concluiu? Sim.
- Dificuldade observada: Teve um pouco de dificuldade para compreender os custos iniciais da instalação de energia solar.
- Comentário: Considerou as informações úteis e conseguiu entender que a substituição por lâmpadas LED exige um investimento menor e pode gerar economia na conta de luz.
- Ajuste realizado: Melhorar a explicação sobre os custos iniciais e as vantagens de cada alternativa.

## Integrantes
- Victor Hugo Lavaqui - RM: 573838