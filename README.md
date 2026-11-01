# O paradoxo da Inteligência Artificial: trabalhar com IA significa trabalhar melhor?

Trabalho Prático 1 — **Modelos Estatísticos para Inteligência Artificial** (MEPA), Mestrado em Inteligência Artificial, IPCA, 2026/2027. Docente: Liliana Coelho.

| Aluno | Nº |
|---|---|
| Gilberto Coutinho | 3083 |
| Rúbem Mendes | 4563 |

**Questão central:** em que medida a utilização de ferramentas de IA está associada à produtividade dos colaboradores, e como se altera essa relação quando se consideram outros fatores individuais e profissionais?

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/gcoutinho-ipca/tp1-mepa-ia-produtividade/blob/main/TP1_MEPA_IA_Produtividade.ipynb)

## Conteúdo

| Ficheiro | O que é |
|---|---|
| `TP1_MEPA_IA_Produtividade.ipynb` | Notebook principal: preparação dos dados, análise descritiva, correlação, ANOVA, intervalo de confiança, regressão simples e múltipla, conclusões. As secções 1 a 7 seguem a numeração do enunciado. Os outputs estão guardados, por isso o GitHub mostra gráficos e tabelas sem ser preciso executar. |
| `Relatorio_TP1_MEPA_IA_Produtividade.docx` | Relatório de investigação, gerado por `scripts_geracao/build_report.py` a partir dos textos e das figuras. |
| `Base_Dados_IA_Produtividade.xlsx` | Base de dados (sintética) fornecida com o enunciado. |
| `Trabalho Final.pdf` | Enunciado do trabalho prático. |
| `CONFORMIDADE.md` | Verificação ponto a ponto do cumprimento do enunciado e o que não é possível cumprir nos ficheiros, com os motivos. |
| `scripts_geracao/build_nb.py` | Gerou a primeira versão do notebook. É histórico: não voltar a correr, porque sobreporia as edições feitas depois no Colab. |
| `scripts_geracao/build_report.py` | Gera o relatório `.docx` (precisa das figuras em `figuras/`, produzidas ao executar o notebook). |
| `requirements.txt` | Dependências para correr localmente. |
| `figuras/` | Criada pelo notebook ao executar. Ignorada pelo git, porque os gráficos já estão embebidos no notebook. |

## Como trabalhar

O GitHub é a versão de referência do notebook. Os dados estão também na pasta partilhada do Google Drive `MEPA_TP1`, que os dois elementos do grupo têm como atalho em «O meu disco».

### No Google Colab

1. **Ficheiro › Abrir notebook › separador GitHub**. Autorizar o acesso ao GitHub com a opção de incluir repositórios privados e escolher este repositório e o notebook. O botão «Abrir no Colab» acima faz o mesmo.
2. **Ambiente de execução › Executar tudo**. O notebook monta o Google Drive e lê os dados da pasta `MEPA_TP1`.
3. **Ficheiro › Guardar uma cópia no GitHub**, no repositório `gcoutinho-ipca/tp1-mepa-ia-produtividade` e ramo `main`, com uma mensagem curta a descrever a alteração.
4. Antes de editar, abrir sempre a versão mais recente a partir do GitHub, e combinar quem está a editar o notebook em cada momento, porque o Colab grava o ficheiro inteiro e sobreporia alterações feitas em paralelo.

### Localmente (VS Code / Jupyter)

```bash
git clone https://github.com/gcoutinho-ipca/tp1-mepa-ia-produtividade.git
cd tp1-mepa-ia-produtividade
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
jupyter lab                   # ou abrir a pasta no VS Code
```

O bloco que monta o Google Drive só corre dentro do Colab. Fora dele, o notebook lê `Base_Dados_IA_Produtividade.xlsx` da pasta atual, onde o ficheiro também está versionado.

Executar tudo de novo sem abrir o Jupyter, e regenerar o relatório a seguir:

```bash
python -m nbconvert --to notebook --execute --inplace TP1_MEPA_IA_Produtividade.ipynb
python scripts_geracao/build_report.py .
```
