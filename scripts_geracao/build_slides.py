# Gera a apresentação (.pptx) do TP de MEPA a partir dos resultados e das figuras do notebook.
# Uso: python scripts_geracao/build_slides.py .   (as figuras têm de existir em figuras/)
import os, sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from lxml import etree
from PIL import Image

PASTA = sys.argv[1] if len(sys.argv) > 1 else "."
FIG = os.path.join(PASTA, "figuras")

NAVY, BLUE, ORANGE = RGBColor(0x1B, 0x2A, 0x41), RGBColor(0x2A, 0x78, 0xD6), RGBColor(0xEB, 0x68, 0x34)
GREEN, YELLOW, GRAY = RGBColor(0x1B, 0xAF, 0x7A), RGBColor(0xED, 0xA1, 0x00), RGBColor(0x52, 0x51, 0x4E)
LIGHT, LIGHTB, WHITE = RGBColor(0xF3, 0xF6, 0xFA), RGBColor(0xE4, 0xEE, 0xFB), RGBColor(0xFF, 0xFF, 0xFF)
HEAD, BODY = "Cambria", "Calibri"

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]
n_slide = [0]


def fill(shape, color):
    shape.fill.solid(); shape.fill.fore_color.rgb = color; shape.line.fill.background()


def box(sl, x, y, w, h, color, shape=MSO_SHAPE.ROUNDED_RECTANGLE, name=None):
    s = sl.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h)); fill(s, color)
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE: s.adjustments[0] = 0.08
    s.shadow.inherit = False
    if name: s.name = name
    return s


def bullet(par, char="•"):
    pPr = par._p.get_or_add_pPr()
    pPr.set("marL", str(Inches(0.28))); pPr.set("indent", str(-Inches(0.22)))
    for tag in ("a:buNone", "a:buChar", "a:buAutoNum"):
        for e in pPr.findall(qn(tag)): pPr.remove(e)
    bu = etree.SubElement(pPr, qn("a:buChar")); bu.set("char", char)


def text(sl, x, y, w, h, linhas, size=16, color=NAVY, font=BODY, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
         bullets=False, space=6, name=None):
    """linhas: lista de str ou de listas de (texto, {bold, color, size, italic})."""
    tb = sl.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    if name: tb.name = name
    tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    for m in ("margin_left", "margin_right", "margin_top", "margin_bottom"): setattr(tf, m, 0)
    for k, linha in enumerate(linhas):
        par = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        par.alignment = align; par.space_after = Pt(space)
        if bullets: bullet(par)
        for t, o in ([(linha, {})] if isinstance(linha, str) else linha):
            r = par.add_run(); r.text = t
            r.font.name = o.get("font", font); r.font.size = Pt(o.get("size", size))
            r.font.bold = o.get("bold", False); r.font.italic = o.get("italic", False)
            r.font.color.rgb = o.get("color", color)
    return tb


def slide(titulo=None, fase=None, notas="", escuro=False):
    sl = prs.slides.add_slide(BLANK); n_slide[0] += 1
    if escuro:
        box(sl, 0, 0, 13.333, 7.5, NAVY, MSO_SHAPE.RECTANGLE, "fundo")
    else:
        if fase: text(sl, 0.6, 0.32, 9, 0.3, [fase.upper()], size=12, color=ORANGE, name="fase")
        if titulo: text(sl, 0.6, 0.58, 12.1, 0.8, [titulo], size=30, font=HEAD, name="titulo")
        text(sl, 0.6, 7.02, 9, 0.3, ["MEPA 2026/2027 · Gilberto Coutinho (3083) e Rúbem Mendes (4563)"], size=10, color=GRAY, name="rodape")
        text(sl, 11.9, 7.02, 0.83, 0.3, [str(n_slide[0])], size=10, color=GRAY, align=PP_ALIGN.RIGHT, name="numero")
    if notas: sl.notes_slide.notes_text_frame.text = notas
    return sl


def img(sl, nome, x, y, w=None, h=None):
    p = os.path.join(FIG, nome); iw, ih = Image.open(p).size
    if w and not h: h = w * ih / iw
    if h and not w: w = h * iw / ih
    sl.shapes.add_picture(p, Inches(x), Inches(y), Inches(w), Inches(h)).name = nome
    return w, h


def table(sl, x, y, larg, linhas, size=13, alt=0.36):
    nr, nc = len(linhas), len(larg)
    t = sl.shapes.add_table(nr, nc, Inches(x), Inches(y), Inches(sum(larg)), Inches(alt * nr)).table
    for j, w in enumerate(larg): t.columns[j].width = Inches(w)
    for i, linha in enumerate(linhas):
        for j, v in enumerate(linha):
            c = t.cell(i, j); c.fill.solid()
            c.fill.fore_color.rgb = BLUE if i == 0 else (LIGHT if i % 2 else WHITE)
            c.margin_left = c.margin_right = Inches(0.08); c.margin_top = c.margin_bottom = Inches(0.04)
            tf = c.text_frame; tf.word_wrap = True; tf.paragraphs[0].text = ""
            r = tf.paragraphs[0].add_run(); r.text = str(v); r.font.name = BODY
            r.font.size = Pt(size); r.font.bold = (i == 0); r.font.color.rgb = WHITE if i == 0 else NAVY
    return t


def stat(sl, x, y, w, grande, rotulo, cor=BLUE, h=1.55):
    box(sl, x, y, w, h, LIGHT)
    text(sl, x + 0.2, y + 0.15, w - 0.4, 0.75, [grande], size=34, color=cor, font=HEAD, name="stat")
    text(sl, x + 0.2, y + 0.9, w - 0.4, h - 0.95, [rotulo], size=13, color=GRAY)


def decisao(sl, x, y, w, h, titulo, linhas, cor=GREEN, size=14):
    box(sl, x, y, w, h, LIGHTB)
    text(sl, x + 0.25, y + 0.18, w - 0.5, 0.4, [[(titulo, {"bold": True, "color": cor})]], size=15)
    text(sl, x + 0.25, y + 0.62, w - 0.5, h - 0.75, linhas, size=size, bullets=True)


# ======================================================================= 1. capa
sl = slide(escuro=True, notas="Apresentar o tema e a pergunta. Dizer logo que não partimos para provar que a IA aumenta a "
           "produtividade: quisemos ver o que os dados permitem dizer. Os dados são sintéticos.")
text(sl, 0.9, 1.0, 11, 0.4, ["MESTRADO EM INTELIGÊNCIA ARTIFICIAL · MODELOS ESTATÍSTICOS PARA IA · 2026/2027"], size=13, color=YELLOW)
text(sl, 0.9, 1.9, 11.5, 2.2, ["O paradoxo da Inteligência Artificial", "Trabalhar com IA significa trabalhar melhor?"],
     size=40, color=WHITE, font=HEAD, space=10)
text(sl, 0.9, 4.45, 11, 1.0, ["Porque escolhemos cada método, fase a fase"], size=22, color=RGBColor(0xCA, 0xDC, 0xFC))
text(sl, 0.9, 5.7, 11, 1.0, ["Gilberto Coutinho (3083) · Rúbem Mendes (4563)", "Docente: Liliana Coelho"], size=16,
     color=WHITE, space=4)

# ======================================================================= 2. pergunta e plano
sl = slide("A pergunta e o plano", "Ponto de partida",
           notas="A direção acha que quem usa mais IA é mais produtivo. O plano segue o enunciado: cada fase usa o que a "
           "anterior mostrou para escolher o método seguinte. Ao longo da apresentação explicamos, em cada fase, que "
           "resultado tivemos e porque é que isso nos levou a um método e não a outro.")
text(sl, 0.6, 1.5, 12.1, 0.9, [[("Em que medida o uso de IA está associado à produtividade, ", {}),
                                 ("e como muda essa relação quando se consideram outros fatores?", {"bold": True})]], size=20)
fases = [("1", "Preparar os dados", "repetidos, faltas, erros"), ("2", "Descrever", "médias, gráficos, forma"),
         ("3", "Associação", "Pearson e Spearman"), ("4", "Inferência", "ANOVA e intervalo"),
         ("5", "Regressão simples", "só o uso de IA"), ("6", "Regressão múltipla", "IA + outros fatores")]
for k, (n, t1, t2) in enumerate(fases):
    x = 0.6 + k * 2.05
    box(sl, x, 2.85, 1.85, 2.1, LIGHT)
    s = box(sl, x + 0.62, 3.05, 0.6, 0.6, BLUE, MSO_SHAPE.OVAL)
    text(sl, x + 0.62, 3.05, 0.6, 0.6, [n], size=20, color=WHITE, font=HEAD, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(sl, x + 0.12, 3.85, 1.61, 0.5, [t1], size=15, align=PP_ALIGN.CENTER, color=NAVY)
    text(sl, x + 0.12, 4.35, 1.61, 0.5, [t2], size=12, align=PP_ALIGN.CENTER, color=GRAY)
text(sl, 0.6, 5.45, 12.1, 1.2, [
    "Regra que seguimos: o método escolhe-se antes de ver o resultado, a partir do tipo de variáveis e das condições verificadas.",
    "Só usámos métodos dados nas aulas e nos materiais de apoio da docente. Nível de significância: 5%."], size=15, bullets=True)

# ======================================================================= 3. dados recebidos
sl = slide("O que encontrámos nos dados", "Fase 1 · Preparar os dados",
           notas="241 linhas para 240 códigos: o C084 estava copiado (linhas iguais em tudo), ficou uma. Três departamentos "
           "mal escritos, corrigidos para os 4 do dicionário. Oito valores em falta, um em cada registo. O C097 tem 19 de "
           "produtividade, muito abaixo do resto: não há prova de erro, por isso ficou, e repetimos as análises sem ele. "
           "Há um teto: 13 pessoas com 98, o máximo. Por fim, tarefas vezes tempo médio: o C069 faz 35 tarefas de 8,74 h, "
           "306 h, cerca de 7,4 semanas de trabalho. O dicionário não diz quanto dura o período; com um mês, 10 pessoas "
           "ficam acima. Podem ser dados sintéticos gerados sem esta regra, ou tempo de duração e não de esforço. Marcámos, "
           "mantivemos e repetimos a correlação e a ANOVA sem elas: nada muda.")
stat(sl, 0.6, 1.6, 2.9, "241 → 240", "linhas → colaboradores: o C084 estava repetido e ficou uma linha")
stat(sl, 3.7, 1.6, 2.9, "8", "valores em falta, cada um num registo diferente (< 1% por variável)", ORANGE)
stat(sl, 6.8, 1.6, 2.9, "7 → 4", "grafias de departamento corrigidas para as 4 do dicionário", GREEN)
stat(sl, 9.9, 1.6, 2.83, "13 × 98", "colaboradores no máximo da escala: há um «teto»", YELLOW)
decisao(sl, 0.6, 3.5, 6.0, 3.25, "O que decidimos", [
    "Retirar só a cópia do C084: é a mesma pessoa e contaria a dobrar.",
    "Não preencher valores em falta: seria inventar dados.",
    "Manter o C097 (produtividade 19): não se prova que é erro. Um valor estranho investiga-se, não se apaga; repetimos as análises sem ele.",
    "Manter C134 e C035 (≈ 25 h de IA): são valores possíveis.",
    "Marcar 10 com tarefas × tempo acima de 1 mês de trabalho (C069: 306 h); sem eles, nada muda."], size=13)
decisao(sl, 6.8, 3.5, 5.93, 3.25, "O que o dicionário do Excel nos disse", [
    "A produtividade é uma avaliação global feita por avaliadores, não calculada a partir das outras colunas.",
    "Tarefas, tempo por tarefa e qualidade medem o mesmo desempenho, ao mesmo tempo.",
    "Cada pessoa deve aparecer uma só vez: confirma a remoção do duplicado."], cor=BLUE, size=14)

# ======================================================================= 4. valores em falta
sl = slide("Valores em falta: retirar, preencher ou manter?", "Fase 1 · Preparar os dados",
           notas="Para cada registo com falha vimos de que análises sai. Nenhum colaborador sai do estudo inteiro. O C154 só "
           "não tem uma variável que não usamos. Os da experiência, formação e complexidade só saem da regressão múltipla. "
           "Os que não têm IA ou produtividade não podem entrar nessas análises sem inventar exatamente o que estudamos. "
           "O teste decisivo: a correlação é praticamente igual com 236 e com 233 casos, por isso a saída deles não mexe nos "
           "resultados. E nenhuma variável tem mais de 2 faltas, por isso não faz sentido retirar variáveis.")
table(sl, 0.6, 1.55, [1.75, 2.35, 2.55, 3.15], [
    ["Registos", "O que falta", "De que análises saem", "Faz sentido?"],
    ["C154", "Tempo por tarefa", "Nenhuma", "Sim: variável não usada"],
    ["C080, C189, C202", "Experiência, formação, complexidade", "Só da regressão múltipla", "Sim: entram em tudo o resto"],
    ["C067, C113", "Uso de IA", "Correlação e regressões", "Sim: seria inventar o que estudamos"],
    ["C030, C131", "Produtividade", "Tudo o que usa produtividade", "Sim: seria inventar o resultado"],
], size=13, alt=0.62)
stat(sl, 10.6, 1.55, 2.13, "0,241", "correlação com 236 casos")
stat(sl, 10.6, 3.25, 2.13, "0,246", "correlação com os 233 do modelo múltiplo", GREEN)
decisao(sl, 0.6, 4.95, 12.13, 1.85, "Conclusão: a exclusão faz sentido", [
    "Ninguém sai do estudo inteiro: cada registo só sai das análises a que lhe falta informação, e os resultados não mudam.",
    "Os 6 incompletos com produtividade conhecida têm média um pouco mais alta (86,0 contra 77,8), mas são 6 em 240.",
    "Nenhuma variável tem mais de 2 faltas: não há razão para retirar variáveis do estudo."], size=14)

# ======================================================================= 5. que variáveis entram
sl = slide("Que variáveis entram no estudo, e porquê", "Fase 1 · Preparar os dados",
           notas="A decisão sobre variáveis vem do papel de cada uma, não das faltas. Entram as que vêm antes do desempenho "
           "e que o enunciado aponta. Tarefas, tempo e qualidade ficam de fora porque o dicionário diz que são indicadores "
           "do mesmo desempenho: explicariam a produtividade com outra medida da produtividade, o R² subia sem ensinar nada, "
           "e podiam esconder o efeito da IA. Carga e departamento quase não se relacionam com a produtividade, por isso "
           "servem só para um teste de robustez.")
colunas = [("Entram no modelo", GREEN, ["Uso de IA: a variável que estudamos", "Experiência (r = 0,50 com a produtividade)",
                                        "Formação em IA (r = 0,51 com o uso de IA)", "Complexidade das tarefas (pedida no enunciado)"]),
           ("Só no teste de robustez", YELLOW, ["Carga de trabalho (r = 0,08)", "Departamento (ANOVA p = 0,70)",
                                                "Pouca relação com a produtividade"]),
           ("Ficam de fora", ORANGE, ["Tarefas concluídas, tempo por tarefa, qualidade", "Medem o mesmo desempenho (dicionário)",
                                      "Fariam subir o R² sem explicar nada", "Podiam esconder o efeito da IA"])]
for k, (t, cor, itens) in enumerate(colunas):
    x = 0.6 + k * 4.1
    box(sl, x, 1.6, 3.9, 4.22, LIGHT)
    text(sl, x + 0.25, 1.95, 3.4, 0.45, [[(t, {"bold": True, "color": cor})]], size=18)
    text(sl, x + 0.25, 2.6, 3.4, 3.1, itens, size=15, bullets=True, space=10)
text(sl, 0.6, 6.15, 12.1, 0.6, ["Critério: entram fatores que vêm antes do desempenho e que podem estar por trás da relação entre IA e produtividade."],
     size=15, color=GRAY)

# ======================================================================= 6. descrição
sl = slide("A produtividade não é normal, e isso conta", "Fase 2 · Descrever",
           notas="Média 78,0 e mediana 79,35: a média representa bem, mas é puxada para baixo por valores muito baixos. "
           "O histograma tem a cauda à esquerda, o Q-Q afasta-se na ponta de baixo e há o teto em 98. O Shapiro-Wilk rejeita "
           "a normalidade. Consequência para o resto: sempre que um teste supõe normalidade, juntamos uma confirmação que não "
           "a supõe (Spearman, Kruskal-Wallis) ou repetimos sem o C097.")
img(sl, "fig_2_4_produtividade_sem_nota.png", 0.6, 1.5, w=12.1)
stat(sl, 0.6, 4.85, 2.4, "78,0", "produtividade média (mediana 79,35)")
stat(sl, 3.2, 4.85, 2.4, "7,7 h", "uso médio de IA por semana", GREEN)
decisao(sl, 5.8, 4.85, 6.93, 1.95, "O que isto muda nas escolhas", [
    "Shapiro-Wilk rejeita a normalidade (p < 0,001), mesmo sem o C097.",
    "Cada teste que supõe normalidade terá uma confirmação que não a supõe."], cor=BLUE, size=14)

# ======================================================================= 7. associação
sl = slide("IA e produtividade: Pearson, confirmado por Spearman", "Fase 3 · Associação",
           notas="O gráfico mostra uma tendência a subir, fraca e sem curva. Como as duas variáveis são quantitativas e a "
           "relação é em linha reta, a medida é Pearson. Como a produtividade não é normal e tem valores afastados, juntámos "
           "Spearman, que usa as posições. Dão o mesmo. Pela escala da docente, 0,24 é fraca. O p pequeno só diz que é "
           "diferente de zero, não que é forte. E correlação não é causa.")
img(sl, "fig_3_1_dispersao_sem_nota.png", 0.6, 1.5, w=7.4)
table(sl, 8.3, 1.5, [2.5, 1.93], [["Medida", "Valor"], ["Pearson r", "0,24 (p < 0,001)"], ["Spearman ρ", "0,27 (p < 0,001)"],
                                   ["Pearson sem C097", "0,25"], ["Sem os 10 incoerentes", "0,24"],
                                   ["r² (variação partilhada)", "6%"]], size=14, alt=0.42)
decisao(sl, 0.6, 4.3, 6.0, 2.5, "Porque estes métodos", [
    "Pearson: duas variáveis quantitativas e relação em linha reta.",
    "Spearman: confirma sem depender da normalidade nem dos valores afastados.",
    "Não escolhemos o que desse o menor p: decidimos antes."], size=14)
decisao(sl, 6.8, 4.3, 5.93, 2.5, "Como se lê", [
    "Fraca: na escala da docente, 0,2 a 0,4.",
    "Significativo não é forte: com 236 pessoas até 0,24 se distingue de zero.",
    "Associação não é causa: a experiência pode estar por trás."], cor=BLUE, size=14)

# ======================================================================= 8. departamentos
sl = slide("Departamentos: das condições à ANOVA", "Fase 4 · Inferência",
           notas="Primeiro verificámos as condições, depois escolhemos. Independência pela recolha. Normalidade: falha só em "
           "Desenvolvimento, e os grupos são grandes. Levene não rejeita variâncias iguais. Pelo fluxograma da docente, isso "
           "leva à ANOVA a um fator. Juntámos Welch (sem variâncias iguais) e Kruskal-Wallis (sem normalidade). Os três dão "
           "cerca de 0,7. Não usámos 6 testes t porque o risco de uma diferença falsa subia para 26%. Não fizemos Tukey porque "
           "só se faz depois de rejeitar H0. O eta quadrado é 0,006, abaixo do limiar de efeito pequeno.")
passos = [("Independência", "pela recolha: 1 pessoa, 1 departamento", GREEN),
          ("Normalidade", "falha só em Desenvolvimento; grupos grandes (31–85)", YELLOW),
          ("Variâncias iguais", "Levene p = 0,52: não rejeitada", GREEN),
          ("ANOVA a um fator", "como manda o fluxograma da docente", BLUE)]
for k, (t1, t2, cor) in enumerate(passos):
    x = 0.6 + k * 3.08
    box(sl, x, 1.55, 2.85, 1.35, LIGHT)
    text(sl, x + 0.2, 1.8, 2.45, 0.4, [[(t1, {"bold": True, "color": cor})]], size=16)
    text(sl, x + 0.2, 2.2, 2.45, 0.7, [t2], size=13, color=GRAY)
    if k < 3:
        a = sl.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x + 2.88), Inches(2.08), Inches(0.17), Inches(0.3)); fill(a, GRAY)
table(sl, 0.6, 3.2, [2.6, 2.3, 1.2], [["Teste", "Estatística", "p"], ["ANOVA (principal)", "F(3, 234) = 0,47", "0,70"],
                                       ["Welch (confirmação)", "F(3; 105,7) = 0,50", "0,68"],
                                       ["Kruskal-Wallis (confirmação)", "H(3) = 1,37", "0,71"], ["η² (tamanho do efeito)", "0,006", "—"]],
      size=14, alt=0.44)
decisao(sl, 7.0, 3.2, 5.73, 3.6, "Porque não outros testes", [
    "6 testes t entre pares: o risco de uma diferença «falsa» subia para cerca de 26%.",
    "Tukey: só se faz depois de a ANOVA rejeitar H0 (aqui p = 0,70).",
    "Bartlett para as variâncias: muito sensível à falta de normalidade; usámos Levene.",
    "Conclusão: sem evidência de diferenças; não rejeitar não prova que são iguais."], cor=ORANGE, size=14)
text(sl, 0.6, 5.55, 6.1, 1.2, ["η² = 0,006: o departamento explica 0,6% da produtividade, abaixo do limiar de efeito pequeno (0,01) da docente."],
     size=14, color=GRAY)

# ======================================================================= 9. intervalo de confiança
sl = slide("Quanto vale a produtividade média?", "Fase 4 · Inferência",
           notas="Intervalo com a distribuição t porque não conhecemos o desvio-padrão da população; com 238 pessoas t e z quase "
           "coincidem. Leitura: se repetíssemos a recolha muitas vezes, 95% dos intervalos apanhariam a verdadeira média. "
           "Não quer dizer que 95% das pessoas estão entre 76,4 e 79,7. Os dados são sintéticos: a população é o processo "
           "que gerou os dados.")
stat(sl, 0.6, 1.6, 5.8, "[76,4 ; 79,7]", "intervalo de confiança a 95% para a produtividade média (78,0 ± 1,6)", BLUE, h=1.9)
decisao(sl, 6.7, 1.6, 6.03, 2.6, "Porque t de Student, e não z", [
    "Não conhecemos o desvio-padrão da população: estimamo-lo com a amostra.",
    "Com 238 pessoas, t e z dão praticamente o mesmo.",
    "A falta de normalidade é moderada e a amostra é grande."], size=14)
decisao(sl, 0.6, 3.85, 5.8, 2.95, "Como se lê", [
    "Se repetíssemos a recolha muitas vezes, cerca de 95% dos intervalos conteriam a verdadeira média.",
    "É um intervalo para a média, não para cada pessoa."], cor=BLUE, size=14)
decisao(sl, 6.7, 4.45, 6.03, 2.35, "Cuidado", [
    "Dados sintéticos: a «população» é o processo que os gerou.",
    "Não cobre o teto em 98 nem erros de registo como o C097."], cor=ORANGE, size=14)

# ======================================================================= 10. regressão simples
sl = slide("Regressão simples: só o uso de IA explica pouco", "Fase 5 · Regressão simples",
           notas="A equação existe e o declive é significativo, mas o R² é 6%. Para 5 contra 10 horas, a diferença média "
           "estimada é 3,1 pontos, sem manter nada constante. O C001 tem resíduo de -9,9: o modelo sobrestima-o, e tem só meio "
           "ano de experiência. Os resíduos estão ligados à experiência (r = 0,45). É esse resultado que nos leva ao modelo "
           "múltiplo: não foi uma escolha arbitrária, foi o diagnóstico do modelo simples.")
text(sl, 0.6, 1.5, 12.1, 0.5, [[("produtividade estimada = 73,04 + 0,627 × horas de IA", {"bold": True, "font": HEAD})]], size=22, align=PP_ALIGN.CENTER)
img(sl, "fig_5_6_residuos_m1_sem_nota.png", 1.4, 2.1, w=10.5)
stat(sl, 0.6, 5.2, 2.3, "6%", "da produtividade explicada (R² = 0,058)", ORANGE, h=1.6)
stat(sl, 3.1, 5.2, 2.3, "+3,1", "pontos entre 5 h e 10 h (média, não causa)", BLUE, h=1.6)
decisao(sl, 5.6, 5.2, 7.13, 1.6, "O resultado que decide o passo seguinte", [
    "Os resíduos estão ligados à experiência (r = 0,45): falta uma variável no modelo.",
    "Por isso passamos à regressão múltipla."], cor=ORANGE, size=14)

# ======================================================================= 11. paradoxo
sl = slide("O paradoxo: a experiência estava por trás", "Fase 6 · Regressão múltipla",
           notas="Juntámos as variáveis uma a uma, sempre com os mesmos 233 casos. Só a formação quase não muda nada. A "
           "experiência corta o coeficiente para metade. Com tudo, cai 80% e deixa de ser significativo. Quem tem mais "
           "experiência usa mais IA e é mais produtivo: a associação inicial era, em grande parte, a experiência disfarçada. "
           "A experiência dá mais 1,6 pontos por ano e é a única claramente significativa.")
img(sl, "fig_6_4_coeficiente_ia_sem_nota.png", 0.6, 1.5, w=7.6)
stat(sl, 8.5, 1.5, 4.23, "0,64 → 0,13", "coeficiente da IA, sem e com os outros fatores (−80%, p = 0,47)", ORANGE, h=1.6)
stat(sl, 8.5, 3.25, 4.23, "+1,6", "pontos de produtividade por cada ano de experiência (p < 0,001)", GREEN, h=1.45)
decisao(sl, 0.6, 4.9, 12.13, 1.9, "Como se explica", [
    "Quem tem mais experiência usa mais IA (r = 0,27) e é mais produtivo (r = 0,50).",
    "Só com a experiência, o coeficiente da IA já cai para metade (0,31): a experiência é o fator de confusão.",
    "Não é multicolinearidade: VIF máximo 1,51 e o erro-padrão da IA quase não muda (0,166 → 0,179)."], size=14)

# ======================================================================= 12. comparar modelos
sl = slide("O modelo múltiplo é mesmo melhor?", "Fase 6 · Regressão múltipla",
           notas="Comparámos os dois modelos com os mesmos 233 colaboradores, como se faz nas aulas. Não usámos o R² simples "
           "porque sobe sempre que se juntam variáveis; o ajustado desconta. O teste F parcial da aula 4 testa as três "
           "variáveis juntas e dá p < 0,001. Mesmo assim, 73% da produtividade continua por explicar.")
table(sl, 0.6, 1.55, [3.6, 2.5, 2.5], [["Critério (mesmos 233 casos)", "M1: só IA", "M2: IA + 3 variáveis"],
                                        ["R²", "0,061", "0,280"], ["R² ajustado", "0,056", "0,267"],
                                        ["Teste F global", "p < 0,001", "p < 0,001"],
                                        ["Teste F parcial (M2 vs M1)", "—", "F(3, 228) = 23,1; p < 0,001"]], size=15, alt=0.5)
stat(sl, 9.5, 1.55, 3.23, "× 5", "o R² ajustado fica quase cinco vezes maior", GREEN, h=1.6)
decisao(sl, 0.6, 4.35, 6.0, 2.45, "Porque estes critérios", [
    "R² ajustado: o R² simples sobe sempre que se juntam variáveis.",
    "Teste F parcial (aula 4): testa as 3 variáveis juntas.",
    "Mesmos casos nos dois modelos, senão a comparação não é justa."], size=14)
decisao(sl, 6.8, 4.35, 5.93, 2.45, "Conclusão", [
    "O modelo múltiplo é claramente melhor e é o que responde à pergunta.",
    "Ainda assim, cerca de 73% da variação fica por explicar."], cor=BLUE, size=14)

# ======================================================================= 13. pressupostos e robustez
sl = slide("Pressupostos e robustez do modelo final", "Fase 6 · Regressão múltipla",
           notas="Primeiro os gráficos, depois os testes, como nas aulas 4 e 5. Sem padrão nem funil nos resíduos, Breusch-Pagan "
           "não rejeita, VIF baixos, Cook abaixo de 1. A normalidade falha quase só por causa do C097: sem ele fica normal. O "
           "Durbin-Watson está lá só por completude, porque não há ordem no tempo. Depois mudámos as nossas escolhas e o "
           "coeficiente da IA ficou sempre entre 0,12 e 0,15, nunca significativo.")
img(sl, "fig_6_6_residuos_m2_sem_nota.png", 0.6, 1.45, w=12.1)
table(sl, 0.6, 4.75, [3.1, 2.7], [["Pressuposto", "Resultado"], ["Variáveis a dizer o mesmo", "VIF ≤ 1,51 (ok abaixo de 5)"],
                                   ["Variância constante", "Breusch-Pagan p = 0,19"], ["Normalidade dos resíduos", "falha só pelo C097"],
                                   ["Observações influentes", "Cook máx. 0,07 (< 1)"]], size=13, alt=0.4)
table(sl, 6.7, 4.75, [4.3, 1.73], [["Versão do modelo", "Coef. IA (p)"], ["Sem o C097", "0,146 (0,38)"],
                                    ["+ carga e departamento", "0,144 (0,45)"], ["Complexidade como categoria", "0,122 (0,50)"],
                                    ["+ interação IA × experiência", "termo 0,028 (0,50)"]], size=13, alt=0.4)

# ======================================================================= 14. testes que não fizemos
sl = slide("Os testes que poderíamos ter feito, e porque não", "Síntese das escolhas",
           notas="Este diapositivo resume as alternativas. A ideia geral: escolhemos sempre o teste indicado pelo tipo de "
           "variáveis e pelas condições verificadas, e juntámos uma confirmação quando uma condição falhava. Nunca escolhemos "
           "pelo menor valor-p.")
table(sl, 0.6, 1.5, [2.9, 2.4, 2.5, 4.33], [
    ["Pergunta", "Usámos", "Alternativa", "Porque não"],
    ["Normalidade", "Shapiro-Wilk + Q-Q", "Kolmogorov-Smirnov", "Shapiro é o recomendado; o Q-Q mostra onde falha"],
    ["Associação IA–produtividade", "Pearson", "Só Spearman", "Relação em linha reta; Spearman fica como confirmação"],
    ["4 departamentos", "ANOVA", "6 testes t", "Risco de diferença «falsa» de cerca de 26%"],
    ["Variâncias iguais", "Levene (mediana)", "Bartlett", "Bartlett é sensível à falta de normalidade"],
    ["Pares de departamentos", "Nenhum", "Tukey", "Só depois de a ANOVA rejeitar H0"],
    ["Média da produtividade", "IC com t", "IC com z", "Desvio-padrão da população desconhecido"],
    ["Explicar a produtividade", "Regressão linear", "Classificar em grupos", "Perde informação de uma variável contínua"],
    ["Comparar modelos", "R² ajustado + F parcial", "R² simples", "O R² sobe sempre com mais variáveis"],
    ["Resíduos não normais", "Repetir sem C097", "Transformar (log)", "A falha vem do C097; mudar a escala complicava a leitura"],
], size=13, alt=0.5)

# ======================================================================= 15. conclusões
sl = slide("Conclusões em quatro níveis", "Conclusão",
           notas="Como pede o enunciado, separamos descrição, inferência, explicação e recomendação. A resposta à pergunta: "
           "quem usa mais IA é um pouco mais produtivo, mas sobretudo por ser mais experiente e formado.")
niveis = [("Descritivo", "Quem usa mais IA é um pouco mais produtivo (mediana 73,0 → 84,9 do quarto que menos usa ao que mais usa), com muitas exceções.", BLUE),
          ("Inferencial", "Associação fraca e significativa (r = 0,24). Departamentos sem diferenças (p ≈ 0,70). Média: [76,4 ; 79,7].", GREEN),
          ("Explicação", "Com experiência, formação e complexidade, o coeficiente da IA cai 80% e deixa de ser significativo. A experiência é o fator principal.", ORANGE),
          ("Recomendação", "Não tornar a IA obrigatória; investir em formação; testar com um estudo piloto controlado.", YELLOW)]
for k, (t1, t2, cor) in enumerate(niveis):
    y = 1.5 + k * 1.15
    box(sl, 0.6, y, 2.6, 0.98, cor)
    text(sl, 0.6, y, 2.6, 0.98, [[(t1, {"bold": True, "color": WHITE})]], size=18, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    box(sl, 3.3, y, 9.43, 0.98, LIGHT)
    text(sl, 3.55, y, 9.0, 0.98, [t2], size=15, anchor=MSO_ANCHOR.MIDDLE)
text(sl, 0.6, 6.25, 12.1, 0.6, [[("Resposta: ", {"bold": True}), ("trabalhar com IA não significa, por si só, trabalhar melhor.", {})]],
     size=18, align=PP_ALIGN.CENTER)

# ======================================================================= 16. recomendação e limitações
sl = slide(escuro=True, notas="Fechar com a recomendação e as duas limitações. Associação não é causa: para saber se a IA "
           "aumenta a produtividade seria preciso um estudo piloto com equipas escolhidas ao acaso.")
text(sl, 0.9, 0.7, 11.5, 0.8, ["Recomendação à direção"], size=32, color=WHITE, font=HEAD)
text(sl, 0.9, 1.6, 5.6, 4.6, [
    [("Não tornar a IA obrigatória.", {"bold": True, "color": YELLOW})],
    "Os dados mostram associação, não causa, e ela desaparece quando se tem em conta a experiência.",
    "Mesmo no melhor cenário, +5 h por semana valeriam cerca de 3 pontos.",
    "Manter a IA disponível e opcional; investir em boa formação.",
    "Fazer um estudo piloto: acesso e formação a equipas escolhidas ao acaso, medindo antes e depois."], size=16, color=WHITE, space=10)
box(sl, 7.0, 1.6, 5.43, 4.6, RGBColor(0x26, 0x3A, 0x5A))
text(sl, 7.3, 1.85, 4.9, 0.5, [[("Limitações", {"bold": True, "color": YELLOW})]], size=20)
text(sl, 7.3, 2.5, 4.9, 3.6, [
    "Uma só medição, sem distribuição ao acaso do uso de IA: não se pode falar de causa.",
    "Dados sintéticos, com teto em 98, um valor suspeito (C097), 10 casos com tarefas × tempo acima da carga e um uso de IA medido só em horas.",
    "O modelo final deixa cerca de 73% da variação por explicar."], size=15, color=WHITE, bullets=True, space=10)
text(sl, 0.9, 6.6, 11.5, 0.5, ["Obrigado. Perguntas?"], size=18, color=RGBColor(0xCA, 0xDC, 0xFC))

out = os.path.join(PASTA, "Apresentacao_TP1_MEPA.pptx")
prs.save(out); print("ok", out, n_slide[0], "diapositivos")
