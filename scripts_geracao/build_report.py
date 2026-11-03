# Gera o relatório (.docx) do TP de MEPA
import re, sys, os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

PASTA = sys.argv[1]
FIG = os.path.join(PASTA, "figuras")
AZUL = RGBColor(0x1C, 0x5C, 0xAB)

doc = Document()
from datetime import datetime, timezone
_cp = doc.core_properties
_cp.author = "Gilberto Coutinho; Rúbem Mendes"
_cp.last_modified_by = "Gilberto Coutinho"
_cp.title = "Inteligência Artificial e Produtividade - Trabalho Prático 1 de MEPA"
_cp.subject = "Modelos Estatísticos para Inteligência Artificial (MEPA) - IPCA 2026/27"
_cp.keywords = "IA; produtividade; regressão; ANOVA"
_cp.comments = ""
_cp.created = _cp.modified = datetime.now(timezone.utc).replace(tzinfo=None, microsecond=0)
_cp.revision = 1
sec = doc.sections[0]
sec.page_height, sec.page_width = Cm(29.7), Cm(21.0)
for m in ("left_margin", "right_margin"): setattr(sec, m, Cm(2.3))
sec.top_margin = sec.bottom_margin = Cm(2.2)

st = doc.styles["Normal"]
st.font.name = "Calibri"; st.font.size = Pt(11)
st.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
st.paragraph_format.space_after = Pt(6); st.paragraph_format.line_spacing = 1.15
for lvl, size in ((1, 15), (2, 12.5), (3, 11.5)):
    h = doc.styles[f"Heading {lvl}"]
    h.font.name = "Calibri"; h.font.size = Pt(size); h.font.color.rgb = AZUL; h.font.bold = True
    h.paragraph_format.space_before = Pt(14 if lvl == 1 else 10); h.paragraph_format.space_after = Pt(4)

def runs(par, texto):
    # **negrito** e *itálico*
    for parte in re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*)", texto):
        if not parte: continue
        if parte.startswith("**"): par.add_run(parte[2:-2]).bold = True
        elif parte.startswith("*"): par.add_run(parte[1:-1]).italic = True
        else: par.add_run(parte)
    return par

def P(texto, align=WD_ALIGN_PARAGRAPH.JUSTIFY, style=None):
    par = doc.add_paragraph(style=style); par.alignment = align
    return runs(par, texto)

def B(*itens, num=False):
    for t in itens:
        par = doc.add_paragraph(style="List Number" if num else "List Bullet")
        par.paragraph_format.space_after = Pt(3); runs(par, t)

def H(t, n=1): doc.add_heading(t, n)

def sombrear(cel, cor):
    tcPr = cel._tc.get_or_add_tcPr(); s = OxmlElement("w:shd")
    s.set(qn("w:val"), "clear"); s.set(qn("w:color"), "auto"); s.set(qn("w:fill"), cor); tcPr.append(s)

def T(cab, linhas, larg=None, nota=None):
    t = doc.add_table(rows=1, cols=len(cab)); t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, c in enumerate(cab):
        cel = t.rows[0].cells[i]; cel.text = ""; r = cel.paragraphs[0].add_run(c); r.bold = True
        r.font.size = Pt(9.5); r.font.color.rgb = RGBColor(255, 255, 255); sombrear(cel, "1C5CAB")
    for k, l in enumerate(linhas):
        cells = t.add_row().cells
        for i, v in enumerate(l):
            cells[i].text = ""; runs(cells[i].paragraphs[0], str(v))
            for r in cells[i].paragraphs[0].runs: r.font.size = Pt(9.5)
            if i > 0 and len(str(v)) < 40: cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            if k % 2: sombrear(cells[i], "EEF4FC")
    for row in t.rows[:-1]:          # manter a tabela inteira na mesma página
        for cel in row.cells:
            for par in cel.paragraphs: par.paragraph_format.keep_with_next = True
    for row in t.rows:
        trPr = row._tr.get_or_add_trPr(); cs = OxmlElement("w:cantSplit"); trPr.append(cs)
    if larg:
        for row in t.rows:
            for i, w in enumerate(larg): row.cells[i].width = Cm(w)
    if nota:
        par = doc.add_paragraph(); r = par.add_run(nota); r.italic = True; r.font.size = Pt(9)
    else:
        doc.add_paragraph().paragraph_format.space_after = Pt(2)

fign = [0]
def F(nome, legenda, w=16):
    doc.add_picture(os.path.join(FIG, nome), width=Cm(w))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    fign[0] += 1
    par = doc.add_paragraph(); par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = par.add_run(f"Figura {fign[0]} – {legenda}"); r.italic = True; r.font.size = Pt(9.5)

def caixa(texto):
    t = doc.add_table(rows=1, cols=1); t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.rows[0]._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
    c = t.rows[0].cells[0]; sombrear(c, "EEF4FC"); c.width = Cm(16.4); c.text = ""
    runs(c.paragraphs[0], texto); c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

# ------------------------------------------------------------------ capa
for _ in range(3): doc.add_paragraph()
for txt, size, bold in [("Universidade Politécnica do Cávado e do Ave", 13, False),
                        ("Mestrado em Inteligência Artificial", 13, False),
                        ("Modelos Estatísticos para Inteligência Artificial — 2026/2027", 12, False)]:
    par = doc.add_paragraph(); par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = par.add_run(txt); r.font.size = Pt(size); r.bold = bold
for _ in range(4): doc.add_paragraph()
par = doc.add_paragraph(); par.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = par.add_run("Trabalho Prático de Investigação"); r.font.size = Pt(14); r.font.color.rgb = AZUL
par = doc.add_paragraph(); par.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = par.add_run("O paradoxo da Inteligência Artificial:\ntrabalhar com IA significa trabalhar melhor?")
r.font.size = Pt(22); r.bold = True; r.font.color.rgb = AZUL
for _ in range(5): doc.add_paragraph()
par = doc.add_paragraph(); par.alignment = WD_ALIGN_PARAGRAPH.CENTER
par.add_run("Relatório de investigação\n\n").font.size = Pt(12)
r = par.add_run("Gilberto Coutinho — n.º 3083\nRúbem Mendes — n.º 4563"); r.font.size = Pt(12); r.bold = True
par = doc.add_paragraph(); par.alignment = WD_ALIGN_PARAGRAPH.CENTER
par.add_run("\nDocente: Liliana Coelho\nNovembro de 2026").font.size = Pt(11)
doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

# ------------------------------------------------------------------ resumo
H("Resumo")
P("Neste trabalho procurámos perceber se a utilização de ferramentas de Inteligência Artificial (IA) está associada à "
  "produtividade de 240 colaboradores de uma empresa tecnológica (dados sintéticos) e se essa associação se mantém quando "
  "entram em jogo outros fatores individuais e profissionais. Depois de limpar a base (um registo duplicado, categorias "
  "escritas de forma diferente e alguns valores em falta), encontrámos uma associação positiva mas fraca entre as horas semanais "
  "de uso de IA e a produtividade (r = 0,24; p < 0,001), que explica apenas cerca de 6% da sua variabilidade. Não encontrámos "
  "diferenças de produtividade entre departamentos (ANOVA, p = 0,70). Num modelo de regressão múltipla que controla a experiência, "
  "a formação em IA e a complexidade das tarefas, o coeficiente da IA reduz-se cerca de 80% (de 0,64 para 0,13 pontos por hora) "
  "e deixa de ser estatisticamente significativo (p = 0,47), enquanto a experiência surge como o fator mais fortemente associado "
  "à produtividade (mais 1,6 pontos por ano; p < 0,001). A vantagem aparente de quem usa mais IA parece dever-se sobretudo a "
  "diferenças de experiência e de formação, pelo que não recomendamos tornar obrigatório o uso de IA com base nestes dados.")
P("**Palavras-chave:** inteligência artificial; produtividade; correlação; ANOVA; regressão linear múltipla; fatores de confusão.",
  align=WD_ALIGN_PARAGRAPH.LEFT)

# ------------------------------------------------------------------ 1
H("1. Formulação do problema e estratégia de investigação")
P("A direção de uma empresa tecnológica acredita que os colaboradores que mais utilizam IA são também os mais produtivos. "
  "A questão central desta investigação é: *em que medida a utilização de ferramentas de IA está associada à produtividade "
  "dos colaboradores e como se altera essa relação quando são considerados outros fatores individuais e profissionais?* "
  "Não partimos para demonstrar que a IA aumenta a produtividade; o objetivo foi avaliar o que os dados permitem, e não "
  "permitem, afirmar.")
P("Seguimos as etapas do enunciado, das mais simples às mais exigentes, de modo que cada uma preparasse a seguinte:")
B("preparação dos dados: duplicados, valores em falta, categorias inconsistentes, valores atípicos e limites de escala;",
  "descrição da produtividade e do uso de IA, globalmente e por departamento;",
  "associação entre as duas variáveis, com um gráfico de dispersão e os coeficientes de correlação de Pearson e de Spearman;",
  "inferência: comparação dos departamentos (ANOVA, confirmada pela ANOVA de Welch e pelo teste de Kruskal-Wallis) e intervalo de confiança para a produtividade média;",
  "explicação estatística: regressão linear simples e regressão múltipla com fatores anteriores ao desempenho, comparação dos modelos (R² ajustado, teste F parcial, AIC/BIC e validação cruzada), diagnóstico dos resíduos e inferência robusta (erros-padrão HC3 e bootstrap);",
  "conclusões e recomendações, distinguindo associação de causalidade.", num=True)
P("Usámos apenas os métodos trabalhados nas aulas da unidade curricular. A análise foi feita em Python (pandas, SciPy, "
  "statsmodels, matplotlib/seaborn) num notebook Google Colab, entregue com este relatório. Adotámos um nível de significância "
  "de 5%. Como os dados são sintéticos, as conclusões ilustram um raciocínio estatístico e não descrevem uma empresa real.")

# ------------------------------------------------------------------ 2
H("2. Conhecimento e preparação da base de dados")
H("2.1. Estrutura, registos e colaboradores", 2)
P("A base contém **241 registos** e 11 variáveis, mas apenas **240 identificadores distintos** (C001 a C240, sem lacunas). "
  "A Tabela 1 classifica as variáveis. A variável que queremos explicar é a produtividade (índice de 0 a 100); a variável "
  "explicativa de interesse é o uso semanal de IA, em horas.")
T(["Variável", "Tipo", "Papel na investigação"], [
    ["id_colaborador", "Identificador", "Não analisada"],
    ["departamento", "Qualitativa nominal (4 categorias)", "Fator de contexto"],
    ["complexidade_tarefas", "Qualitativa ordinal (1–5)", "Fator anterior (controlo)"],
    ["experiencia_anos", "Quantitativa contínua", "Fator anterior"],
    ["formacao_ia_horas", "Quantitativa contínua", "Fator anterior"],
    ["uso_ia_horas", "Quantitativa contínua", "**Explicativa de interesse**"],
    ["carga_trabalho_horas", "Quantitativa contínua", "Fator de contexto"],
    ["tarefas_concluidas", "Quantitativa discreta", "Indicador de desempenho"],
    ["tempo_medio_tarefa_horas", "Quantitativa contínua", "Indicador de desempenho"],
    ["qualidade_trabalho", "Quantitativa contínua (0–100)", "Indicador de desempenho"],
    ["produtividade", "Quantitativa contínua (0–100)", "**Variável resposta**"],
], larg=[4.6, 6.0, 5.6], nota="Tabela 1 – Tipos de variáveis e papel na investigação. A complexidade, embora ordinal, é tratada como numérica nos modelos (5 níveis igualmente espaçados).")

H("2.2. Problemas identificados e decisões tomadas", 2)
T(["Problema", "Evidência", "Decisão e justificação"], [
    ["Colaborador repetido", "C084 aparece 2 vezes, com valores iguais em todas as variáveis",
     "Mantivemos uma ocorrência: é uma linha duplicada; mantê-la daria peso duplo a C084"],
    ["Valores em falta", "9 valores em 8 registos: uso_ia (2), produtividade (2), experiência, formação, complexidade e tempo médio (1 cada)",
     "Sem imputação (menos de 1% por variável); cada análise usa os registos completos nas variáveis envolvidas"],
    ["Categorias inconsistentes", "«desenvolvimento», «Operacoes», «Analise de Dados» (1 registo cada)",
     "Uniformizadas, ficando 4 departamentos: Desenvolvimento (85), Operações (66), Análise de Dados (58), Comunicação (31)"],
    ["Efeitos de teto e de chão", "13 colaboradores com produtividade = 98 (máximo); 34 com tempo médio = 0,40 h; 9 com qualidade = 100",
     "Mantidos; registados como limitação (a escala parece truncada)"],
    ["Valor atípico na resposta", "C097: produtividade = 19 (o seguinte é 43,5), pouco coerente com 34 tarefas e qualidade 71",
     "Mantido (não há prova de erro); análises principais repetidas sem C097"],
    ["Uso de IA extremo", "C134 (25 h) e C035 (24,8 h) acima do bigode superior da caixa de bigodes (21,2 h)",
     "Mantidos (valores plausíveis); influência vigiada nos modelos"],
], larg=[3.3, 6.4, 6.5], nota="Tabela 2 – Síntese da preparação dos dados.")
P("Não encontrámos valores impossíveis (negativos, produtividade acima de 100 ou uso de IA superior à carga de trabalho). "
  "Os 11 colaboradores com 0 h de uso de IA são plausíveis e foram mantidos.")
H("2.3. Casos disponíveis para análise", 2)
P("Ficam **240 colaboradores**; nenhum foi excluído por inteiro. O número de casos varia consoante a análise: 238 com "
  "produtividade (descrição e ANOVA), 236 com uso de IA e produtividade (correlação e regressão simples) e 233 com todas as "
  "variáveis do modelo múltiplo. Para comparar os dois modelos de regressão em pé de igualdade, reestimámos o modelo simples "
  "com os mesmos 233 casos.")

# ------------------------------------------------------------------ 3
H("3. Caracterização dos colaboradores (análise descritiva)")
T(["Estatística", "Produtividade", "Uso de IA (h/semana)"], [
    ["n", "238", "238"], ["Média", "78,03", "7,72"], ["Mediana", "79,35", "7,60"],
    ["Desvio-padrão", "12,84", "4,93"], ["Mínimo – Máximo", "19,0 – 98,0", "0,0 – 25,0"],
    ["Q1 – Q3", "70,2 – 87,5", "3,8 – 10,8"],
], larg=[5.5, 5.0, 5.0], nota="Tabela 3 – Estatísticas descritivas da produtividade e do uso de IA.")
P("**Produtividade média.** A produtividade média é 78,0 pontos (desvio-padrão 12,8). A média representa razoavelmente os dados: "
  "está perto da mediana (79,35) e metade dos colaboradores situa-se entre 70,2 e 87,5. Fica, ainda assim, um pouco abaixo da "
  "mediana por causa de alguns valores muito baixos (C097 = 19; C129 = 43,5), pelo que a mediana descreve um pouco melhor o "
  "colaborador típico.")
P("**Uso de IA.** Em média, os colaboradores usam IA 7,7 h por semana (mediana 7,6 h), com bastante heterogeneidade "
  "(desvio-padrão 4,9 h). Dois colaboradores ficam acima do bigode superior da caixa de bigodes: C134 (25,0 h) e C035 (24,8 h), "
  "como se vê na Figura 1.")
F("fig_2_2_uso_ia.png", "Distribuição do uso semanal de IA (histograma e caixa de bigodes).", 15)
P("**Departamentos.** O departamento mais produtivo é Operações (média 79,2), seguido de Comunicação (78,6), Desenvolvimento (78,0) "
  "e Análise de Dados (76,5). O que mais usa IA é Desenvolvimento (9,0 h/semana); Operações é apenas o segundo (7,2 h). "
  "Portanto, o departamento mais produtivo não é o que mais usa IA, e as diferenças de produtividade (no máximo 2,7 pontos) "
  "são pequenas face à variabilidade dentro de cada departamento (desvios-padrão entre 11,6 e 14,0).")
P("**Simetria da produtividade.** A distribuição é só aproximadamente simétrica. A cauda esquerda é mais longa, a média fica "
  "abaixo da mediana e o gráfico Q-Q afasta-se da reta na cauda inferior (Figura 2). Na cauda direita nota-se o efeito de teto em "
  "98. O coeficiente de assimetria é −0,61 (sem C097, −0,29). O teste de Shapiro-Wilk rejeita a normalidade (p < 0,001) e continua a "
  "rejeitá-la sem C097, em boa parte por causa desse teto.")
F("fig_2_4_produtividade.png", "Distribuição da produtividade: histograma com média e mediana, caixa de bigodes e gráfico Q-Q.")
P("**Máximos.** A produtividade máxima (98,0) é atingida por 13 colaboradores, com usos de IA entre 4,9 h (C014) e 16,3 h (C036); "
  "vários são muito experientes (C014, C015 e C178, com 19 anos). Se for preciso apontar um só, o desempate pela qualidade do trabalho e "
  "depois pelas tarefas concluídas indica C237 (Desenvolvimento; qualidade 100, 40 tarefas, 12,7 h de IA). O colaborador que mais usa IA (C134, 25 h) tem produtividade "
  "71,6, abaixo da média, e cerca de 71% dos colaboradores são mais produtivos do que ele. Não são as mesmas pessoas. Estes casos "
  "mostram que muito uso de IA não garante produtividade elevada; se existir associação, será uma tendência média.")

# ------------------------------------------------------------------ 4
H("4. Associação entre o uso de IA e a produtividade")
F("fig_3_1_dispersao.png", "Uso de IA vs produtividade (com a reta de mínimos quadrados) e produtividade por quartil de uso de IA.")
P("**Tendência.** A Figura 3 sugere uma tendência crescente, mas ténue: a mediana da produtividade passa de 73,0 no primeiro quartil "
  "de uso para 84,9 no quarto. A dispersão é, porém, enorme para qualquer nível de uso (com cerca de 8 h/semana observam-se "
  "produtividades entre 19 e 98) e não há sinais de curvatura, pelo que uma reta descreve razoavelmente a tendência.")
P("**Medida de associação.** Como as duas variáveis são quantitativas e a relação parece aproximadamente linear, usámos o "
  "coeficiente de correlação de Pearson. Dado que a produtividade não é normal, tem valores atípicos e um teto, calculámos "
  "também o ρ de Spearman, que se baseia nas ordens e é menos sensível a valores extremos.")
T(["Medida", "Valor", "Valor-p"], [
    ["r de Pearson", "0,241", "< 0,001"], ["ρ de Spearman", "0,266", "< 0,001"],
    ["r de Pearson sem C097", "0,252", "< 0,001"], ["r² (variabilidade partilhada)", "0,058", "—"],
], larg=[6.5, 4.0, 4.0], nota="Tabela 4 – Associação entre uso de IA e produtividade (n = 236).")
P("**Classificação.** Com r ≈ 0,24 a associação é positiva mas fraca: pelas convenções habituais, valores abaixo de 0,3 "
  "consideram-se fracos e só acima de 0,5 se fala de uma associação forte. O uso de IA partilha apenas cerca de 6% da "
  "variabilidade da produtividade. A associação é estatisticamente significativa porque, com n = 236, até correlações pequenas "
  "são detetáveis; significância não é sinónimo de intensidade.")
P("**Os que mais usam IA são os mais produtivos?** Não necessariamente. C134 (25 h) tem 71,6; C078 (18 h) tem 58,7; C004 (16,3 h) tem 70,3. "
  "Em sentido contrário, C014 (4,9 h) atinge 98 e C053 (0 h) tem 90. Entre os 11 colaboradores que não usam IA, a produtividade vai "
  "de 48,9 (C238) a 90,0 (C053).")
P("**Associação não é causalidade.** Os dados são observacionais e transversais, sem atribuição aleatória do uso de IA. A correlação "
  "positiva é compatível com (i) fatores de confusão, como a experiência, correlacionada com o uso de IA (r = 0,27) e com a "
  "produtividade (r = 0,50); (ii) causalidade inversa, se os colaboradores produtivos tiverem mais margem para explorar a IA; "
  "(iii) autosseleção de quem adota a ferramenta. Não permite, por isso, afirmar que a IA aumenta a produtividade.")

# ------------------------------------------------------------------ 5
H("5. Diferenças entre departamentos e estimação da produtividade média (inferência)")
F("fig_4_1_departamentos.png", "Produtividade por departamento (caixas de bigodes, observações individuais e médias).", 14)
P("**Hipóteses.** Sendo μ_AD, μ_C, μ_D e μ_O as produtividades médias populacionais de cada departamento: "
  "H₀: μ_AD = μ_C = μ_D = μ_O; H₁: pelo menos duas médias diferem.")
P("**Condições de aplicação da ANOVA a um fator.** (1) *Independência*: assegurada pelo desenho (cada colaborador surge uma vez e "
  "pertence a um só departamento). (2) *Normalidade por grupo* (Shapiro-Wilk): não rejeitada em Análise de Dados (p = 0,36), Comunicação "
  "(p = 0,32) e Operações (p = 0,06); rejeitada em Desenvolvimento (p < 0,001), que é o grupo onde está C097. Como o guia das aulas "
  "recorda, a decisão não depende só do valor-p: os grupos são grandes (31 a 85) e o desvio deve-se essencialmente a um valor extremo. "
  "(3) *Homogeneidade de variâncias*: teste de Levene com p = 0,52, não rejeitada; os desvios-padrão vão de 11,6 a 14,0. "
  "Decidimos usar a ANOVA como teste principal e duas confirmações: a ANOVA de Welch, que não exige variâncias iguais (os grupos "
  "têm dimensões diferentes, de 31 a 85), e o teste de Kruskal-Wallis, não paramétrico.")
T(["Teste", "Estatística", "Valor-p"], [
    ["ANOVA a um fator", "F(3, 234) = 0,47", "0,702"],
    ["ANOVA de Welch", "F(3; 105,7) = 0,50", "0,681"],
    ["Kruskal-Wallis", "H(3) = 1,37", "0,713"],
    ["ANOVA sem C097", "—", "0,632"],
], larg=[5.5, 5.0, 4.0], nota="Tabela 5 – Comparação da produtividade entre departamentos.")
P("**Interpretação do valor-p.** Um valor-p de 0,70 significa que, se a produtividade média fosse realmente igual nos quatro departamentos, "
  "diferenças entre médias amostrais iguais ou superiores às observadas surgiriam em cerca de 70% das amostras. Como p > 0,05, não "
  "rejeitamos H₀. Os três testes concordam, pelo que a conclusão não depende de assumir variâncias iguais nem normalidade, e o "
  "resultado não depende de C097. A dimensão do efeito confirma a leitura: η² = 0,006, isto é, "
  "o departamento explica apenas 0,6% da variabilidade da produtividade. Não se justificam, por isso, comparações múltiplas.")
P("**O que se pode e não pode afirmar.** Não há evidência de diferenças entre departamentos, mas isso não prova que as médias sejam "
  "iguais: diferenças pequenas (2 a 3 pontos) podem existir e não ser detetadas, sobretudo em Comunicação (n = 31). "
  "Fica por esclarecer se o efeito da IA difere entre departamentos, se o índice de produtividade é comparável entre tarefas de natureza "
  "diferente e se diferenças de composição (experiência, formação) escondem diferenças reais. Um resultado útil: o departamento não é "
  "um fator de confusão relevante na relação entre IA e produtividade.")
P("**Intervalo de confiança.** A produtividade média estimada é 78,03 (erro-padrão 0,83), com IC 95% = [76,4 ; 79,7] (distribuição t, "
  "n = 238). Se o processo de amostragem fosse repetido muitas vezes, cerca de 95% dos intervalos assim construídos conteriam a "
  "verdadeira média. O intervalo é estreito, logo a média está bem estimada; com esta dimensão de amostra a assimetria não compromete o "
  "resultado. Como os dados são sintéticos, a «população» é o mecanismo que gerou os dados e não uma empresa real; o intervalo traduz "
  "apenas a incerteza de amostragem e não cobre erros de medição, o teto em 98 ou eventuais erros de registo.")

# ------------------------------------------------------------------ 6
H("6. Regressão linear simples: a IA explica a produtividade?")
P("Estimámos por mínimos quadrados o modelo produtividade = β₀ + β₁·uso_IA + ε (n = 236). O teste ao declive rejeita H₀: β₁ = 0 "
  "(t = 3,80; p < 0,001), pelo que é possível construir a equação:")
par = P("**produtividade estimada = 73,04 + 0,627 × uso_ia_horas**", align=WD_ALIGN_PARAGRAPH.CENTER)
B("b₀ = 73,04 (IC 95%: 70,0 a 76,0): produtividade média estimada para quem não usa IA (0 h), situação observada em 11 colaboradores.",
  "b₁ = 0,627 (IC 95%: 0,30 a 0,95; p < 0,001): por cada hora semanal adicional de uso de IA, a produtividade média estimada é 0,63 "
  "pontos mais alta. É uma comparação entre colaboradores diferentes, não o efeito de um colaborador aumentar o seu uso.")
P("**5 h vs 10 h.** O modelo estima 76,2 (5 h) e 79,3 (10 h): uma diferença de 5 × 0,627 ≈ 3,1 pontos (IC 95%: 1,5 a 4,8). Esta "
  "comparação refere-se à média de colaboradores com esses níveis de uso (o intervalo de previsão para um indivíduo com 5 h vai de cerca "
  "de 52 a 101); não mantém nada constante (quem usa 10 h tende a ser mais experiente e mais formado); é associativa e não causal; "
  "e não envolve extrapolação, porque os dois valores estão dentro do intervalo observado (0 a 25 h).")
P("**Capacidade explicativa.** R² = 0,058 (R² ajustado = 0,054): o uso de IA explica cerca de 6% da variabilidade da produtividade. "
  "Saber as horas de IA de um colaborador ajuda muito pouco a prever a sua produtividade.")
P("**Um colaborador concreto (C001).** C001 (Operações) usa IA 7,7 h/semana; o modelo prevê 73,04 + 0,627 × 7,7 ≈ 77,9, mas a "
  "produtividade observada é 68,0. O resíduo de −9,9 pontos é a parte da produtividade que o uso de IA não explica: C001 está "
  "cerca de 10 pontos abaixo do colaborador típico com o mesmo uso. Uma explicação plausível é ter apenas 0,5 anos de experiência.")
F("fig_5_6_residuos_m1.png", "Diagnóstico de resíduos do modelo simples (M1).")
P("**Análise de resíduos.** No gráfico dos resíduos contra os valores ajustados não há curvatura nem padrão, e a dispersão parece "
  "constante (Breusch-Pagan p = 0,98). A independência é assumida pelo desenho (dados transversais, um registo por colaborador) e a "
  "estatística de Durbin-Watson (1,84) não indica autocorrelação. "
  "A normalidade é rejeitada (Shapiro-Wilk p < 0,001): o histograma e o Q-Q mostram uma cauda esquerda longa, com C097 (resíduo −58,9) "
  "e C129 (−36,8), e uma cauda direita achatada pelo teto em 98; sem C097 o problema atenua-se (p = 0,03) e o declive mantém-se em 0,63. "
  "A distância de Cook máxima é 0,06 (C134), muito abaixo de 1: nenhuma observação domina o ajustamento. "
  "O problema principal, contudo, está no que falta ao modelo: R² = 0,06, resíduos entre −59 e +24 pontos e uma correlação de 0,45 "
  "(p < 0,001) entre os resíduos e a experiência, sinal claro de que ficou de fora uma variável importante. O modelo descreve uma "
  "tendência média, mas não explica nem prevê a produtividade individual.")

# ------------------------------------------------------------------ 7
H("7. Regressão linear múltipla: será que a IA explica tudo?")
H("7.1. Seleção de variáveis", 2)
F("fig_6_1_correlacoes.png", "Matriz de correlações de Pearson entre as variáveis quantitativas.", 12.5)
P("A Figura 6 mostra que, além do uso de IA, a produtividade se correlaciona com a experiência (0,50), a qualidade (0,46), as "
  "tarefas concluídas (0,44) e o tempo médio por tarefa (−0,48). Estas três últimas são, porém, indicadores do próprio desempenho, "
  "provavelmente componentes ou consequências da mesma medida de produtividade. Incluí-las teria três problemas: circularidade "
  "(explicar a produtividade com partes dela própria, inflacionando o R² sem ganho de conhecimento); se a IA melhorar a produtividade "
  "através de mais tarefas ou de menos tempo por tarefa, controlar esses indicadores apagaria o efeito que queremos estudar; e não "
  "são variáveis que a direção possa controlar à partida. Deixámo-las de fora.")
P("Incluímos, com o uso de IA, três variáveis anteriores ao desempenho e apontadas no enunciado como possíveis influências: "
  "experiência (associada à produtividade e ao uso de IA, logo potencial fator de confusão), formação em IA (muito associada "
  "ao uso de IA, r = 0,51) e complexidade das tarefas (característica do posto de trabalho). A carga de trabalho e o departamento, "
  "fracamente associados à produtividade, serviram para um teste de robustez.")
H("7.2. Modelo estimado", 2)
T(["Variável", "Coeficiente", "Erro-padrão", "t", "Valor-p", "IC 95%"], [
    ["Constante", "67,32", "2,60", "25,86", "< 0,001", "62,19 a 72,45"],
    ["Uso de IA (h/sem.)", "**0,129**", "0,179", "0,72", "**0,471**", "−0,22 a 0,48"],
    ["Experiência (anos)", "1,584", "0,190", "8,32", "< 0,001", "1,21 a 1,96"],
    ["Formação em IA (h)", "0,231", "0,122", "1,90", "0,059", "−0,01 a 0,47"],
    ["Complexidade (1–5)", "−0,661", "0,716", "−0,92", "0,357", "−2,07 a 0,75"],
], larg=[3.8, 2.4, 2.4, 1.8, 2.2, 3.6],
  nota="Tabela 6 – Modelo de regressão múltipla M2 (n = 233; R² = 0,280; R² ajustado = 0,267; F(4, 228) = 22,1; p < 0,001).")
P("**produtividade estimada = 67,32 + 0,129·uso_IA + 1,584·experiência + 0,231·formação_IA − 0,661·complexidade**",
  align=WD_ALIGN_PARAGRAPH.CENTER)
P("**Coeficiente da IA.** Entre colaboradores com a mesma experiência, formação em IA e complexidade de tarefas, cada hora semanal "
  "adicional de IA está associada a uma produtividade média apenas 0,13 pontos mais alta, valor não significativo (p = 0,47) cujo "
  "intervalo de confiança inclui o zero e valores negativos. A experiência é o único preditor claramente significativo (mais 1,58 pontos "
  "por ano); a formação em IA tem uma associação positiva no limiar da significância (p = 0,059); a complexidade não é significativa. "
  "A constante não tem interpretação prática (complexidade 0 está fora do domínio). Como as unidades são diferentes, comparámos a "
  "importância relativa das variáveis com coeficientes padronizados (desvios-padrão de produtividade por desvio-padrão da variável): "
  "experiência 0,50, formação em IA 0,13, uso de IA 0,05 e complexidade −0,05. A experiência pesa cerca de dez vezes mais do que o uso de IA.")
H("7.3. Alteração do coeficiente da IA", 2)
F("fig_6_4_coeficiente_ia.png", "Coeficiente do uso de IA (e IC 95%) à medida que se acrescentam variáveis de controlo (mesmos 233 casos).", 14)
P("Com os mesmos 233 casos, o coeficiente da IA passa de 0,639 (p < 0,001) no modelo simples para 0,129 (p = 0,47) no modelo "
  "múltiplo, uma redução de cerca de 80%. A Figura 7 mostra quem «absorve» a associação: acrescentar só a formação quase não muda o "
  "coeficiente (0,60), mas acrescentar a experiência reduz-o para metade (0,31; p = 0,04), e experiência e formação em conjunto "
  "levam-no a 0,13. A explicação está na matriz de correlações: os colaboradores mais experientes e mais formados usam mais IA "
  "(r = 0,27 e 0,51 com o uso de IA) e a experiência está fortemente ligada à produtividade (r = 0,50). Quem usa mais IA é mais "
  "produtivo, mas em grande parte por ser mais experiente, não por usar mais IA. É este o «paradoxo» do título.")
P("Uma reserva: se a formação levar a mais uso de IA e este a mais produtividade, controlar a formação pode retirar à IA parte de um "
  "efeito real. Mesmo assim, controlando apenas a experiência, que não é consequência de usar IA, o coeficiente já cai para metade.")
H("7.4. Comparação dos modelos", 2)
T(["Critério", "M1: só IA", "M2: IA + 3 variáveis"], [
    ["n (mesmos casos)", "233", "233"], ["N.º de preditores", "1", "4"],
    ["R²", "0,061", "0,280"], ["R² ajustado", "0,056", "**0,267**"],
    ["Teste F global", "F(1, 231) = 14,9; p < 0,001", "F(4, 228) = 22,1; p < 0,001"],
    ["Teste F parcial (M2 vs M1)", "—", "F(3, 228) = 23,1; p < 0,001"],
    ["AIC / BIC (menor é melhor)", "1839,5 / 1846,4", "**1783,6 / 1800,9**"],
    ["RMSE em validação cruzada (5 partições)", "12,5", "**11,0**"],
], larg=[5.5, 5.0, 5.5], nota="Tabela 7 – Comparação da capacidade explicativa dos modelos. O modelo alargado com carga de trabalho e "
   "departamento (8 preditores) tem AIC 1785,2, BIC 1816,3 e RMSE 11,1, todos piores do que o M2.")
P("A comparação foi feita com as mesmas observações, condição necessária para comparar os R². Como o R² nunca desce quando se "
  "acrescentam variáveis, olhámos sobretudo para o R² ajustado, que penaliza o número de preditores: sobe de 0,056 para 0,267, "
  "quase cinco vezes. Com 233 observações para 4 preditores (cerca de 58 por preditor), o ganho não se explica pela complexidade "
  "adicional, e o teste F parcial aos modelos encaixados confirma que as três variáveis acrescentadas melhoram significativamente o "
  "ajustamento (F(3, 228) = 23,1; p < 0,001).")
P("Confirmámos a escolha com dois critérios que não se limitam ao ajustamento na amostra. O AIC e o BIC, que penalizam o número de "
  "parâmetros, são mínimos no M2; acrescentar ainda a carga de trabalho e o departamento piora ambos, porque os cinco parâmetros "
  "adicionais não compensam. Na validação cruzada (cada modelo estimado em 4/5 dos colaboradores e avaliado nos restantes, com as "
  "mesmas partições para todos), o erro médio de previsão desce de 12,5 pontos no M1 para 11,0 no M2, e o modelo alargado não "
  "melhora (11,1). As variáveis acrescentadas melhoram, portanto, a previsão para colaboradores que o modelo não viu. O modelo com "
  "mais variáveis apresenta uma melhoria relevante, embora cerca de 73% da variabilidade fique por explicar e um erro típico de "
  "11 pontos mostre que a produtividade individual continua difícil de prever.")
H("7.5. Diagnóstico do modelo múltiplo", 2)
F("fig_6_6_residuos_m2.png", "Diagnóstico de resíduos do modelo múltiplo (M2).")
P("**Associação entre as explicativas.** A correlação mais alta entre preditores é entre uso de IA e formação (0,51); as restantes são "
  "fracas. Todos os VIF são inferiores a 1,6 (máximo 1,51, no uso de IA), muito abaixo do limiar de 5 referido nas aulas. O erro-padrão "
  "do coeficiente da IA quase não muda (0,165 no modelo simples, 0,179 no múltiplo), pelo que a perda de significância da IA não vem "
  "de multicolinearidade; vem de o modelo passar a descontar a experiência.")
P("**Resíduos.** Não há curvatura nem padrão nos resíduos contra os valores ajustados, nem evidência de heterocedasticidade "
  "(Breusch-Pagan p = 0,19); a independência é assumida pelo desenho e o Durbin-Watson (1,95) não indica autocorrelação. A distância de "
  "Cook máxima é 0,07 (C097), muito abaixo de 1. A normalidade é rejeitada (p < 0,001), mas quase só por causa "
  "de C097, com um resíduo de −60,6: sem C097 os resíduos são compatíveis com a normalidade (Shapiro-Wilk p = 0,97) e o coeficiente "
  "da IA praticamente não muda (0,146; p = 0,38). Tratar a complexidade como categórica, em vez de numérica, também não altera a conclusão "
  "(coeficiente da IA 0,122; p = 0,50) e não melhora o ajustamento de forma significativa (F(3, 225) = 1,55; p = 0,20), o que valida a "
  "simplificação assumida na Tabela 1 (Tabela 8).")
P("**Inferência robusta.** Como a normalidade dos resíduos é rejeitada, confirmámos a incerteza do coeficiente da IA por duas vias "
  "que não dependem dela nem da variância constante: erros-padrão robustos HC3 e bootstrap de pares (2000 reamostragens dos 233 "
  "colaboradores). Os intervalos obtidos (Tabela 8) são praticamente iguais ao clássico e incluem sempre o zero; no bootstrap, cerca "
  "de 23% das reamostragens dão um coeficiente nulo ou negativo. No modelo alargado, o VIF máximo sobe para 1,75, ainda muito abaixo de 5.")
T(["Variante do modelo M2", "Coef. IA", "Valor-p", "IC 95% do coef. IA", "R² ajustado"], [
    ["M2 (erros-padrão clássicos)", "0,129", "0,471", "−0,22 a 0,48", "0,267"],
    ["M2 com erros-padrão robustos HC3", "0,129", "0,458", "−0,21 a 0,47", "0,267"],
    ["M2, bootstrap de pares (2000)", "0,129", "—", "−0,21 a 0,46", "0,267"],
    ["M2 sem C097", "0,146", "0,384", "—", "0,302"],
    ["M2 + carga de trabalho + departamento (HC3)", "0,144", "0,450", "−0,23 a 0,52", "0,274"],
    ["M2 com complexidade como categórica", "0,122", "0,500", "—", "0,272"],
], larg=[6.2, 2.0, 2.0, 3.4, 2.6], nota="Tabela 8 – Análise de robustez: a conclusão sobre a IA não depende das opções tomadas nem dos pressupostos do modelo.")
H("7.6. Modelo mais adequado", 2)
P("Consideramos o modelo múltiplo (M2) o mais adequado para responder à questão de investigação: só ele permite avaliar como a relação "
  "se altera quando se consideram outros fatores; explica quase cinco vezes mais variabilidade com o mesmo número de observações e "
  "tem o melhor AIC, BIC e erro de previsão em validação cruzada, mesmo face a um modelo com mais variáveis; "
  "corrige a atribuição indevida à IA de uma associação que pertence sobretudo à experiência; e é simples, usa apenas fatores "
  "anteriores ao desempenho e cumpre razoavelmente os pressupostos. O modelo simples mantém valor descritivo (a associação bruta), "
  "mas não explicativo.")

# ------------------------------------------------------------------ 8
H("8. Conclusões")
P("Seguindo a nota final do enunciado, separamos as conclusões em quatro níveis:")
T(["Nível", "Conclusão"], [
    ["Descritivo", "Quem usa mais IA tende a ser ligeiramente mais produtivo (mediana 73,0 no 1.º quartil de uso contra 84,9 no 4.º), "
     "mas com grande variabilidade individual. Os departamentos têm produtividades semelhantes; Desenvolvimento usa mais IA sem ser o mais produtivo."],
    ["Inferencial", "Associação positiva, fraca e significativa (r = 0,24; p < 0,001). Sem diferenças entre departamentos (ANOVA p = 0,70; Welch p = 0,68; Kruskal-Wallis p = 0,71). "
     "Produtividade média: IC 95% [76,4 ; 79,7]."],
    ["Explicação estatística", "Controlando experiência, formação e complexidade, o coeficiente da IA cai cerca de 80% e deixa de ser significativo "
     "(0,13; p = 0,47). A experiência é o principal fator associado à produtividade (mais 1,6 pontos por ano)."],
    ["Recomendação", "Não tornar a IA obrigatória; investir em formação; avaliar o efeito causal com um estudo piloto controlado."],
], larg=[3.8, 12.4], nota="Tabela 9 – Síntese das conclusões por nível de análise.")
H("8.1. Os colaboradores que utilizam mais IA são mais produtivos?", 2)
P("Descritivamente sim, mas pouco. Existe uma associação positiva, fraca e estatisticamente significativa (r = 0,24; ρ = 0,27), que "
  "explica cerca de 6% da variabilidade da produtividade, e há numerosos contraexemplos (C134, com 25 h, tem 71,6; C014, com 4,9 h, "
  "tem 98). A afirmação da direção é verdadeira como tendência média, mas enganadora como regra individual.")
H("8.2. A relação mantém-se quando se consideram outros fatores?", 2)
P("Não. Ao comparar colaboradores com a mesma experiência, formação em IA e complexidade de tarefas, a associação entre uso "
  "de IA e produtividade é pequena e não significativa (0,13 pontos por hora; IC 95% de −0,22 a 0,48). O resultado mantém-se sem C097, "
  "com a carga de trabalho e o departamento no modelo, com erros-padrão robustos (HC3) e por bootstrap.")
H("8.3. Resultado mais inesperado", 2)
P("O que mais nos surpreendeu foi o desaparecimento quase total da associação da IA quando se controlam outros fatores, apesar de a "
  "associação bruta ser claramente significativa (b = 0,639, p < 0,001, contra b = 0,129, p = 0,47, com os mesmos 233 colaboradores). "
  "Como os VIF são baixos (< 1,6), a explicação não é a multicolinearidade, mas o facto de os mais experientes usarem mais IA "
  "(r = 0,27) e serem mais produtivos (r = 0,50). Também nos surpreendeu que o colaborador que mais usa IA esteja abaixo da média e "
  "que o departamento que mais usa IA não se distinga em produtividade.")
H("8.4. Limitações", 2)
B("Desenho observacional e transversal: uma única medição, sem atribuição aleatória do uso de IA. Não permite inferir causalidade nem "
  "excluir causalidade inversa ou fatores de confusão não medidos (motivação, competência digital, tipo de tarefa, qualidade da ferramenta).",
  "Qualidade e medição dos dados: dados sintéticos; índice de produtividade de construção desconhecida (provavelmente ligado a "
  "tarefas, tempo e qualidade); efeitos de teto e de chão (13 colaboradores em 98, 34 com 0,40 h por tarefa) que comprimem a "
  "variabilidade no topo; um valor suspeito (C097); e o uso de IA mede quantidade (horas), não a adequação ou a qualidade do uso.")
P("Além disso, o modelo final deixa cerca de 73% da variabilidade por explicar e a complexidade, que é ordinal, foi tratada como numérica "
  "(a análise de robustez mostrou que tratá-la como categórica não altera as conclusões).")
H("8.5. Recomendação à direção: tornar obrigatório o uso de IA?", 2)
P("Não recomendamos tornar obrigatória a utilização de IA com base nestes resultados. A evidência é de associação, não de "
  "causalidade: a associação bruta já é fraca e desaparece quando se comparam colaboradores com experiência e formação semelhantes. "
  "Mesmo aceitando o modelo simples, impor mais 5 h semanais de IA estaria associado, no máximo, a cerca de 3 pontos de produtividade, com "
  "custos (tempo, licenças, resistência à mudança) que não avaliámos. Uma obrigação uniforme ignora ainda que o benefício pode depender "
  "do tipo de tarefa e da competência de cada colaborador.")
P("Em alternativa, sugerimos: (1) manter a IA disponível e opcional; (2) investir em formação de qualidade, cuja associação "
  "com a produtividade é positiva, ainda que marginal; (3) realizar um estudo piloto controlado, por exemplo com atribuição aleatória de acesso "
  "e formação a equipas comparáveis e medição antes e depois, para estimar o efeito causal; (4) melhorar a medição da "
  "produtividade (sem teto) e do tipo de uso de IA.")
P("Respondendo à questão central: o uso de IA está associado positivamente, mas de forma fraca, à produtividade, e essa associação "
  "deve-se sobretudo ao facto de os colaboradores que mais usam IA serem também mais experientes e formados. Nestes dados, trabalhar "
  "com IA não significa, por si só, trabalhar melhor.")

# ------------------------------------------------------------------ refs
H("Referências")
for r in ["Coelho, L. (2026). *Modelos Estatísticos para Inteligência Artificial*, Aulas 1 a 5 e guia de testes paramétricos e não paramétricos (material de apoio da UC). Mestrado em Inteligência Artificial, IPCA.",
          "Montgomery, D. C., Peck, E. A., & Vining, G. G. (2021). *Introduction to linear regression analysis* (6.ª ed.). Wiley.",
          "Seabold, S., & Perktold, J. (2010). statsmodels: Econometric and statistical modeling with Python. *Proceedings of the 9th Python in Science Conference*.",
          "Virtanen, P., et al. (2020). SciPy 1.0: Fundamental algorithms for scientific computing in Python. *Nature Methods, 17*, 261–272."]:
    par = P(r, align=WD_ALIGN_PARAGRAPH.LEFT); par.paragraph_format.left_indent = Cm(0.8); par.paragraph_format.first_line_indent = Cm(-0.8)
H("Anexo – Notebook", 2)
P("Todo o código, outputs e interpretações por pergunta (1.1 a 7.5) estão no notebook **TP1_MEPA_IA_Produtividade.ipynb**, "
  "versionado no repositório GitHub do grupo e executável no Google Colab (dados lidos do próprio repositório) ou localmente "
  "(instruções na secção 0 do notebook).", align=WD_ALIGN_PARAGRAPH.LEFT)
H("Anexo – Correspondência com as perguntas do enunciado", 2)
T(["Perguntas do enunciado", "Onde estão respondidas neste relatório"], [
    ["1.1 a 1.6 – Conhecimento e preparação da base de dados", "1.1 e 1.4: secção 2.1 e Tabela 1; 1.2, 1.3 e 1.5: secção 2.2 e Tabela 2; 1.6: secção 2.3"],
    ["2.1 a 2.5 – Caracterização dos colaboradores", "Secção 3: Tabela 3 (2.1 e 2.2), Figura 1 (2.2), parágrafo «Departamentos» (2.3), Figura 2 e parágrafo «Simetria» (2.4), parágrafo «Máximos» (2.5)"],
    ["3.1 a 3.5 – Associação entre IA e produtividade", "Secção 4: Figura 3 e «Tendência» (3.1), Tabela 4 e «Medida de associação» (3.2), «Classificação» (3.3), exemplos concretos (3.4), «Associação não é causalidade» (3.5)"],
    ["4.1 a 4.6 – Diferenças entre departamentos e intervalo de confiança", "Secção 5: Figura 4 (4.1), «Hipóteses» (4.2), «Condições de aplicação» (4.3), Tabela 5 e «Interpretação do valor-p» (4.4), «O que se pode e não pode afirmar» (4.5), «Intervalo de confiança» (4.6)"],
    ["5.1 a 5.6 – Regressão linear simples", "Secção 6: equação e coeficientes (5.1 e 5.2), «5 h vs 10 h» (5.3), «Capacidade explicativa» (5.4), «Um colaborador concreto» (5.5), Figura 5 e «Análise de resíduos» (5.6)"],
    ["6.1 a 6.7 – Regressão linear múltipla", "Secções 7.1 (6.1 e 6.2, Figura 6), 7.2 (6.2 e 6.3, Tabela 6), 7.3 (6.4, Figura 7), 7.4 (6.5, Tabela 7), 7.5 (6.6, Figura 8 e Tabela 8) e 7.6 (6.7)"],
    ["7.1 a 7.5 – Conclusão da investigação", "Secções 8.1 a 8.5 e Tabela 9 (níveis descritivo, inferencial, explicação estatística e recomendação)"],
], larg=[6.0, 10.2], nota="Tabela 10 – Correspondência entre as perguntas do enunciado e as secções do relatório. O notebook segue diretamente a numeração do enunciado.")

# rodapé com numeração
from docx.oxml import OxmlElement as E
fp = sec.footer.paragraphs[0]; fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
for tag, txt in (("begin", None), (None, "PAGE"), ("end", None)):
    r = fp.add_run()
    if tag:
        f = E("w:fldChar"); f.set(qn("w:fldCharType"), tag); r._r.append(f)
    else:
        i = E("w:instrText"); i.set(qn("xml:space"), "preserve"); i.text = txt; r._r.append(i)
sec.different_first_page_header_footer = True

doc.save(os.path.join(PASTA, "Relatorio_TP1_MEPA_IA_Produtividade.docx"))
print("ok")
