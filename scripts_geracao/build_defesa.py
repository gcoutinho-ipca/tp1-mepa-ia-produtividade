# Gera Apresentacao_Defesa_TP1_MEPA.pptx (10 slides) no estilo dos slides das aulas de MEPA:
# faixa azul-escura no topo, blocos verdes, marcadores em triângulo, rodapé azul com paginação.
# Uso: python scripts_geracao/build_defesa.py .   (as figuras têm de existir em figuras/)
import os, sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from lxml import etree
from PIL import Image

REPO = sys.argv[1] if len(sys.argv) > 1 else "."
LOGO = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo_upca.png")
FIG = os.path.join(REPO, "figuras")
OUT = os.path.join(REPO, "Apresentacao_Defesa_TP1_MEPA.pptx")

NAVY = RGBColor(0x1B, 0x33, 0x53)      # faixa do título e texto de destaque
GREEN = RGBColor(0x00, 0x7D, 0x46)     # cabeçalho dos blocos
TINT = RGBColor(0xE9, 0xF6, 0xEE)      # corpo dos blocos
BRIGHT = RGBColor(0x00, 0xC1, 0x4A)    # verde do logótipo (barra da capa)
FOOT = RGBColor(0x33, 0x33, 0xB3)      # texto do rodapé
INK = RGBColor(0x22, 0x26, 0x2B)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
ORANGE = RGBColor(0xC2, 0x4A, 0x14)
FONT = "Segoe UI"
TOTAL = 10
RODAPE = "O paradoxo da Inteligência Artificial   |   TP1 de MEPA"

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
TITLE_ONLY = prs.slide_layouts[5]
num = [0]


def rect(sl, x, y, w, h, fill, shape=MSO_SHAPE.RECTANGLE, line=None, name=None):
    s = sl.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid(); s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line; s.line.width = Pt(1.5)
    s.shadow.inherit = False
    if name: s.name = name
    return s


def marcador(par, cor=NAVY):
    pPr = par._p.get_or_add_pPr()
    pPr.set("marL", str(Inches(0.3))); pPr.set("indent", str(-Inches(0.3)))
    clr = etree.SubElement(pPr, qn("a:buClr")); c = etree.SubElement(clr, qn("a:srgbClr")); c.set("val", str(cor))
    sz = etree.SubElement(pPr, qn("a:buSzPct")); sz.set("val", "70000")
    bu = etree.SubElement(pPr, qn("a:buChar")); bu.set("char", "▶")


def escreve(tf, linhas, size, color=INK, align=PP_ALIGN.LEFT, bullets=False, space=5, bold=False):
    """linhas: lista de str ou de listas de (texto, opções) com opções bold, color, size, italic."""
    tf.word_wrap = True
    for k, linha in enumerate(linhas):
        par = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        par.alignment = align; par.space_after = Pt(space)
        if bullets: marcador(par)
        if isinstance(linha, list) and len(linha) == 2 and isinstance(linha[0], str): linha = [tuple(linha)]
        for t, o in ([(linha, {})] if isinstance(linha, str) else linha):
            r = par.add_run(); r.text = t
            r.font.name = FONT; r.font.size = Pt(o.get("size", size))
            r.font.bold = o.get("bold", bold); r.font.italic = o.get("italic", False)
            r.font.color.rgb = o.get("color", color)


def texto(sl, x, y, w, h, linhas, size=16, anchor=MSO_ANCHOR.TOP, name=None, **kw):
    tb = sl.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    if name: tb.name = name
    tf = tb.text_frame; tf.vertical_anchor = anchor
    for m in ("margin_left", "margin_right", "margin_top", "margin_bottom"): setattr(tf, m, 0)
    escreve(tf, linhas, size, **kw)
    return tb


def bloco(sl, x, y, w, h, titulo, linhas, size=15, bullets=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE,
          cab=0.42, space=5):
    """Bloco ao estilo das aulas: cabeçalho verde com texto branco e corpo em verde muito claro."""
    c = rect(sl, x, y, w, cab, GREEN, name="Bloco: " + titulo)
    tf = c.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.12); tf.margin_top = tf.margin_bottom = 0
    escreve(tf, [titulo], 16, color=WHITE)
    b = rect(sl, x, y + cab, w, h - cab, TINT, name="Corpo: " + titulo)
    tf = b.text_frame; tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(0.14); tf.margin_top = tf.margin_bottom = Inches(0.08)
    escreve(tf, linhas, size, bullets=bullets, align=align, space=space)
    return b


def numero(sl, x, y, w, h, rotulo, valor, legenda, vsize=34):
    """Bloco com um número em destaque, como os blocos «40%» e «60%» da aula 1."""
    bloco(sl, x, y, w, h, rotulo,
          [[(valor, {"size": vsize, "bold": True, "color": NAVY})], [(legenda, {"size": 14})]],
          align=PP_ALIGN.CENTER, space=0)


def figura(sl, nome, x, y, w, h, alt):
    """Coloca a figura centrada na caixa (x, y, w, h), sem a deformar."""
    cam = os.path.join(FIG, nome + ".png")
    iw, ih = Image.open(cam).size
    k = min(w / iw, h / ih)
    fw, fh = iw * k, ih * k
    p = sl.shapes.add_picture(cam, Inches(x + (w - fw) / 2), Inches(y + (h - fh) / 2), Inches(fw), Inches(fh))
    p.name = alt
    p._element.nvPicPr.cNvPr.set("descr", alt)
    return p


def tabela(sl, x, y, w, linhas, larguras, size=14, alt=0.4):
    n, m = len(linhas), len(linhas[0])
    t = sl.shapes.add_table(n, m, Inches(x), Inches(y), Inches(w), Inches(alt * n)).table
    for j, lw in enumerate(larguras): t.columns[j].width = Inches(w * lw / sum(larguras))
    for i, lin in enumerate(linhas):
        t.rows[i].height = Inches(alt)
        for j, v in enumerate(lin):
            c = t.cell(i, j)
            c.fill.solid(); c.fill.fore_color.rgb = GREEN if i == 0 else (TINT if i % 2 == 0 else WHITE)
            c.margin_left = c.margin_right = Inches(0.1); c.margin_top = c.margin_bottom = Inches(0.03)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            c.text_frame.clear()
            escreve(c.text_frame, [v], size, color=WHITE if i == 0 else INK, bold=(i == 0), space=0,
                    align=PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER)
    return t


def slide(titulo, notas):
    num[0] += 1
    sl = prs.slides.add_slide(TITLE_ONLY)
    faixa = rect(sl, 0, 0, 13.333, 0.9, NAVY, name="Faixa do título")
    sl.shapes._spTree.remove(faixa._element); sl.shapes._spTree.insert(2, faixa._element)   # atrás do título
    t = sl.shapes.title
    t.left, t.top, t.width, t.height = Inches(0.42), Inches(0.12), Inches(12.5), Inches(0.72)
    tf = t.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE; tf.margin_left = 0
    escreve(tf, [titulo], 26, color=WHITE, bold=True)
    texto(sl, 0.42, 7.08, 9, 0.3, [RODAPE], size=11, color=FOOT, name="Rodapé")
    texto(sl, 11.9, 7.08, 1.0, 0.3, [f"{num[0]}/{TOTAL}"], size=11, color=FOOT, align=PP_ALIGN.RIGHT, name="Paginação")
    sl.notes_slide.notes_text_frame.text = notas
    return sl


# ── 1 · Capa (como a capa das aulas: logótipo à esquerda, barra verde em baixo) ──────────────
num[0] += 1
sl = prs.slides.add_slide(TITLE_ONLY)
lw = 3.3; lh = lw * 143 / 352
logo = sl.shapes.add_picture(LOGO, Inches(0.75), Inches(0.85), Inches(lw), Inches(lh))
logo.name = "Logótipo UPCA"; logo._element.nvPicPr.cNvPr.set("descr", "Logótipo da Universidade Politécnica do Cávado e do Ave")
texto(sl, 4.55, 0.85, 8.2, 0.9, [["Modelos Estatísticos para Inteligência Artificial", {"bold": True, "color": NAVY}]], size=24)
texto(sl, 4.55, 1.45, 8.2, 0.5, [["Trabalho Prático 1", {"color": GREEN}]], size=20)
t = sl.shapes.title
t.left, t.top, t.width, t.height = Inches(4.55), Inches(2.2), Inches(8.2), Inches(1.5)
tf = t.text_frame; tf.vertical_anchor = MSO_ANCHOR.TOP; tf.margin_left = 0
escreve(tf, ["O paradoxo da Inteligência Artificial"], 36, color=NAVY, bold=True)
texto(sl, 4.55, 3.55, 8.2, 0.6, [["Trabalhar com IA significa trabalhar melhor?", {"color": NAVY}]], size=22)
texto(sl, 4.55, 4.7, 8.2, 1.8, [
    [("Mestrado em Inteligência Artificial", {"bold": True, "color": NAVY})],
    "Gilberto Coutinho (n.º 3083) e Rúbem Mendes (n.º 4563)",
    "Docente: Liliana Coelho",
    "Ano letivo 2026/2027",
], size=16, space=4)
rect(sl, 0, 7.38, 13.333, 0.12, BRIGHT, name="Barra da capa")
sl.notes_slide.notes_text_frame.text = (
    "Apresentar o grupo e a pergunta do título. A direção da empresa acredita que quem usa mais IA é mais "
    "produtivo; o trabalho verifica se os dados sustentam essa ideia.")

# ── 2 · Questão e percurso ───────────────────────────────────────────────────────────────────
sl = slide("Questão de investigação e percurso",
           "Dizer a questão central e percorrer as seis etapas. Sublinhar a regra seguida em todo o trabalho: um "
           "método principal escolhido pelo tipo de variáveis e um método de confirmação. Só métodos dados nas aulas.")
bloco(sl, 0.7, 1.25, 11.93, 1.35, "Questão central",
      ["Em que medida a utilização de ferramentas de IA está associada à produtividade dos colaboradores, e como "
       "se altera essa relação quando se consideram outros fatores individuais e profissionais?"], size=17)
etapas = [("Preparar", "241 linhas, 240 pessoas"), ("Descrever", "centro, forma, outliers"),
          ("Associar", "Pearson e Spearman"), ("Comparar", "ANOVA e IC da média"),
          ("Modelar", "regressão simples e múltipla"), ("Concluir", "recomendação")]
cw, gap, x0, y0 = 1.78, 0.25, 0.7, 3.1
for i, (a, b) in enumerate(etapas):
    x = x0 + i * (cw + gap)
    c = rect(sl, x, y0, cw, 1.05, WHITE, MSO_SHAPE.ROUNDED_RECTANGLE, line=NAVY, name="Etapa: " + a)
    c.adjustments[0] = 0.12
    tf = c.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = tf.margin_right = Inches(0.05); tf.margin_top = tf.margin_bottom = 0
    escreve(tf, [[(a, {"bold": True, "color": NAVY, "size": 16})], [(b, {"size": 12})]], 12, align=PP_ALIGN.CENTER, space=0)
    if i < len(etapas) - 1:
        s = rect(sl, x + cw + 0.05, y0 + 0.43, 0.15, 0.19, GREEN, MSO_SHAPE.ISOSCELES_TRIANGLE, name="Seta")
        s.rotation = 90
bloco(sl, 0.7, 4.75, 11.93, 1.95, "Ideia-chave",
      [[("Em cada etapa, um método principal ", {}), ("escolhido pelo tipo de variáveis", {"bold": True, "color": NAVY}),
        (" e um método de confirmação ", {}), ("que não depende da condição que falhou", {"bold": True, "color": NAVY}), (".", {})],
       "Só métodos dados nas aulas. Nível de significância: 5%. Dados sintéticos, de um único momento."],
      size=17, space=8)

# ── 3 · Preparação dos dados ─────────────────────────────────────────────────────────────────
sl = slide("Preparação dos dados: corrigir o erro, marcar o suspeito",
           "241 linhas mas 240 códigos: o C084 estava copiado. Os 8 valores em falta não foram preenchidos, por "
           "isso o número de casos muda conforme a análise. O C097 e os 10 casos incoerentes foram marcados e "
           "mantidos; as análises foram repetidas sem eles e nada muda.")
passos = [("Excel", "241", "linhas"), ("Base limpa", "240", "colaboradores"), ("Descrição e ANOVA", "238", "com produtividade"),
          ("Correlação e M1", "236", "com IA e produtividade"), ("Modelo M2", "233", "com as 5 variáveis")]
cw, gap = 2.2, 0.2325
for i, (r, v, l) in enumerate(passos):
    numero(sl, 0.7 + i * (cw + gap), 1.25, cw, 1.75, r, v, l)
bloco(sl, 0.7, 3.3, 5.8, 2.0, "Corrigido (erro comprovado)",
      ["C084 em duas linhas iguais: ficou uma", "3 grafias de departamento uniformizadas: 4 departamentos"],
      bullets=True, size=16)
bloco(sl, 6.83, 3.3, 5.8, 2.0, "Marcado e mantido (apenas suspeito)",
      ["C097 com produtividade 19 (o seguinte é 43,5)", "10 casos em que tarefas × tempo excedem um mês",
       "13 colaboradores no teto da escala (98)"], bullets=True, size=16)
bloco(sl, 0.7, 5.55, 11.93, 1.2, "Valores em falta: 8, um em cada um de 8 registos",
      [[("Não foram preenchidos, para não inventar dados. ", {}),
        ("A correlação é igual com 236 casos (0,241) e com 233 (0,246).", {"bold": True, "color": NAVY})]], size=16)

# ── 4 · Descrição e normalidade ──────────────────────────────────────────────────────────────
sl = slide("A produtividade não segue uma distribuição normal",
           "Três gráficos, cada um mostra uma coisa: o histograma a forma, o box-plot os outliers, o Q-Q onde falha "
           "a normalidade (em baixo pelos valores baixos, em cima pelo teto em 98). O Shapiro-Wilk rejeita mesmo sem "
           "o C097. Consequência prática: Spearman ao lado do Pearson, Kruskal-Wallis ao lado da ANOVA.")
figura(sl, "fig_2_4_produtividade_sem_nota", 0.7, 1.1, 11.93, 3.35, "Histograma, box-plot e gráfico Q-Q da produtividade")
numero(sl, 0.7, 4.65, 2.75, 1.95, "Média e mediana", "78,0 e 79,4", "cauda à esquerda", vsize=24)
numero(sl, 3.7, 4.65, 2.75, 1.95, "Shapiro-Wilk", "p < 0,001", "sem C097: p = 0,0009", vsize=24)
bloco(sl, 6.7, 4.65, 5.93, 1.95, "Consequência para o resto do trabalho",
      [[("Cada teste que supõe normalidade leva ao lado um ", {}),
        ("teste que não a exige", {"bold": True, "color": NAVY}), (".", {})],
       "Causas: valores muito baixos (C097) e teto em 98."], size=16, space=6)

# ── 5 · Associação ───────────────────────────────────────────────────────────────────────────
sl = slide("IA e produtividade: associação positiva, mas fraca",
           "Pearson porque as duas variáveis são quantitativas e a relação é em linha reta. Spearman como confirmação "
           "porque a produtividade não é normal, tem outliers e teto. Concordam. O p pequeno só diz que r é diferente "
           "de zero; a intensidade lê-se no r. Contraexemplos: C134 usa 25 h e tem 71,6; C014 usa 4,9 h e tem 98.")
figura(sl, "fig_3_1_dispersao_sem_nota", 0.55, 1.1, 8.5, 4.05, "Dispersão do uso de IA contra a produtividade e box-plots por quartil")
numero(sl, 9.3, 1.25, 3.33, 1.2, "Pearson (principal)", "r = 0,24", "p < 0,001; n = 236", vsize=24)
numero(sl, 9.3, 2.6, 3.33, 1.2, "Spearman (confirmação)", "ρ = 0,27", "p < 0,001", vsize=24)
numero(sl, 9.3, 3.95, 3.33, 1.2, "Variação acompanhada", "r² = 0,06", "cerca de 6%", vsize=24)
bloco(sl, 0.7, 5.4, 11.93, 1.35, "Significativo não quer dizer forte",
      [[("O valor-p diz que a associação é diferente de zero; a intensidade lê-se no r. ", {}),
        ("Na escala das aulas, entre 0,2 e 0,4 a associação é fraca.", {"bold": True, "color": NAVY}),
        (" E associação não é causa.", {})]], size=16)

# ── 6 · Departamentos ────────────────────────────────────────────────────────────────────────
sl = slide("Os departamentos não diferem na produtividade",
           "Condições verificadas antes de escolher o teste. Levene não rejeita, logo ANOVA clássica. Welch e "
           "Kruskal-Wallis confirmam. Não se fizeram testes t par a par: seriam 6 e o risco de um falso positivo "
           "subia para cerca de 26%. Sem Tukey porque a ANOVA não rejeitou. Não rejeitar H0 não prova igualdade.")
figura(sl, "fig_4_1_departamentos_sem_nota", 0.55, 1.1, 6.3, 3.6, "Box-plots da produtividade por departamento")
tabela(sl, 7.1, 1.25, 5.53, [["Teste", "Estatística", "p"],
                             ["ANOVA a um fator", "F(3, 234) = 0,47", "0,70"],
                             ["ANOVA de Welch", "F(3; 105,7) = 0,50", "0,68"],
                             ["Kruskal-Wallis", "H(3) = 1,37", "0,71"]], [2.3, 2.3, 0.9])
bloco(sl, 7.1, 3.05, 5.53, 1.65, "Condições (verificadas antes do teste)",
      ["Independência: pela recolha dos dados", "Normalidade por grupo: falha em Desenvolvimento",
       "Variâncias iguais: Levene p = 0,52"], bullets=True, size=14, space=3)
bloco(sl, 0.7, 4.95, 5.8, 1.8, "Porquê ANOVA e não testes t?",
      [[("4 grupos seriam 6 testes t: o risco de um falso positivo subia de 5% para ", {}),
        ("cerca de 26%", {"bold": True, "color": NAVY}), (". A ANOVA faz um único teste.", {})]], size=15)
bloco(sl, 6.83, 4.95, 5.8, 1.8, "Leitura",
      ["η² = 0,006: abaixo de um efeito pequeno (0,01)", "Sem Tukey: só depois de rejeitar H0",
       "IC 95% da média (t de Student): 76,4 a 79,7"], bullets=True, size=15, space=3)

# ── 7 · Modelo 1 ─────────────────────────────────────────────────────────────────────────────
sl = slide("Modelo 1: a IA sozinha explica 6% da produtividade",
           "Equação e leitura do declive: comparação entre pessoas diferentes, não o efeito de aumentar o uso. "
           "Resíduos: sem curva nem funil; a normalidade falha pela cauda esquerda (C097, C129) e pelo teto. O ponto "
           "decisivo é a correlação de 0,45 entre os resíduos e a experiência: falta uma variável no modelo.")
eq = rect(sl, 0.7, 1.2, 7.6, 0.75, WHITE, line=NAVY, name="Equação do modelo 1")
tf = eq.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
escreve(tf, [[("produtividade = 73,04 + 0,627 × horas de IA", {"bold": True, "color": NAVY})]], 20, align=PP_ALIGN.CENTER)
texto(sl, 8.55, 1.2, 4.1, 0.75, [[("R² = 0,058", {"bold": True, "color": NAVY, "size": 20})],
                                 [("de 5 h para 10 h: mais 3,1 pontos", {"size": 14})]], size=14, space=0, anchor=MSO_ANCHOR.MIDDLE)
figura(sl, "fig_5_6_residuos_m1_sem_nota", 0.7, 2.1, 11.93, 2.75, "Resíduos do modelo 1: contra os valores ajustados, histograma e Q-Q")
bloco(sl, 0.7, 5.0, 5.8, 1.75, "Pressupostos",
      ["Linha reta e variância constante: cumpridos (Breusch-Pagan p = 0,98)",
       "Normalidade dos resíduos: rejeitada (C097 e teto)"], bullets=True, size=15, space=3)
bloco(sl, 6.83, 5.0, 5.8, 1.75, "O que os resíduos revelam",
      [[("Correlação entre os resíduos e a experiência: ", {}), ("r = 0,45", {"bold": True, "color": NAVY}),
        (". Os mais experientes ficam sempre acima do previsto: falta uma variável no modelo.", {})]], size=15)

# ── 8 · Modelo 2 ─────────────────────────────────────────────────────────────────────────────
sl = slide("Modelo 2: com a experiência, o efeito da IA quase desaparece",
           "É o gráfico central. Os cinco modelos usam os mesmos 233 casos. Só com a formação o coeficiente quase "
           "não muda; só com a experiência cai para metade (0,31; p = 0,044); com as duas cai para 0,13 e o intervalo "
           "inclui o zero. Não é multicolinearidade: o erro-padrão quase não muda (0,166 e 0,179) e o VIF é 1,51.")
figura(sl, "fig_6_4_coeficiente_ia_sem_nota", 0.55, 1.1, 7.0, 3.4, "Coeficiente do uso de IA em cinco modelos sucessivos, com IC a 95%")
tabela(sl, 7.8, 1.25, 4.83, [["Modelo 2 (n = 233)", "Coeficiente", "p"],
                             ["Uso de IA (h/semana)", "0,129", "0,47"],
                             ["Experiência (anos)", "1,584", "< 0,001"],
                             ["Formação em IA (h)", "0,231", "0,059"],
                             ["Complexidade (1 a 5)", "−0,661", "0,36"]], [2.6, 1.4, 1.1], alt=0.44)
texto(sl, 7.8, 3.6, 4.83, 0.8, ["Cada coeficiente lê-se mantendo as outras variáveis iguais. Variáveis escolhidas por "
                                "serem anteriores ao desempenho."], size=13)
numero(sl, 0.7, 4.75, 3.3, 2.0, "Coeficiente da IA", "0,64 → 0,13", "menos 80%; p = 0,47", vsize=28)
bloco(sl, 4.25, 4.75, 8.38, 2.0, "Ideia-chave: a experiência é um fator de confusão",
      [[("Quem tem mais experiência usa mais IA (r = 0,27) e é mais produtivo (r = 0,50). ", {}),
        ("Quem usa mais IA é mais produtivo sobretudo porque é mais experiente.", {"bold": True, "color": NAVY})],
       "Tarefas, tempo por tarefa e qualidade ficaram de fora: medem o próprio desempenho."], size=15, space=6)

# ── 9 · Escolha do modelo ────────────────────────────────────────────────────────────────────
sl = slide("Porque escolhemos o modelo 2",
           "Comparação justa: mesmos 233 casos. O R² sobe sempre, por isso usa-se o ajustado. O F parcial testa as "
           "três variáveis em conjunto. Pressupostos razoavelmente cumpridos; a normalidade dos resíduos só passa sem "
           "o C097. Em todas as versões de robustez o coeficiente da IA fica entre 0,12 e 0,15 e nunca é significativo.")
tabela(sl, 0.7, 1.25, 6.4, [["Mesmos 233 casos", "M1 (só IA)", "M2 (IA + 3)"],
                            ["R²", "0,061", "0,280"],
                            ["R² ajustado", "0,056", "0,267"],
                            ["Erro por explicar (SQR)", "35 990", "27 590"],
                            ["Coeficiente da IA", "0,639", "0,129"]], [2.8, 1.8, 1.8], size=15, alt=0.46)
numero(sl, 7.4, 1.25, 5.23, 2.3, "Teste F parcial (modelos encaixados)", "F(3, 228) = 23,1", "p < 0,001: a melhoria não se deve ao acaso", vsize=28)
bloco(sl, 0.7, 3.85, 5.8, 2.9, "Pressupostos do modelo 2",
      ["Multicolinearidade: VIF máximo 1,51 (preocupa acima de 5)", "Variância constante: Breusch-Pagan p = 0,19",
       "Normalidade dos resíduos: p = 0,97 sem o C097", "Influência: distância de Cook máxima 0,07"],
      bullets=True, size=15, space=4)
bloco(sl, 6.83, 3.85, 5.8, 2.9, "Robustez: coeficiente da IA nunca significativo",
      ["Sem o C097: 0,146 (p = 0,38)", "Com carga de trabalho e departamento: 0,144 (p = 0,45)",
       "Complexidade como categoria: 0,122 (p = 0,50)", "Interação IA × experiência: 0,028 (p = 0,50)"],
      bullets=True, size=15, space=4)

# ── 10 · Conclusões ──────────────────────────────────────────────────────────────────────────
sl = slide("Conclusões e recomendação",
           "Separar os quatro níveis pedidos no enunciado. Fechar com a resposta à questão central. Limitações: um só "
           "momento e sem distribuição ao acaso (não permite falar de causa); dados sintéticos, teto em 98, IA medida "
           "só em horas. O modelo final deixa cerca de 73% da variação por explicar.")
niveis = [("Descritivo", ["Produtividade média 78,0", "Uso de IA: 7,7 h por semana", "Mais IA, um pouco mais de produtividade, com muitas exceções"]),
          ("Inferencial", ["r = 0,24, fraca e significativa", "Departamentos sem diferenças (p = 0,70)", "IC 95% da média: 76,4 a 79,7"]),
          ("Explicação", ["Coeficiente da IA: 0,64 passa a 0,13 (p = 0,47)", "Experiência: mais 1,6 pontos por ano", "M2 explica 27% da variação"]),
          ("Recomendação", ["Não tornar a IA obrigatória", "Manter opcional e investir em formação", "Estudo piloto com equipas escolhidas ao acaso"])]
cw, gap = 2.83, 0.2033
for i, (t, l) in enumerate(niveis):
    bloco(sl, 0.7 + i * (cw + gap), 1.25, cw, 3.25, t, l, bullets=True, size=14, space=6, anchor=MSO_ANCHOR.TOP)
bloco(sl, 0.7, 4.75, 5.8, 2.0, "Limitações",
      ["Um só momento, sem distribuição ao acaso: associação e não causa",
       "Dados sintéticos, teto em 98 e IA medida só em horas"], bullets=True, size=15, space=4)
r = rect(sl, 6.83, 4.75, 5.8, 2.0, NAVY, name="Resposta à questão central")
tf = r.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
tf.margin_left = tf.margin_right = Inches(0.25)
escreve(tf, [[("Resposta à questão central", {"size": 14, "color": RGBColor(0xBF, 0xE8, 0xD0)})],
             [("Trabalhar com IA não significa, por si só, trabalhar melhor.", {"size": 22, "bold": True, "color": WHITE})]],
        22, color=WHITE, space=6)

assert num[0] == TOTAL, num[0]
prs.core_properties.title = "O paradoxo da Inteligência Artificial: defesa do TP1 de MEPA"
prs.core_properties.author = "Gilberto Coutinho; Rúbem Mendes"
prs.save(OUT)
print(OUT)
