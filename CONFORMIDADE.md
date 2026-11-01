# Conformidade com o enunciado (`Trabalho Final.pdf`)

Verificação, ponto a ponto, de que o notebook `TP1_MEPA_IA_Produtividade.ipynb` e o relatório `Relatorio_TP1_MEPA_IA_Produtividade.docx` respondem ao que o enunciado pede. Feita em 1 de novembro de 2026 sobre o enunciado (4 páginas no ficheiro), o notebook (123 células, executado do início ao fim sem erros) e o relatório (8 secções, 8 figuras, 9 tabelas).

## Resumo

| Bloco | Itens | Cumpridos nos ficheiros | Observações |
|---|---|---|---|
| Perguntas 1.1 a 7.5 | 40 | 40 | Todas respondidas no notebook e no relatório, com interpretação própria |
| Requisitos de organização | 5 | 5 | Pares, relatório, notebook executável, interpretação por etapa, outputs contidos |
| Nota final do enunciado | 2 | 2 | Conclusões remetem à questão central; quatro níveis distinguidos |
| Critérios de avaliação | 6 | 5 | A «Defesa oral e domínio do trabalho» (10%) só se cumpre na apresentação |

Grau de cumprimento dos itens verificáveis em ficheiros: 100%. O que não é possível cumprir nos ficheiros, e porquê, está na última secção.

## Rastreabilidade pergunta a pergunta

Secções do notebook seguem a numeração do enunciado. Secções do relatório estão indicadas por número (o relatório começa a numeração na secção 2 para a preparação dos dados).

| Item | Pergunta (resumo) | Notebook | Relatório | Estado | Evidência / nota |
|---|---|---|---|---|---|
| 1.1 | Registos e colaboradores distintos | 1.1 | 2.1 | OK | 241 registos, 240 identificadores (C001 a C240) |
| 1.2 | Colaboradores repetidos e resolução | 1.2 | 2.2, Tabela 2 | OK | C084 duplicado em todas as colunas; mantida uma ocorrência |
| 1.3 | Valores em falta, variáveis e registos | 1.3 | 2.2, Tabela 2 | OK | 9 valores em 8 registos, por variável; sem imputação, justificado |
| 1.4 | Variáveis quantitativas/qualitativas; variável a explicar | 1.4 | 2.1, Tabela 1 | OK | Tabela de tipos; resposta = produtividade |
| 1.5 | Categorias inconsistentes e valores a analisar | 1.5 | 2.2 | OK | 3 grafias corrigidas; tetos/chão, C097, 0 h de IA; verificação explícita de valores impossíveis (reforço de 2026-11-01) |
| 1.6 | Colaboradores disponíveis; variação do n | 1.6 | 2.3 | OK | 240; n = 238 / 236 / 233 consoante a análise |
| 2.1 | Produtividade média e representatividade | 2.1 | 3 | OK | 78,0; mediana 79,35; Q1 a Q3 |
| 2.2 | Uso médio de IA e valores muito superiores | 2.2 | 3, Figura 1 | OK | 7,7 h; C134 e C035 acima do bigode superior |
| 2.3 | Departamento mais produtivo vs. mais IA | 2.3 | 3 | OK | Operações vs. Desenvolvimento; não coincidem |
| 2.4 | Simetria com representações gráficas | 2.4 | 3, Figura 2 | OK | Histograma, caixa de bigodes, Q-Q, Shapiro-Wilk; coeficiente de assimetria −0,61 (reforço) |
| 2.5 | Mais produtivo vs. mais IA; mesma pessoa? | 2.5 | 3 | OK | 13 empatados em 98 (teto); C134 abaixo da média; não é a mesma pessoa |
| 3.1 | Gráfico uso de IA vs produtividade; tendência | 3.1 | 4, Figura 3 | OK | Dispersão com reta e caixas por quartil |
| 3.2 | Medida de associação justificada | 3.2 | 4, Tabela 4 | OK | Pearson 0,24 e Spearman 0,27, escolha justificada |
| 3.3 | Forte, moderada, fraca ou inexistente | 3.3 | 4 | OK | Fraca; r² ≈ 0,06; significância vs intensidade |
| 3.4 | Mais IA implica mais produtivo? Exemplos | 3.4 | 4 | OK | C134, C078, C004 vs C014, C053 |
| 3.5 | Associação permite afirmar causalidade? | 3.5 | 4 | OK | Confusão, causalidade inversa, autosseleção |
| 4.1 | Produtividade semelhante entre departamentos? | 4.1 | 5, Figura 4 | OK | Médias 76,5 a 79,2 |
| 4.2 | Hipóteses estatísticas | 4.2 | 5 | OK | H₀/H₁ para ANOVA e para Kruskal-Wallis |
| 4.3 | Condições a verificar e como | 4.3 | 5 | OK | Independência, Shapiro-Wilk por grupo, Levene |
| 4.4 | Análise, resultados e valor-p no contexto | 4.4 | 5, Tabela 5 | OK | F(3, 234) = 0,47, p = 0,70; KW p = 0,71; interpretação do p |
| 4.5 | O que se afirma e o que fica por esclarecer | 4.5 | 5 | OK | Não rejeitar ≠ provar igualdade; limitações |
| 4.6 | IC 95% para a produtividade média | 4.6 | 5 | OK | [76,4 ; 79,7]; natureza sintética discutida |
| 5.1 | Equação só com horas de IA? | 5.1 | 6 | OK | OLS, teste ao declive p < 0,001 |
| 5.2 | Equação e significado dos coeficientes | 5.2 | 6 | OK | 73,04 + 0,627·uso_IA; b₀ e b₁ interpretados |
| 5.3 | Diferença 5 h vs 10 h e condições | 5.3 | 6 | OK | 3,1 pontos (IC 1,5 a 4,8); condições enumeradas |
| 5.4 | Proporção da variabilidade explicada | 5.4 | 6 | OK | R² = 0,058 |
| 5.5 | Colaborador: observado vs estimado | 5.5 | 6 | OK | C001: 68,0 vs 77,9; resíduo −9,9 |
| 5.6 | Análise de resíduos | 5.6 | 6, Figura 5 | OK | Resíduos vs ajustados, histograma, Q-Q, Shapiro-Wilk, Breusch-Pagan; Durbin-Watson e distância de Cook (reforço); variável omitida detetada |
| 6.1 | Outras variáveis; risco de indicadores de desempenho | 6.1 | 7.1, Figura 6 | OK | Matriz de correlações; exclusão justificada de tarefas, tempo e qualidade |
| 6.2 | Modelo com IA + pelo menos 2 variáveis | 6.2 | 7.2, Tabela 6 | OK | IA + experiência + formação + complexidade (n = 233) |
| 6.3 | Equação e coeficiente da IA ceteris paribus | 6.3 | 7.2 | OK | 0,129 (p = 0,47), interpretação «mantendo o resto constante» |
| 6.4 | O coeficiente alterou-se? Interpretação | 6.4 | 7.3, Figura 7 | OK | Queda de 80%; quem absorve a associação |
| 6.5 | Comparar capacidade explicativa; melhoria relevante? | 6.5 | 7.4, Tabela 7 | OK | Mesmos 233 casos; R² ajustado 0,056 vs 0,267; teste F parcial F(3, 228) = 23,1, p < 0,001 (reforço) |
| 6.6 | Associação entre explicativas; resíduos | 6.6 | 7.5, Figura 8, Tabela 8 | OK | Correlações, VIF < 1,6, diagnóstico completo, robustez sem C097 e com mais variáveis |
| 6.7 | Modelo mais adequado e porquê | 6.7 | 7.6 | OK | Modelo múltiplo, quatro razões |
| 7.1 | Quem usa mais IA é mais produtivo? | 7.1 | 8.1 | OK | Sim como tendência fraca; não como regra |
| 7.2 | Relação mantém-se com outros fatores? | 7.2 | 8.2 | OK | Não; experiência é o fator principal |
| 7.3 | Resultado mais inesperado com evidência | 7.3 | 8.3 | OK | Desaparecimento do efeito da IA; b, p e VIF |
| 7.4 | Duas limitações | 7.4 | 8.4 | OK | Desenho observacional; qualidade/medição dos dados |
| 7.5 | Recomendar IA obrigatória? Associação vs causalidade | 7.5 | 8.5 | OK | Não recomendado; alternativas; estudo piloto |

## Requisitos de organização e nota final

| Requisito do enunciado | Estado | Onde / como |
|---|---|---|
| Trabalho a pares | OK | Gilberto Coutinho (3083) e Rúbem Mendes (4563), identificados no notebook e no relatório |
| Entregar relatório de investigação | OK | `Relatorio_TP1_MEPA_IA_Produtividade.docx`: resumo, formulação do problema, 7 secções de análise, conclusões, referências, anexo |
| Entregar notebook organizado e executável | OK | Secções 0 a 7 na ordem do enunciado; executado do zero em 2026-11-01 (0 erros, cerca de 17 s); corre no Colab (dados no Drive) e localmente (dados no repositório) |
| Em cada etapa, resultados relevantes e interpretação própria | OK | Cada célula de código é seguida de uma célula de interpretação; decisões justificadas (não imputar, manter C097, excluir indicadores de desempenho) |
| Evitar reprodução de código ou outputs extensos | OK | Sumários `slim`, tabelas curtas; o output mais longo (13 colaboradores com produtividade 98) é a resposta direta à pergunta 2.5 |
| Dados sintéticos: não concluir sobre empresa real | OK | Dito na introdução, em 4.6 e nas limitações |
| Nota final: conclusões remetem à questão central | OK | 7.5 termina a responder à questão central; resumo do relatório idem |
| Nota final: distinguir descritivo, inferencial, explicação estatística e recomendação | OK | Tabela 9 do relatório; tabela «Síntese por nível de análise» no fim do capítulo 7 do notebook (reforço) |
| Recursos: opções metodológicas justificadas pelo grupo | OK | Escolha de Pearson/Spearman, ANOVA + Kruskal-Wallis, seleção de variáveis, modelo final, todas justificadas |

## Critérios de avaliação e onde se sustentam

| Dimensão | Peso | Evidência principal |
|---|---|---|
| Formulação do problema e estratégia de investigação | 15% | Introdução do notebook; secção 1 do relatório (questão, objetivo, etapas) |
| Preparação e exploração dos dados | 15% | Capítulos 1 e 2; Tabelas 1 a 3; verificação de duplicados, faltas, categorias, impossíveis, extremos |
| Seleção e fundamentação metodológica | 25% | 3.2, 4.3, 5.1, 6.1 e 6.2; condições de aplicação verificadas; testes de confirmação; teste F parcial |
| Interpretação e avaliação dos modelos | 20% | 5.2 a 5.6, 6.3 a 6.7; coeficientes, R² ajustado, resíduos, VIF, Durbin-Watson, Cook, robustez |
| Discussão crítica e conclusões | 15% | Capítulo 7 e secção 8 do relatório; limitações; associação vs causalidade |
| Defesa oral e domínio do trabalho | 10% | Não verificável em ficheiros (ver abaixo) |

## O que não é possível cumprir nos ficheiros, e porquê

1. **Defesa oral (10%)**. Só se cumpre na apresentação. Para a preparar, os pontos de apoio são a tabela «Síntese por nível de análise» (notebook, capítulo 7), a Figura 7 (evolução do coeficiente da IA) e a Tabela 9 do relatório.
2. **Possível página 5 do enunciado**. O rodapé do PDF diz «Página n de 5», mas o ficheiro tem 4 páginas e a página 4 termina na «Nota final». Se existir uma página 5 (prazo, formato de entrega, regras da defesa), não está no ficheiro e não pôde ser verificada. Confirmar na plataforma da unidade curricular.
3. **Causalidade**. As perguntas 3.5 e 7.5 pedem para explicar se a associação permite afirmar causalidade. Com dados observacionais e transversais não é possível estabelecê-la; o trabalho explica porquê e propõe o desenho que o permitiria (estudo piloto com atribuição aleatória). Não é um incumprimento, é a resposta correta à pergunta.
4. **Dados sintéticos**. Por natureza, as conclusões ilustram o raciocínio estatístico e não descrevem uma empresa real, como o próprio enunciado avisa.

## Pendentes que dependem do grupo

- Confirmar a grafia do nome do segundo elemento: o notebook e o relatório usam «Rúbem Mendes»; a versão anterior do README usava «Rúben». O README foi alinhado com os entregáveis.
- A capa do relatório diz «Outubro de 2026». Se a entrega for em novembro, atualizar a data em `scripts_geracao/build_report.py` e regenerar o relatório.
- Convidar o segundo elemento para o repositório GitHub (privado). A conta conhecida é o email institucional `a4563@alunos.ipca.pt`, que não corresponde a nenhum utilizador GitHub público; o convite tem de ser feito por email na página de colaboradores do repositório (Settings › Collaborators › Add people), pois a API só aceita nomes de utilizador.
- Preparar a defesa oral.
