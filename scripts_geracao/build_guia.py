# Gera GUIA_ANALISE_PASSO_A_PASSO.html (autossuficiente: figuras em base64, diagramas em SVG).
# Uso: python scripts_geracao/build_guia.py .   (as figuras têm de existir em figuras/)
import base64, html, os, sys, textwrap

REPO = sys.argv[1] if len(sys.argv) > 1 else "."
OUT = os.path.join(REPO, "GUIA_ANALISE_PASSO_A_PASSO.html")


def img(nome, alt):
    with open(os.path.join(REPO, "figuras", nome + ".png"), "rb") as f:
        b = base64.b64encode(f.read()).decode()
    return f'<img alt="{html.escape(alt)}" src="data:image/png;base64,{b}">'


# ── Fluxograma da escolha dos testes (SVG gerado) ────────────────────────────
def fluxograma():
    W, COLW, GAP = 1000, 226, 22
    xs = [14 + i * (COLW + GAP) for i in range(4)]
    cols = [
        [("q", "Quem usa mais IA tende a ser mais produtivo?"),
         ("c", "Duas variáveis quantitativas. O diagrama de dispersão mostra tendência linear, sem curvatura"),
         ("m", "Correlação de Pearson: r = 0,24"),
         ("c", "O diagrama mostra observações extremas (C097) e acumulação em 98; Pearson é sensível a elas"),
         ("m", "Spearman, que se baseia nas ordens: rs = 0,27"),
         ("r", "Conduzem à mesma leitura: associação positiva fraca")],
        [("q", "A produtividade média difere entre departamentos?"),
         ("c", "Quantos grupos? Com 2 seria um teste t. Aqui são 4: é precisa uma comparação global"),
         ("c", "Pressupostos: independência (desenho da recolha), normalidade por grupo (Shapiro-Wilk), variâncias (Levene p = 0,52)"),
         ("m", "ANOVA a um fator: p = 0,70"),
         ("m", "Mesma leitura com Welch (p = 0,68) e Kruskal-Wallis (p = 0,71)"),
         ("r", "Não rejeitamos H0. Sem comparações pós-hoc de Tukey")],
        [("q", "Qual é a produtividade média da população?"),
         ("c", "O desvio-padrão da população é desconhecido e estima-se pela amostra"),
         ("m", "Intervalo de confiança com a distribuição t de Student (237 graus de liberdade)"),
         ("r", "IC 95%: 76,4 a 79,7 pontos")],
        [("q", "Podemos explicar a produtividade a partir das horas de IA?"),
         ("m", "Regressão linear simples (M1): R² = 0,058"),
         ("c", "Os resíduos do M1 estão associados à experiência (r = 0,45): há estrutura por explicar"),
         ("m", "Regressão linear múltipla (M2): IA + experiência + formação + complexidade"),
         ("c", "Na base comum: R² ajustado e teste F parcial. Depois VIF e resíduos"),
         ("r", "O M2 responde à pergunta. Coeficiente da IA: de 0,64 para 0,13")],
    ]
    top_h = 40
    parts = []
    parts.append(f'<rect class="b-top" x="{W/2-190}" y="6" width="380" height="{top_h}" rx="20"/>')
    parts.append(f'<text class="t-top" x="{W/2}" y="31" text-anchor="middle">Que pergunta queremos responder?</text>')
    y0 = 6 + top_h + 44
    maxy = 0
    for x, col in zip(xs, cols):
        cx = x + COLW / 2
        # ligação do topo à coluna
        parts.append(f'<path class="ln" d="M{W/2} {6+top_h} V{6+top_h+18} H{cx} V{y0-6}" marker-end="url(#seta)"/>')
        y = y0
        for i, (kind, txt) in enumerate(col):
            lines = textwrap.wrap(txt, 33)
            h = 16 * len(lines) + 18
            rx = 18 if kind == "q" else 6
            parts.append(f'<rect class="b-{kind}" x="{x}" y="{y}" width="{COLW}" height="{h}" rx="{rx}"/>')
            for j, ln in enumerate(lines):
                parts.append(f'<text class="t-{kind}" x="{cx}" y="{y+21+16*j}" text-anchor="middle">{html.escape(ln)}</text>')
            y += h
            if i < len(col) - 1:
                parts.append(f'<path class="ln" d="M{cx} {y} V{y+16}" marker-end="url(#seta)"/>')
                y += 22
        maxy = max(maxy, y)
    H = maxy + 12
    return (f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
            f'aria-label="Fluxograma da escolha dos testes estatísticos">'
            '<defs><marker id="seta" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
            '<path d="M0 0 L10 5 L0 10 z" class="ah"/></marker></defs>' + "".join(parts) + "</svg>")


TRIANGULO = """
<svg viewBox="0 0 620 300" width="620" height="300" role="img" aria-label="Esquema do fator de confusão">
<defs><marker id="seta2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" class="ah"/></marker>
<marker id="seta3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" class="ah-w"/></marker></defs>
<rect class="b-m" x="210" y="14" width="200" height="54" rx="8"/>
<text class="t-m" x="310" y="38" text-anchor="middle">Experiência (anos)</text>
<text class="t-s" x="310" y="56" text-anchor="middle">controlada no modelo múltiplo</text>
<rect class="b-c" x="20" y="212" width="190" height="54" rx="8"/>
<text class="t-c" x="115" y="236" text-anchor="middle">Uso de IA</text>
<text class="t-s2" x="115" y="254" text-anchor="middle">horas por semana</text>
<rect class="b-c" x="410" y="212" width="190" height="54" rx="8"/>
<text class="t-c" x="505" y="236" text-anchor="middle">Produtividade</text>
<text class="t-s2" x="505" y="254" text-anchor="middle">0 a 100 pontos</text>
<path class="ln2" d="M258 68 L140 208" marker-end="url(#seta2)"/>
<path class="ln2" d="M362 68 L480 208" marker-end="url(#seta2)"/>
<path class="ln-w" d="M210 239 L406 239" marker-end="url(#seta3)"/>
<text class="t-l" x="176" y="126" text-anchor="end">r = 0,27</text>
<text class="t-ls" x="166" y="143" text-anchor="end">mais experientes usam mais IA</text>
<text class="t-l" x="444" y="126">r = 0,50</text>
<text class="t-ls" x="456" y="143">e são mais produtivos</text>
<text class="t-l" x="308" y="228" text-anchor="middle">0,64 sozinha</text>
<text class="t-ls" x="308" y="258" text-anchor="middle">0,13 com controlos (p = 0,47)</text>
</svg>
"""

HTML = r"""<!doctype html>
<html lang="pt-PT">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Guia da análise passo a passo</title>
<style>
:root{
  --bg:#f7f6f2; --card:#ffffff; --ink:#1f1e1c; --mut:#5b5a55; --line:#dcdad1;
  --acc:#1f63b8; --acc-bg:#e4eefb; --warn:#b4530f; --warn-bg:#fdeede; --ok:#14784f; --ok-bg:#e1f4ea;
  --q-bg:#fff4d6; --q-line:#d49b00;
}
@media (prefers-color-scheme: dark){
  :root{ --bg:#17171a; --card:#212126; --ink:#ecebe6; --mut:#a9a8a2; --line:#3a3a41;
    --acc:#7fb2f5; --acc-bg:#1d2f47; --warn:#f0a465; --warn-bg:#3d2815; --ok:#6fd0a2; --ok-bg:#173426;
    --q-bg:#3a3115; --q-line:#d4a72c; }
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
main{max-width:1060px;margin:0 auto;padding:28px 16px 64px}
h1{font-size:1.9rem;line-height:1.2;margin:0 0 6px;text-wrap:balance}
h2{font-size:1.35rem;margin:52px 0 10px;padding-top:14px;border-top:2px solid var(--line);text-wrap:balance}
h2 .n{display:inline-block;min-width:1.9em;height:1.9em;line-height:1.9em;text-align:center;border-radius:50%;
  background:var(--acc);color:var(--card);font-size:.95rem;margin-right:10px;vertical-align:2px}
h3{font-size:1.05rem;margin:26px 0 6px}
p{margin:8px 0;max-width:76ch}
.sub{color:var(--mut);margin:0 0 18px}
a{color:var(--acc)}
code{font:0.9em ui-monospace,Consolas,monospace;background:var(--acc-bg);padding:1px 5px;border-radius:4px}
nav{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 16px;margin:18px 0}
nav ol{margin:6px 0 0;padding-left:22px;columns:2;column-gap:32px}
nav li{margin:2px 0;break-inside:avoid}
@media (max-width:640px){nav ol{columns:1}}
.box{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin:14px 0}
.box.key{border-left:5px solid var(--acc)}
.box.warn{border-left:5px solid var(--warn);background:var(--warn-bg)}
.box.ok{border-left:5px solid var(--ok);background:var(--ok-bg)}
.box h3{margin-top:0}
.tag{display:inline-block;font-size:.72rem;font-weight:600;letter-spacing:.04em;text-transform:uppercase;color:var(--mut)}
figure{margin:16px 0;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px}
figure .canvas{overflow-x:auto}
figure img{display:block;max-width:100%;height:auto;background:#fff;border-radius:6px;padding:6px}
figcaption{font-size:.9rem;color:var(--mut);margin-top:10px;max-width:90ch}
figcaption b{color:var(--ink)}
.tw{overflow-x:auto;margin:12px 0}
table{border-collapse:collapse;width:100%;background:var(--card);font-size:.93rem}
th,td{border:1px solid var(--line);padding:7px 10px;text-align:left;vertical-align:top}
th{background:var(--acc-bg);font-weight:600}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.yes{color:var(--ok);font-weight:600}.no{color:var(--warn);font-weight:600}
/* percurso */
.steps{display:grid;gap:10px;margin:14px 0}
.step{display:grid;grid-template-columns:44px 1fr;gap:12px;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px;position:relative}
.step .k{width:40px;height:40px;border-radius:50%;background:var(--acc);color:var(--card);display:grid;place-items:center;font-weight:700}
.step h3{margin:0 0 2px;font-size:1rem}
.step .g{display:grid;grid-template-columns:repeat(3,1fr);gap:4px 18px;font-size:.92rem}
.step .g div span{display:block;font-size:.7rem;text-transform:uppercase;letter-spacing:.04em;color:var(--mut);font-weight:600}
@media (max-width:720px){.step .g{grid-template-columns:1fr}}
.step:not(:last-child)::after{content:"";position:absolute;left:33px;bottom:-11px;border:6px solid transparent;border-top-color:var(--acc);z-index:1}
/* funil */
.funil{display:flex;flex-wrap:wrap;align-items:stretch;gap:6px;margin:14px 0}
.funil .f{flex:1 1 150px;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 12px}
.funil .f b{display:block;font-size:1.7rem;line-height:1.1;color:var(--acc);font-variant-numeric:tabular-nums}
.funil .f small{color:var(--mut);display:block;line-height:1.35}
.funil .ar{align-self:center;color:var(--mut);font-size:1.2rem}
/* svg */
svg{display:block;font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
svg text{font-size:12px;fill:var(--ink)}
.b-top{fill:var(--ink)} .t-top{fill:var(--bg);font-size:14px;font-weight:600}
.b-q{fill:var(--q-bg);stroke:var(--q-line);stroke-width:1.5} .t-q{font-weight:600}
.b-c{fill:var(--card);stroke:var(--line);stroke-width:1.5}
.b-m{fill:var(--acc-bg);stroke:var(--acc);stroke-width:1.5} .t-m{font-weight:600}
.b-r{fill:var(--ok-bg);stroke:var(--ok);stroke-width:1.5}
.ln{fill:none;stroke:var(--mut);stroke-width:1.4} .ah{fill:var(--mut)}
.ln2{fill:none;stroke:var(--acc);stroke-width:2.2}
.ln-w{fill:none;stroke:var(--warn);stroke-width:2.2;stroke-dasharray:7 5} .ah-w{fill:var(--warn)}
svg .t-s,svg .t-s2,svg .t-ls{font-size:11px;fill:var(--mut)}
svg .t-l{font-size:13px;font-weight:700}
.leg{display:flex;flex-wrap:wrap;gap:6px 18px;font-size:.85rem;color:var(--mut);margin-top:8px}
.leg i{display:inline-block;width:14px;height:14px;border-radius:4px;vertical-align:-2px;margin-right:5px;border:1.5px solid}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media (max-width:760px){.cols{grid-template-columns:1fr}}
ul{padding-left:22px;margin:8px 0;max-width:76ch} li{margin:4px 0}
footer{margin-top:48px;color:var(--mut);font-size:.88rem;border-top:1px solid var(--line);padding-top:12px}
@media print{body{background:#fff} h2{break-after:avoid} figure,.box,.step,table{break-inside:avoid}}
.doc{background:var(--card);border:1px solid var(--line);border-left:5px solid var(--ok);border-radius:10px;padding:10px 16px;margin:14px 0}
.doc .tag{color:var(--ok)}
.doc p{margin:4px 0}
.doc q{quotes:"«" "»";font-style:italic}
.ref{font-size:.8rem;color:var(--mut);white-space:nowrap}
table.ficha td:first-child{width:9.5em;font-weight:600;background:var(--acc-bg)}
.chips{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin:10px 0}
.chips span{background:var(--acc-bg);border:1px solid var(--acc);border-radius:999px;padding:3px 12px;font-size:.92rem}
.chips i{color:var(--mut);font-style:normal}
</style>
</head>
<body>
<main>

<span class="tag">TP1 de MEPA · Mestrado em Inteligência Artificial · IPCA 2026/27</span>
<h1>O paradoxo da IA: guia da análise passo a passo</h1>
<p class="sub">Para o Gilberto e o Rúbem reverem, antes da defesa, o que foi feito em cada etapa e porque se escolheu cada método. As explicações seguem a forma e o vocabulário das aulas da docente; cada caixa verde cita a aula e o diapositivo de onde vem. Segue a numeração do notebook <code>TP1_MEPA_IA_Produtividade.ipynb</code>.</p>

<div class="box key">
<h3>A história toda em quatro frases</h3>
<p>Quem usa mais IA é, em média, um pouco mais produtivo, mas a associação é fraca (r = 0,24) e o uso de IA, sozinho, explica cerca de 6% da variabilidade observada na produtividade.</p>
<p>Não existe evidência de que a produtividade média difira entre departamentos (ANOVA, p = 0,70).</p>
<p>Controlando a experiência, a formação em IA e a complexidade das tarefas, o coeficiente da IA passa de 0,64 para 0,13 pontos por hora e deixa de haver evidência estatística de associação (p = 0,47). A experiência é a única explicativa com associação clara: mais 1,6 pontos por ano.</p>
<p>Por isso o grupo não recomenda tornar a IA obrigatória: os resultados descrevem associações e não permitem estabelecer relações causais.</p>
</div>

<nav>
<b>Índice</b>
<ol>
<li><a href="#s1">O percurso completo</a></li>
<li><a href="#s2">Como a docente pede que se explique um método</a></li>
<li><a href="#s3">Preparação dos dados</a></li>
<li><a href="#s4">Como se escolheu cada método</a></li>
<li><a href="#s5">Teste t ou ANOVA?</a></li>
<li><a href="#s6">Normalidade: o que se avalia e para quê</a></li>
<li><a href="#s7">Associação: Pearson e Spearman</a></li>
<li><a href="#s8">Departamentos: ANOVA</a></li>
<li><a href="#s9">Regressão linear simples (M1)</a></li>
<li><a href="#s10">Regressão linear múltipla (M2)</a></li>
<li><a href="#s11">Diagnósticos dos dois modelos</a></li>
<li><a href="#s12">Pontos frágeis a ter prontos na defesa</a></li>
<li><a href="#s13">Glossário nas palavras das aulas</a></li>
</ol>
</nav>

<h2 id="s1"><span class="n">1</span>O percurso completo</h2>
<p>Cada etapa começa numa pergunta do enunciado e termina numa resposta. O fio condutor é uma observação feita na etapa 3 (vários dos que usam muita IA e são muito produtivos têm muita experiência) que só se esclarece na etapa 6.</p>

<div class="steps">
 <div class="step"><div class="k">1</div><div><h3>Verificar a qualidade dos dados</h3><div class="g">
  <div><span>Pergunta</span>Podemos começar imediatamente a analisar?</div>
  <div><span>O que se fez</span>Procurar duplicados, valores em falta e categorias inconsistentes; investigar os valores extremos</div>
  <div><span>Resultado</span>240 colaboradores; 238, 236 ou 233 casos completos conforme a análise</div></div></div></div>
 <div class="step"><div class="k">2</div><div><h3>Análise univariada</h3><div class="g">
  <div><span>Pergunta</span>Como são a produtividade e o uso de IA?</div>
  <div><span>O que se fez</span>Centro, dispersão e distribuição: medidas, histograma, boxplot e Q-Q</div>
  <div><span>Resultado</span>Média 78,0 e mediana 79,35; assimetria à esquerda e acumulação no máximo (98)</div></div></div></div>
 <div class="step"><div class="k">3</div><div><h3>Análise bivariada</h3><div class="g">
  <div><span>Pergunta</span>Quem usa mais IA tende a ser mais produtivo?</div>
  <div><span>O que se fez</span>Diagrama de dispersão; depois Pearson e Spearman</div>
  <div><span>Resultado</span>r = 0,24 e r<sub>s</sub> = 0,27: associação positiva fraca</div></div></div></div>
 <div class="step"><div class="k">4</div><div><h3>Inferência</h3><div class="g">
  <div><span>Pergunta</span>A produtividade média difere entre departamentos? Qual é a média na população?</div>
  <div><span>O que se fez</span>ANOVA de um fator, depois de avaliar os pressupostos; intervalo de confiança com t</div>
  <div><span>Resultado</span>p = 0,70: não rejeitamos H0; IC 95% de 76,4 a 79,7</div></div></div></div>
 <div class="step"><div class="k">5</div><div><h3>Regressão linear simples (M1)</h3><div class="g">
  <div><span>Pergunta</span>Podemos explicar a produtividade a partir das horas de IA?</div>
  <div><span>O que se fez</span>Ajustar a reta, fazer inferência sobre o declive, avaliar o R² e diagnosticar os resíduos</div>
  <div><span>Resultado</span>73,04 + 0,627 × IA; R² = 0,058; resíduos associados à experiência</div></div></div></div>
 <div class="step"><div class="k">6</div><div><h3>Regressão linear múltipla (M2)</h3><div class="g">
  <div><span>Pergunta</span>Como se relaciona a IA com a produtividade quando outros fatores são considerados em simultâneo?</div>
  <div><span>O que se fez</span>Teste F global, testes t, R² ajustado, F parcial na base comum, VIF e resíduos</div>
  <div><span>Resultado</span>Coeficiente da IA 0,13 (p = 0,47); R² ajustado 0,267</div></div></div></div>
 <div class="step"><div class="k">7</div><div><h3>Responder à pergunta inicial</h3><div class="g">
  <div><span>Pergunta</span>Deve a IA ser obrigatória?</div>
  <div><span>O que se fez</span>Separar descrição, inferência, explicação estatística e recomendação</div>
  <div><span>Resultado</span>Não recomendar; propor formação e um estudo piloto</div></div></div></div>
</div>
<p class="sub">Esquema 1. As sete etapas do trabalho, com a pergunta, o que se fez e o resultado de cada uma.</p>

<h2 id="s2"><span class="n">2</span>Como a docente pede que se explique um método</h2>
<p>Em todas as aulas a explicação de um método tem a mesma forma: começa numa pergunta, escolhe-se a análise, executa-se, lê-se o resultado e responde-se à pergunta no contexto. É esta a forma a usar na defesa.</p>

<div class="chips"><span>Pergunta</span><i>→</i><span>Método</span><i>→</i><span>Python</span><i>→</i><span>Resultado</span><i>→</i><span>Interpretação</span><i>→</i><span>Resposta</span></div>
<p class="sub">Esquema 2. O percurso de cada análise, tal como aparece na aula 3 (diapositivo 34).</p>

<div class="doc">
<span class="tag">Nas palavras da docente</span>
<p><q>Não quero apenas um p-valor. Para cada pergunta quero uma análise completa.</q> <span class="ref">Aula 3, diap. 38</span></p>
<p><q>Não comecem pelo teste. Comecem pela pergunta.</q> <span class="ref">Aula 3, diap. 35</span></p>
<p><q>Não executamos vários testes para escolher aquele que produz o menor p-valor. O método é escolhido antes de olhar para o resultado.</q> <span class="ref">Aula 3, diap. 15</span></p>
<p><q>Não quero apenas "rejeito" ou "não rejeito H0". Quero a conclusão no contexto do problema.</q> <span class="ref">Aula 4, diap. 57</span></p>
<p><q>Não fazemos testes "porque sim". Cada análise responde a uma pergunta concreta sobre o modelo.</q> <span class="ref">Aula 4, diap. 51</span></p>
</div>

<div class="tw"><table class="ficha">
<tr><th>Parte</th><th>O que a docente pede (aula 3, diap. 38)</th><th>Exemplo com a ANOVA dos departamentos</th></tr>
<tr><td>1. Escolha</td><td>Porque é que o método escolhido é adequado à pergunta e aos dados?</td><td>Uma variável quantitativa (produtividade) e uma qualitativa com quatro grupos independentes (departamento): comparação global de médias com a ANOVA.</td></tr>
<tr><td>2. Resultado</td><td>O que significa o resultado estatístico obtido?</td><td>F(3, 234) = 0,47: a variabilidade entre departamentos é pequena face à variabilidade dentro dos departamentos.</td></tr>
<tr><td>3. Decisão</td><td>Rejeitamos ou não rejeitamos H0?</td><td>Como p = 0,70 &gt; 0,05, não rejeitamos H0.</td></tr>
<tr><td>4. Resposta</td><td>O que podemos concluir, no contexto da pergunta inicial?</td><td>Ao nível de significância de 5%, não existe evidência estatística suficiente para concluir que a produtividade média difere entre departamentos. Isto não prova que as médias são iguais.</td></tr>
</table></div>
<p class="sub">Tabela 1. As quatro partes de uma resposta completa. As secções 7 a 10 deste guia usam esta mesma ficha para cada método. O infográfico «Guia de Inferência Estatística» pede o mesmo na conclusão: o teste utilizado e a justificação da escolha, a estatística de teste e o valor-p, a decisão e a interpretação no contexto; e acrescenta a dimensão do efeito.</p>

<h3>Vocabulário: dizer como nas aulas</h3>
<div class="tw"><table>
<tr><th>Nas aulas diz-se</th><th>No notebook ou no relatório aparece</th><th>Nota</th></tr>
<tr><td>p-valor</td><td>valor-p</td><td>Os diapositivos das aulas 2 a 5 usam sempre «p-valor»; os infográficos e o guião da aula 8 usam «valor-p». Significam o mesmo.</td></tr>
<tr><td>p &lt; 0,05 rejeitamos H0; p ≥ 0,05 não rejeitamos</td><td>«rejeitamos quando p ≤ 0,05»</td><td>Os diapositivos (aula 3, diap. 12) escrevem p &lt; 0,05; os infográficos escrevem p ≤ 0,05, como o notebook. Nenhum resultado do trabalho é exatamente 0,05, por isso a decisão é a mesma nas duas formas.</td></tr>
<tr><td>intercepto e declive</td><td>ordenada na origem e declive</td><td>Aula 4, diap. 11.</td></tr>
<tr><td>diagrama de dispersão</td><td>gráfico de dispersão</td><td>Aula 2, diap. 21.</td></tr>
<tr><td>valores extremos, outliers</td><td>valores atípicos, valores afastados</td><td>Aula 1, diap. 29: «Um outlier investiga-se. Não se elimina automaticamente.»</td></tr>
<tr><td>variabilidade explicada pelo modelo</td><td>variação explicada</td><td>Aula 4, diap. 29.</td></tr>
<tr><td>associação parcial; controlando as restantes variáveis; mantendo constantes</td><td>comparando colaboradores com a mesma experiência</td><td>Aula 4, diap. 63. As duas formas são corretas; a primeira é a da docente.</td></tr>
<tr><td>comparações pós-hoc (Tukey)</td><td>comparações par a par</td><td>Aula 3, diap. 33.</td></tr>
<tr><td>homoscedasticidade; heteroscedasticidade</td><td>variância constante dos resíduos</td><td>Aula 4, diap. 48.</td></tr>
<tr><td>«não encontramos evidência de...»; «compatível com o pressuposto»</td><td>«pressuposto cumprido»</td><td>Aula 4, diap. 99: não rejeitar é compatibilidade com o modelo, não prova.</td></tr>
<tr><td>ajustando pelas restantes; omissões importantes</td><td>fator de confusão</td><td>O termo «fator de confusão» não aparece nos diapositivos das aulas 1 a 5, nos guiões de código nem nos infográficos (nas aulas 6 e 7 só surge «matriz de confusão», que é outra coisa). Pode usar-se, mas explicado com as palavras da aula 4 (diap. 41 e 66).</td></tr>
<tr><td>(não usado nas aulas 1 a 5)</td><td>robustez, análise de sensibilidade</td><td>Na defesa basta dizer «repetimos a análise sem o C097 para ver se a conclusão muda».</td></tr>
</table></div>
<p class="sub">Tabela 2. Diferenças de vocabulário entre as aulas e os textos do trabalho. Não mudam nenhum resultado; mudam a forma de o dizer.</p>

<h2 id="s3"><span class="n">3</span>Preparação dos dados</h2>
<div class="doc">
<span class="tag">Nas palavras da docente</span>
<p><q>Antes de qualquer análise devemos verificar a qualidade dos dados.</q> Procuram-se valores em falta, observações duplicadas e categorias registadas de forma inconsistente. <q>Um modelo estatístico não corrige automaticamente problemas existentes nos dados.</q> <span class="ref">Aula 2, diap. 7</span></p>
</div>

<div class="funil">
 <div class="f"><b>241</b><small>linhas no Excel</small></div><div class="ar">→</div>
 <div class="f"><b>240</b><small>colaboradores, depois de eliminar a duplicação do C084</small></div><div class="ar">→</div>
 <div class="f"><b>238</b><small>com produtividade (descrição, ANOVA, IC)</small></div><div class="ar">→</div>
 <div class="f"><b>236</b><small>com produtividade e uso de IA (correlação, M1)</small></div><div class="ar">→</div>
 <div class="f"><b>233</b><small>casos completos nas cinco variáveis do M2</small></div>
</div>
<p class="sub">Esquema 3. Porque é que o número de casos muda de análise para análise: há 8 valores em falta, um em cada um de 8 registos, e cada análise usa os casos com informação nas variáveis de que precisa.</p>

<div class="tw"><table>
<tr><th>O que se encontrou</th><th>Decisão</th><th>Como a docente trata o mesmo caso</th><th>Efeito verificado</th></tr>
<tr><td>C084 em duas linhas iguais</td><td>Fica uma</td><td>«Não temos dois participantes diferentes. Temos o mesmo registo repetido. Neste caso faz sentido eliminar uma das linhas.» «Antes de eliminar, vamos observar.» <span class="ref">Aula 2, diap. 9 e 10</span></td><td>240 identificadores únicos</td></tr>
<tr><td>8 valores em falta</td><td>Não imputar; excluir apenas os casos sem informação nas variáveis de cada análise</td><td>«Isto não significa que devemos eliminar imediatamente três participantes. A decisão depende da análise.» <span class="ref">Aula 2, diap. 8</span> «Excluímos apenas os casos sem informação nas variáveis desta análise.» <span class="ref">Aula 5, diap. 8</span></td><td>r = 0,241 com 236 casos e 0,246 com 233</td></tr>
<tr><td>3 grafias diferentes de departamento</td><td>Uniformizar</td><td>«Para nós representam a mesma categoria. Para o Python são categorias diferentes.» «Corrigimos apenas a forma como a informação estava escrita. Não alterámos o significado dos dados.» <span class="ref">Aula 2, diap. 12 e 13</span></td><td>4 departamentos: 85, 66, 58 e 31</td></tr>
<tr><td>C097 com produtividade 19 (o valor seguinte é 43,5)</td><td>Manter e repetir as análises sem ele</td><td>«Um outlier investiga-se. Não se elimina automaticamente.» <span class="ref">Aula 1, diap. 29</span></td><td>Nenhuma conclusão muda</td></tr>
<tr><td>13 colaboradores com produtividade 98 (o máximo observado)</td><td>Manter e registar como limitação</td><td>Não há caso equivalente nas aulas. É uma característica da escala de avaliação.</td><td>Contribui para o desvio à normalidade</td></tr>
<tr><td>10 casos em que tarefas × tempo por tarefa excedem um mês de trabalho</td><td>Assinalar, manter e repetir sem eles</td><td>A mesma regra dos outliers: investigar primeiro. O limite de um mês é uma suposição do grupo.</td><td>r = 0,241; ANOVA p = 0,557</td></tr>
<tr><td>Complexidade das tarefas é ordinal (1 a 5)</td><td>Tratada como quantitativa no modelo</td><td>A docente faz a mesma opção com a produtividade: «Uma diferença de um ponto é interpretada como comparável ao longo da escala. Esta opção exige justificação numa investigação real.» <span class="ref">Aula 4, diap. 4</span></td><td>Como categoria o modelo não melhora (p = 0,20)</td></tr>
<tr><td>Tarefas, tempo por tarefa e qualidade</td><td>Ficam fora dos modelos</td><td>É o dicionário da base que avisa: são indicadores do mesmo desempenho, medidos ao mesmo tempo.</td><td>Modelos só com fatores anteriores ao desempenho</td></tr>
</table></div>
<p class="sub">Tabela 3. Decisões de preparação dos dados (blocos 1.2 a 1.6 e 6.1 do notebook) e a regra das aulas que as sustenta.</p>

<h2 id="s4"><span class="n">4</span>Como se escolheu cada método</h2>
<div class="doc">
<span class="tag">Nas palavras da docente</span>
<p><q>Antes de escolher o teste...</q> devemos considerar: que pergunta queremos responder; que tipo de variável temos; quantos grupos estamos a comparar; se as observações são independentes; como se distribuem os dados; se existem valores extremos; qual é a dimensão das amostras; que pressupostos exige o método. <span class="ref">Aula 3, diap. 15</span></p>
<p><q>A pergunta determina a ferramenta estatística de que precisamos.</q> <span class="ref">Aula 2, diap. 35</span></p>
<p><q>Não existe um método universalmente "melhor". A escolha depende da pergunta, dos dados e dos pressupostos.</q> <span class="ref">Aula 3, diap. 14</span></p>
</div>

<figure>
<div class="canvas">@@FLUXO@@</div>
<div class="leg">
 <span><i style="background:var(--q-bg);border-color:var(--q-line)"></i>pergunta</span>
 <span><i style="background:var(--card);border-color:var(--line)"></i>o que se observou nos dados</span>
 <span><i style="background:var(--acc-bg);border-color:var(--acc)"></i>método aplicado</span>
 <span><i style="background:var(--ok-bg);border-color:var(--ok)"></i>resposta</span>
</div>
<figcaption><b>Esquema 4.</b> Fluxograma da escolha dos métodos. Cada coluna é uma das quatro perguntas do trabalho e lê-se de cima para baixo, pela ordem das aulas: pergunta, observação dos dados, método, resposta.</figcaption>
</figure>

<div class="box warn">
<h3>O método principal foi escolhido antes de ver o resultado</h3>
<p>O trabalho apresenta, ao lado de alguns testes, uma segunda análise (Spearman ao lado de Pearson; Welch e Kruskal-Wallis ao lado da ANOVA). Isto só é compatível com a regra da aula 3 se ficar claro, na defesa, que:</p>
<ul>
<li>o método principal foi decidido antes de olhar para os p-valores, a partir da pergunta e dos pressupostos (bloco 4.3 do notebook: «Decisão, tomada antes de ver o resultado»);</li>
<li>a decisão sobre H0 é a do método principal; as outras análises não serviram para escolher o menor p-valor;</li>
<li>comparar análises é o que as aulas pedem: «Pearson e Spearman conduzem à mesma leitura?» <span class="ref">Aula 2, diap. 37</span> e «Compare os valores-p da ANOVA clássica e da ANOVA de Welch» <span class="ref">guião da aula 8, pergunta 8</span>.</li>
</ul>
</div>

<h2 id="s5"><span class="n">5</span>Teste t ou ANOVA?</h2>
<p>Nas aulas, a escolha entre os dois depende de quantos grupos se comparam. A distribuição t aparece ainda em dois outros sítios do trabalho, que não são comparações de grupos.</p>

<div class="doc">
<span class="tag">Nas palavras da docente</span>
<p><q>Porque não fazemos três testes t?</q> <q>Cada teste envolve um risco de Erro Tipo I. Quando realizamos várias comparações separadas, aumentamos o risco global de encontrar pelo menos uma diferença significativa apenas por acaso. Precisamos de uma comparação global.</q> <span class="ref">Aula 3, diap. 30</span></p>
<p>O Erro Tipo I é rejeitar H0 quando H0 é verdadeira: um falso positivo, com probabilidade α. <span class="ref">Aula 3, diap. 18</span></p>
</div>

<div class="tw"><table>
<tr><th>Pergunta (como no quadro da aula 3, diap. 34)</th><th>Ferramenta</th><th>No trabalho</th></tr>
<tr><td>Qual é a média populacional?</td><td>Intervalo de confiança, com a distribuição t</td><td>Bloco 4.6: IC 95% de 76,4 a 79,7</td></tr>
<tr><td>Dois grupos apresentam diferenças?</td><td>Teste t (de Student ou de Welch, conforme o Levene) ou Mann-Whitney</td><td>Não se aplica: o enunciado não pede nenhuma comparação entre dois grupos</td></tr>
<tr><td>Três ou mais grupos apresentam diferenças?</td><td>ANOVA</td><td>Bloco 4.4: quatro departamentos</td></tr>
<tr><td>Existe evidência de associação linear? (declive)</td><td>Teste t ao declive</td><td>Blocos 5.1 e 6.3: um teste t por coeficiente</td></tr>
</table></div>
<p class="sub">Tabela 4. Onde entra cada ferramenta. Com quatro departamentos seriam seis testes t; se fossem independentes, o risco global de pelo menos um falso positivo passaria de 5% para cerca de 26% (1 − 0,95<sup>6</sup>).</p>

<div class="box">
<h3>O teste t dentro da regressão</h3>
<p>Para testar H0: β<sub>1</sub> = 0 compara-se o valor estimado com a sua incerteza: t = b<sub>1</sub> / SE(b<sub>1</sub>). «Quanto maior for b<sub>1</sub> relativamente ao seu erro-padrão, maior será a evidência contra H0.» <span class="ref">Aula 4, diap. 21</span></p>
<p>No trabalho: IA no M1, t = 3,80 (p &lt; 0,001); IA no M2, t = 0,72 (p = 0,47); experiência no M2, t = 8,32 (p &lt; 0,001).</p>
<p>Na regressão simples o teste F global equivale ao teste t ao declive (F = t²): «Não são duas evidências independentes.» <span class="ref">Aula 4, diap. 28</span> No M1, 3,796² = 14,41, que é o F do modelo.</p>
</div>

<h2 id="s6"><span class="n">6</span>Normalidade: o que se avalia e para quê</h2>
<div class="doc">
<span class="tag">Nas palavras da docente</span>
<p><q>Não estamos a testar se X ou Y são normais. Estamos a avaliar os resíduos do modelo.</q> <span class="ref">Aula 4, diap. 45</span></p>
<p><q>A hipótese de normalidade dos erros permite justificar, no modelo clássico, as distribuições utilizadas para realizar a inferência sobre os coeficientes</q>: testes t, p-valores e intervalos de confiança. <span class="ref">Aula 4, diap. 45</span></p>
<p><q>"Paramétrico" não significa simplesmente "os dados são normais". Cada método tem pressupostos próprios.</q> <span class="ref">Aula 3, diap. 13</span></p>
<p>Shapiro-Wilk: H0, os resíduos seguem uma distribuição normal; H1, não seguem. <q>Um p-valor elevado indica que o teste não detetou um desvio suficiente para rejeitar a normalidade. Não prova que os erros sejam normais.</q> <span class="ref">Aula 5, diap. 43</span></p>
<p>Q-Q: <q>comparamos os quantis dos resíduos com quantis de uma normal. Uma disposição aproximadamente linear é compatível com o modelo normal.</q> <span class="ref">Aula 5, diap. 43</span></p>
<p>O teste faz-se <q>sempre em conjunto com gráficos (histograma, Q-Q plot) e análise de valores atípicos</q>. <q>Em amostras grandes, testes de normalidade podem detetar desvios muito pequenos que não são relevantes do ponto de vista prático.</q> <q>Em modelos de regressão, avaliar a normalidade dos resíduos (não apenas da variável resposta).</q> <span class="ref">Infográfico «Testes de normalidade»</span></p>
</div>

<p>No trabalho a normalidade aparece em três sítios. Só o terceiro é um pressuposto de um modelo; o primeiro é descrição.</p>

<div class="tw"><table>
<tr><th>O que se avaliou</th><th>Para quê</th><th class="num">p (todos)</th><th class="num">p sem C097</th><th>Leitura, como nas aulas</th></tr>
<tr><td>A distribuição da produtividade (2.4)</td><td>Descrever a variável: centro, dispersão, forma e valores extremos. Não é pressuposto de nenhum modelo</td><td class="num no">0,00002</td><td class="num no">0,0009</td><td>Existe evidência de desvio à normalidade. A mediana é mais robusta perante a assimetria</td></tr>
<tr><td>A produtividade em cada departamento (4.3)</td><td>Pressuposto da ANOVA, verificado por grupo como no guião da aula 3 (bloco 13)</td><td class="num"><span class="yes">AD 0,36 · Com 0,32 · Op 0,06</span> · <span class="no">Dev 0,0004</span></td><td class="num no">Dev 0,027</td><td>Em três grupos não há evidência contra a normalidade; em Desenvolvimento há</td></tr>
<tr><td>Os resíduos do M1 (5.6)</td><td>Sustenta os testes t, os p-valores e os IC do modelo</td><td class="num no">0,0001</td><td class="num no">0,030</td><td>Evidência contra o pressuposto de normalidade</td></tr>
<tr><td>Os resíduos do M2 (6.6)</td><td>O mesmo, para o modelo final</td><td class="num no">0,00002</td><td class="num yes">0,965</td><td>Com todos os casos há evidência contra; sem o C097 os resíduos são compatíveis com o pressuposto</td></tr>
</table></div>
<p class="sub">Tabela 5. Resultados do Shapiro-Wilk. A laranja, H0 rejeitada a 5%; a verde, não rejeitada (o que é compatibilidade e não prova de normalidade). AD = Análise de Dados, Com = Comunicação, Op = Operações, Dev = Desenvolvimento.</p>

<figure>
@@FIG24@@
<figcaption><b>Figura A</b> (bloco 2.4, Figura 2 do relatório). «Número + gráfico + contexto é mais informativo do que qualquer um deles isoladamente» (aula 2, diap. 19). O histograma mostra a forma, o boxplot os valores extremos (C097 e C129) e o Q-Q onde os pontos se afastam da reta: na cauda inferior, pelos valores muito baixos, e na superior, onde ficam em linha horizontal porque 13 colaboradores têm o máximo de 98.</figcaption>
</figure>

<div class="box warn">
<h3>Normalidade na ANOVA: por grupo ou nos resíduos?</h3>
<p>O notebook testou cada grupo, como no guião da aula 3 (bloco 13) e no guia de escolha da docente («Independentes: avaliar em cada grupo»). No guião da aula 8 (pergunta 7) a normalidade avalia-se nos resíduos do modelo: «avaliamos aproximadamente a distribuição dos resíduos do modelo». As duas formas foram dadas.</p>
<p>Calculado para este guia (não está no notebook): o Shapiro-Wilk dos resíduos da ANOVA dá p = 0,00006, e p = 0,003 sem o C097. A leitura é a mesma: há evidência de desvio à normalidade, por isso o trabalho acompanhou a ANOVA com o Kruskal-Wallis.</p>
</div>

<h2 id="s7"><span class="n">7</span>Associação: Pearson e Spearman</h2>
<div class="doc">
<span class="tag">Nas palavras da docente</span>
<p><q>Primeiro observamos. Só depois calculamos.</q> No diagrama de dispersão procuramos direção, intensidade, forma e valores atípicos. <span class="ref">Aula 2, diap. 21 e 22</span></p>
<p>Pearson mede <q>a intensidade e direção de uma associação linear entre duas variáveis quantitativas</q>. <span class="ref">Aula 2, diap. 25</span> <q>Pearson trabalha diretamente com os valores observados e pode ser sensível a observações extremas.</q> <span class="ref">Aula 2, diap. 27</span></p>
<p>Spearman mede <q>a intensidade e direção de uma associação monotónica</q> e <q>baseia-se nas suas ordens</q>. É útil quando a relação é monotónica mas não necessariamente linear, quando existem valores extremos ou com variáveis ordinais. <span class="ref">Aula 2, diap. 28</span></p>
<p><q>Correlação não implica causalidade.</q> <span class="ref">Aula 2, diap. 25</span></p>
</div>

<div class="tw"><table class="ficha">
<tr><th>Parte</th><th>Associação entre uso de IA e produtividade (bloco 3.2)</th></tr>
<tr><td>Pergunta</td><td>Quem usa mais IA tende a ser mais produtivo?</td></tr>
<tr><td>Escolha</td><td>As duas variáveis são quantitativas e o diagrama de dispersão mostra uma tendência ascendente sem curvatura: Pearson. O mesmo diagrama mostra observações extremas (C097 com 19) e a acumulação em 98, e Pearson é sensível a observações extremas (o infográfico de Pearson põe como pressuposto a ausência de outliers influentes): por isso calcula-se também Spearman, que usa as ordens e é mais robusto a outliers. É a mesma razão por que Spearman aparece na aula 2 (a observação com 9 cafés por dia).</td></tr>
<tr><td>Resultado</td><td>r = 0,241 (n = 236) e r<sub>s</sub> = 0,266. Os dois têm sinal positivo.</td></tr>
<tr><td>Interpretação</td><td>Direção: positiva. Intensidade: fraca. O gráfico é coerente com o coeficiente: tendência ascendente com muita dispersão. Observações que merecem atenção: C097, C134 e C035. Pearson e Spearman conduzem à mesma leitura.</td></tr>
<tr><td>Resposta</td><td>Nesta amostra, maior uso de IA está associado a maior produtividade, com intensidade fraca. Isto não permite concluir que a IA seja a causa de maior produtividade.</td></tr>
</table></div>
<p>Intensidade: no infográfico da correlação de Pearson, 0,2 ≤ |r| &lt; 0,4 é uma associação fraca e |r| &lt; 0,2 é muito fraca ou inexistente; o de Spearman usa a mesma escala. O «Guia de Inferência Estatística» dá como referência 0,1 (fraca), 0,3 (moderada) e 0,5 (forte). Com r = 0,24 a leitura é «fraca» nas duas.</p>
<p class="sub">Tabela 6. A ficha da correlação responde às cinco perguntas que a docente exige em vez de «apenas o valor da correlação» (aula 2, diap. 37): direção, intensidade, coerência com o gráfico, observações a merecer atenção e concordância entre Pearson e Spearman.</p>

<figure>
@@FIG31@@
<figcaption><b>Figura B</b> (bloco 3.1, Figura 3 do relatório). À esquerda, o diagrama de dispersão: cada ponto é um colaborador. À direita, boxplots da produtividade por quartil de uso de IA. A tendência é ascendente, mas para o mesmo número de horas de IA a produtividade pode ser muito diferente: a IA não explica sozinha toda a produtividade.</figcaption>
</figure>

<div class="box warn">
<h3>Significância estatística e intensidade são coisas diferentes</h3>
<p>O p-valor da correlação (p &lt; 0,001) diz que há evidência de associação. A intensidade lê-se no coeficiente: r = 0,24 é fraco e r² = 0,058. A docente faz a mesma distinção na regressão: «Significância estatística ≠ capacidade explicativa elevada» <span class="ref">Aula 4, diap. 32</span>.</p>
</div>

<h2 id="s8"><span class="n">8</span>Departamentos: ANOVA</h2>
<div class="doc">
<span class="tag">Nas palavras da docente</span>
<p><q>A ANOVA compara variabilidade entre grupos com variabilidade dentro dos grupos. Se os grupos forem muito diferentes entre si relativamente à variabilidade existente dentro dos grupos, temos evidência contra a igualdade das médias.</q> <span class="ref">Aula 3, diap. 31</span></p>
<p>H0: as médias populacionais são iguais. H1: pelo menos uma média difere. <q>Não significa que todas as médias sejam diferentes.</q> <span class="ref">Guião da aula 8, pergunta 5</span></p>
<p>A ANOVA responde a «Existe pelo menos uma diferença?», não a «Entre que grupos existe essa diferença?». Para isso são precisas comparações pós-hoc. <span class="ref">Aula 3, diap. 33</span></p>
<p><q>O valor-p responde à compatibilidade com a hipótese nula; η² descreve a magnitude da variabilidade associada ao fator na amostra.</q> <span class="ref">Guião da aula 8, pergunta 10</span></p>
</div>

<div class="tw"><table class="ficha">
<tr><th>Parte</th><th>Produtividade por departamento (blocos 4.1 a 4.5)</th></tr>
<tr><td>Pergunta</td><td>A produtividade média difere entre departamentos?</td></tr>
<tr><td>Escolha</td><td>Produtividade: variável quantitativa. Departamento: variável qualitativa. Quatro grupos independentes. Já não se comparam duas médias, por isso é precisa uma comparação global: ANOVA de um fator.</td></tr>
<tr><td>Hipóteses</td><td>H0: μ<sub>AD</sub> = μ<sub>C</sub> = μ<sub>D</sub> = μ<sub>O</sub>. H1: pelo menos uma média difere.</td></tr>
<tr><td>Resultado</td><td>F(3, 234) = 0,47; p = 0,70. η² = 0,006.</td></tr>
<tr><td>Decisão</td><td>Como p = 0,70 &gt; 0,05, não rejeitamos H0.</td></tr>
<tr><td>Resposta</td><td>Ao nível de significância de 5%, não existe evidência estatística suficiente para concluir que a produtividade média difere entre departamentos. Não rejeitar H0 não significa provar que H0 é verdadeira (aula 3, diap. 12). Como o teste global não sugere diferenças, não se fazem comparações pós-hoc de Tukey.</td></tr>
</table></div>
<p class="sub">Tabela 7. Ficha da ANOVA de um fator.</p>

<h3>O caminho do guia de escolha da docente</h3>
<p>O infográfico «Testes paramétricos e não paramétricos: guia de escolha para comparar grupos» tem três passos. O bloco 4.3 do notebook percorre-os pela mesma ordem.</p>
<div class="steps">
 <div class="step"><div class="k">1</div><div><h3>Avaliar a normalidade: Shapiro-Wilk + gráfico Q-Q</h3><div class="g">
  <div><span>O que diz o guia</span>Grupos independentes: avaliar em cada grupo. «A escolha não depende apenas do valor p: considerar os gráficos, os valores extremos e a dimensão amostral.»</div>
  <div><span>No trabalho</span>p = 0,36; 0,32; 0,06 e, em Desenvolvimento, 0,0004 (0,027 sem o C097)</div>
  <div><span>Leitura</span>Evidência contra a normalidade num grupo, ligada a um valor extremo; grupos de 31 a 85 colaboradores</div></div></div></div>
 <div class="step"><div class="k">2</div><div><h3>Avaliar as variâncias: Levene</h3><div class="g">
  <div><span>O que diz o guia</span>H0: as variâncias populacionais dos grupos são iguais. p &gt; 0,05: não rejeitamos a igualdade</div>
  <div><span>No trabalho</span>p = 0,52</div>
  <div><span>Leitura</span>Não rejeitamos a igualdade das variâncias</div></div></div></div>
 <div class="step"><div class="k">3</div><div><h3>Escolher o teste conforme o desenho do estudo</h3><div class="g">
  <div><span>O que diz o guia</span>Três ou mais grupos independentes: Levene p &gt; 0,05, ANOVA clássica. Se a via paramétrica for inadequada, Kruskal-Wallis</div>
  <div><span>No trabalho</span>ANOVA de um fator</div>
  <div><span>Notas do guia</span>«Welch também pode ser usado quando Levene não rejeita a igualdade. p &gt; 0,05 não prova os pressupostos.» «Os testes por postos não testam diretamente médias.»</div></div></div></div>
</div>
<p class="sub">Esquema 5. Os três passos do guia de escolha da docente, com os valores do trabalho.</p>

<h3>Pressupostos avaliados antes do teste (bloco 4.3)</h3>
<div class="tw"><table>
<tr><th>Pressuposto</th><th>Como se avalia nas aulas</th><th>No trabalho</th><th>Leitura</th></tr>
<tr><td>Independência</td><td>«Depende do desenho da recolha; não é garantida por testes aos resíduos.» <span class="ref">Guião da aula 8, pergunta 7</span></td><td>Um registo por colaborador (depois de eliminar a duplicação), cada um num só departamento</td><td>Assumida pelo desenho</td></tr>
<tr><td>Normalidade</td><td>Shapiro-Wilk por grupo <span class="ref">guião da aula 3, bloco 13</span></td><td>p = 0,36; 0,32; 0,06 e, em Desenvolvimento, 0,0004</td><td>Evidência de desvio num grupo</td></tr>
<tr><td>Homogeneidade das variâncias</td><td>Teste de Levene centrado na mediana. «É uma ferramenta, não uma prova absoluta.» <span class="ref">Guião da aula 8, pergunta 7</span></td><td>p = 0,52; desvios-padrão de 11,6 a 14,0</td><td>Não encontramos evidência de variâncias distintas</td></tr>
</table></div>
<p class="sub">Tabela 8. Pressupostos da ANOVA. Um p-valor superior a 0,05 não prova que o pressuposto esteja satisfeito (guião da aula 8, pergunta 16). O infográfico da ANOVA de uma via diz que ela «é robusta a desvios moderados da normalidade, especialmente quando os tamanhos amostrais são semelhantes»; como aqui não são semelhantes, o trabalho apresenta também a ANOVA de Welch.</p>

<div class="tw"><table>
<tr><th>Análise</th><th>Porque aparece</th><th>Estatística</th><th class="num">p</th></tr>
<tr><td>ANOVA de um fator (método escolhido)</td><td>Levene com p &gt; 0,05: «pode aplicar testes paramétricos que assumem variâncias iguais», entre eles a ANOVA clássica <span class="ref">infográfico «Teste de Levene»</span></td><td>F(3, 234) = 0,47</td><td class="num">0,702</td></tr>
<tr><td>ANOVA de Welch</td><td>«Alternativa à ANOVA clássica quando as variâncias são desiguais. Não exige homogeneidade de variâncias.» <span class="ref">Guião da aula 8, pergunta 8</span> «É mais robusta, especialmente quando os tamanhos amostrais são diferentes» <span class="ref">infográfico «ANOVA de Welch»</span>; aqui os grupos vão de 31 a 85</td><td>F(3; 105,7) = 0,50</td><td class="num">0,681</td></tr>
<tr><td>Kruskal-Wallis</td><td>«Alternativa não paramétrica à ANOVA»; compara as medianas dos grupos a partir das ordens e «é mais robusto a valores atípicos e a distribuições assimétricas». Pressupõe distribuições com forma semelhante. <span class="ref">Infográfico «Teste de Kruskal-Wallis»</span></td><td>H(3) = 1,37</td><td class="num">0,713</td></tr>
<tr><td>ANOVA sem o C097</td><td>O outlier foi investigado, não eliminado</td><td></td><td class="num">0,632</td></tr>
<tr><td>ANOVA sem os 10 casos assinalados</td><td>O mesmo</td><td></td><td class="num">0,557</td></tr>
</table></div>
<p class="sub">Tabela 9. A decisão é a da ANOVA de um fator. As outras análises mostram que a leitura é a mesma; não serviram para escolher o menor p-valor (blocos 4.4a e 4.4b).</p>

<figure>
@@FIG41@@
<figcaption><b>Figura C</b> (bloco 4.1, Figura 4 do relatório). As médias vão de 76,5 a 79,2 e as caixas sobrepõem-se quase por completo: a variabilidade entre departamentos (2,7 pontos entre a maior e a menor média) é pequena face à variabilidade dentro dos departamentos (desvios-padrão de 11,6 a 14,0). «Diferenças nas médias amostrais não implicam necessariamente diferenças estatisticamente significativas» (guião da aula 8, pergunta 4).</figcaption>
</figure>

<p>Dimensão do efeito: η² = 0,006 é a fração da variabilidade amostral atribuída às diferenças entre departamentos, ou seja, 0,6%. Nos valores de referência do «Guia de Inferência Estatística» (0,01 pequeno; 0,06 médio; 0,14 grande) fica abaixo de um efeito pequeno. O mesmo guia lembra que «a significância estatística não indica a magnitude do efeito».</p>

<h3>Intervalo de confiança da média (bloco 4.6)</h3>
<div class="doc">
<span class="tag">Nas palavras da docente</span>
<p>Uma estimativa pontual <q>é simples, mas não mostra a incerteza da estimação</q>. O intervalo é estimativa ± margem de erro. <q>Se repetíssemos muitas vezes o processo de amostragem e construíssemos um intervalo da mesma forma, aproximadamente 95% desses intervalos conteriam o verdadeiro parâmetro populacional. O intervalo de confiança quantifica a incerteza da estimação.</q> <span class="ref">Aula 3, diap. 7 e 8</span></p>
</div>
<p>No trabalho: média 78,03, erro-padrão 0,832, margem de erro 1,64, IC 95% = [76,39; 79,67], calculado com <code>stats.t.interval</code> como na aula 3 (diap. 9). Resposta: estimamos que a produtividade média populacional se situe aproximadamente entre 76,4 e 79,7 pontos. O intervalo refere-se à média e não aos colaboradores. O infográfico dos intervalos de confiança admite o IC com z para amostras grandes (n ≥ 30); com n = 238 os dois quase coincidem (valores críticos 1,970 e 1,960).</p>

<h2 id="s9"><span class="n">9</span>Regressão linear simples (M1)</h2>
<div class="doc">
<span class="tag">Nas palavras da docente</span>
<p>Correlação: <q>Existe associação entre X e Y?</q> Regressão: <q>Como varia Y quando X varia? Constrói uma equação que permite explicar e prever.</q> <span class="ref">Aula 4, diap. 10</span></p>
<p><q>Um modelo linear só faz sentido se a forma dos dados for compatível, pelo menos aproximadamente, com uma relação linear. Primeiro observamos. Depois modelamos.</q> <span class="ref">Aula 4, diap. 6</span></p>
<p><q>A regressão não termina quando o Python apresenta os coeficientes: o objetivo final é responder à pergunta que originou a análise.</q> <span class="ref">Aula 4, diap. 58</span></p>
</div>

<p>A tabela segue as perguntas a que a docente diz que devem conseguir responder (aula 4, diap. 57), pela mesma ordem.</p>
<div class="tw"><table>
<tr><th>Pergunta da aula 4</th><th>Ferramenta</th><th>No M1 (n = 236)</th></tr>
<tr><td>Qual é a variável resposta Y e a explicativa X?</td><td></td><td>Y = produtividade; X = horas semanais de uso de IA</td></tr>
<tr><td>O gráfico sugere uma relação aproximadamente linear?</td><td>Diagrama de dispersão</td><td>Tendência positiva, sem curvatura evidente (Figura B)</td></tr>
<tr><td>Qual é a equação estimada?</td><td>Mínimos quadrados: a reta que minimiza a soma dos quadrados dos resíduos</td><td>Produtividade estimada = 73,04 + 0,627 × (horas de IA)</td></tr>
<tr><td>O que significa o declive?</td><td>Coeficiente b<sub>1</sub></td><td>Por cada hora semanal adicional de IA, o modelo estima um aumento médio de aproximadamente 0,63 pontos na produtividade</td></tr>
<tr><td>E o intercepto?</td><td>Coeficiente b<sub>0</sub></td><td>Produtividade média prevista para X = 0: 73,04. Aqui tem interpretação, porque há 11 colaboradores com 0 horas</td></tr>
<tr><td>Existe evidência estatística de associação?</td><td>Teste t ao declive: H0: β<sub>1</sub> = 0</td><td>t = 3,80; p &lt; 0,001. Rejeitamos H0: existe evidência de uma associação linear positiva</td></tr>
<tr><td>Qual é o intervalo de confiança e o que significa?</td><td>Erro-padrão e IC 95%</td><td>[0,30; 0,95]. Como não contém zero, é coerente com o teste</td></tr>
<tr><td>Quanto da variabilidade de Y é explicado?</td><td>R²</td><td>R² = 0,058: as horas de IA explicam aproximadamente 5,8% da variabilidade observada na produtividade</td></tr>
<tr><td>O gráfico dos resíduos revela algum padrão?</td><td>Resíduos contra valores previstos</td><td>Sem curvatura sistemática nem padrão de funil (Figura D)</td></tr>
<tr><td>Os resíduos são compatíveis com a normalidade?</td><td>Q-Q e Shapiro-Wilk</td><td>p = 0,0001: há evidência contra o pressuposto (ver secção 11)</td></tr>
<tr><td>Existe evidência de heteroscedasticidade?</td><td>Breusch-Pagan</td><td>p = 0,976: não encontramos evidência de heteroscedasticidade</td></tr>
<tr><td>Qual é a resposta à pergunta inicial?</td><td></td><td>Existe evidência de associação linear positiva entre o uso de IA e a produtividade, mas o modelo explica uma parte pequena da variabilidade</td></tr>
</table></div>
<p class="sub">Tabela 10. O M1 lido pela ordem das perguntas da aula 4 (blocos 5.1 a 5.6).</p>

<div class="box">
<h3>Os 94% que ficam por explicar</h3>
<p>«Isto não significa que exista algum problema com o modelo. Significa que as horas de sono, consideradas isoladamente, explicam apenas uma parte das diferenças observadas na produtividade.» <span class="ref">Aula 4, diap. 31</span> No trabalho passa-se o mesmo com as horas de IA: outros fatores não incluídos no modelo poderão contribuir para o resto, e é isso que leva à regressão múltipla, tal como na aula 4 (diap. 59).</p>
</div>

<h3>Prever uma média ou um indivíduo? (bloco 5.3)</h3>
<p>Para 5 h o modelo prevê uma produtividade média de 76,2 e para 10 h de 79,3: uma diferença de 3,1 pontos (5 × 0,627). «IC para a média: quantifica a incerteza da produtividade média dos indivíduos com X = 7. Intervalo de previsão: quantifica a incerteza para a produtividade de um novo indivíduo.» <span class="ref">Aula 4, diap. 35</span> O intervalo individual é mais largo porque inclui a variabilidade do novo indivíduo: para 5 h vai de cerca de 52 a 101. «Uma previsão é uma estimativa, não uma certeza.» <span class="ref">Aula 4, diap. 33</span></p>

<h3>Os resíduos (blocos 5.5 e 5.6)</h3>
<div class="doc">
<span class="tag">Nas palavras da docente</span>
<p>Resíduo: e<sub>i</sub> = y<sub>i</sub> − ŷ<sub>i</sub>. Se e<sub>i</sub> &lt; 0, o valor observado é inferior ao previsto. <q>Se o modelo for adequado, aquilo que ficou por explicar não deverá apresentar um padrão sistemático.</q> <span class="ref">Aula 4, diap. 42</span></p>
<p><q>Os resíduos permitem-nos observar aquilo que o modelo deixou por explicar.</q> <span class="ref">Aula 4, diap. 44</span></p>
</div>
<p>Exemplo do enunciado: o C001 usa 7,7 h; o modelo prevê 77,9 e o valor observado é 68,0. O resíduo é −9,9: o valor observado é inferior ao previsto.</p>

<figure>
@@FIG56@@
<figcaption><b>Figura D</b> (bloco 5.6a, Figura 5 do relatório). À esquerda, resíduos contra valores previstos: procura-se uma nuvem sem padrão evidente, distribuída em torno de zero, sem curvatura sistemática nem padrão de funil. Ao centro, o histograma dos resíduos: esperam-se muitos erros pequenos e poucos erros muito grandes. À direita, o Q-Q: os pontos acompanham a reta, com desvios na cauda inferior (C097 e C129).</figcaption>
</figure>

<div class="box ok">
<h3>O passo que justifica a regressão múltipla</h3>
<p>No bloco 5.6c correlacionaram-se os resíduos do M1 com as variáveis que ficaram fora do modelo. Com a experiência, r = 0,45 (p &lt; 0,001); com as outras é praticamente nula. Aquilo que ficou por explicar apresenta, portanto, um padrão sistemático associado à experiência. Nas palavras da aula 4 (diap. 41): «Omissões importantes podem comprometer essa interpretação».</p>
</div>

<h2 id="s10"><span class="n">10</span>Regressão linear múltipla (M2)</h2>
<div class="doc">
<span class="tag">Nas palavras da docente</span>
<p><q>A pergunta mudou e, por isso, o modelo também tem de mudar.</q> <span class="ref">Aula 4, diap. 62</span></p>
<p><q>Na regressão múltipla, cada coeficiente mede uma associação parcial.</q> Interpretar b<sub>j</sub> implica manter constantes as restantes variáveis. <q>Esta é uma das ideias mais importantes da regressão linear múltipla.</q> <span class="ref">Aula 4, diap. 63</span></p>
<p><q>Ao introduzir outras variáveis, estamos a estimar a associação do sono controlando esses outros fatores.</q> <span class="ref">Aula 4, diap. 66</span></p>
<p><q>A regressão múltipla não substitui a regressão simples. Permite responder a uma pergunta diferente, considerando simultaneamente vários fatores.</q> <span class="ref">Aula 4, diap. 96</span></p>
</div>

<figure>
<div class="canvas">@@TRI@@</div>
<figcaption><b>Esquema 6.</b> A experiência está associada ao uso de IA e à produtividade (setas azuis, correlações de Pearson). A seta tracejada é o coeficiente da IA: 0,64 no modelo simples e 0,13 quando se controlam a experiência, a formação e a complexidade. O notebook chama a isto «fator de confusão»; nas aulas diz-se que se estima a associação controlando os outros fatores.</figcaption>
</figure>

<h3>Escolher as variáveis explicativas (bloco 6.1)</h3>
<div class="tw"><table>
<tr><th>Variável</th><th class="num">r com a produtividade</th><th>Decisão</th><th>Razão</th></tr>
<tr><td>Experiência</td><td class="num">0,50</td><td class="yes">Entra</td><td>Anterior ao desempenho e associada ao uso de IA (0,27)</td></tr>
<tr><td>Formação em IA</td><td class="num">0,15</td><td class="yes">Entra</td><td>Anterior ao desempenho e associada ao uso de IA (0,51)</td></tr>
<tr><td>Complexidade das tarefas</td><td class="num">−0,01</td><td class="yes">Entra</td><td>Característica do posto de trabalho, referida no enunciado</td></tr>
<tr><td>Carga de trabalho, departamento</td><td class="num">0,08; ANOVA p = 0,70</td><td>Só numa análise adicional</td><td>Pouca relação com a produtividade</td></tr>
<tr><td>Tarefas, tempo por tarefa, qualidade</td><td class="num">0,44; −0,48; 0,46</td><td class="no">Ficam de fora</td><td>O dicionário diz que são indicadores do mesmo desempenho</td></tr>
</table></div>
<p class="sub">Tabela 11. Seleção das variáveis explicativas.</p>

<p>A leitura do modelo segue a ordem do <code>summary()</code> ensinada na aula 5 (diap. 11): modelo global, capacidade explicativa, coeficientes, significância individual.</p>

<div class="tw"><table>
<tr><th>Pergunta (aula 4, diap. 93)</th><th>Ferramenta</th><th>No M2 (n = 233)</th></tr>
<tr><td>As variáveis contribuem globalmente?</td><td>Teste F. H0: β<sub>1</sub> = β<sub>2</sub> = β<sub>3</sub> = β<sub>4</sub> = 0; H1: pelo menos um β<sub>j</sub> ≠ 0</td><td>F(4, 228) = 22,1; p &lt; 0,001. Rejeitamos H0: o modelo é globalmente significativo</td></tr>
<tr><td>Que variáveis contribuem individualmente?</td><td>Testes t. H0: β<sub>j</sub> = 0</td><td>Experiência: p &lt; 0,001. Formação: p = 0,059. IA: p = 0,47. Complexidade: p = 0,36</td></tr>
<tr><td>Qual a incerteza dos coeficientes?</td><td>IC 95%</td><td>IA: [−0,22; 0,48], contém zero. Experiência: [1,21; 1,96]</td></tr>
<tr><td>Quanto explica o modelo?</td><td>R²</td><td>0,280: cerca de 28% da variabilidade observada</td></tr>
<tr><td>Quanto explica considerando a complexidade do modelo?</td><td>R² ajustado</td><td>0,267</td></tr>
<tr><td>As explicativas estão demasiado relacionadas?</td><td>VIF</td><td>Entre 1,01 e 1,51</td></tr>
<tr><td>Os resíduos são compatíveis com a normalidade?</td><td>Q-Q e Shapiro-Wilk</td><td>p = 0,00002; sem o C097, p = 0,965</td></tr>
<tr><td>A variância dos erros parece constante?</td><td>Breusch-Pagan</td><td>p = 0,185: não encontramos evidência de heteroscedasticidade</td></tr>
</table></div>
<p class="sub">Tabela 12. O M2 lido pelo quadro «Porque fizemos todas estas análises?» da aula 4 (blocos 6.2 a 6.6).</p>

<div class="box key">
<p><b>Produtividade estimada = 67,32 + 0,129 (IA) + 1,584 (experiência) + 0,231 (formação) − 0,661 (complexidade)</b></p>
<p><b>Uso de IA.</b> Mantendo constantes a experiência, a formação em IA e a complexidade das tarefas, uma hora semanal adicional de IA está associada, em média, a um aumento estimado de aproximadamente 0,13 pontos na produtividade. Como p = 0,47 &gt; 0,05 e o IC 95% contém zero, não existe evidência estatística suficiente, a 5%, de associação linear parcial entre o uso de IA e a produtividade.</p>
<p><b>Experiência.</b> Mantendo constantes as restantes variáveis, um ano adicional de experiência está associado, em média, a um aumento estimado de aproximadamente 1,58 pontos. Como p &lt; 0,001 e o IC 95% não contém zero, existe evidência estatística de associação linear positiva, controlando as restantes variáveis.</p>
<p><b>Intercepto.</b> 67,32 é a previsão quando todas as explicativas são zero. Como a complexidade mínima é 1, essa combinação está fora das condições observadas e a interpretação prática é limitada.</p>
</div>

<div class="doc">
<span class="tag">Nas palavras da docente</span>
<p><q>Não ordenamos a importância das explicativas apenas pelos coeficientes em valor absoluto: uma unidade representa mudanças diferentes em cada variável. O p-valor elevado do stress não demonstra ausência de associação nem obriga a eliminar automaticamente essa variável.</q> <span class="ref">Aula 5, diap. 22</span></p>
<p>Aplica-se ao trabalho duas vezes: a complexidade ficou no modelo apesar de p = 0,36, e o p-valor elevado da IA não demonstra que a IA não tem associação com a produtividade.</p>
</div>

<figure>
@@FIG64@@
<figcaption><b>Figura E</b> (bloco 6.4, Figura 7 do relatório). O coeficiente da IA em cinco modelos estimados na mesma base de 233 colaboradores. Com a formação quase não muda (0,60); com a experiência passa para 0,31 (p = 0,044); com as duas passa para 0,13 e o IC 95% passa a conter zero. Na aula 4 (diap. 66) acontece o mesmo em menor escala: o coeficiente do sono passa de 0,563 para 0,409 ao introduzir outras variáveis.</figcaption>
</figure>

<h3>O que se ganhou com o modelo múltiplo? (bloco 6.5)</h3>
<div class="doc">
<span class="tag">Nas palavras da docente</span>
<p><q>Quando acrescentamos variáveis explicativas, o R² não diminui. Mesmo uma variável com pouca utilidade pode fazer o R² aumentar ligeiramente.</q> O R² ajustado <q>penaliza a inclusão de variáveis que não acrescentam informação suficiente</q>. <span class="ref">Aula 4, diap. 77</span></p>
<p><q>Uma comparação justa. Para comparar diretamente o ajustamento, voltamos a estimar o modelo simples nos mesmos 77 participantes do modelo múltiplo.</q> <span class="ref">Aula 4, diap. 79</span></p>
<p><q>O F global compara todos os declives com zero. Este F parcial pergunta se [as variáveis adicionais] acrescentam informação ao modelo que já contém [a primeira].</q> <span class="ref">Aula 4, diap. 81</span></p>
</div>

<div class="tw"><table>
<tr><th>Modelo na base comum</th><th class="num">n</th><th class="num">R²</th><th class="num">R² ajustado</th></tr>
<tr><td>IA</td><td class="num">233</td><td class="num">0,061</td><td class="num">0,056</td></tr>
<tr><td>IA + experiência + formação + complexidade</td><td class="num">233</td><td class="num">0,280</td><td class="num">0,267</td></tr>
</table></div>
<p class="sub">Tabela 13. Comparação na base comum, no formato da aula 4 (diap. 79). O modelo simples original continua a ser a análise com 236 colaboradores; a versão com 233 serve apenas para esta comparação.</p>

<p><b>Teste F parcial</b> (modelos encaixados, <code>compare_f_test</code>). Testamos conjuntamente H0: β<sub>experiência</sub> = β<sub>formação</sub> = β<sub>complexidade</sub> = 0, mantendo a IA no modelo. Obtemos F = 23,1 com gl = (3, 228) e p &lt; 0,001. Rejeitamos a hipótese conjunta a 5%: as variáveis adicionais contribuem conjuntamente para o ajuste. Como avisa a docente, o modelo múltiplo tem maior capacidade de ajuste nesta amostra; a tabela não demonstra melhor previsão em novos dados (aula 4, diap. 79).</p>

<h2 id="s11"><span class="n">11</span>Diagnósticos dos dois modelos</h2>
<div class="doc">
<span class="tag">Nas palavras da docente</span>
<p><q>Não verificamos pressupostos por rotina: queremos saber se podemos confiar nas conclusões inferenciais.</q> <span class="ref">Aula 4, diap. 40</span></p>
<p><q>Primeiro observamos. Depois, se necessário, testamos.</q> <span class="ref">Aula 5, diap. 34</span></p>
<p><q>Shapiro-Wilk: não rejeitar é compatibilidade com o modelo normal, não prova de normalidade dos erros. Breusch-Pagan: não rejeitar indica ausência de evidência detetada de heteroscedasticidade, não garantia de variância constante. VIF: resume inflação da variância por relações entre explicativas. Não demonstra ausência de variáveis omitidas nem causalidade. [...] Nenhum teste isolado certifica todo o modelo.</q> <span class="ref">Aula 4, diap. 99</span></p>
</div>

<div class="tw"><table>
<tr><th>Aspeto (quadro da aula 5, diap. 50)</th><th>Porque interessa</th><th>M1: resultado e leitura</th><th>M2: resultado e leitura</th></tr>
<tr><td>Forma da relação</td><td>Um padrão nos resíduos significa que existe estrutura que a reta não captou</td><td>Gráfico dos resíduos: sem curvatura clara</td><td>Gráfico dos resíduos: sem curvatura clara</td></tr>
<tr><td>Variância constante (homoscedasticidade)</td><td>Se a variância dos erros não for constante, os erros-padrão usuais podem deixar de ser adequados</td><td>Sem padrão de funil; Breusch-Pagan p = 0,976: não rejeitamos</td><td>Sem padrão de funil; Breusch-Pagan p = 0,185: não rejeitamos</td></tr>
<tr><td>Normalidade dos resíduos</td><td>Sustenta as distribuições usadas nos testes t, no teste F e nos IC</td><td class="no">Shapiro p = 0,0001: rejeitamos. Sem o C097, p = 0,030: rejeitamos</td><td><span class="no">Shapiro p = 0,00002: rejeitamos.</span> <span class="yes">Sem o C097, p = 0,965: não rejeitamos</span></td></tr>
<tr><td>Independência</td><td>É uma condição do desenho da recolha. Nem Shapiro-Wilk nem Breusch-Pagan a verificam</td><td>Assumida pelo desenho: um registo por colaborador. Durbin-Watson 1,84, apenas descritivo</td><td>Assumida pelo desenho. Durbin-Watson 1,95, apenas descritivo</td></tr>
<tr><td>Observações influentes</td><td>A distância de Cook assinala observações a investigar, não a eliminar automaticamente</td><td>Máximo 0,060 (C134); 7 acima da referência exploratória 4/n</td><td>Máximo 0,066 (C097); 7 acima da referência exploratória 4/n</td></tr>
<tr><td>Multicolinearidade</td><td>Se os preditores fornecerem informação muito semelhante, torna-se difícil separar a contribuição de cada um</td><td>Não se aplica: uma só explicativa</td><td>VIF de 1,01 a 1,51: sem inflação elevada</td></tr>
</table></div>
<p class="sub">Tabela 14. Diagnósticos dos dois modelos (blocos 5.6a e 6.6a), com a leitura no formato do quadro-síntese da aula 5.</p>

<figure>
@@FIG66@@
<figcaption><b>Figura F</b> (bloco 6.6a, Figura 8 do relatório). Diagnóstico do M2. Os resíduos distribuem-se em torno de zero sem padrão sistemático evidente. No Q-Q os pontos acompanham globalmente a reta; o ponto isolado na cauda inferior é o C097, com resíduo −60,6.</figcaption>
</figure>

<div class="box">
<h3>Durbin-Watson: o que dizer</h3>
<p>«A ordem das linhas é a dos participantes, sem sequência temporal justificada. Por isso, DW [...] é apenas descritivo e não demonstra independência. A independência é uma condição do desenho da recolha.» <span class="ref">Aula 4, diap. 54</span> No trabalho a ordem é a do código do colaborador, por isso aplica-se exatamente o mesmo.</p>
</div>

<div class="box">
<h3>VIF: como ler</h3>
<p>«O VIF indica quanto a variância da estimativa de um coeficiente está aumentada devido à relação da respetiva variável com as outras explicativas.» <span class="ref">Aula 4, diap. 83</span> Leitura prática: próximo de 1, pouca relação com as restantes; entre 1 e 5, geralmente sem preocupação importante; superior a 5, merece atenção. «Estes limites são regras práticas, não fronteiras absolutas.» <span class="ref">Aula 4, diap. 84</span></p>
<p>No M2 o maior VIF é 1,51 (uso de IA): não existem indícios de multicolinearidade problemática. Isto importa para o resultado central. Com multicolinearidade, «uma variável importante pode parecer não significativa» porque o erro-padrão aumenta. Aqui o erro-padrão do coeficiente da IA quase não muda (0,166 no modelo simples e 0,179 no múltiplo, na base comum); o que mudou foi a própria estimativa, de 0,64 para 0,13.</p>
</div>

<h3>A conclusão muda se as opções do grupo forem outras? (bloco 6.6b)</h3>
<div class="tw"><table>
<tr><th>Versão do modelo</th><th class="num">Coeficiente da IA</th><th class="num">p</th><th class="num">R² ajustado</th></tr>
<tr><td>M2</td><td class="num">0,129</td><td class="num">0,471</td><td class="num">0,267</td></tr>
<tr><td>M2 sem o C097</td><td class="num">0,146</td><td class="num">0,384</td><td class="num">0,302</td></tr>
<tr><td>M2 com carga de trabalho e departamento</td><td class="num">0,144</td><td class="num">0,446</td><td class="num">0,274</td></tr>
<tr><td>M2 com a complexidade como categoria</td><td class="num">0,122</td><td class="num">0,500</td><td class="num">0,272</td></tr>
</table></div>
<p class="sub">Tabela 15. Em todas as versões o coeficiente da IA fica entre 0,12 e 0,15 e nunca há evidência estatística de associação parcial. A interação IA × experiência também não é significativa (0,028; p = 0,50).</p>

<h2 id="s12"><span class="n">12</span>Pontos frágeis a ter prontos na defesa</h2>
<p>São os sítios onde uma pergunta atenta pode apanhar uma resposta decorada. Em cada um está o que os resultados mostram e a resposta que se aguenta, nas palavras das aulas.</p>

<div class="box warn">
<h3>1. «Fizeram três testes aos departamentos. Não é escolher o p-valor?»</h3>
<p>É a pergunta mais provável, porque a regra da aula 3 é explícita: o método é escolhido antes de olhar para o resultado.</p>
<p>Resposta segura: o método foi escolhido antes, a partir dos pressupostos (Levene sem evidência de variâncias distintas, logo ANOVA de um fator), e a decisão é a da ANOVA. O Welch e o Kruskal-Wallis foram definidos à partida para ver se a leitura dependia dos pressupostos em dúvida, como o guião da aula 8 pede ao mandar comparar a ANOVA clássica com a de Welch. Os três dão a mesma leitura; nenhum foi usado para escolher.</p>
</div>

<div class="box warn">
<h3>2. «A normalidade falha só por causa do C097»</h3>
<p>Os comentários de alguns blocos dizem-no assim, mas os resultados são mais matizados (Tabela 5). Sem o C097, a produtividade continua a mostrar desvio à normalidade (p = 0,0009), o grupo Desenvolvimento também (p = 0,027) e os resíduos do M1 também (p = 0,030). Só os resíduos do M2 ficam compatíveis com o pressuposto (p = 0,965).</p>
<p>Resposta segura: o que interessa à inferência são os resíduos do modelo e não a variável (aula 4, diap. 45). No modelo final, sem o C097, não há evidência contra a normalidade dos resíduos e o coeficiente da IA quase não muda (0,146; p = 0,38). E nenhum teste isolado certifica todo o modelo (aula 4, diap. 99).</p>
</div>

<div class="box warn">
<h3>Shapiro-Wilk com 238 observações?</h3>
<p>O «Guia de Inferência Estatística» associa o Shapiro-Wilk a amostras pequenas (n &lt; 50) e o Kolmogorov-Smirnov a amostras maiores. O infográfico «Testes de normalidade» recomenda o Shapiro-Wilk por ser mais potente em amostras pequenas e médias, e é o único teste de normalidade que aparece no código dos diapositivos e dos guiões das aulas 3, 4, 5 e 8.</p>
<p>Resposta segura: usou-se o teste das aulas, sempre com o histograma e o Q-Q. Em amostras grandes o teste pode detetar desvios pequenos sem relevância prática, por isso a leitura apoia-se também nos gráficos, que mostram onde está o desvio (C097 e o máximo de 98).</p>
</div>

<div class="box warn">
<h3>3. «Disseram que os pressupostos estão cumpridos»</h3>
<p>O notebook escreve em alguns sítios «cumpridos». A docente evita essa palavra: não rejeitar H0 no Breusch-Pagan é ausência de evidência detetada de heteroscedasticidade, não garantia de variância constante (aula 4, diap. 99; aula 5, diap. 48).</p>
<p>Resposta segura: «os diagnósticos avaliados são compatíveis com o uso do modelo» (aula 5, diap. 50).</p>
</div>

<div class="box warn">
<h3>4. Dois declives para o modelo simples: 0,627 e 0,639</h3>
<p>0,627 é o modelo simples original, com 236 colaboradores. 0,639 é o mesmo modelo estimado na base comum de 233, apenas para a comparação com o múltiplo. É o que a aula 4 faz (diap. 66 e 80): o modelo simples com 78 participantes dá 0,5495 e na base comum de 77 dá 0,5630.</p>
</div>

<div class="box warn">
<h3>5. Só com a experiência, a IA ainda é significativa</h3>
<p>Com IA e experiência no modelo, o coeficiente da IA é 0,31 com p = 0,044. A evidência só deixa de existir quando entra também a formação, que está associada ao uso de IA (r = 0,51).</p>
<p>Resposta segura: um p-valor elevado «não demonstra ausência de associação» (aula 5, diap. 22). O IC 95% do M2 vai de −0,22 a 0,48: os dados não mostram evidência de associação parcial, mas também não provam que ela é zero. E o VIF não demonstra ausência de variáveis omitidas nem causalidade (aula 4, diap. 99).</p>
</div>

<div class="box warn">
<h3>6. «Então a IA não tem efeito?»</h3>
<p>Não se pode falar de efeito. «Encontramos associações condicionais no modelo. Não demonstramos que alterar as horas de sono ou estudo provoque, por si só, a mudança estimada na produtividade.» <span class="ref">Aula 5, diap. 54</span> Vale o mesmo para as horas de IA e para a experiência.</p>
</div>

<div class="box warn">
<h3>7. O máximo de 98 e as previsões acima de 100</h3>
<p>Treze colaboradores têm exatamente 98. O intervalo de previsão individual para 10 h vai até 103,9, fora da escala. Os intervalos de previsão dependem da especificação e dos pressupostos (aula 5, diap. 54): o modelo descreve a média e a previsão para um indivíduo é muito mais incerta.</p>
</div>

<div class="box warn">
<h3>8. Outras perguntas curtas</h3>
<ul>
<li>O R² descreve o ajuste aos dados usados para estimar o modelo. Não demonstra a precisão em novos colaboradores (aula 5, diap. 54).</li>
<li>O limite de um mês nos casos incoerentes é uma suposição do grupo, porque o dicionário não define o período. Por isso os casos foram assinalados e não eliminados.</li>
<li>Os 6 registos incompletos com produtividade conhecida têm média 86,0 contra 77,8 nos completos. São 6 em 240 e a correlação não muda, mas «não interpretamos a exclusão como aleatória sem investigar o mecanismo de ausência» (guião da aula 8, pergunta 2); foi o que o bloco 1.6b fez.</li>
<li>Os dados são sintéticos e de um só momento: nenhuma conclusão descreve uma empresa real.</li>
<li>O M2 deixa cerca de 72% da variabilidade por explicar, o que não significa que exista um problema com o modelo.</li>
</ul>
</div>

<h2 id="s13"><span class="n">13</span>Glossário nas palavras das aulas</h2>
<div class="tw"><table>
<tr><th>Termo</th><th>Como a docente o define</th><th>Onde</th></tr>
<tr><td>p-valor</td><td>Assumindo H0 verdadeira, indica quão incompatível é o resultado observado com essa hipótese. No teste de preparação: admitindo H0 e os pressupostos do teste, é a probabilidade de obter um resultado tão extremo ou mais extremo do que o observado. Não é a probabilidade de H0 ser verdadeira. Se p &lt; 0,05 rejeitamos H0; se p ≥ 0,05 não rejeitamos (os infográficos escrevem p ≤ 0,05).</td><td>Aula 3, diap. 12; teste de preparação, pergunta 17</td></tr>
<tr><td>H0 e H1</td><td>H0 é a hipótese que colocamos à prova. H1 representa aquilo para que procuramos evidência.</td><td>Aula 3, diap. 11</td></tr>
<tr><td>Não rejeitar H0</td><td>Não significa provar que H0 é verdadeira.</td><td>Aula 3, diap. 12</td></tr>
<tr><td>Erro Tipo I e Tipo II</td><td>Tipo I: rejeitar H0 quando é verdadeira (falso positivo), com probabilidade α. Tipo II: não rejeitar H0 quando é falsa (falso negativo).</td><td>Aula 3, diap. 18 e 19</td></tr>
<tr><td>Método paramétrico</td><td>Baseia a inferência em parâmetros da população e num modelo probabilístico com determinados pressupostos.</td><td>Aula 3, diap. 13</td></tr>
<tr><td>Método não paramétrico</td><td>Exige menos pressupostos sobre a forma da distribuição e frequentemente utiliza a ordenação dos valores em vez dos valores originais.</td><td>Aula 3, diap. 14</td></tr>
<tr><td>Intervalo de confiança</td><td>Estimativa ± margem de erro. Quantifica a incerteza da estimação. Não diz que 95% das observações estão no intervalo, nem que a média populacional tem 95% de probabilidade de estar neste intervalo concreto.</td><td>Aula 3, diap. 8; teste de preparação, pergunta 14</td></tr>
<tr><td>Correlação de Pearson</td><td>Mede a intensidade e direção de uma associação linear entre duas variáveis quantitativas.</td><td>Aula 2, diap. 25</td></tr>
<tr><td>Correlação de Spearman</td><td>Mede a intensidade e direção de uma associação monotónica; baseia-se nas ordens.</td><td>Aula 2, diap. 28</td></tr>
<tr><td>ANOVA</td><td>Compara a variabilidade entre grupos com a variabilidade dentro dos grupos.</td><td>Aula 3, diap. 31</td></tr>
<tr><td>η² (eta quadrado)</td><td>Fração da variabilidade amostral atribuída às diferenças entre grupos.</td><td>Guião da aula 8, pergunta 6</td></tr>
<tr><td>Declive e intercepto</td><td>Declive: variação média de Y por unidade de X. Intercepto: valor médio esperado de Y quando X = 0.</td><td>Aula 4, diap. 11</td></tr>
<tr><td>Resíduo</td><td>e<sub>i</sub> = y<sub>i</sub> − ŷ<sub>i</sub>: mede o erro cometido pelo modelo nessa observação.</td><td>Aula 5, diap. 6</td></tr>
<tr><td>Erro-padrão</td><td>Mede a variabilidade esperada da estimativa entre diferentes amostras.</td><td>Aula 4, diap. 20</td></tr>
<tr><td>R²</td><td>Variabilidade explicada pelo modelo a dividir pela variabilidade total observada.</td><td>Aula 4, diap. 29</td></tr>
<tr><td>R² ajustado</td><td>Tem em conta a capacidade explicativa e o número de variáveis do modelo.</td><td>Aula 4, diap. 77</td></tr>
<tr><td>Teste F global</td><td>Consideradas em conjunto, as variáveis ajudam a explicar Y? H0: todos os declives são zero.</td><td>Aula 4, diap. 68 e 69</td></tr>
<tr><td>Teste F parcial</td><td>Pergunta se as variáveis adicionais acrescentam informação ao modelo que já contém as outras.</td><td>Aula 4, diap. 81</td></tr>
<tr><td>Homoscedasticidade</td><td>A dispersão dos erros é aproximadamente constante ao longo dos valores previstos.</td><td>Aula 4, diap. 48</td></tr>
<tr><td>Multicolinearidade</td><td>Uma variável explicativa está fortemente relacionada com uma ou mais das restantes.</td><td>Aula 5, diap. 27</td></tr>
<tr><td>VIF</td><td>Indica quanto a variância da estimativa de um coeficiente está aumentada devido à relação da variável com as outras explicativas.</td><td>Aula 4, diap. 83</td></tr>
</table></div>

<footer>
Todos os números vêm dos resultados guardados no notebook <code>TP1_MEPA_IA_Produtividade.ipynb</code>, exceto o Shapiro-Wilk dos resíduos da ANOVA (secção 6), calculado para este guia. As citações da docente vêm dos PDF das aulas 1 a 5, dos guiões de código das aulas 3, 5 e 8 e dos infográficos da pasta de apoio; a numeração dos diapositivos da aula 4 é a da versão de 101 páginas que está na pasta <code>docs apoio</code>. O ficheiro <code>aula_4.pdf</code> da pasta principal é uma versão anterior, de 84 páginas, em que os mesmos diapositivos têm números mais baixos e faltam alguns (4, 21, 28, 35, 41, 54, 66, 79, 81 e 99). As figuras A a F estão na pasta <code>figuras/</code> e foram geradas pelo notebook em 14 de novembro de 2026. A produtividade e os resíduos do M2 têm por coincidência quase o mesmo resultado no Shapiro-Wilk (W = 0,966 nos dois casos); são testes diferentes. Nível de significância em todo o trabalho: 5%.
</footer>
</main>
</body>
</html>
"""

subs = {
    "@@FLUXO@@": fluxograma(),
    "@@TRI@@": TRIANGULO,
    "@@FIG24@@": img("fig_2_4_produtividade", "Histograma, box-plot e gráfico Q-Q da produtividade"),
    "@@FIG31@@": img("fig_3_1_dispersao", "Dispersão do uso de IA contra a produtividade e box-plots por quartil"),
    "@@FIG41@@": img("fig_4_1_departamentos", "Box-plots da produtividade por departamento"),
    "@@FIG56@@": img("fig_5_6_residuos_m1", "Diagnóstico dos resíduos do modelo 1"),
    "@@FIG64@@": img("fig_6_4_coeficiente_ia", "Coeficiente do uso de IA em cinco modelos sucessivos"),
    "@@FIG66@@": img("fig_6_6_residuos_m2", "Diagnóstico dos resíduos do modelo 2"),
}
for k, v in subs.items():
    assert k in HTML, k
    HTML = HTML.replace(k, v)
with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(HTML)
print(OUT, round(len(HTML) / 1e6, 2), "MB")
