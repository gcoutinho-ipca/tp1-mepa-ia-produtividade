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
    for row in (t.rows if nota else t.rows[:-1]):   # manter a tabela (e a legenda) na mesma página
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
P("Neste trabalho quisemos perceber se os colaboradores que usam mais ferramentas de Inteligência Artificial (IA) são também "
  "os mais produtivos, e se essa relação se mantém quando se têm em conta outros fatores, como a experiência e a formação. "
  "Usámos uma base de 240 colaboradores de uma empresa tecnológica (dados sintéticos). Depois de limpar os dados (uma linha "
  "repetida, nomes de departamentos mal escritos e 8 valores em falta), encontrámos uma relação positiva mas fraca entre as "
  "horas semanais de IA e a produtividade (r = 0,24; p < 0,001): o uso de IA explica só cerca de 6% das diferenças de "
  "produtividade. Os departamentos não diferem entre si (ANOVA, p = 0,70). Quando comparamos colaboradores com a mesma "
  "experiência, formação em IA e complexidade de tarefas, o efeito associado à IA cai cerca de 80% (de 0,64 para 0,13 pontos "
  "por hora) e deixa de ser estatisticamente significativo (p = 0,47). O fator mais ligado à produtividade é a experiência "
  "(mais 1,6 pontos por ano; p < 0,001). A vantagem de quem usa mais IA explica-se sobretudo por serem pessoas mais "
  "experientes e com mais formação, pelo que não recomendamos tornar o uso de IA obrigatório com base nestes dados.")
P("**Palavras-chave:** inteligência artificial; produtividade; correlação; ANOVA; regressão linear múltipla; fatores de confusão.",
  align=WD_ALIGN_PARAGRAPH.LEFT)

# ------------------------------------------------------------------ 1
H("1. O problema e o plano da investigação")
P("A direção de uma empresa tecnológica acredita que os colaboradores que mais usam IA são também os mais produtivos. "
  "A pergunta deste trabalho é: *em que medida a utilização de ferramentas de IA está associada à produtividade dos "
  "colaboradores e como se altera essa relação quando são considerados outros fatores individuais e profissionais?* "
  "Não partimos para provar que a IA aumenta a produtividade. O objetivo foi ver o que os dados permitem, e não permitem, dizer.")
P("Seguimos as etapas do enunciado, das mais simples às mais exigentes, de forma que cada uma preparasse a seguinte:")
B("preparar os dados: linhas repetidas, valores em falta, categorias mal escritas, valores estranhos e limites da escala;",
  "descrever a produtividade e o uso de IA, no total e por departamento;",
  "ver se as duas variáveis andam juntas, com um gráfico de dispersão e as correlações de Pearson e de Spearman;",
  "inferência: comparar os departamentos (ANOVA, confirmada pela ANOVA de Welch e pelo teste de Kruskal-Wallis) e estimar a produtividade média com um intervalo de confiança;",
  "explicação: uma regressão linear simples (só com o uso de IA) e uma regressão múltipla com fatores que vêm antes do desempenho, comparando as duas e verificando os seus pressupostos;",
  "conclusões e recomendações, separando associação de causa.", num=True)
P("Só usámos métodos dados nas aulas e nos materiais de apoio da docente (guiões de código e infográficos). Cada escolha foi "
  "feita antes de olhar para o resultado, como a docente recomenda. A análise foi feita em Python (pandas, SciPy, statsmodels, "
  "matplotlib e seaborn) num notebook do Google Colab, entregue com este relatório; todas as figuras foram geradas por esse "
  "notebook. Usámos um nível de significância de 5%. Como os dados são sintéticos, as conclusões ilustram um raciocínio "
  "estatístico e não descrevem uma empresa real.")

# ------------------------------------------------------------------ 2
H("2. Conhecer e preparar os dados")
H("2.1. Estrutura, registos e colaboradores", 2)
P("A base tem **241 linhas** e 11 variáveis, mas só **240 códigos de colaborador diferentes** (de C001 a C240). O Excel inclui "
  "também um dicionário de dados, que usámos para confirmar o tipo de cada variável (Tabela 1). Duas informações do dicionário "
  "foram importantes: a produtividade é uma **avaliação global feita por avaliadores, não calculada a partir das outras "
  "colunas**; e tarefas concluídas, tempo por tarefa e qualidade são **indicadores do mesmo desempenho, medidos ao mesmo tempo**. "
  "A variável que queremos explicar é a produtividade (0 a 100); a que nos interessa como explicação é o uso de IA, em horas por semana.")
T(["Variável", "Tipo", "Papel na investigação"], [
    ["id_colaborador", "Identificador", "Não analisada"],
    ["departamento", "Qualitativa nominal (4 categorias)", "Fator de contexto"],
    ["complexidade_tarefas", "Qualitativa ordinal (1–5)", "Fator anterior (controlo)"],
    ["experiencia_anos", "Quantitativa contínua", "Fator anterior"],
    ["formacao_ia_horas", "Quantitativa contínua", "Fator anterior"],
    ["uso_ia_horas", "Quantitativa contínua", "**Explicativa de interesse**"],
    ["carga_trabalho_horas", "Quantitativa contínua", "Fator de contexto"],
    ["tarefas_concluidas", "Quantitativa discreta", "Indicador do mesmo desempenho"],
    ["tempo_medio_tarefa_horas", "Quantitativa contínua", "Indicador do mesmo desempenho"],
    ["qualidade_trabalho", "Quantitativa contínua (0–100)", "Indicador do mesmo desempenho"],
    ["produtividade", "Quantitativa contínua (0–100)", "**Variável resposta**"],
], larg=[4.6, 6.0, 5.6], nota="Tabela 1 – Tipos de variáveis e papel na investigação. A complexidade, embora ordinal, é tratada como número nos modelos (supõe níveis igualmente espaçados; verificado na secção 7.5).")

H("2.2. Problemas encontrados e decisões", 2)
T(["Problema", "O que vimos", "O que decidimos e porquê"], [
    ["Colaborador repetido", "C084 aparece 2 vezes, com valores iguais em tudo",
     "Ficou uma só linha: é a mesma pessoa copiada (o dicionário diz que cada pessoa aparece uma vez)"],
    ["Valores em falta", "8 valores, um em cada um de 8 registos: produtividade (2), uso de IA (2), experiência, formação, complexidade e tempo médio (1 cada)",
     "Não preenchemos (seria inventar dados); cada análise usa quem tem a informação de que precisa (ver 2.3)"],
    ["Departamentos mal escritos", "«desenvolvimento», «Operacoes», «Analise de Dados» (1 registo cada)",
     "Corrigidos: ficam os 4 departamentos do dicionário (85, 66, 58 e 31 pessoas)"],
    ["Teto na escala", "13 colaboradores com produtividade 98 (o máximo); 34 com o tempo mínimo por tarefa; 9 com qualidade 100",
     "Mantidos; fica como limitação (não se distinguem os melhores)"],
    ["Valor estranho na produtividade", "C097 tem 19 (o seguinte é 43,5), o que não bate certo com as suas 34 tarefas e qualidade 71",
     "Mantido (não se prova que é erro); análises principais repetidas sem ele"],
    ["Uso de IA muito alto", "C134 (25 h) e C035 (24,8 h) para lá do bigode da caixa (21,2 h)",
     "Mantidos (valores possíveis); verificámos que não pesam demasiado nos modelos"],
], larg=[3.3, 6.4, 6.5], nota="Tabela 2 – Síntese da preparação dos dados.")
P("Não há valores impossíveis (negativos, produtividade acima de 100 ou mais horas de IA do que de trabalho). Os 11 "
  "colaboradores que não usam IA (0 h) são um valor possível e foram mantidos.")

H("2.3. Faz sentido deixar de fora os registos com falhas?", 2)
P("Ficam **240 colaboradores**; nenhum foi excluído por inteiro. Cada um dos 8 registos com uma falha só sai das análises "
  "de que lhe falta informação (Tabela 3), por isso o número de casos varia: 238 com produtividade, 236 com uso de IA e "
  "produtividade, e 233 com todas as variáveis do modelo múltiplo.")
T(["Registos", "O que falta", "De que análises saem", "Faz sentido?"], [
    ["C154", "Tempo médio por tarefa", "Nenhuma", "Sim: a variável não é usada nos modelos"],
    ["C080, C189, C202", "Experiência, formação, complexidade", "Só da regressão múltipla", "Sim: entram em tudo o resto"],
    ["C067, C113", "Uso de IA", "Correlação e regressões", "Sim: preencher seria inventar a variável que estudamos"],
    ["C030, C131", "Produtividade", "Tudo o que usa a produtividade", "Sim: preencher seria inventar o resultado"],
], larg=[3.2, 4.0, 4.3, 4.7], nota="Tabela 3 – Avaliação dos registos com valores em falta.")
P("Os 6 registos incompletos com produtividade conhecida têm uma produtividade média um pouco mais alta (86,0 contra 77,8), mas "
  "são só 6 em 240. O que interessa é saber se a saída destes casos muda os resultados, e não muda: a correlação entre IA e "
  "produtividade é praticamente igual com 236 casos (r = 0,241) e com os 233 do modelo múltiplo (r = 0,246). Também não faz "
  "sentido retirar nenhuma variável do estudo por causa das faltas, porque em nenhuma faltam mais de 2 valores. Para comparar "
  "os dois modelos de regressão de forma justa, voltámos a estimar o modelo simples com os mesmos 233 casos.")

# ------------------------------------------------------------------ 3
H("3. Quem são os colaboradores (análise descritiva)")
T(["Estatística", "Produtividade", "Uso de IA (h/semana)"], [
    ["n", "238", "238"], ["Média", "78,03", "7,72"], ["Mediana", "79,35", "7,60"],
    ["Desvio-padrão", "12,84", "4,93"], ["Mínimo – Máximo", "19,0 – 98,0", "0,0 – 25,0"],
    ["Q1 – Q3", "70,2 – 87,5", "3,8 – 10,8"],
], larg=[5.5, 5.0, 5.0], nota="Tabela 4 – Estatísticas descritivas da produtividade e do uso de IA.")
P("**Produtividade média.** É de 78,0 pontos (desvio-padrão 12,8). A média representa bem os dados: está perto da mediana "
  "(79,35) e metade dos colaboradores tem entre 70,2 e 87,5. Fica um pouco abaixo da mediana por causa de alguns valores muito "
  "baixos (C097 = 19; C129 = 43,5), por isso a mediana descreve um pouco melhor o colaborador típico.")
P("**Uso de IA.** Em média, os colaboradores usam IA 7,7 h por semana (mediana 7,6 h), com bastante variação (desvio-padrão "
  "4,9 h). Há mais gente com poucas horas e alguns com muitas. Dois colaboradores ficam para lá do bigode da caixa: C134 (25,0 h) "
  "e C035 (24,8 h) (Figura 1).")
F("fig_2_2_uso_ia.png", "Distribuição do uso semanal de IA (histograma e caixa de bigodes).", 15)
P("**Departamentos.** O mais produtivo é Operações (média 79,2), seguido de Comunicação (78,6), Desenvolvimento (78,0) e Análise "
  "de Dados (76,5). O que mais usa IA é Desenvolvimento (9,0 h por semana); Operações vem em segundo (7,2 h). O departamento mais "
  "produtivo não é, portanto, o que mais usa IA. As diferenças de produtividade (no máximo 2,7 pontos) são pequenas face à "
  "variação dentro de cada departamento (desvios-padrão entre 11,6 e 14,0).")
P("**Simetria da produtividade.** A distribuição não é bem simétrica. A cauda esquerda é mais comprida, a média fica abaixo da "
  "mediana e, no gráfico Q-Q, os pontos afastam-se da reta na ponta de baixo (Figura 2). Na ponta de cima vê-se o teto em 98. "
  "O teste de Shapiro-Wilk confirma que a distribuição não é normal (p < 0,001), mesmo sem o C097. Por isso, ao lado de cada "
  "teste que supõe normalidade, usámos um teste de confirmação que não a exige.")
F("fig_2_4_produtividade.png", "Distribuição da produtividade: histograma com média e mediana, caixa de bigodes e gráfico Q-Q.")
P("**Mais produtivo e quem mais usa IA.** A produtividade máxima (98) é atingida por 13 colaboradores, com usos de IA entre "
  "4,9 h (C014) e 16,3 h (C036); vários têm muita experiência (C014, C015 e C178, com 19 anos). Se for preciso escolher um só, o "
  "desempate pela qualidade e depois pelas tarefas concluídas indica o C237 (Desenvolvimento; qualidade 100, 40 tarefas, 12,7 h "
  "de IA). Quem mais usa IA (C134, 25 h) tem produtividade 71,6, abaixo da média: cerca de 71% dos colaboradores são mais "
  "produtivos do que ele. Não são as mesmas pessoas. Usar muita IA não garante ser muito produtivo; se houver relação, será uma "
  "tendência média.")

# ------------------------------------------------------------------ 4
H("4. O uso de IA anda junto com a produtividade?")
F("fig_3_1_dispersao.png", "Uso de IA vs produtividade (com a reta de mínimos quadrados) e produtividade por quartil de uso de IA.")
P("**Tendência.** A Figura 3 mostra uma tendência a subir, mas fraca: a mediana da produtividade passa de 73,0 no quarto de "
  "colaboradores que menos usa IA para 84,9 no quarto que mais usa. A dispersão é, porém, enorme em qualquer nível de uso (com "
  "cerca de 8 h por semana há produtividades entre 19 e 98) e não se vê nenhuma curva, por isso uma reta descreve razoavelmente "
  "a tendência.")
P("**Que medida usámos e porquê.** As duas variáveis são quantitativas e a relação é aproximadamente em linha reta, por isso "
  "usámos o coeficiente de correlação de Pearson. Como a produtividade não é normal, tem valores afastados e um teto, calculámos "
  "também o de Spearman, que usa as posições dos valores e é menos sensível a esses problemas, como a docente recomenda.")
T(["Medida", "Valor", "Valor-p"], [
    ["r de Pearson", "0,241", "< 0,001"], ["ρ de Spearman", "0,266", "< 0,001"],
    ["r de Pearson sem C097", "0,252", "< 0,001"], ["r² (variação partilhada)", "0,058", "—"],
], larg=[6.5, 4.0, 4.0], nota="Tabela 5 – Associação entre uso de IA e produtividade (n = 236).")
P("**Classificação.** A associação é positiva e **fraca**: na escala dos infográficos da docente, valores entre 0,2 e 0,4 são "
  "uma associação fraca. O uso de IA acompanha só cerca de 6% da variação da produtividade. A associação é estatisticamente "
  "significativa porque, com 236 pessoas, até uma relação fraca se distingue do zero; significativo não quer dizer forte.")
P("**Quem mais usa IA é sempre o mais produtivo?** Não. O C134 (25 h) tem 71,6; o C078 (18 h) tem 58,7; o C004 (16,3 h) tem 70,3. "
  "No sentido contrário, o C014 (4,9 h) atinge 98 e o C053 (0 h) tem 90. Entre os 11 que não usam IA, a produtividade vai de "
  "48,9 (C238) a 90,0 (C053).")
P("**Associação não é causa.** Os dados foram recolhidos num único momento e ninguém decidiu ao acaso quem usava IA. A relação "
  "positiva pode dever-se a (i) um terceiro fator que influencia as duas coisas, como a experiência, ligada ao uso de IA "
  "(r = 0,27) e à produtividade (r = 0,50); (ii) causa ao contrário, se os mais produtivos tiverem mais margem para experimentar "
  "a IA; (iii) escolha pessoal de quem adota a ferramenta. Não podemos, por isso, dizer que a IA aumenta a produtividade.")

# ------------------------------------------------------------------ 5
H("5. Diferenças entre departamentos e produtividade média (inferência)")
F("fig_4_1_departamentos.png", "Produtividade por departamento (caixas de bigodes, colaboradores e médias).", 14)
P("**Hipóteses.** Sendo μ_AD, μ_C, μ_D e μ_O as produtividades médias de cada departamento na população: "
  "H₀: μ_AD = μ_C = μ_D = μ_O; H₁: pelo menos duas médias são diferentes.")
P("**Condições da ANOVA a um fator.** (1) *Independência*: garantida pela recolha (cada colaborador aparece uma vez e pertence "
  "a um só departamento). (2) *Normalidade em cada grupo* (Shapiro-Wilk): não rejeitada em Análise de Dados (p = 0,36), Comunicação "
  "(p = 0,32) e Operações (p = 0,06); rejeitada em Desenvolvimento (p < 0,001), o grupo do C097 (sem ele o desvio é menor, mas o "
  "teste continua a rejeitar, p = 0,03). Como a docente sublinha, a decisão não depende só do valor-p: os grupos são grandes "
  "(31 a 85) e a ANOVA aguenta bem desvios moderados da normalidade com grupos grandes e variâncias parecidas. (3) *Variâncias "
  "iguais*: o teste de Levene dá p = 0,52, não rejeitada; os desvios-padrão vão de 11,6 a 14,0.")
P("**Escolha do teste.** Seguimos o fluxograma da docente: com o Levene a não rejeitar a igualdade das variâncias, o teste "
  "indicado é a ANOVA a um fator. Juntámos duas confirmações dos mesmos materiais: a ANOVA de Welch, que não exige variâncias "
  "iguais (os grupos têm tamanhos muito diferentes), e o teste de Kruskal-Wallis, que não exige normalidade. Não fizemos testes t "
  "entre todos os pares de departamentos: seriam 6 testes e o risco de encontrar uma diferença «falsa» subia para cerca de 26%.")
T(["Teste", "Estatística", "Valor-p"], [
    ["ANOVA a um fator", "F(3, 234) = 0,47", "0,702"],
    ["ANOVA de Welch", "F(3; 105,7) = 0,50", "0,681"],
    ["Kruskal-Wallis", "H(3) = 1,37", "0,713"],
    ["ANOVA sem C097", "—", "0,632"],
], larg=[5.5, 5.0, 4.0], nota="Tabela 6 – Comparação da produtividade entre departamentos.")
P("**Como se lê o valor-p.** Um valor-p de 0,70 quer dizer que, se a produtividade média fosse mesmo igual nos quatro "
  "departamentos, diferenças como as observadas (ou maiores) apareceriam em cerca de 70% das amostras. Como p > 0,05, não "
  "rejeitamos H₀. Os três testes concordam e o resultado não depende do C097. O tamanho do efeito confirma: η² = 0,006, ou seja, "
  "o departamento explica só 0,6% da variação da produtividade, abaixo do limiar de efeito pequeno (0,01) dado pela docente. "
  "Como a ANOVA não rejeitou H₀, não se fazem comparações par a par (Tukey).")
P("**O que se pode e não pode afirmar.** Não há evidência de diferenças entre departamentos, mas isso não prova que as médias "
  "sejam iguais: pode haver pequenas diferenças (2 a 3 pontos) que estes dados não detetam, sobretudo em Comunicação (31 pessoas). "
  "Fica por esclarecer se a IA tem o mesmo efeito em todos os departamentos, se a avaliação de produtividade é comparável entre "
  "trabalhos diferentes e se as diferenças de experiência e formação entre departamentos escondem diferenças reais. Uma conclusão "
  "útil: o departamento não deve estar por trás da relação entre IA e produtividade.")
P("**Intervalo de confiança.** A produtividade média estimada é 78,03 (erro-padrão 0,83), com IC 95% = [76,4 ; 79,7], calculado "
  "com a distribuição t de Student porque não conhecemos o desvio-padrão da população. Se a recolha fosse repetida muitas vezes, "
  "cerca de 95% dos intervalos calculados desta forma conteriam a verdadeira média. O intervalo é estreito, logo a média está bem "
  "estimada; atenção que é um intervalo para a média e não diz onde estão 95% dos colaboradores. Como os dados são sintéticos, a "
  "«população» é o processo que gerou os dados; o intervalo mede só a incerteza de trabalhar com uma amostra e não cobre erros "
  "de medição, o teto em 98 ou eventuais erros de registo.")

# ------------------------------------------------------------------ 6
H("6. Regressão linear simples: a IA explica a produtividade?")
P("Estimámos por mínimos quadrados o modelo produtividade = β₀ + β₁·uso_IA + ε (n = 236). O teste ao declive rejeita H₀: β₁ = 0 "
  "(t = 3,80; p < 0,001), por isso é possível escrever a equação:")
P("**produtividade estimada = 73,04 + 0,627 × uso_ia_horas**", align=WD_ALIGN_PARAGRAPH.CENTER)
B("b₀ = 73,04 (IC 95%: 70,0 a 76,0): produtividade média estimada para quem não usa IA (0 h), situação que existe em 11 colaboradores.",
  "b₁ = 0,627 (IC 95%: 0,30 a 0,95; p < 0,001): por cada hora semanal a mais de IA, a produtividade média estimada é 0,63 pontos "
  "mais alta. É uma comparação entre pessoas diferentes, não o que acontece a uma pessoa se passar a usar mais IA.")
P("**5 h vs 10 h.** O modelo estima 76,2 (5 h) e 79,3 (10 h): uma diferença de 5 × 0,627 ≈ 3,1 pontos (IC 95%: 1,5 a 4,8). Esta "
  "comparação fala da média de colaboradores com esse uso, não de duas pessoas concretas (para uma pessoa com 5 h, o intervalo de "
  "previsão vai de cerca de 52 a 101); não mantém nada constante (quem usa 10 h tende a ter mais experiência e formação); é uma "
  "associação e não um efeito causal; e não há extrapolação, porque os dois valores estão dentro dos observados (0 a 25 h). O limite "
  "de cima do intervalo de previsão passa de 100 (até 103,9 com 10 h), o que é impossível na escala: a reta não sabe que a escala "
  "acaba em 100, mais um sinal do teto em 98 e de que o modelo não serve para prever pessoas concretas.")
P("**Quanto explica.** R² = 0,058 (R² ajustado = 0,054): o uso de IA explica cerca de 6% da variação da produtividade. Saber as "
  "horas de IA de alguém ajuda muito pouco a prever a sua produtividade; como a docente avisa, um declive significativo não quer "
  "dizer que o modelo explique muito.")
P("**Um colaborador concreto (C001).** O C001 (Operações) usa IA 7,7 h por semana; o modelo prevê 73,04 + 0,627 × 7,7 ≈ 77,9, mas "
  "a produtividade real é 68,0. O resíduo de −9,9 pontos é a parte da produtividade que o uso de IA não explica: o C001 está cerca "
  "de 10 pontos abaixo de um colaborador típico com o mesmo uso. Uma pista: tem apenas meio ano de experiência.")
F("fig_5_6_residuos_m1.png", "Análise dos resíduos do modelo simples (M1).")
P("**Análise dos resíduos.** Seguimos a ordem das aulas 4 e 5: primeiro os gráficos, depois os testes. No gráfico dos resíduos "
  "contra os valores ajustados não há curva nem forma de funil, e o teste de Breusch-Pagan não deteta variância desigual (p = 0,98). "
  "A independência vem da forma como os dados foram recolhidos (um registo por colaborador, num único momento); o Durbin-Watson "
  "(1,84) é apresentado só por completude, porque, como a docente explica, sem ordem no tempo é apenas descritivo. A normalidade "
  "dos resíduos é rejeitada (Shapiro-Wilk p < 0,001): o histograma e o Q-Q mostram uma cauda comprida à esquerda, com o C097 "
  "(resíduo −58,9) e o C129 (−36,8); sem o C097 o problema diminui (p = 0,03) e o declive fica igual (0,63). A distância de Cook "
  "máxima é 0,06 (C134); sete observações passam a referência 4/n da aula 5, mas nenhuma muda o modelo. "
  "O problema principal, porém, é o que falta ao modelo: R² = 0,06, resíduos entre −59 e +24 pontos e uma correlação de 0,45 "
  "(p < 0,001) entre os resíduos e a experiência. O modelo deixou de fora uma variável importante. Descreve uma tendência média, "
  "mas não explica nem prevê a produtividade de cada pessoa.")

# ------------------------------------------------------------------ 7
H("7. Regressão linear múltipla: a IA explica tudo?")
H("7.1. Que variáveis entram no modelo", 2)
F("fig_6_1_correlacoes.png", "Matriz de correlações de Pearson entre as variáveis quantitativas.", 12.5)
P("Além do uso de IA, a produtividade está ligada à experiência (0,50), à qualidade (0,46), às tarefas concluídas (0,44) e ao "
  "tempo médio por tarefa (−0,48) (Figura 6). Estas três últimas não entram no modelo. O dicionário da base diz que são "
  "**indicadores do mesmo desempenho, medidos ao mesmo tempo**: a produtividade não é calculada a partir delas, mas mede a mesma "
  "coisa vista de outro ângulo. Incluí-las teria três problemas: redundância (explicar o desempenho com outras medidas do "
  "desempenho faz subir o R² sem ensinar nada); esconder o efeito que queremos estudar (se a IA ajudar através de mais tarefas ou "
  "de menos tempo por tarefa, pô-las no modelo apagaria esse efeito); e não servem para decidir, porque a direção não escolhe à "
  "partida quantas tarefas alguém conclui.")
P("Entraram, com o uso de IA, três variáveis que vêm antes do desempenho e que o enunciado aponta como possíveis influências: "
  "a experiência (ligada à produtividade e ao uso de IA, logo possível fator de confusão, isto é, algo que influencia as duas "
  "coisas ao mesmo tempo), a formação em IA (muito ligada ao uso de IA, r = 0,51) e a complexidade das tarefas (característica do "
  "posto de trabalho). A carga de trabalho e o departamento, pouco ligados à produtividade, ficaram para um teste de robustez.")
H("7.2. Modelo estimado", 2)
T(["Variável", "Coeficiente", "Erro-padrão", "t", "Valor-p", "IC 95%"], [
    ["Constante", "67,32", "2,60", "25,86", "< 0,001", "62,19 a 72,45"],
    ["Uso de IA (h/sem.)", "**0,129**", "0,179", "0,72", "**0,471**", "−0,22 a 0,48"],
    ["Experiência (anos)", "1,584", "0,190", "8,32", "< 0,001", "1,21 a 1,96"],
    ["Formação em IA (h)", "0,231", "0,122", "1,90", "0,059", "−0,01 a 0,47"],
    ["Complexidade (1–5)", "−0,661", "0,716", "−0,92", "0,357", "−2,07 a 0,75"],
], larg=[3.8, 2.4, 2.4, 1.8, 2.2, 3.6],
  nota="Tabela 7 – Modelo de regressão múltipla M2 (n = 233; R² = 0,280; R² ajustado = 0,267; F(4, 228) = 22,1; p < 0,001).")
P("**produtividade estimada = 67,32 + 0,129·uso_IA + 1,584·experiência + 0,231·formação_IA − 0,661·complexidade**",
  align=WD_ALIGN_PARAGRAPH.CENTER)
P("**Coeficiente da IA.** Comparando colaboradores com a mesma experiência, formação em IA e complexidade de tarefas, cada hora "
  "semanal a mais de IA corresponde a uma produtividade média só 0,13 pontos mais alta, um valor não significativo (p = 0,47) cujo "
  "intervalo de confiança inclui o zero e valores negativos. A experiência é a única variável claramente significativa (mais 1,58 "
  "pontos por ano); a formação em IA tem uma relação positiva à beira da significância (p = 0,059); a complexidade não é "
  "significativa. A constante não tem leitura prática (complexidade 0 não existe). Como as variáveis estão em unidades diferentes "
  "(anos, horas, níveis), não as ordenamos por importância pelo tamanho dos coeficientes, como a docente alerta na aula 5.")
H("7.3. O que acontece ao coeficiente da IA", 2)
F("fig_6_4_coeficiente_ia.png", "Coeficiente do uso de IA (e IC 95%) à medida que se juntam variáveis ao modelo (mesmos 233 casos).", 14)
P("Com os mesmos 233 casos, o coeficiente da IA passa de 0,639 (p < 0,001) no modelo simples para 0,129 (p = 0,47) no modelo "
  "múltiplo, uma descida de cerca de 80%. A Figura 7 mostra que variável «rouba» a associação: juntar só a formação quase não muda "
  "o coeficiente (0,60), mas juntar a experiência corta-o para metade (0,31; p = 0,04), e experiência e formação juntas levam-no a "
  "0,13. A explicação está nas correlações: quem tem mais experiência e formação usa mais IA (r = 0,27 e 0,51) e a experiência está "
  "muito ligada à produtividade (r = 0,50). Quem usa mais IA é mais produtivo, mas sobretudo por ser mais experiente, e não por "
  "usar mais IA. É este o «paradoxo» do título.")
P("Uma ressalva: se a formação levar a usar mais IA e isso levar a mais produtividade, ao controlar a formação podemos estar a "
  "tirar à IA parte de um efeito real. Mesmo assim, controlando só a experiência, que não é consequência de usar IA, o coeficiente "
  "já cai para metade.")
H("7.4. Comparação dos dois modelos", 2)
T(["Critério", "M1: só IA", "M2: IA + 3 variáveis"], [
    ["n (mesmos casos)", "233", "233"], ["N.º de variáveis explicativas", "1", "4"],
    ["R²", "0,061", "0,280"], ["R² ajustado", "0,056", "**0,267**"],
    ["Teste F global", "F(1, 231) = 14,9; p < 0,001", "F(4, 228) = 22,1; p < 0,001"],
    ["Teste F parcial (M2 vs M1)", "—", "F(3, 228) = 23,1; p < 0,001"],
], larg=[5.5, 5.0, 5.5], nota="Tabela 8 – Comparação da capacidade explicativa dos modelos.")
P("Comparámos os modelos com os mesmos colaboradores, como se faz nas aulas, senão os R² não seriam comparáveis. O R² sobe "
  "sempre que se juntam variáveis, mesmo inúteis, por isso olhámos para o R² ajustado, que desconta o número de variáveis: sobe de "
  "0,056 para 0,267, quase cinco vezes. Com 233 pessoas para 4 variáveis (cerca de 58 por variável), o ganho não vem de termos "
  "complicado o modelo. O teste F parcial (aula 4) confirma que as três variáveis juntas melhoram o modelo: o erro que fica por "
  "explicar (soma dos quadrados dos resíduos) desce de 35 990 para 27 590 e F(3, 228) = 23,1 (p < 0,001). O modelo com mais "
  "variáveis é claramente melhor, embora cerca de 73% da variação continue por explicar.")
H("7.5. Pressupostos do modelo múltiplo e robustez", 2)
F("fig_6_6_residuos_m2.png", "Análise dos resíduos do modelo múltiplo (M2).")
P("**Relação entre as variáveis explicativas.** A correlação mais alta é entre uso de IA e formação (0,51); as restantes são fracas. "
  "Todos os VIF ficam abaixo de 1,6 (o maior é 1,51, no uso de IA) e, na referência da docente, valores entre 1 e 5 não preocupam. "
  "O erro-padrão do coeficiente da IA quase não muda (0,166 no modelo simples, 0,179 no múltiplo, com os mesmos 233 casos): a IA "
  "perde significância porque o modelo passa a ter em conta a experiência, não por multicolinearidade.")
P("**Resíduos.** Não há curva nem forma de funil nos resíduos contra os valores ajustados, e o Breusch-Pagan não deteta variância "
  "desigual (p = 0,19); a independência vem da forma como os dados foram recolhidos. A distância de Cook máxima é 0,07 (C097). A "
  "normalidade é rejeitada (p < 0,001), mas quase só por causa do C097, com um resíduo de −60,6: sem ele os resíduos são "
  "compatíveis com a normalidade (Shapiro-Wilk p = 0,97) e o coeficiente da IA quase não muda (0,146; p = 0,38).")
P("**Robustez das nossas escolhas.** Repetimos o modelo mudando as decisões que tomámos (Tabela 9). Em todas as versões o "
  "coeficiente da IA fica entre 0,12 e 0,15 e nunca é significativo. Tratar a complexidade como categoria não melhora o modelo "
  "(F(3, 225) = 1,55; p = 0,20), o que justifica tratá-la como número. O termo de interação IA × experiência é praticamente nulo: "
  "a IA não está mais ligada à produtividade nos experientes do que nos inexperientes.")
T(["Versão do modelo M2", "Coef. IA", "Valor-p", "R² ajustado"], [
    ["M2", "0,129", "0,471", "0,267"],
    ["M2 sem C097", "0,146", "0,384", "0,302"],
    ["M2 + carga de trabalho + departamento", "0,144", "0,446", "0,274"],
    ["M2 com complexidade como categoria", "0,122", "0,500", "0,272"],
    ["M2 + interação IA × experiência", "termo: 0,028", "0,499", "—"],
], larg=[7.0, 2.8, 2.8, 3.0], nota="Tabela 9 – Robustez: a conclusão sobre a IA não depende das escolhas feitas.")
H("7.6. Modelo mais adequado", 2)
P("Escolhemos o modelo múltiplo (M2) para responder à questão de investigação: só ele mostra como muda a relação quando se têm "
  "em conta outros fatores; explica quase cinco vezes mais com os mesmos colaboradores, e o teste F parcial confirma a melhoria; "
  "corrige o mérito que o modelo simples dava à IA e que é sobretudo da experiência; e é simples, usa só fatores que vêm antes do "
  "desempenho e cumpre razoavelmente os pressupostos. O modelo simples continua útil para descrever a relação «em bruto», mas não "
  "para a explicar.")

# ------------------------------------------------------------------ 8
H("8. Conclusões")
P("Como pede a nota final do enunciado, separamos as conclusões em quatro níveis:")
T(["Nível", "Conclusão"], [
    ["Descritivo", "Quem usa mais IA tende a ser um pouco mais produtivo (mediana 73,0 no quarto que menos usa contra 84,9 no que mais usa), "
     "mas com muitas exceções. Os departamentos têm produtividades parecidas; Desenvolvimento usa mais IA sem ser o mais produtivo."],
    ["Inferencial", "Associação positiva, fraca e significativa (r = 0,24; p < 0,001). Sem diferenças entre departamentos (ANOVA p = 0,70; Welch p = 0,68; Kruskal-Wallis p = 0,71). "
     "Produtividade média: IC 95% [76,4 ; 79,7]."],
    ["Explicação estatística", "Com a experiência, a formação e a complexidade no modelo, o coeficiente da IA cai cerca de 80% e deixa de ser significativo "
     "(0,13; p = 0,47). A experiência é o fator mais ligado à produtividade (mais 1,6 pontos por ano)."],
    ["Recomendação", "Não tornar a IA obrigatória; investir em formação; avaliar o efeito com um estudo piloto controlado."],
], larg=[3.8, 12.4], nota="Tabela 10 – Síntese das conclusões por nível de análise.")
H("8.1. Os colaboradores que usam mais IA são mais produtivos?", 2)
P("Em média, sim, mas pouco. A associação é positiva, fraca e significativa (r = 0,24; ρ = 0,27) e explica cerca de 6% da variação "
  "da produtividade, e há muitos contraexemplos (o C134, com 25 h, tem 71,6; o C014, com 4,9 h, tem 98). A ideia da direção é "
  "verdadeira como tendência média, mas errada como regra para cada pessoa.")
H("8.2. A relação mantém-se quando se consideram outros fatores?", 2)
P("Não. Comparando colaboradores com a mesma experiência, formação em IA e complexidade de tarefas, a associação entre uso de IA "
  "e produtividade é pequena e não significativa (0,13 pontos por hora; IC 95% de −0,22 a 0,48). O resultado mantém-se sem o C097, "
  "juntando a carga de trabalho e o departamento, e com a complexidade tratada como categoria.")
H("8.3. Resultado mais inesperado", 2)
P("O que mais nos surpreendeu foi a associação da IA quase desaparecer quando se tem em conta a experiência, apesar de ser "
  "claramente significativa sozinha (b = 0,639, p < 0,001, contra b = 0,129, p = 0,47, com os mesmos 233 colaboradores). Como os "
  "VIF são baixos (< 1,6), a explicação não é a multicolinearidade: os mais experientes usam mais IA (r = 0,27) e são mais "
  "produtivos (r = 0,50), e a associação inicial era, em grande parte, a experiência «disfarçada». Também nos surpreendeu que quem "
  "mais usa IA esteja abaixo da média e que o departamento que mais usa IA não se distinga em produtividade.")
H("8.4. Limitações", 2)
B("**Tipo de estudo.** Uma única medição, sem distribuição ao acaso do uso de IA. Não permite falar de causa nem excluir que a "
  "relação vá no sentido contrário ou se deva a fatores não medidos (motivação, competência digital, tipo de tarefa, qualidade da ferramenta).",
  "**Qualidade e medição dos dados.** Dados sintéticos; uma produtividade avaliada por avaliadores, com um teto em 98 (13 "
  "colaboradores) que impede distinguir os melhores; um valor suspeito (C097); e um uso de IA medido em horas, que não diz se a IA "
  "é bem usada.")
P("Além disso, o modelo final deixa cerca de 73% da variação por explicar e a complexidade, que é ordinal, foi tratada como número "
  "(a análise de robustez mostrou que tratá-la como categoria não muda as conclusões).")
H("8.5. Recomendação à direção: tornar obrigatório o uso de IA?", 2)
P("Não recomendamos tornar obrigatório o uso de IA com base nestes resultados. Os dados mostram associação, não causa: a "
  "associação «em bruto» já é fraca e desaparece quando se comparam colaboradores com experiência e formação semelhantes. Mesmo no "
  "cenário mais favorável (o modelo simples), impor mais 5 h semanais de IA estaria ligado, no máximo, a cerca de 3 pontos de "
  "produtividade, com custos (tempo, licenças, resistência à mudança) que não avaliámos. Uma obrigação igual para todos ignora "
  "ainda que o benefício pode depender do tipo de tarefa e de quem usa a ferramenta.")
P("Em alternativa, sugerimos: (1) manter a IA disponível e opcional; (2) investir em boa formação, cuja relação com a "
  "produtividade é positiva, embora no limite da significância; (3) fazer um estudo piloto controlado, por exemplo dando acesso e "
  "formação a equipas escolhidas ao acaso e medindo a produtividade antes e depois, para saber se a IA causa mais produtividade; "
  "(4) melhorar a medição, com uma escala de produtividade sem teto e registo de como a IA é usada.")
P("Respondendo à questão central: o uso de IA está associado à produtividade de forma positiva, mas fraca, e essa associação "
  "deve-se sobretudo a os colaboradores que mais usam IA serem também mais experientes e com mais formação. Nestes dados, "
  "trabalhar com IA não significa, por si só, trabalhar melhor.")

# ------------------------------------------------------------------ refs
H("Referências")
for r in ["Coelho, L. (2026). *Modelos Estatísticos para Inteligência Artificial*: aulas 1 a 8, guiões de código e infográficos de testes estatísticos (material de apoio da UC). Mestrado em Inteligência Artificial, IPCA.",
          "Montgomery, D. C., Peck, E. A., & Vining, G. G. (2021). *Introduction to linear regression analysis* (6.ª ed.). Wiley.",
          "Seabold, S., & Perktold, J. (2010). statsmodels: Econometric and statistical modeling with Python. *Proceedings of the 9th Python in Science Conference*.",
          "Virtanen, P., et al. (2020). SciPy 1.0: Fundamental algorithms for scientific computing in Python. *Nature Methods, 17*, 261–272."]:
    par = P(r, align=WD_ALIGN_PARAGRAPH.LEFT); par.paragraph_format.left_indent = Cm(0.8); par.paragraph_format.first_line_indent = Cm(-0.8)
H("Anexo – Notebook", 2)
P("Todo o código, os resultados e as interpretações de cada pergunta (1.1 a 7.5) estão no notebook **TP1_MEPA_IA_Produtividade.ipynb**, "
  "guardado no repositório GitHub do grupo e executável no Google Colab (os dados são lidos do próprio repositório) ou localmente "
  "(instruções na secção 0 do notebook). Cada bloco de código tem um comentário que explica o que faz, porquê e como se lê o resultado.",
  align=WD_ALIGN_PARAGRAPH.LEFT)
H("Anexo – Correspondência com as perguntas do enunciado", 2)
T(["Perguntas do enunciado", "Onde estão respondidas neste relatório"], [
    ["1.1 a 1.6 – Conhecimento e preparação da base de dados", "1.1 e 1.4: secção 2.1 e Tabela 1; 1.2, 1.3 e 1.5: secção 2.2 e Tabela 2; 1.6: secção 2.3 e Tabela 3"],
    ["2.1 a 2.5 – Caracterização dos colaboradores", "Secção 3: Tabela 4 (2.1 e 2.2), Figura 1 (2.2), «Departamentos» (2.3), Figura 2 e «Simetria» (2.4), «Mais produtivo e quem mais usa IA» (2.5)"],
    ["3.1 a 3.5 – Associação entre IA e produtividade", "Secção 4: Figura 3 e «Tendência» (3.1), Tabela 5 e «Que medida usámos» (3.2), «Classificação» (3.3), exemplos concretos (3.4), «Associação não é causa» (3.5)"],
    ["4.1 a 4.6 – Diferenças entre departamentos e intervalo de confiança", "Secção 5: Figura 4 (4.1), «Hipóteses» (4.2), «Condições» e «Escolha do teste» (4.3), Tabela 6 e «Como se lê o valor-p» (4.4), «O que se pode e não pode afirmar» (4.5), «Intervalo de confiança» (4.6)"],
    ["5.1 a 5.6 – Regressão linear simples", "Secção 6: equação e coeficientes (5.1 e 5.2), «5 h vs 10 h» (5.3), «Quanto explica» (5.4), «Um colaborador concreto» (5.5), Figura 5 e «Análise dos resíduos» (5.6)"],
    ["6.1 a 6.7 – Regressão linear múltipla", "Secções 7.1 (6.1 e 6.2, Figura 6), 7.2 (6.2 e 6.3, Tabela 7), 7.3 (6.4, Figura 7), 7.4 (6.5, Tabela 8), 7.5 (6.6, Figura 8 e Tabela 9) e 7.6 (6.7)"],
    ["7.1 a 7.5 – Conclusão da investigação", "Secções 8.1 a 8.5 e Tabela 10 (níveis descritivo, inferencial, explicação estatística e recomendação)"],
], larg=[6.0, 10.2], nota="Tabela 11 – Correspondência entre as perguntas do enunciado e as secções do relatório. O notebook segue diretamente a numeração do enunciado.")

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
