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
        [("q", "As duas variáveis quantitativas andam juntas?"),
         ("c", "O gráfico de dispersão (3.1) mostra uma relação em linha reta, sem curva"),
         ("m", "Correlação de Pearson: r = 0,24"),
         ("c", "A produtividade não é normal, tem outliers e um teto em 98"),
         ("m", "Confirmação com Spearman (usa as ordens): ρ = 0,27"),
         ("r", "Os dois concordam: associação positiva e fraca")],
        [("q", "A produtividade média difere entre grupos?"),
         ("c", "Quantos grupos? Com 2 seria um teste t. Aqui são 4 departamentos"),
         ("c", "Condições: independência (pela recolha), normalidade por grupo (Shapiro-Wilk), variâncias iguais (Levene p = 0,52)"),
         ("m", "ANOVA a um fator: p = 0,70"),
         ("m", "Confirmações: Welch p = 0,68 e Kruskal-Wallis p = 0,71"),
         ("r", "Não se rejeita H0. Sem Tukey, que só se faz depois de rejeitar")],
        [("q", "Qual é a produtividade média da população?"),
         ("c", "O desvio-padrão da população é desconhecido e estima-se pela amostra"),
         ("m", "Intervalo de confiança com a distribuição t de Student (237 graus de liberdade)"),
         ("r", "IC 95%: 76,4 a 79,7 pontos")],
        [("q", "O uso de IA explica a produtividade?"),
         ("m", "Regressão linear simples (M1): R² = 0,058"),
         ("c", "Os resíduos do M1 estão ligados à experiência (r = 0,45): falta uma variável"),
         ("m", "Regressão linear múltipla (M2): IA + experiência + formação + complexidade"),
         ("c", "Comparar com R² ajustado e teste F parcial. Verificar VIF e resíduos"),
         ("r", "Escolhe-se o M2. O coeficiente da IA cai de 0,64 para 0,13")],
    ]
    top_h = 40
    parts = []
    parts.append(f'<rect class="b-top" x="{W/2-190}" y="6" width="380" height="{top_h}" rx="20"/>')
    parts.append(f'<text class="t-top" x="{W/2}" y="31" text-anchor="middle">Que pergunta queres responder?</text>')
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
<text class="t-s" x="310" y="56" text-anchor="middle">o fator de confusão</text>
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
</style>
</head>
<body>
<main>

<span class="tag">TP1 de MEPA · Mestrado em Inteligência Artificial · IPCA 2026/27</span>
<h1>O paradoxo da IA: guia da análise passo a passo</h1>
<p class="sub">Para o Gilberto e o Rúbem reverem, antes da defesa, o que foi feito em cada etapa e porque se escolheu cada método. Segue a numeração do notebook <code>TP1_MEPA_IA_Produtividade.ipynb</code>.</p>

<div class="box key">
<h3>A história toda em quatro frases</h3>
<p>Quem usa mais IA é, em média, um pouco mais produtivo, mas a associação é fraca (r = 0,24) e o uso de IA sozinho acompanha cerca de 6% da variação da produtividade.</p>
<p>Os departamentos não diferem (ANOVA p = 0,70).</p>
<p>Quando se comparam colaboradores com a mesma experiência, formação em IA e complexidade de tarefas, o coeficiente da IA cai de 0,64 para 0,13 pontos por hora e deixa de ser significativo (p = 0,47). Quem pesa é a experiência: mais 1,6 pontos por ano.</p>
<p>Por isso o grupo não recomenda tornar a IA obrigatória: os dados mostram associação e não causa.</p>
</div>

<nav>
<b>Índice</b>
<ol>
<li><a href="#s1">O percurso completo</a></li>
<li><a href="#s2">Preparação dos dados</a></li>
<li><a href="#s3">Como se escolheu cada teste</a></li>
<li><a href="#s4">t de Student ou ANOVA?</a></li>
<li><a href="#s5">A normalidade, verificada em três sítios</a></li>
<li><a href="#s6">Associação: Pearson e Spearman</a></li>
<li><a href="#s7">Departamentos: ANOVA e confirmações</a></li>
<li><a href="#s8">Regressão simples (M1) e os seus resíduos</a></li>
<li><a href="#s9">De M1 para M2: o fator de confusão</a></li>
<li><a href="#s10">Diagnóstico dos dois modelos lado a lado</a></li>
<li><a href="#s11">Pontos frágeis a ter prontos na defesa</a></li>
<li><a href="#s12">Mini glossário</a></li>
</ol>
</nav>

<h2 id="s1"><span class="n">1</span>O percurso completo</h2>
<p>Cada etapa responde a uma pergunta do enunciado e prepara a seguinte. O que liga tudo é uma suspeita que nasce na etapa 3 (vários dos que usam muita IA e são muito produtivos têm muita experiência) e que só se confirma na etapa 6.</p>

<div class="steps">
 <div class="step"><div class="k">1</div><div><h3>Conhecer e limpar os dados</h3><div class="g">
  <div><span>Pergunta</span>Os dados estão em condições de ser analisados?</div>
  <div><span>O que se fez</span>Retirar a linha repetida, corrigir grafias, marcar valores suspeitos sem os apagar</div>
  <div><span>Resultado</span>240 colaboradores; 238, 236 ou 233 casos conforme a análise</div></div></div></div>
 <div class="step"><div class="k">2</div><div><h3>Descrever</h3><div class="g">
  <div><span>Pergunta</span>Como são a produtividade e o uso de IA?</div>
  <div><span>O que se fez</span>Média, mediana, quartis; histograma, box-plot, Q-Q e Shapiro-Wilk</div>
  <div><span>Resultado</span>Média 78,0 e mediana 79,35; distribuição com cauda à esquerda e teto em 98; não é normal</div></div></div></div>
 <div class="step"><div class="k">3</div><div><h3>Medir a associação</h3><div class="g">
  <div><span>Pergunta</span>IA e produtividade andam juntas?</div>
  <div><span>O que se fez</span>Dispersão, Pearson e Spearman</div>
  <div><span>Resultado</span>r = 0,24 e ρ = 0,27: positiva, significativa e fraca</div></div></div></div>
 <div class="step"><div class="k">4</div><div><h3>Inferir</h3><div class="g">
  <div><span>Pergunta</span>Os departamentos diferem? Qual é a média na população?</div>
  <div><span>O que se fez</span>Shapiro por grupo e Levene; ANOVA com Welch e Kruskal-Wallis; IC com t</div>
  <div><span>Resultado</span>p = 0,70, sem diferenças; IC 95% de 76,4 a 79,7</div></div></div></div>
 <div class="step"><div class="k">5</div><div><h3>Regressão simples (M1)</h3><div class="g">
  <div><span>Pergunta</span>A IA, sozinha, explica a produtividade?</div>
  <div><span>O que se fez</span>Reta de mínimos quadrados e análise dos resíduos</div>
  <div><span>Resultado</span>73,04 + 0,627 × IA; R² = 0,058; resíduos ligados à experiência</div></div></div></div>
 <div class="step"><div class="k">6</div><div><h3>Regressão múltipla (M2)</h3><div class="g">
  <div><span>Pergunta</span>A relação mantém-se com outros fatores?</div>
  <div><span>O que se fez</span>Juntar experiência, formação e complexidade; R² ajustado, F parcial, VIF, resíduos, robustez</div>
  <div><span>Resultado</span>Coeficiente da IA 0,13 (p = 0,47); R² ajustado 0,267</div></div></div></div>
 <div class="step"><div class="k">7</div><div><h3>Concluir</h3><div class="g">
  <div><span>Pergunta</span>Deve a IA ser obrigatória?</div>
  <div><span>O que se fez</span>Separar descrição, inferência, explicação e recomendação</div>
  <div><span>Resultado</span>Não recomendar; propor formação e um estudo piloto</div></div></div></div>
</div>
<p class="sub">Esquema 1. As sete etapas do trabalho, com a pergunta, o método e o resultado de cada uma.</p>

<h2 id="s2"><span class="n">2</span>Preparação dos dados</h2>
<p>A regra seguida em toda a preparação foi a mesma: corrigir o que é erro comprovado, e marcar (sem apagar) o que é apenas suspeito, repetindo depois as análises sem esses casos para ver se alguma conclusão muda.</p>

<div class="funil">
 <div class="f"><b>241</b><small>linhas no Excel</small></div><div class="ar">→</div>
 <div class="f"><b>240</b><small>colaboradores, depois de retirar a cópia do C084</small></div><div class="ar">→</div>
 <div class="f"><b>238</b><small>com produtividade (descrição, ANOVA, IC)</small></div><div class="ar">→</div>
 <div class="f"><b>236</b><small>com produtividade e uso de IA (correlação, M1)</small></div><div class="ar">→</div>
 <div class="f"><b>233</b><small>com as cinco variáveis do M2</small></div>
</div>
<p class="sub">Esquema 2. Porque é que o número de casos muda de análise para análise: há 8 valores em falta, um em cada um de 8 registos, e não foram preenchidos.</p>

<div class="tw"><table>
<tr><th>O que se encontrou</th><th>Decisão</th><th>Porquê</th><th>Efeito verificado</th></tr>
<tr><td>C084 em duas linhas iguais</td><td>Fica uma</td><td>É a mesma pessoa copiada; contaria a dobrar</td><td>240 identificadores únicos</td></tr>
<tr><td>8 valores em falta</td><td>Não preencher; cada análise usa quem tem os dados de que precisa</td><td>Preencher com a média seria inventar dados e reduzir a variação real</td><td>r = 0,241 com 236 casos e 0,246 com 233</td></tr>
<tr><td>3 grafias erradas de departamento</td><td>Corrigir</td><td>Sem isso a ANOVA veria 7 departamentos, 3 deles com uma pessoa</td><td>4 departamentos: 85, 66, 58 e 31</td></tr>
<tr><td>C097 com produtividade 19 (o valor seguinte é 43,5)</td><td>Manter e repetir sem ele</td><td>Está dentro da escala e não há prova de erro</td><td>Nenhuma conclusão muda</td></tr>
<tr><td>13 colaboradores com produtividade 98 (teto)</td><td>Manter e registar como limitação</td><td>Não se corrige sem saber como é feita a avaliação</td><td>Ajuda a explicar a falta de normalidade</td></tr>
<tr><td>10 casos em que tarefas × tempo por tarefa excedem um mês de trabalho</td><td>Marcar, manter e repetir sem eles</td><td>Cada valor é plausível sozinho; o limite de um mês é uma suposição do grupo</td><td>r = 0,241; ANOVA p = 0,557</td></tr>
<tr><td>Tarefas, tempo por tarefa e qualidade</td><td>Ficam fora dos modelos</td><td>O dicionário diz que são indicadores do mesmo desempenho; usá-los seria explicar o desempenho com o desempenho</td><td>Modelos só com fatores anteriores ao desempenho</td></tr>
</table></div>
<p class="sub">Tabela 1. Decisões de preparação dos dados (blocos 1.2 a 1.6 e 6.1 do notebook).</p>

<h2 id="s3"><span class="n">3</span>Como se escolheu cada teste</h2>
<p>O teste depende de duas coisas: a pergunta que se quer responder e o tipo das variáveis envolvidas. Só depois entram as condições de aplicação, que decidem se o teste clássico chega ou se precisa de um teste de confirmação ao lado.</p>

<figure>
<div class="canvas">@@FLUXO@@</div>
<div class="leg">
 <span><i style="background:var(--q-bg);border-color:var(--q-line)"></i>pergunta</span>
 <span><i style="background:var(--card);border-color:var(--line)"></i>o que se verificou ou se sabe</span>
 <span><i style="background:var(--acc-bg);border-color:var(--acc)"></i>método aplicado</span>
 <span><i style="background:var(--ok-bg);border-color:var(--ok)"></i>conclusão</span>
</div>
<figcaption><b>Esquema 3.</b> Fluxograma da escolha dos métodos. Cada coluna é uma das quatro perguntas do trabalho; lê-se de cima para baixo. O padrão repete-se: um método principal, escolhido pelo tipo de variáveis, e um método de confirmação que não depende da condição que falhou.</figcaption>
</figure>

<h2 id="s4"><span class="n">4</span>t de Student ou ANOVA?</h2>
<p>As duas coisas aparecem no trabalho, em sítios diferentes. A confusão habitual é pensar que são alternativas para o mesmo problema. A distribuição t serve sempre que se trabalha com uma média (ou um coeficiente) e o desvio-padrão é estimado pela amostra. A ANOVA serve para comparar três ou mais médias de uma só vez.</p>

<div class="tw"><table>
<tr><th>Onde</th><th>O que se usa</th><th>Porquê</th></tr>
<tr><td>Comparar a produtividade dos 4 departamentos (4.4)</td><td>ANOVA a um fator</td><td>São 4 grupos. Com testes t seriam 6 comparações par a par e a probabilidade de pelo menos um falso positivo subia de 5% para cerca de 26% (1 − 0,95<sup>6</sup> = 0,265, supondo testes independentes). A ANOVA faz um único teste com o risco fixo em 5%.</td></tr>
<tr><td>Intervalo de confiança da média (4.6)</td><td>t de Student, 237 graus de liberdade</td><td>O desvio-padrão da população não é conhecido. Com n = 238 o valor crítico de t (1,970) quase coincide com o da normal (1,960).</td></tr>
<tr><td>Teste a cada coeficiente das regressões (5.1 e 6.3)</td><td>teste t</td><td>Testa se o coeficiente é diferente de zero. IA no M1: t = 3,80 (p &lt; 0,001). IA no M2: t = 0,72 (p = 0,47). Experiência no M2: t = 8,32 (p &lt; 0,001).</td></tr>
<tr><td>Comparar M1 com M2 (6.5)</td><td>teste F parcial</td><td>Testa três coeficientes em conjunto; o t só testa um de cada vez.</td></tr>
</table></div>
<p class="sub">Tabela 2. Onde entram a distribuição t e a distribuição F neste trabalho.</p>

<div class="box">
<h3>Quando é que um teste t para grupos seria a escolha certa?</h3>
<p>Se a pergunta comparasse só dois grupos, por exemplo colaboradores com e sem formação em IA, ou Desenvolvimento contra os restantes. O enunciado não pede nenhuma comparação desse tipo. Com dois grupos, a ANOVA e o teste t clássico (o que supõe variâncias iguais) dão exatamente o mesmo valor-p (F = t²), por isso a ANOVA é a generalização do teste t para mais grupos.</p>
</div>

<h2 id="s5"><span class="n">5</span>A normalidade, verificada em três sítios</h2>
<p>A normalidade foi verificada em três sítios: na produtividade em si, em cada departamento e nos resíduos das regressões (uma vez para cada modelo, o que dá as quatro linhas da tabela). As ferramentas são sempre o gráfico Q-Q e o teste de Shapiro-Wilk, mas o objetivo muda. Em todos, a hipótese nula do Shapiro-Wilk é «os dados seguem uma distribuição normal», logo um p pequeno significa que a normalidade é rejeitada.</p>

<div class="tw"><table>
<tr><th>O que se testou</th><th>Para quê</th><th class="num">p (todos)</th><th class="num">p sem C097</th><th>O que se fez a seguir</th></tr>
<tr><td>A produtividade em si (2.4)</td><td>Descrever a forma da distribuição e orientar as escolhas seguintes</td><td class="num no">0,00002</td><td class="num no">0,0009</td><td>Juntar a cada teste que supõe normalidade um teste que não a exige</td></tr>
<tr><td>A produtividade em cada departamento (4.3)</td><td>Condição da ANOVA</td><td class="num"><span class="yes">AD 0,36 · Com 0,32 · Op 0,06</span> · <span class="no">Dev 0,0004</span></td><td class="num no">Dev 0,027</td><td>ANOVA mantida (grupos de 31 a 85, variâncias iguais) e confirmada com Kruskal-Wallis</td></tr>
<tr><td>Os resíduos do M1 (5.6)</td><td>Pressuposto da regressão: valida os valores-p e os IC dos coeficientes</td><td class="num no">0,0001</td><td class="num no">0,030</td><td>Repetir sem C097: o declive fica igual (0,627)</td></tr>
<tr><td>Os resíduos do M2 (6.6)</td><td>O mesmo, para o modelo final</td><td class="num no">0,00002</td><td class="num yes">0,965</td><td>Repetir sem C097: o coeficiente da IA quase não muda (0,146; p = 0,38)</td></tr>
</table></div>
<p class="sub">Tabela 3. Resultados do Shapiro-Wilk. A laranja, normalidade rejeitada a 5%; a verde, não rejeitada. AD = Análise de Dados, Com = Comunicação, Op = Operações, Dev = Desenvolvimento.</p>

<figure>
@@FIG24@@
<figcaption><b>Figura A</b> (bloco 2.4, Figura 2 do relatório). A mesma variável vista de três maneiras. O histograma mostra a forma, o box-plot mostra os valores afastados (C097 e C129) e o Q-Q mostra onde a distribuição se afasta da normal: em baixo, por causa dos valores muito baixos, e em cima, onde os pontos ficam em linha horizontal por causa do teto em 98.</figcaption>
</figure>

<div class="box key">
<h3>Porquê Shapiro-Wilk e porquê olhar também para o gráfico</h3>
<p>O Shapiro-Wilk é o teste que a docente recomenda para amostras pequenas e médias. O gráfico Q-Q acrescenta o que o teste não diz: em que zona a distribuição falha. Aqui há duas causas distintas, uma cauda comprida à esquerda e um teto à direita.</p>
<p>O que se deve testar numa regressão são os resíduos e não a variável resposta. A produtividade pode não ser normal e o modelo estar bem, desde que o que sobra depois de o modelo explicar o que consegue seja aproximadamente normal. É o que acontece no M2 sem o C097.</p>
</div>

<h2 id="s6"><span class="n">6</span>Associação: Pearson e Spearman</h2>
<div class="cols">
<div class="box"><h3>Pearson (principal)</h3><p>Mede a associação em linha reta entre duas variáveis quantitativas. Escolheu-se porque as duas variáveis são quantitativas e o gráfico não mostra curva.</p><p>r = 0,241 (p = 0,0002; n = 236).</p></div>
<div class="box"><h3>Spearman (confirmação)</h3><p>Faz o mesmo cálculo com as posições (ordens) em vez dos valores, por isso é pouco sensível a outliers, ao teto e à falta de normalidade.</p><p>ρ = 0,266 (p = 0,00004).</p></div>
</div>
<p>Os dois concordam, logo a conclusão não depende dos problemas da distribuição. Sem o C097, r = 0,252; sem os 10 casos marcados, r = 0,241.</p>

<figure>
@@FIG31@@
<figcaption><b>Figura B</b> (bloco 3.1, Figura 3 do relatório). À esquerda, cada ponto é um colaborador e a reta resume a tendência. À direita, os box-plots por quartil de uso de IA tornam a subida visível apesar da dispersão. A leitura conjunta é a mensagem do capítulo 3: a tendência existe, mas para qualquer nível de uso há produtividades muito diferentes.</figcaption>
</figure>

<div class="box warn">
<h3>Significativo não quer dizer forte</h3>
<p>O valor-p responde à pergunta «a associação é diferente de zero?». A intensidade lê-se no próprio r. Com 236 pessoas, até uma associação fraca se distingue do zero. Na escala dos infográficos da docente, entre 0,2 e 0,4 a associação é fraca; e r² = 0,058 diz que o uso de IA acompanha cerca de 6% da variação da produtividade.</p>
</div>

<h2 id="s7"><span class="n">7</span>Departamentos: ANOVA e confirmações</h2>
<p>Hipóteses: H0, as quatro médias são iguais; H1, pelo menos duas são diferentes. Antes de correr o teste verificaram-se as três condições e decidiu-se o método, para a escolha não depender do resultado.</p>

<div class="tw"><table>
<tr><th>Condição</th><th>Como se verificou</th><th>Resultado</th><th>Consequência</th></tr>
<tr><td>Independência</td><td>Pela forma de recolha: cada colaborador aparece uma vez e pertence a um só departamento</td><td class="yes">Cumprida</td><td>Não há teste; decorre do desenho do estudo e da remoção do duplicado</td></tr>
<tr><td>Normalidade em cada grupo</td><td>Shapiro-Wilk por departamento</td><td>Falha em Desenvolvimento (p = 0,0004; sem C097, 0,027)</td><td>Juntar o Kruskal-Wallis, que não exige normalidade</td></tr>
<tr><td>Variâncias iguais</td><td>Levene com a mediana (o Bartlett é muito sensível à falta de normalidade)</td><td class="yes">p = 0,52; desvios-padrão de 11,6 a 14,0</td><td>ANOVA clássica como teste principal. Juntar o Welch por prudência, porque os grupos têm tamanhos muito diferentes (31 a 85)</td></tr>
</table></div>
<p class="sub">Tabela 4. Condições de aplicação da ANOVA a um fator (bloco 4.3).</p>

<div class="tw"><table>
<tr><th>Teste</th><th>O que não exige</th><th>Estatística</th><th class="num">p</th></tr>
<tr><td>ANOVA a um fator (principal)</td><td></td><td>F(3, 234) = 0,47</td><td class="num">0,702</td></tr>
<tr><td>ANOVA de Welch</td><td>variâncias iguais</td><td>F(3; 105,7) = 0,50</td><td class="num">0,681</td></tr>
<tr><td>Kruskal-Wallis</td><td>normalidade</td><td>H(3) = 1,37</td><td class="num">0,713</td></tr>
<tr><td>ANOVA sem C097</td><td></td><td></td><td class="num">0,632</td></tr>
<tr><td>ANOVA sem os 10 casos marcados</td><td></td><td></td><td class="num">0,557</td></tr>
</table></div>
<p class="sub">Tabela 5. Os três testes e as duas repetições dão a mesma resposta: não se rejeita H0 (blocos 4.4a e 4.4b).</p>

<figure>
@@FIG41@@
<figcaption><b>Figura C</b> (bloco 4.1, Figura 4 do relatório). As caixas sobrepõem-se quase por completo e as médias (76,5 a 79,2) distam no máximo 2,7 pontos, pouco face aos desvios-padrão de 11,6 a 14,0 dentro de cada departamento. É a intuição por trás da ANOVA: compara a variação entre grupos com a variação dentro dos grupos.</figcaption>
</figure>

<ul>
<li>Leitura de p = 0,70: se as médias fossem iguais, diferenças como estas ou maiores apareceriam em cerca de 70% das amostras.</li>
<li>Tamanho do efeito: η² = 0,006, ou seja, o departamento explica 0,6% da variação. Fica abaixo do limiar de efeito pequeno (0,01).</li>
<li>Sem teste de Tukey: as comparações par a par só se fazem depois de a ANOVA rejeitar H0.</li>
<li>Não rejeitar H0 não prova que as médias são iguais; diz que estes dados não mostram diferenças.</li>
</ul>

<h3>Intervalo de confiança da média (4.6)</h3>
<p>Média 78,03, erro-padrão 0,832, IC 95% de 76,39 a 79,67. Usa a distribuição t porque o desvio-padrão é estimado pela amostra. Apesar de a produtividade não ser normal, com 238 casos a média amostral comporta-se de forma aproximadamente normal, por isso o intervalo continua adequado. O intervalo é para a média e não para os colaboradores: a maioria deles está fora de 76,4 a 79,7.</p>

<h2 id="s8"><span class="n">8</span>Regressão simples (M1) e os seus resíduos</h2>
<div class="box key">
<p><b>produtividade estimada = 73,04 + 0,627 × horas de IA</b> (n = 236)</p>
<p>73,04 é a produtividade média estimada de quem não usa IA (há 11 pessoas nessa situação, por isso o valor tem leitura). Por cada hora semanal a mais, a produtividade média estimada é 0,63 pontos mais alta (IC 95%: 0,30 a 0,95). R² = 0,058.</p>
</div>
<p>O resíduo de cada colaborador é a diferença entre o valor observado e o estimado. Exemplo do enunciado: o C001 usa 7,7 h, o modelo estima 77,9 e o valor real é 68,0; o resíduo é −9,9. Os resíduos servem para duas coisas: verificar os pressupostos do modelo e descobrir o que o modelo não está a ver.</p>

<figure>
@@FIG56@@
<figcaption><b>Figura D</b> (bloco 5.6a, Figura 5 do relatório). Os três gráficos de diagnóstico do M1. À esquerda procura-se curva (relação mal especificada) ou funil (variância não constante): não há nenhum dos dois. Ao centro e à direita avalia-se a normalidade dos resíduos: a cauda esquerda, dominada pelo C097 e pelo C129, é o que leva o Shapiro-Wilk a rejeitar.</figcaption>
</figure>

<div class="box ok">
<h3>O passo que justifica o capítulo 6</h3>
<p>No bloco 5.6c correlacionaram-se os resíduos do M1 com as variáveis que ficaram de fora. Com a experiência a correlação é 0,45 (p &lt; 0,001); com a formação, a complexidade e a carga é praticamente nula. Os mais experientes ficam sistematicamente acima do que o M1 prevê. Isto é a assinatura de uma variável omitida, e é a razão estatística para passar ao modelo múltiplo.</p>
</div>

<h2 id="s9"><span class="n">9</span>De M1 para M2: o fator de confusão</h2>
<p>Um fator de confusão é uma variável que influencia ao mesmo tempo a explicação (uso de IA) e a resposta (produtividade). Se ficar de fora do modelo, o coeficiente da IA recebe mérito que não é seu.</p>

<figure>
<div class="canvas">@@TRI@@</div>
<figcaption><b>Esquema 4.</b> A experiência está ligada ao uso de IA e à produtividade (setas azuis, correlações de Pearson). A seta tracejada é a relação que interessa: o coeficiente da IA vale 0,64 quando está sozinha no modelo e 0,13 quando se comparam pessoas com a mesma experiência, formação e complexidade.</figcaption>
</figure>

<h3>Que variáveis entraram no M2 e porquê</h3>
<div class="tw"><table>
<tr><th>Variável</th><th class="num">r com a produtividade</th><th>Decisão</th><th>Razão</th></tr>
<tr><td>Experiência</td><td class="num">0,50</td><td class="yes">Entra</td><td>Anterior ao desempenho e ligada ao uso de IA (0,27)</td></tr>
<tr><td>Formação em IA</td><td class="num">0,15</td><td class="yes">Entra</td><td>Anterior ao desempenho e muito ligada ao uso de IA (0,51)</td></tr>
<tr><td>Complexidade das tarefas</td><td class="num">−0,01</td><td class="yes">Entra (controlo)</td><td>Característica do posto de trabalho, referida no enunciado</td></tr>
<tr><td>Carga de trabalho, departamento</td><td class="num">0,08; ANOVA p = 0,70</td><td>Só no teste de robustez</td><td>Pouca relação com a produtividade</td></tr>
<tr><td>Tarefas, tempo por tarefa, qualidade</td><td class="num">0,44; −0,48; 0,46</td><td class="no">Ficam de fora</td><td>Medem o mesmo desempenho; fariam subir o R² sem explicar nada e podiam esconder o efeito da IA</td></tr>
</table></div>
<p class="sub">Tabela 6. Seleção das variáveis explicativas (bloco 6.1).</p>

<figure>
@@FIG64@@
<figcaption><b>Figura E</b> (bloco 6.4, Figura 7 do relatório). É o gráfico que conta a história do trabalho. Todos os modelos usam os mesmos 233 casos. Juntar só a formação quase não mexe no coeficiente (0,60); juntar só a experiência corta-o para metade (0,31; p = 0,044); com as duas, cai para 0,13 e o intervalo passa a incluir o zero.</figcaption>
</figure>

<h3>O M2 é mesmo melhor do que o M1?</h3>
<div class="tw"><table>
<tr><th></th><th class="num">M1 (só IA)</th><th class="num">M2 (IA + 3 variáveis)</th><th>Porque se olha para isto</th></tr>
<tr><td>n</td><td class="num">233</td><td class="num">233</td><td>A comparação só é justa com os mesmos casos; por isso o M1 foi estimado de novo com 233</td></tr>
<tr><td>R²</td><td class="num">0,061</td><td class="num">0,280</td><td>Sobe sempre que se juntam variáveis, mesmo inúteis</td></tr>
<tr><td>R² ajustado</td><td class="num">0,056</td><td class="num">0,267</td><td>Desconta o número de variáveis; é o que se compara</td></tr>
<tr><td>Soma dos quadrados dos resíduos</td><td class="num">35 990</td><td class="num">27 590</td><td>O erro que fica por explicar</td></tr>
<tr><td>Teste F parcial</td><td class="num" colspan="2">F(3, 228) = 23,1; p &lt; 0,001</td><td>Testa se as três variáveis juntas melhoram o modelo. Aplica-se porque o M1 está contido no M2 (modelos encaixados)</td></tr>
</table></div>
<p class="sub">Tabela 7. Comparação dos dois modelos (bloco 6.5).</p>

<div class="box key">
<p><b>produtividade estimada = 67,32 + 0,129 × IA + 1,584 × experiência + 0,231 × formação − 0,661 × complexidade</b> (n = 233)</p>
<p>Cada coeficiente lê-se «mantendo as outras variáveis iguais». Só a experiência é claramente significativa (p &lt; 0,001). A formação fica no limite (p = 0,059). Os coeficientes não se comparam em tamanho entre si porque estão em unidades diferentes.</p>
</div>

<h2 id="s10"><span class="n">10</span>Diagnóstico dos dois modelos lado a lado</h2>
<p>Em cada pressuposto seguiu-se a ordem das aulas: primeiro o gráfico, depois o teste.</p>
<div class="tw"><table>
<tr><th>Pressuposto</th><th>Ferramenta</th><th>O que se procura</th><th>M1</th><th>M2</th></tr>
<tr><td>Relação em linha reta</td><td>Resíduos contra valores ajustados</td><td>Ausência de curva</td><td class="yes">Sem padrão</td><td class="yes">Sem padrão</td></tr>
<tr><td>Variância constante</td><td>O mesmo gráfico e o teste de Breusch-Pagan (H0: variância constante)</td><td>Ausência de funil; p &gt; 0,05</td><td class="yes">p = 0,976</td><td class="yes">p = 0,185</td></tr>
<tr><td>Independência</td><td>Desenho do estudo. O Durbin-Watson só faz sentido com ordem temporal</td><td>Um registo por pessoa</td><td class="yes">Pelo desenho (DW 1,84)</td><td class="yes">Pelo desenho (DW 1,95)</td></tr>
<tr><td>Normalidade dos resíduos</td><td>Histograma, Q-Q e Shapiro-Wilk</td><td>p &gt; 0,05</td><td class="no">p = 0,0001; sem C097, 0,030</td><td><span class="no">p = 0,00002</span>; <span class="yes">sem C097, 0,965</span></td></tr>
<tr><td>Observações influentes</td><td>Distância de Cook (referência 4/n; preocupante acima de 1)</td><td>Nenhuma domina o ajuste</td><td class="yes">Máximo 0,060 (C134); 7 acima de 4/n</td><td class="yes">Máximo 0,066 (C097); 7 acima de 4/n</td></tr>
<tr><td>Multicolinearidade</td><td>VIF (preocupa acima de 5)</td><td>Explicativas que não dizem o mesmo</td><td>Não se aplica (uma só variável)</td><td class="yes">Máximo 1,51</td></tr>
</table></div>
<p class="sub">Tabela 8. Pressupostos da regressão nos dois modelos (blocos 5.6a e 6.6a).</p>

<figure>
@@FIG66@@
<figcaption><b>Figura F</b> (bloco 6.6a, Figura 8 do relatório). Diagnóstico do M2. Comparada com a Figura D, a nuvem da esquerda continua sem padrão e o Q-Q segue a reta em quase todo o comprimento; o ponto isolado em baixo é o C097, com resíduo −60,6.</figcaption>
</figure>

<h3>Robustez: a conclusão depende das escolhas do grupo?</h3>
<div class="tw"><table>
<tr><th>Versão do modelo</th><th class="num">Coeficiente da IA</th><th class="num">p</th><th class="num">R² ajustado</th></tr>
<tr><td>M2</td><td class="num">0,129</td><td class="num">0,471</td><td class="num">0,267</td></tr>
<tr><td>M2 sem C097</td><td class="num">0,146</td><td class="num">0,384</td><td class="num">0,302</td></tr>
<tr><td>M2 com carga de trabalho e departamento</td><td class="num">0,144</td><td class="num">0,446</td><td class="num">0,274</td></tr>
<tr><td>M2 com a complexidade como categoria</td><td class="num">0,122</td><td class="num">0,500</td><td class="num">0,272</td></tr>
</table></div>
<p class="sub">Tabela 9. Em todas as versões o coeficiente da IA fica entre 0,12 e 0,15 e nunca é significativo (bloco 6.6b). A interação IA × experiência também é nula (0,028; p = 0,50) e tratar a complexidade como categoria não melhora o modelo (F(3, 225) = 1,55; p = 0,20).</p>

<div class="box">
<h3>Porque é que a queda do coeficiente não é multicolinearidade</h3>
<p>A multicolinearidade incha o erro-padrão dos coeficientes. Aqui o erro-padrão do coeficiente da IA quase não muda: 0,166 no M1 e 0,179 no M2, com os mesmos 233 casos, e o VIF é 1,51. O que mudou foi a própria estimativa (de 0,64 para 0,13), que é o comportamento esperado quando se junta um fator de confusão.</p>
</div>

<h2 id="s11"><span class="n">11</span>Pontos frágeis a ter prontos na defesa</h2>
<p>São os sítios onde uma pergunta atenta pode apanhar uma resposta decorada. Em cada um está o que os resultados mostram e a resposta que se aguenta.</p>

<div class="box warn">
<h3>1. «A normalidade falha só por causa do C097»</h3>
<p>Os comentários de alguns blocos dizem-no assim, mas os resultados são mais matizados (Tabela 3). Sem o C097, a produtividade continua a rejeitar a normalidade (p = 0,0009), o grupo Desenvolvimento também (p = 0,027) e os resíduos do M1 também (p = 0,030). Só os resíduos do M2 passam (p = 0,965).</p>
<p>Resposta segura: há duas causas, o C097 e o teto em 98. Por isso cada teste paramétrico foi acompanhado de um teste que não exige normalidade (Spearman, Kruskal-Wallis), os grupos são grandes, e no modelo final os resíduos ficam compatíveis com a normalidade sem o C097.</p>
</div>

<div class="box warn">
<h3>2. Dois declives para o modelo simples: 0,627 e 0,639</h3>
<p>0,627 é o M1 com os 236 casos que têm IA e produtividade (capítulo 5). 0,639 é o mesmo modelo estimado só com os 233 casos do M2, para a comparação do capítulo 6 ser feita com as mesmas pessoas. A queda de 80% calcula-se a partir de 0,639.</p>
</div>

<div class="box warn">
<h3>3. Só com a experiência, a IA ainda é significativa</h3>
<p>Com IA e experiência no modelo, o coeficiente da IA é 0,31 com p = 0,044. Só deixa de ser significativo quando entra também a formação, que está muito ligada ao uso de IA (r = 0,51). Se a formação levar a usar mais IA, controlá-la pode estar a retirar à IA parte de um efeito real.</p>
<p>Resposta segura: a experiência não é consequência de usar IA e, sozinha, já corta o coeficiente para metade. E o intervalo do M2 (−0,22 a 0,48) é largo: os dados não mostram um efeito, mas também não provam que ele é zero.</p>
</div>

<div class="box warn">
<h3>4. O teto em 98 e as previsões acima de 100</h3>
<p>Treze colaboradores têm exatamente 98. A reta não sabe que a escala acaba em 100, por isso o intervalo de previsão para 10 h vai até 103,9. O modelo descreve a tendência média e não serve para prever uma pessoa concreta. Fica como limitação.</p>
</div>

<div class="box warn">
<h3>5. Outras perguntas curtas</h3>
<ul>
<li>O limite de um mês nos casos incoerentes é uma suposição do grupo, porque o dicionário não define o período. Por isso os casos foram marcados e não apagados.</li>
<li>Os 6 registos incompletos com produtividade conhecida têm média 86,0 contra 77,8 nos completos. São 6 em 240 e a correlação não muda com ou sem eles, mas não se pode garantir que as faltas são ao acaso.</li>
<li>A complexidade é ordinal e foi tratada como número; testou-se como categoria e nada muda.</li>
<li>O Durbin-Watson está lá por completude: sem ordem temporal não testa nada.</li>
<li>Os dados são sintéticos e de um só momento: nenhuma conclusão é causal nem descreve uma empresa real.</li>
<li>O M2 deixa cerca de 73% da variação por explicar.</li>
</ul>
</div>

<h2 id="s12"><span class="n">12</span>Mini glossário</h2>
<div class="tw"><table>
<tr><th>Termo</th><th>Em uma frase</th></tr>
<tr><td>Valor-p</td><td>Probabilidade de obter um resultado tão ou mais extremo do que o observado, se a hipótese nula fosse verdadeira. Rejeita-se H0 quando p ≤ 0,05.</td></tr>
<tr><td>Shapiro-Wilk</td><td>Testa se os dados são compatíveis com uma distribuição normal (H0: são normais).</td></tr>
<tr><td>Gráfico Q-Q</td><td>Compara os quantis dos dados com os de uma normal; pontos sobre a reta indicam normalidade.</td></tr>
<tr><td>Levene</td><td>Testa se os grupos têm variâncias iguais (H0: são iguais).</td></tr>
<tr><td>ANOVA a um fator</td><td>Compara as médias de três ou mais grupos num só teste, dividindo a variação entre grupos pela variação dentro dos grupos.</td></tr>
<tr><td>Welch</td><td>Versão da ANOVA que não exige variâncias iguais.</td></tr>
<tr><td>Kruskal-Wallis</td><td>Alternativa à ANOVA baseada em ordens; não exige normalidade.</td></tr>
<tr><td>η² (eta quadrado)</td><td>Parte da variação explicada pelo fator: 0,01 pequeno, 0,06 médio, 0,14 grande.</td></tr>
<tr><td>Tukey</td><td>Comparações par a par, feitas só depois de a ANOVA rejeitar H0.</td></tr>
<tr><td>Resíduo</td><td>Valor observado menos valor estimado pelo modelo.</td></tr>
<tr><td>R² e R² ajustado</td><td>Parte da variação da resposta explicada pelo modelo; o ajustado penaliza o número de variáveis.</td></tr>
<tr><td>Teste F parcial</td><td>Compara dois modelos encaixados: testa se as variáveis acrescentadas, em conjunto, melhoram o ajuste.</td></tr>
<tr><td>Breusch-Pagan</td><td>Testa se a variância dos resíduos é constante (H0: é constante).</td></tr>
<tr><td>Distância de Cook</td><td>Mede quanto o modelo mudaria se uma observação fosse retirada.</td></tr>
<tr><td>VIF</td><td>Mede quanto a variância de um coeficiente aumenta por a variável estar ligada às outras explicativas; entre 1 e 5 não preocupa.</td></tr>
<tr><td>Fator de confusão</td><td>Variável ligada ao mesmo tempo à explicação e à resposta, que distorce a relação entre as duas se ficar fora do modelo.</td></tr>
</table></div>

<footer>
Todos os números vêm dos resultados guardados no notebook <code>TP1_MEPA_IA_Produtividade.ipynb</code>. As figuras A a F estão na pasta <code>figuras/</code> e foram geradas pelo notebook em 9 de novembro de 2026. A produtividade e os resíduos do M2 têm por coincidência quase o mesmo resultado no Shapiro-Wilk (W = 0,966 nos dois casos); são testes diferentes. Para o detalhe de cada bloco e as respostas curtas às perguntas prováveis, ver <code>GUIAO_DEFESA.md</code>. Nível de significância em todo o trabalho: 5%.
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
