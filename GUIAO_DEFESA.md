# Guião de apoio à defesa oral

Apoio para a dimensão «Defesa oral e domínio do trabalho» (10% da avaliação). Tudo o que está aqui tem a evidência no notebook (secções com a numeração do enunciado) e no relatório.

## A mensagem em 60 segundos

A direção acredita que quem usa mais IA é mais produtivo. Nos dados, isso é verdade como tendência, mas fraca: a correlação entre horas de IA e produtividade é 0,24 e o uso de IA explica cerca de 6% da variabilidade. Quando comparamos colaboradores com a mesma experiência, formação em IA e complexidade de tarefas, a associação quase desaparece: o coeficiente da IA cai cerca de 80%, de 0,64 para 0,13 pontos por hora, e deixa de ser significativo. O fator que realmente pesa é a experiência: mais 1,6 pontos por ano, e um coeficiente padronizado dez vezes maior do que o da IA. A vantagem aparente de quem usa mais IA explica-se sobretudo por essas pessoas serem mais experientes e mais formadas. Por isso não recomendamos tornar a IA obrigatória: a evidência é de associação, não de causalidade, e o ganho esperado seria pequeno mesmo no cenário mais favorável.

## Números a saber de cor

| O quê | Valor | Onde |
|---|---|---|
| Registos / colaboradores / casos no modelo múltiplo | 241 / 240 / 233 | 1.1, 1.6 |
| Produtividade média (mediana) | 78,0 (79,4) | 2.1 |
| Uso médio de IA | 7,7 h/semana | 2.2 |
| Correlação IA–produtividade (Pearson / Spearman) | 0,24 / 0,27, p < 0,001 | 3.2 |
| ANOVA departamentos | F(3, 234) = 0,47; p = 0,70; η² = 0,006 | 4.4 |
| IC 95% da produtividade média | [76,4 ; 79,7] | 4.6 |
| Modelo simples | 73,04 + 0,627 × uso_IA; R² = 0,058 | 5.2, 5.4 |
| Coeficiente da IA no modelo múltiplo | 0,129; p = 0,47; IC −0,22 a 0,48 | 6.3 |
| Experiência no modelo múltiplo | 1,58 por ano; p < 0,001; beta padronizado 0,50 | 6.3 |
| R² ajustado simples vs múltiplo (mesmos 233 casos) | 0,056 vs 0,267; F parcial (3, 228) = 23,1 | 6.5 |
| VIF máximo | 1,51 | 6.6 |

## Perguntas prováveis e respostas curtas

**Porque não imputaram os valores em falta?** São 9 valores em 8 registos, menos de 1% por variável. Imputar pela média reduziria artificialmente a variabilidade e podia distorcer as relações que queremos estudar. Cada análise usa os registos completos nas variáveis envolvidas, e dizemos sempre o n (1.3, 1.6).

**Porque mantiveram o C097, com produtividade 19?** Não há prova de erro: o valor está dentro da escala. Investigámos em vez de eliminar: repetimos todas as análises principais sem ele e nenhuma conclusão muda (3.2, 4.4, 5.6, 6.6). A distância de Cook máxima é 0,07, muito abaixo de 1.

**Porquê Pearson e também Spearman?** Pearson porque as duas variáveis são quantitativas e a relação parece linear. Spearman como confirmação, porque a produtividade não é normal, tem valores atípicos e um teto em 98. Os dois concordam (3.2).

**A normalidade falha num grupo; porque usaram a ANOVA?** Os grupos são grandes (31 a 85), o desvio deve-se essencialmente a um valor extremo e as variâncias são homogéneas (Levene p = 0,52). Decidimos à partida usar a ANOVA como teste principal e o Kruskal-Wallis como confirmação. Deram o mesmo resultado (4.3, 4.4).

**O que significa p = 0,70 neste contexto?** Se as médias fossem iguais nos quatro departamentos, diferenças como as observadas apareceriam em cerca de 70% das amostras. Não rejeitamos a igualdade, mas isso não a prova: diferenças pequenas podem existir e não ter sido detetadas (4.4, 4.5).

**Porque excluíram tarefas concluídas, tempo por tarefa e qualidade do modelo?** Medem o próprio desempenho, provavelmente são componentes do índice de produtividade. Incluí-las seria circular, inflaria o R² sem explicar nada e apagaria o efeito da IA que passa por essas vias (6.1).

**Porque é que o coeficiente da IA cai tanto no modelo múltiplo?** Variável omitida: os colaboradores mais experientes e mais formados usam mais IA (correlações 0,27 e 0,51) e a experiência está fortemente ligada à produtividade (0,50). Não é multicolinearidade, porque os VIF são baixos e o erro-padrão do coeficiente quase não muda (6.4, 6.6).

**O modelo múltiplo é mesmo melhor?** Sim: com os mesmos 233 casos, o R² ajustado passa de 0,06 para 0,27 e o teste F parcial às três variáveis acrescentadas dá p < 0,001. Mesmo assim, 73% da variabilidade fica por explicar (6.5).

**Então a IA não serve para nada?** Não é isso que os dados dizem. Dizem que, nestes dados, as horas de IA por si só não estão associadas a mais produtividade depois de descontar a experiência e a formação. A formação em IA tem uma associação positiva no limiar da significância (p = 0,06). O efeito pode depender do tipo de tarefa e da qualidade do uso, que não medimos (7.4, 7.5).

**O que fariam para provar causalidade?** Um estudo piloto com atribuição aleatória de acesso e formação a equipas comparáveis, medindo a produtividade antes e depois, e uma medida de produtividade sem teto (7.5).

**Que limitações destacam?** Desenho observacional e transversal, sem atribuição aleatória; dados sintéticos com índice de produtividade de construção desconhecida, efeitos de teto e de chão, um valor suspeito e uma medida de IA que conta horas e não qualidade de uso (7.4).

## Figuras para mostrar

- Figura 3 do relatório (3.1): dispersão com a reta e caixas por quartil, para a tendência fraca com muita dispersão.
- Figura 7 do relatório (6.4): o coeficiente da IA a encolher à medida que se controlam fatores. É o gráfico que conta a história do «paradoxo».
- Tabela 9 do relatório ou a síntese final do notebook: os quatro níveis, descritivo, inferencial, explicação estatística e recomendação.
