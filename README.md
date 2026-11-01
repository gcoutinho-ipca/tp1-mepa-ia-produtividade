# O paradoxo da Inteligência Artificial: trabalhar com IA significa trabalhar melhor?

Trabalho Prático 1 — **Modelos Estatísticos para Inteligência Artificial** (MEPA), Mestrado em Inteligência Artificial, IPCA, 2026/2027.

| Aluno | Nº |
|---|---|
| Gilberto Coutinho | 3083 |
| Rúben Mendes | 4563 |

**Questão central:** em que medida a utilização de ferramentas de IA está associada à produtividade dos trabalhadores?

## Conteúdo

- `TP1_MEPA_IA_Produtividade.ipynb` — notebook principal (análise exploratória, testes de hipóteses e modelos de regressão com `statsmodels`). Os outputs estão guardados no ficheiro, por isso o GitHub mostra os gráficos e tabelas sem ser preciso executar.
- `requirements.txt` — dependências para correr localmente.

## Como correr

**No Google Colab:** abrir o notebook diretamente a partir deste repositório (Ficheiro › Abrir notebook › GitHub).

**Localmente (VS Code / Jupyter):**

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
jupyter lab                   # ou abrir a pasta no VS Code
```

O bloco que monta o Google Drive só corre dentro do Colab; fora dele é ignorado.
