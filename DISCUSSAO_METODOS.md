# Discussão: métodos das aulas e divergências entre os dois notebooks

> **Estado (03/11/2026): decisões aplicadas** ao notebook, ao relatório, ao guião e à nova apresentação (`Apresentacao_TP1_MEPA.pptx`). Saíram: assimetria e curtose como números, coeficientes padronizados, AIC/BIC, validação cruzada, HC3 e bootstrap. Ficaram (a regressão foi dada em aula): as versões da regressão com departamento e complexidade como categorias e o teste da interação IA × experiência. Entraram: a leitura do dicionário do Excel, a avaliação dos registos com falhas (bloco 1.6b), a escala de correlação e os limiares de η² da docente e o teste F parcial com `compare_f_test`.

Documento para o Gilberto e o Rúbem decidirem em conjunto. Regra combinada: **só métodos dados pela docente** e um trabalho fácil de defender.

Fontes lidas (pasta `MEPA - docs apoio`): os 5 PDFs das aulas e a aula extra das classes, os guiões de código das aulas 1 a 8, o teste de preparação e os 28 infográficos. Comparação feita com `TP1_MEPA_IA_Produtividade.ipynb` (o nosso) e `MEIA_G01.ipynb` (do Rúbem, entretanto retirado do repositório).

## 1. O que a docente deu (e onde)

| Método | Dado em aula? | Onde |
|---|---|---|
| Descritivas, AIQ, histograma, caixa de bigodes | Sim | Aulas 1 e 2, teste de preparação |
| Assimetria e curtose **como números** | **Não** (só a leitura visual da assimetria) | Aula 1 p25–27 |
| Gráfico Q-Q, Shapiro-Wilk | Sim | Aulas 4 e 5, guião 3 bloco 13, infográfico «Testes de normalidade» |
| Levene (com mediana) | Sim | Guião 3 bloco 13, aula 8, infográfico «Levene» |
| ANOVA a um fator | Sim | Aula 3 p28–33, aula 8 |
| ANOVA de Welch | Sim | Aula 8 P8, infográfico «ANOVA de Welch» |
| Kruskal-Wallis | Sim | Infográfico «Kruskal–Wallis» (não está nos PDFs) |
| Eta quadrado (com limiares 0,01 / 0,06 / 0,14) | Sim | Aula 8 P6 e P10, infográfico «Guia de Inferência» |
| Tukey (só depois de rejeitar H0) | Sim | Guião 3 bloco 13, aula 8 P9 |
| Pearson, Spearman | Sim | Aula 2, infográficos (escala: 0,2–0,4 fraca) |
| IC para a média com t | Sim | Aula 3 p9 |
| Regressão simples e múltipla, R², R² ajustado, teste F global | Sim | Aulas 4 e 5 |
| IC da média vs intervalo de previsão | Sim | Aula 4 p35–38 |
| Teste F parcial (modelos encaixados) | Sim, com `compare_f_test` | Aula 4 p81 |
| VIF (limiar 5 como regra prática) | Sim | Aula 4 p82–86, aula 5 p25–32 |
| Breusch-Pagan, resíduos vs ajustados | Sim | Aula 4 p48–50, aula 5 p47–48 |
| Durbin-Watson | Sim, **mas a docente diz que sem ordem temporal é só descritivo** | Aula 4 p54–55, aula 5 p49 |
| Distância de Cook (referência 4/n) | Sim | Guião 5 bloco 10 |
| Treino/teste, RMSE | Sim (regressão linear) | Guião 5 bloco 12 |
| Validação cruzada | Só na regressão logística | Aula 7 P15 |
| AIC | Só impresso na logística, sem comparar modelos | Aula 6, aula 7 |
| Variáveis categóricas `C()` e interação | Só na ANOVA, **nunca numa regressão** | Aula 8 |
| **Coeficientes padronizados** | **Não** | — |
| **BIC, bootstrap, erros-padrão robustos HC3** | **Não** | — |
| Teste RESET, Lilliefors, Holm/Bonferroni par a par, ómega², permutações, k-means | Não (ou só mencionado) | — |

## 2. O que o nosso notebook usa e não foi dado

Proposta: retirar tudo isto. Nenhuma conclusão muda, porque todos estes resultados confirmavam os clássicos.

| Bloco | O que retirar | Substituir por |
|---|---|---|
| 2.4 | Coeficientes de assimetria (−0,61) e curtose (0,96) | Leitura visual do histograma, da caixa e do Q-Q (como na aula 1) |
| 6.3 | Coeficientes padronizados («a experiência pesa 10× mais») | Dizer que a experiência é a única variável significativa e que não se comparam coeficientes com unidades diferentes (aula 5 p22) |
| 6.5b | AIC, BIC e validação cruzada | Nada: R² ajustado + teste F parcial chegam (aula 4) |
| 6.6b | Modelo com departamento e complexidade categórica (usam `C()` numa regressão) e o termo de interação IA × experiência | Fica só «M2 sem C097» como análise de sensibilidade |
| 6.6c | Erros-padrão HC3 e bootstrap | Nada |
| 6.5a | `anova_lm` para o F parcial | `m2.compare_f_test(m1_233)`, a função usada na aula 4 p81 (mesmo resultado) |

**Acrescentar** (dá jeito na defesa porque é a linguagem da docente):
- 3.3: classificar r = 0,24 com a escala do infográfico de Pearson (0,2–0,4 = fraca).
- 4.4: η² = 0,006 é inferior a 0,01, o limiar de efeito «pequeno» do Guia de Inferência, logo é um efeito desprezável.
- 5.6 e 6.6: Cook com a referência 4/n da aula 5 (já calculado).

**Corrigir (erro factual):** o relatório e o notebook dizem que a produtividade é «provavelmente composta» por tarefas, tempo e qualidade. A folha `Dicionario` do Excel diz o contrário: é uma «avaliação global padronizada por avaliadores, **NÃO calculada diretamente das colunas anteriores**». A exclusão dessas variáveis continua certa, mas pela razão que o próprio dicionário dá: «são indicadores contemporâneos do desempenho; discutir possível redundância».

## 3. Divergências entre os dois notebooks

| # | Tema | Nosso notebook | Notebook do Rúbem | Proposta |
|---|---|---|---|---|
| 1 | Modelo múltiplo principal | IA + experiência + formação + complexidade (4 variáveis, b_IA = 0,129) | Acrescenta carga de trabalho e departamento com `C()` (8 termos, b_IA = 0,144) | **O nosso**: o departamento como `C()` numa regressão não foi dado; a ANOVA já mostrou que o departamento não explica a produtividade |
| 2 | Teste principal entre departamentos | ANOVA clássica, com Welch e Kruskal-Wallis a confirmar | Welch principal | **ANOVA clássica**: é o que o fluxograma da docente manda quando o Levene não rejeita (p = 0,52). Welch e Kruskal-Wallis ficam como confirmação (ambos dados) |
| 3 | Inferência nas regressões | Erros-padrão clássicos | HC3 como principal | **Clássicos**: HC3 não foi dado |
| 4 | Força da correlação | «Fraca», com convenção | «Não usamos fronteiras universais» | **Classificar**: o enunciado pede (3.3) e a docente dá a escala no infográfico |
| 5 | Pergunta 7.3 | «Resultado mais inesperado» | «Saliente, sem inventar uma surpresa» | **Responder ao que o enunciado pergunta**: o mais inesperado |
| 6 | Sensibilidade a atípicos | Repetir sem C097 | Retira as 9 observações assinaladas por Cook | **Só C097**: a docente diz que Cook assinala para investigar, não para eliminar |
| 7 | Exercícios extra (secções 11–16 e blocos A–P) | Não tem | t a uma amostra, dois grupos, proporções, qui-quadrado, Fisher, multinomial, k-means, permutações, Holm, Lilliefors, RESET | **Fora da entrega**: o enunciado não os pede e cada um é mais uma pergunta possível na defesa. Podem ficar num ficheiro de estudo à parte |
| 8 | Leitura dos dados | Folha `Dados`; não lia o dicionário | Lê `Dados` e `Dicionario` | **Adotar a do Rúbem**: mostrar o dicionário em 1.4 e usá-lo na justificação de 6.1 |
| 9 | Valores em falta | Corrigido para 8 | 8 | Iguais |
| 10 | Execução no Colab | Descarrega do GitHub automaticamente | Pede para carregar o Excel (`files.upload`) | **Nosso**: a docente só tem de carregar em «Executar tudo» |
| 11 | Referências a ficheiros | — | Cita `analise.py`, `suplemento.py`, `METODOLOGIA.md`, `RELATORIO.md`, que não estão na entrega | Retirar |
| 12 | Identificação | Nomes e números dos dois | «Preencher autores», sigla «MEIA … G01» | Confirmar a sigla da UC e o número do grupo |
| 13 | Declaração de uso de IA | Não tem | Tem | Decidir em conjunto (o enunciado permite IA e não exige declaração) |

**Os números coincidem** nos dois notebooks em tudo o que é comum: n, médias, IC, correlações, ANOVA, Welch, Kruskal-Wallis, regressão simples, C001, coeficiente da IA com os mesmos 233 casos (0,639). A divergência é de escolha de métodos e de âmbito, não de resultados.

## 4. Proposta final para a defesa

Um notebook único (o nosso, já comentado bloco a bloco), só com métodos das aulas, e a mensagem de sempre: associação fraca (r = 0,24), que quase desaparece quando se controla a experiência (0,64 → 0,13), sem diferenças entre departamentos, e por isso nenhuma recomendação de tornar a IA obrigatória. Depois de acordada, aplicamos as alterações ao notebook, ao relatório, ao guião e à apresentação.
