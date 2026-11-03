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
| `GUIAO_DEFESA.md` | Apoio à defesa oral: mensagem principal, diagrama de fluxo do notebook, porque se escolheu cada teste, números a saber e respostas curtas às perguntas prováveis. |
| `Apresentacao_TP1_MEPA.pptx` | Apresentação para a defesa: porque se escolheu cada método em cada fase, incluindo o tratamento dos valores em falta. Gerada por `scripts_geracao/build_slides.py` com as figuras do notebook. |
| `DISCUSSAO_METODOS.md` | Comparação entre os métodos usados e os dados nas aulas, divergências com o notebook do Rúbem e decisões tomadas. |
| `MEIA_G01.ipynb`, `MEIA_G01_Apresentacao.pptx` | Versões de trabalho do Rúbem, guardadas como referência. Não são a entrega. |
| `scripts_geracao/build_nb.py` | Gerou a primeira versão do notebook. É histórico: não voltar a correr, porque sobreporia as edições feitas depois no Colab. |
| `scripts_geracao/build_report.py` | Gera o relatório `.docx` (precisa das figuras em `figuras/`, produzidas ao executar o notebook). |
| `scripts_geracao/build_slides.py` | Gera a apresentação `.pptx` (também precisa das figuras em `figuras/`). |
| `requirements.txt` | Dependências para correr localmente. |
| `figuras/` | Criada pelo notebook ao executar. Ignorada pelo git, porque os gráficos já estão embebidos no notebook. |

## Como trabalhar

O repositório é público e é a versão de referência do notebook e dos dados. O notebook vai buscar `Base_Dados_IA_Produtividade.xlsx` diretamente ao repositório, por isso corre em qualquer conta Google (incluindo a da docente) sem montar o Drive.

### No Google Colab

1. Clicar no botão «Abrir no Colab» acima, ou **Ficheiro › Abrir notebook › separador GitHub** e escolher este repositório e o notebook.
2. **Ambiente de execução › Executar tudo**. A primeira célula de código descarrega os dados do repositório.

Para guardar alterações (só os elementos do grupo, que têm de ser colaboradores do repositório):

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

Localmente, o notebook usa o `Base_Dados_IA_Produtividade.xlsx` que já está no clone e não o descarrega.

### Fluxo de trabalho do grupo

1. `git pull` antes de começar, para trazer o que o colega guardou a partir do Colab.
2. Editar e executar localmente (ou no Colab).
3. `git commit` e `git push`: o link do Colab passa logo a abrir a nova versão.
4. Uma pessoa de cada vez no notebook, porque um `.ipynb` editado em paralelo não se funde bem.

Executar tudo de novo sem abrir o Jupyter, e regenerar o relatório a seguir:

```bash
python -m nbconvert --to notebook --execute --inplace TP1_MEPA_IA_Produtividade.ipynb
python scripts_geracao/build_report.py .
python scripts_geracao/build_slides.py .
```
