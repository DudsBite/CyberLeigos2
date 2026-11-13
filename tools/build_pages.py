#!/usr/bin/env python3
"""Gera as páginas HTML do CyberLeigos com cabeçalho, rodapé e ícones idênticos.
Uso (na raiz do projeto):  python3 tools/build_pages.py
Só é necessário ao alterar o cabeçalho/rodapé/lista de páginas; o site publicado é estático."""
import os, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUPABASE_CDN = "https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.45.4/dist/umd/supabase.js"

ICONS = {
 "flag": '<path d="M16 3l11 4v8c0 7-5 12-11 14C10 27 5 22 5 15V7z"/><path d="M11 16l4 4 7-8"/>',
 "shield": '<path d="M16 3l11 4v8c0 7-5 12-11 14C10 27 5 22 5 15V7z"/><path d="M11 16l4 4 7-8"/>',
 "key": '<circle cx="10" cy="16" r="5"/><path d="M15 16h14M25 16v5M21 16v4"/>',
 "lock": '<rect x="7" y="14" width="18" height="13" rx="2"/><path d="M11 14v-3a5 5 0 0 1 10 0v3M16 19v3"/>',
 "mail": '<rect x="4" y="7" width="24" height="18" rx="2"/><path d="M5 9l11 9 11-9"/>',
 "chat": '<path d="M5 6h22v15H14l-6 5v-5H5z"/><path d="M11 13.5h.01M16 13.5h.01M21 13.5h.01"/>',
 "eye": '<path d="M3 16s5-9 13-9 13 9 13 9-5 9-13 9S3 16 3 16z"/><circle cx="16" cy="16" r="4"/>',
 "phone": '<rect x="9" y="3" width="14" height="26" rx="3"/><path d="M14 25h4"/>',
 "wifi": '<path d="M4 12a17 17 0 0 1 24 0M8 17a11 11 0 0 1 16 0M12 22a5 5 0 0 1 8 0M16 26h.01"/>',
 "bug": '<ellipse cx="16" cy="18" rx="6" ry="8"/><path d="M12 10a4 4 0 0 1 8 0M10 14l-5-2M22 14l5-2M10 20H4M28 20h-6M10 25l-4 2M22 25l4 2M16 12v14"/>',
 "mask": '<path d="M5 8h22v8c0 6-5 10-11 10S5 22 5 16z"/><path d="M10 14h4M18 14h4M12 20c2 2 6 2 8 0"/>',
 "database": '<ellipse cx="16" cy="8" rx="10" ry="4"/><path d="M6 8v16c0 2.2 4.5 4 10 4s10-1.8 10-4V8M6 16c0 2.2 4.5 4 10 4s10-1.8 10-4"/>',
 "globe": '<circle cx="16" cy="16" r="12"/><ellipse cx="16" cy="16" rx="5" ry="12"/><path d="M4 16h24"/>',
 "alert": '<path d="M16 4L29 27H3z"/><path d="M16 13v7M16 24h.01"/>',
 "cloud": '<path d="M9 24a6 6 0 0 1-.5-12 8 8 0 0 1 15.2 1.5A5 5 0 0 1 23 24z"/>',
 "cart": '<path d="M3 5h4l3 14h14l3-10H8"/><circle cx="12" cy="25" r="2"/><circle cx="22" cy="25" r="2"/>',
 "users": '<circle cx="12" cy="11" r="4"/><path d="M4 26c0-5 4-8 8-8s8 3 8 8"/><circle cx="23" cy="12" r="3"/><path d="M23 18c4 0 6 3 6 6"/>',
 "brain": '<rect x="8" y="8" width="16" height="16" rx="2"/><path d="M12 4v4M20 4v4M12 24v4M20 24v4M4 12h4M4 20h4M24 12h4M24 20h4"/><circle cx="16" cy="16" r="2"/>',
 "refresh": '<path d="M26 16a10 10 0 1 1-3-7.1"/><path d="M26 5v6h-6"/>',
 "sos": '<circle cx="16" cy="16" r="11"/><circle cx="16" cy="16" r="4"/><path d="M8.2 8.2l4.6 4.6M19.2 19.2l4.6 4.6M23.8 8.2l-4.6 4.6M12.8 19.2l-4.6 4.6"/>',
 "user": '<circle cx="16" cy="11" r="5"/><path d="M5 28c0-6 5-10 11-10s11 4 11 10"/>',
 "trophy": '<path d="M10 5h12v7a6 6 0 0 1-12 0z"/><path d="M10 8H5v2a5 5 0 0 0 5 5M22 8h5v2a5 5 0 0 1-5 5M16 18v5M11 27h10M13 23h6"/>',
 "flame": '<path d="M16 3c1 5 8 8 8 15a8 8 0 0 1-16 0c0-3 2-5 3-7 1 2 2 3 3 3 0-4 0-7 2-11z"/>',
 "star": '<path d="M16 4l3.8 7.9 8.7 1.2-6.3 6.1 1.5 8.6L16 23.7 8.3 27.8l1.5-8.6-6.3-6.1 8.7-1.2z"/>',
 "check": '<path d="M6 17l7 7 13-14"/>',
 "x": '<path d="M8 8l16 16M24 8L8 24"/>',
 "book": '<path d="M5 6h9a3 3 0 0 1 2 1 3 3 0 0 1 2-1h9v20h-9a3 3 0 0 0-2 1 3 3 0 0 0-2-1H5z"/><path d="M16 7v19"/>',
 "gamepad": '<rect x="3" y="9" width="26" height="14" rx="6"/><path d="M10 13v6M7 16h6M21 15h.01M24 18h.01"/>',
 "target": '<circle cx="16" cy="16" r="12"/><circle cx="16" cy="16" r="7"/><circle cx="16" cy="16" r="2"/>',
 "home": '<path d="M4 15L16 4l12 11M7 13v14h18V13M13 27v-8h6v8"/>',
 "chart": '<path d="M5 27V5M5 27h22M10 22v-6M16 22V10M22 22v-9"/>',
 "logout": '<path d="M12 5H6v22h6M20 10l6 6-6 6M26 16H12"/>',
 "chevron-down": '<path d="M8 12l8 8 8-8"/>',
 "chevron-right": '<path d="M12 8l8 8-8 8"/>',
 "chevron-left": '<path d="M20 8l-8 8 8 8"/>',
 "menu": '<path d="M5 9h22M5 16h22M5 23h22"/>',
 "search": '<circle cx="14" cy="14" r="8"/><path d="M20 20l8 8"/>',
 "clock": '<circle cx="16" cy="16" r="12"/><path d="M16 9v7l5 3"/>',
 "folder": '<path d="M4 8h8l3 3h13v15H4z"/>',
 "computer": '<rect x="4" y="5" width="24" height="16" rx="2"/><path d="M11 27h10M16 21v6"/>',
 "network": '<circle cx="16" cy="7" r="3"/><circle cx="7" cy="25" r="3"/><circle cx="25" cy="25" r="3"/><path d="M16 10v6M16 16L8.5 22.5M16 16l7.5 6.5"/>',
 "medal": '<circle cx="16" cy="19" r="8"/><path d="M11 3l5 8 5-8M13 19l2 2 4-4"/>',
 "camera": '<rect x="3" y="9" width="26" height="17" rx="3"/><circle cx="16" cy="17" r="5"/><path d="M11 9l2-3h6l2 3"/>',
 "mic": '<rect x="12" y="3" width="8" height="15" rx="4"/><path d="M7 14a9 9 0 0 0 18 0M16 23v5M12 28h8"/>',
 "pin": '<path d="M16 28s-9-8-9-15a9 9 0 0 1 18 0c0 7-9 15-9 15z"/><circle cx="16" cy="13" r="3"/>',
 "contacts": '<rect x="6" y="4" width="20" height="24" rx="2"/><circle cx="16" cy="13" r="4"/><path d="M9 24c1-4 4-6 7-6s6 2 7 6"/>',
 "drive": '<rect x="4" y="12" width="24" height="10" rx="2"/><path d="M8 17h.01M12 17h8"/>',
 "link": '<path d="M13 19a5 5 0 0 0 7 0l4-4a5 5 0 0 0-7-7l-1 1M19 13a5 5 0 0 0-7 0l-4 4a5 5 0 0 0 7 7l1-1"/>',
 "send": '<path d="M27 5L4 14l8 4 4 9z"/>',
 "info": '<circle cx="16" cy="16" r="12"/><path d="M16 14v8M16 10h.01"/>',
 "edit": '<path d="M5 27l1-6L21 6l5 5-15 15z"/>',
 "play": '<path d="M10 6l16 10-16 10z"/>',
 "heart": '<path d="M16 27S4 19 4 11a6 6 0 0 1 12-2 6 6 0 0 1 12 2c0 8-12 16-12 16z"/>',
 "lightbulb": '<path d="M12 22v-3a8 8 0 1 1 8 0v3zM13 27h6M14 24h4"/>',
 "eye-off": '<path d="M3 16s5-9 13-9c2 0 4 .6 5.6 1.5M29 16s-5 9-13 9c-2 0-4-.6-5.6-1.5M5 5l22 22"/>',
 "usb": '<rect x="10" y="3" width="12" height="10" rx="1"/><path d="M13 7h.01M19 7h.01M12 13v14h8V13"/>',
}

def sprite():
    s = ['<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>']
    for k, v in ICONS.items():
        s.append('<symbol id="i-%s" viewBox="0 0 32 32">%s</symbol>' % (k, v))
    s.append('</defs></svg>')
    return "".join(s)

def ico(name, cls=""):
    return '<svg class="ico %s" aria-hidden="true" focusable="false"><use href="#i-%s"/></svg>' % (cls, name)

NAV = [("licoes.html", "Lições"), ("tarefas.html", "Tarefas"), ("quizzes.html", "Quizzes"),
       ("minigames.html", "Minigames"), ("ranking.html", "Ranking")]
MORE = [("progresso.html", "Meu progresso"), ("glossario.html", "Glossário"), ("tier-list.html", "Tier List de navegadores"), ("sobre.html", "Sobre o CyberLeigos")]

def header(current):
    def a(h, t):
        cur = ' aria-current="page"' if h == current else ""
        return '<a href="%s"%s>%s</a>' % (h, cur, t)
    nav = "".join(a(h, t) for h, t in NAV)
    more = "".join(a(h, t) for h, t in MORE)
    return f'''<a href="#conteudo" class="skip-link">Pular para o conteúdo</a>
<header class="navbar">
  <div class="nav-inner">
    <a href="index.html" class="logo" aria-label="CyberLeigos — página inicial">{ico("flag")}<span>CyberLeigos</span></a>
    <nav id="navLinks" class="nav-links" aria-label="Navegação principal">
      {nav}
      <div class="nav-more"><button type="button" aria-expanded="false" aria-haspopup="true">Mais {ico("chevron-down", "ico-sm")}</button><div class="nav-more-menu">{more}</div></div>
    </nav>
    <div class="nav-right">
      <a class="xp-chip" href="progresso.html" title="Seus pontos de experiência">{ico("star")}<span><b data-cl-xp>0</b> XP</span></a>
      <div class="auth-slot" id="authSlot"><span class="auth-skeleton" aria-label="Carregando conta"></span></div>
      <button class="nav-toggle" id="navToggle" type="button" aria-expanded="false" aria-controls="navLinks" aria-label="Abrir ou fechar menu">{ico("menu")}</button>
    </div>
  </div>
</header>'''

def footer():
    return f'''<footer class="site-footer">
  <div class="footer-inner">
    <div>
      <p class="footer-logo">{ico("flag")} CyberLeigos</p>
      <p class="footer-slogan">Cibersegurança sem complicação.</p>
    </div>
    <div class="footer-cols">
      <div><h4>Aprender</h4><a href="licoes.html">Lições</a><a href="quizzes.html">Quizzes</a><a href="minigames.html">Minigames</a><a href="glossario.html">Glossário</a></div>
      <div><h4>Sua jornada</h4><a href="tarefas.html">Tarefas diárias</a><a href="progresso.html">Progresso</a><a href="ranking.html">Ranking</a><a href="perfil.html">Perfil</a></div>
      <div><h4>Mais</h4><a href="tier-list.html">Tier List</a><a href="sobre.html">Sobre</a></div>
    </div>
  </div>
  <p class="footer-note">Conteúdo educativo. Em caso de incidente de segurança, procure os canais oficiais e profissionais especializados.</p>
</footer>'''

CORE_JS = ["assets/supabase-config.js", "assets/js/core.js", "assets/js/auth.js", "assets/js/progress.js", "assets/js/app.js", "assets/js/fx.js"]

def page(fname, title, body, current=None, scripts=(), data=(), css=(), desc="", body_class="", main_class="", head_extra=""):
    d = desc or "CyberLeigos: aprenda cibersegurança sem complicação, com lições, quizzes, minigames e tarefas diárias."
    css_tags = "".join('<link rel="stylesheet" href="%s">' % c for c in ("assets/css/style.css",) + tuple(css))
    needs_sb = True
    js = ['<script src="%s" defer></script>' % SUPABASE_CDN] if needs_sb else []
    srcs = [CORE_JS[0], CORE_JS[1]] + list(data) + CORE_JS[2:] + list(scripts)
    # data scripts precisam do core; auth/progress/app/fx depois; páginas por último
    js += ['<script src="%s" defer></script>' % s for s in srcs]
    t = html.escape(title) + (" | CyberLeigos" if title != "CyberLeigos" else "")
    out = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{head_extra}
<meta name="theme-color" content="#111111">
<meta name="description" content="{html.escape(d)}">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<title>{t}</title>
{css_tags}
</head>
<body class="{body_class}">
{sprite()}
{header(current or fname)}
<main id="conteudo" class="{main_class}">
{body}
</main>
{footer()}
{chr(10).join(js)}
</body>
</html>
'''
    with open(os.path.join(ROOT, fname), "w", encoding="utf-8") as f:
        f.write(out)

LESSONS_DATA = ["assets/js/data/lessons-1.js", "assets/js/data/lessons-2.js"]
QUIZ_DATA = ["assets/js/data/quizzes.js"]
DAILY_DATA = ["assets/js/data/daily.js"]
GAMES_DATA = ["assets/js/data/games.js"]
GLOSS_DATA = ["assets/js/data/glossary.js"]

def container(inner, cls=""):
    return '<div class="container %s">%s</div>' % (cls, inner)

def auth_page(fname, title, inner, scripts):
    body = f'<div class="auth-page"><div class="container" style="display:grid;place-items:center">{inner}</div></div>'
    page(fname, title, body, current=fname, scripts=scripts, data=())

def build():
    # ---------- INÍCIO ----------
    home = f'''
<section class="hero"><div class="container hero-grid">
  <div>
    <p class="eyebrow">Portal educativo de segurança digital</p>
    <h1>Entenda cibersegurança <span>sem complicação.</span></h1>
    <p class="hero-sub">Aprenda a reconhecer golpes, proteger suas contas e navegar com mais segurança. Lições curtas, desafios do dia a dia e minigames, no seu ritmo e do zero.</p>
    <div class="hero-actions">
      <a href="licoes.html" class="btn btn-primary" id="heroStart">{ico("play")} Começar a aprender</a>
      <a href="tarefas.html" class="btn">{ico("target")} Tarefas de hoje</a>
    </div>
  </div>
  <div class="window hero-card">
    <div class="title-bar">{ico("lightbulb", "ico-sm")}<span class="tb-title">Teste rápido: dá para clicar?</span></div>
    <div class="window-body"><div class="mini-lesson" id="miniLesson"></div></div>
  </div>
</div></section>

<section class="section"><div class="container">
  <div class="section-title"><h2>Como funciona</h2></div>
  <ol class="steps-how">
    <li class="reveal"><h3>Aprenda em lições curtas</h3><p>Cada lição leva poucos minutos, usa situações do dia a dia e explica cada termo técnico na hora.</p></li>
    <li class="reveal"><h3>Pratique de verdade</h3><p>Quizzes, tarefas diárias e minigames colocam você na pele de quem precisa decidir.</p></li>
    <li class="reveal"><h3>Ganhe XP e suba de nível</h3><p>Cada atividade concluída vale pontos. Sua sequência de dias mostra o quanto você está evoluindo.</p></li>
    <li class="reveal"><h3>Compare-se no ranking</h3><p>Crie uma conta gratuita para salvar seu progresso e aparecer entre os melhores aprendizes.</p></li>
  </ol>
</div></section>

<section class="section"><div class="container">
  <div class="stat-strip" id="homeStats" aria-label="Seu progresso">
    <div class="stat xp">{ico("star")}<div><b data-cl-xp>0</b><span>pontos de XP</span></div></div>
    <div class="stat">{ico("flame")}<div><b data-cl-streak>0</b><span>dias seguidos</span></div></div>
    <div class="stat">{ico("book")}<div><b data-cl-done>0</b><span>lições concluídas</span></div></div>
    <div class="stat">{ico("target")}<div><b id="homeDaily">0/3</b><span>tarefas de hoje</span></div></div>
  </div>
</div></section>

<section class="section"><div class="container">
  <div class="section-title"><h2>Por onde começar</h2><a href="licoes.html">Ver todas as lições →</a></div>
  <div class="grid grid-3" id="homeLessons"></div>
</div></section>

<section class="section"><div class="container">
  <div class="section-title"><h2>Aprenda jogando</h2><a href="minigames.html">Ver todos os minigames →</a></div>
  <div class="grid grid-3" id="homeGames"></div>
</div></section>

<section class="section"><div class="container">
  <div class="cta-band reveal" id="homeCta">
    <div><h2>Salve seu progresso e entre no ranking</h2><p>Criar uma conta é gratuito. Seus pontos ficam guardados e acompanham você em qualquer aparelho.</p></div>
    <a class="btn" href="cadastro.html">Criar minha conta</a>
  </div>
</div></section>'''
    page("index.html", "CyberLeigos", home, current="index.html", data=LESSONS_DATA + QUIZ_DATA + DAILY_DATA + GAMES_DATA, scripts=["assets/js/pages/home.js"])

    # ---------- LIÇÕES ----------
    page("licoes.html", "Lições", f'''
<div class="container">
  <div class="page-head"><p class="eyebrow">Trilha de aprendizado</p><h1>Lições</h1>
    <p class="lead">21 lições curtas para aprender no seu ritmo. Siga a ordem sugerida ou escolha o assunto que mais interessa agora.</p></div>
  <div class="panel-soft overall" id="overall" style="margin:10px 0 20px"></div>
  <div class="search-box" style="margin-bottom:22px">{ico("search")}<input type="search" id="lessonSearch" placeholder="Buscar assunto (ex.: Pix, senha, Wi-Fi)" aria-label="Buscar lições"></div>
  <div id="lessonUnits"></div>
  <p class="empty hidden" id="noLesson">Nenhuma lição encontrada. Tente outra palavra ou consulte o <a href="glossario.html">glossário</a>.</p>
</div>''', data=LESSONS_DATA, scripts=["assets/js/pages/licoes.js"])

    page("licao.html", "Lição", f'''
<div class="container"><div class="lesson-layout" id="lessonRoot"><p class="muted" style="padding:40px 0">Carregando lição…</p></div></div>''',
         current="licoes.html", data=LESSONS_DATA, scripts=["assets/js/pages/licao.js"])

    # ---------- TAREFAS ----------
    page("tarefas.html", "Tarefas diárias", f'''
<div class="container">
  <div class="page-head"><p class="eyebrow">Hábito diário</p><h1>Tarefas diárias</h1>
    <p class="lead">Três desafios novos por dia. Responda, aprenda com a explicação e ganhe XP. Concluindo as três, você leva um bônus.</p></div>
  <div class="stat-strip" style="margin:14px 0 22px">
    <div class="stat xp">{ico("star")}<div><b data-cl-xp>0</b><span>pontos de XP</span></div></div>
    <div class="stat">{ico("flame")}<div><b data-cl-streak>0</b><span>dias seguidos</span></div></div>
    <div class="stat">{ico("target")}<div><b id="tDone">0/3</b><span>concluídas hoje</span></div></div>
    <div class="stat">{ico("clock")}<div><b id="tTimer">--</b><span>para novas tarefas</span></div></div>
  </div>
  <div class="task-list" id="taskList"></div>
  <div id="taskBonus" style="margin-top:22px"></div>
  <div id="taskGuest" class="panel-soft hidden" style="margin-top:22px"></div>
</div>''', data=DAILY_DATA, scripts=["assets/js/pages/tarefas.js"])

    # ---------- QUIZZES ----------
    page("quizzes.html", "Quizzes", f'''
<div class="container">
  <div class="page-head"><p class="eyebrow">Teste seus conhecimentos</p><h1>Quizzes</h1>
    <p class="lead">Escolha um nível. A cada partida você recebe 8 perguntas sorteadas, com explicação depois de cada resposta.</p></div>
  <div id="quizStage"></div>
</div>''', data=QUIZ_DATA, scripts=["assets/js/pages/quizzes.js"])

    # ---------- MINIGAMES ----------
    page("minigames.html", "Minigames", f'''
<div class="container">
  <div class="page-head"><p class="eyebrow">Aprenda jogando</p><h1>Minigames</h1>
    <p class="lead">Sete experiências interativas para treinar o olhar de segurança em situações parecidas com as reais. Todas as situações são fictícias.</p></div>
  <div class="grid grid-3" id="gameGrid"></div>
</div>''', data=GAMES_DATA, scripts=["assets/js/pages/minigames.js"])

    games = ["phishing", "permissoes", "resposta", "backup", "wifi", "senhas", "links"]
    page("minigame.html", "Minigame", '<div class="container"><div id="gameRoot" class="quiz-wrap" style="max-width:860px"><p class="muted" style="padding:40px 0">Carregando…</p></div></div>',
         current="minigames.html", data=GAMES_DATA, css=["assets/css/games.css"],
         scripts=["assets/js/games/shell.js"] + ["assets/js/games/%s.js" % g for g in games] + ["assets/js/pages/minigame.js"])

    # ---------- PROGRESSO ----------
    page("progresso.html", "Meu progresso", f'''
<div class="container">
  <div class="page-head"><p class="eyebrow">Sua jornada</p><h1>Meu progresso</h1>
    <p class="lead" id="progLead">Acompanhe seus pontos, seu nível, suas conquistas e as lições que já concluiu.</p></div>
  <div id="progGuest" class="panel-soft hidden" style="margin-bottom:20px"></div>
  <div class="grid grid-2" style="align-items:start">
    <div class="panel level-box" id="levelBox"></div>
    <div class="stat-strip" style="grid-template-columns:1fr 1fr" id="progStats"></div>
  </div>
  <div class="section"><div class="section-title"><h2>Conquistas</h2></div><div class="badge-grid" id="badges"></div></div>
  <div class="section"><div class="section-title"><h2>Lições</h2><a href="licoes.html">Abrir trilha →</a></div><div id="progLessons" class="lesson-list"></div></div>
  <div class="section"><div class="section-title"><h2>Quizzes e minigames</h2></div><div class="grid grid-2" id="progOther"></div></div>
</div>''', data=LESSONS_DATA + QUIZ_DATA + GAMES_DATA + DAILY_DATA, scripts=["assets/js/pages/progresso.js"])

    # ---------- RANKING ----------
    page("ranking.html", "Ranking", f'''
<div class="container">
  <div class="page-head"><p class="eyebrow">Comunidade</p><h1>Ranking</h1>
    <p class="lead">Os aprendizes com mais XP no CyberLeigos. Só aparecem nome de exibição, foto e pontos.</p></div>
  <div class="row row-between" style="margin:8px 0 18px"><span class="muted small" id="rkStamp" aria-live="polite"></span><button class="btn btn-sm" id="rkRefresh" type="button">{ico("refresh", "ico-sm")} Atualizar</button></div>
  <div id="rkMe"></div>
  <div id="rkPodium"></div>
  <div class="rk-list" id="rkList" aria-live="polite"></div>
  <div class="center" style="margin-top:18px"><button class="btn hidden" id="rkMore" type="button">Mostrar mais</button></div>
</div>''', scripts=["assets/js/pages/ranking.js"])

    # ---------- PERFIL ----------
    page("perfil.html", "Meu perfil", f'''
<div class="container" id="profileRoot"><p class="muted" style="padding:40px 0">Carregando seu perfil…</p></div>''', scripts=["assets/js/pages/perfil.js"], data=LESSONS_DATA + QUIZ_DATA + DAILY_DATA + GAMES_DATA)

    # ---------- GLOSSÁRIO ----------
    page("glossario.html", "Glossário", f'''
<div class="container">
  <div class="page-head"><p class="eyebrow">Termos em linguagem simples</p><h1>Glossário</h1>
    <p class="lead">Palavras do mundo digital explicadas sem complicação, em ordem alfabética.</p></div>
  <div class="search-box">{ico("search")}<input type="search" id="glSearch" placeholder="Buscar termo (ex.: VPN, phishing)" aria-label="Buscar no glossário"></div>
  <dl class="glossary" id="glossaryList"></dl>
  <p class="empty hidden" id="noGloss">Nenhum termo encontrado. Tente outra palavra.</p>
</div>''', data=GLOSS_DATA + LESSONS_DATA, scripts=["assets/js/pages/glossario.js"])

    # ---------- SOBRE ----------
    page("sobre.html", "Sobre o CyberLeigos", f'''
<div class="container" style="max-width:820px">
  <div class="page-head"><p class="eyebrow">Sobre</p><h1>Cibersegurança para quem não é de tecnologia</h1>
    <p class="lead">O CyberLeigos nasceu de uma ideia simples: proteger-se na internet deveria ser algo que qualquer pessoa consegue aprender.</p></div>
  <div class="section"><div class="window"><div class="title-bar">{ico("flag", "ico-sm")}<h2>Nossa proposta</h2></div><div class="window-body">
    <p>Golpes digitais funcionam porque exploram pressa, medo e confiança, e não porque a pessoa é "burra". Entender como eles funcionam é a melhor defesa.</p>
    <p>Por isso o CyberLeigos ensina com <b>lições curtas</b>, <b>situações do dia a dia</b> e <b>prática</b>. Não é preciso saber nada de tecnologia para começar.</p>
    <h3>Como a plataforma funciona</h3>
    <ul class="check-list">
      <li><b>Lições:</b> 21 temas, de senhas e golpes por mensagem até backups e inteligência artificial.</li>
      <li><b>Tarefas diárias:</b> três desafios novos por dia para criar o hábito.</li>
      <li><b>Quizzes e minigames:</b> treino em situações fictícias, sem risco nenhum.</li>
      <li><b>XP, níveis e ranking:</b> cada atividade concluída vale pontos, uma única vez.</li>
    </ul>
    <h3>Sua conta e seus dados</h3>
    <p>Você pode usar o CyberLeigos sem conta. Nesse caso, seus pontos valem apenas durante a visita. Com uma conta gratuita, seu progresso fica salvo e você aparece no ranking com o <b>nome de exibição</b> e a <b>foto</b> que escolher. Seu e-mail nunca é mostrado a outras pessoas.</p>
    <h3>Importante</h3>
    <p>O conteúdo é educativo e não substitui orientação profissional. Em caso de golpe ou incidente, siga os passos da lição <a href="licao.html?id=incidente">Como agir diante de um incidente</a> e procure os canais oficiais.</p>
    <div class="hero-actions" style="margin-top:18px"><a class="btn btn-primary" href="licoes.html">Começar a aprender</a><a class="btn" href="cadastro.html">Criar conta</a></div>
  </div></div></div>
</div>''')

    # ---------- TIER LIST ----------
    # conteúdo vem de tools/_tierlist_fragments (gerado a partir do site original)
    gen = os.path.join(ROOT, "tools", "_tierlist.html")
    if os.path.exists(gen):
        frag = open(gen, encoding="utf-8").read()
        page("tier-list.html", "Tier List de navegadores", frag, current="tier-list.html", scripts=["assets/js/pages/tierlist.js"])

    # ---------- AUTENTICAÇÃO ----------
    eye = ico("eye")
    google = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#4285F4" d="M23.5 12.3c0-.8-.1-1.6-.2-2.3H12v4.5h6.5a5.6 5.6 0 0 1-2.4 3.7v3h3.9c2.3-2.1 3.5-5.2 3.5-8.9z"/><path fill="#34A853" d="M12 24c3.2 0 6-1.1 8-2.9l-3.9-3c-1.1.7-2.5 1.2-4.1 1.2-3.1 0-5.8-2.1-6.7-5H1.3v3.1A12 12 0 0 0 12 24z"/><path fill="#FBBC05" d="M5.3 14.3a7.2 7.2 0 0 1 0-4.6V6.6H1.3a12 12 0 0 0 0 10.8z"/><path fill="#EA4335" d="M12 4.8c1.8 0 3.3.6 4.6 1.8l3.4-3.4A12 12 0 0 0 1.3 6.6l4 3.1c.9-2.8 3.6-4.9 6.7-4.9z"/></svg>'
    def pw(id_, label, auto, extra=""):
        return f'''<div class="field"><label for="{id_}">{label}</label><div class="input-wrap"><input id="{id_}" name="{id_}" type="password" autocomplete="{auto}" required><button type="button" class="toggle-pw" data-target="{id_}" aria-label="Mostrar senha" aria-pressed="false">{eye}</button></div><div class="field-err" id="{id_}Err" role="alert"></div>{extra}</div>'''
    brand = f'<div class="brand">{ico("flag", "ico-lg")} CyberLeigos</div>'
    login = f'''<div class="auth-card">{brand}<h1>Bem-vindo de volta!</h1><p class="sub">Entre para salvar seu progresso e aparecer no ranking.</p>
<form class="form" id="loginForm" novalidate>
  <div id="formMsg" role="status" aria-live="polite"></div>
  <div class="field"><label for="email">E-mail</label><input id="email" name="email" type="email" autocomplete="email" inputmode="email" required placeholder="voce@exemplo.com"><div class="field-err" id="emailErr" role="alert"></div></div>
  {pw("password", "Senha", "current-password")}
  <div style="text-align:right;margin-top:-6px"><a href="recuperar-senha.html">Esqueci minha senha</a></div>
  <button class="btn btn-primary btn-block" type="submit" id="submitBtn">Entrar</button>
</form>
<div class="sep" style="margin:16px 0">ou</div>
<button class="btn btn-google btn-block" type="button" id="googleBtn">{google} Continuar com Google</button>
<p class="auth-links">Não tem uma conta? <a href="cadastro.html" id="toSignup">Crie uma!</a></p></div>'''
    auth_page("login.html", "Entrar", login, ["assets/js/pages/auth-pages.js"])

    signup = f'''<div class="auth-card">{brand}<h1>Crie sua conta</h1><p class="sub">É gratuito e leva menos de um minuto.</p>
<form class="form" id="signupForm" novalidate>
  <div id="formMsg" role="status" aria-live="polite"></div>
  <div class="field"><label for="name">Nome de exibição</label><input id="name" name="name" type="text" autocomplete="nickname" maxlength="30" required placeholder="Como quer ser chamado"><div class="field-hint">É o nome que aparece no ranking. Não use seu nome completo se preferir.</div><div class="field-err" id="nameErr" role="alert"></div></div>
  <div class="field"><label for="email">E-mail</label><input id="email" name="email" type="email" autocomplete="email" inputmode="email" required placeholder="voce@exemplo.com"><div class="field-err" id="emailErr" role="alert"></div></div>
  {pw("password", "Senha", "new-password", '<ul class="pw-reqs" id="pwReqs"><li data-r="len">Pelo menos 8 caracteres</li><li data-r="let">Uma letra</li><li data-r="num">Um número</li></ul><div class="pw-meter" id="pwMeter" data-s="0"><i></i><i></i><i></i><i></i></div>')}
  {pw("password2", "Confirme a senha", "new-password")}
  <button class="btn btn-primary btn-block" type="submit" id="submitBtn">Criar conta</button>
</form>
<div class="sep" style="margin:16px 0">ou</div>
<button class="btn btn-google btn-block" type="button" id="googleBtn">{google} Cadastrar com Google</button>
<p class="auth-links">Já tem uma conta? <a href="login.html">Entrar</a></p></div>'''
    auth_page("cadastro.html", "Criar conta", signup, ["assets/js/pages/auth-pages.js"])

    rec = f'''<div class="auth-card">{brand}<h1>Recuperar senha</h1><p class="sub">Informe o e-mail da sua conta. Enviaremos um link para você criar uma nova senha.</p>
<form class="form" id="resetForm" novalidate>
  <div id="formMsg" role="status" aria-live="polite"></div>
  <div class="field"><label for="email">E-mail</label><input id="email" name="email" type="email" autocomplete="email" inputmode="email" required placeholder="voce@exemplo.com"><div class="field-err" id="emailErr" role="alert"></div></div>
  <button class="btn btn-primary btn-block" type="submit" id="submitBtn">Enviar link de recuperação</button>
</form>
<p class="auth-links"><a href="login.html">← Voltar ao login</a></p></div>'''
    auth_page("recuperar-senha.html", "Recuperar senha", rec, ["assets/js/pages/auth-pages.js"])

    red = f'''<div class="auth-card">{brand}<h1>Nova senha</h1><p class="sub" id="redSub">Escolha uma nova senha para a sua conta.</p>
<form class="form" id="newPwForm" novalidate>
  <div id="formMsg" role="status" aria-live="polite"></div>
  {pw("password", "Nova senha", "new-password", '<ul class="pw-reqs" id="pwReqs"><li data-r="len">Pelo menos 8 caracteres</li><li data-r="let">Uma letra</li><li data-r="num">Um número</li></ul><div class="pw-meter" id="pwMeter" data-s="0"><i></i><i></i><i></i><i></i></div>')}
  {pw("password2", "Confirme a nova senha", "new-password")}
  <button class="btn btn-primary btn-block" type="submit" id="submitBtn">Salvar nova senha</button>
</form>
<div id="redExpired" class="hidden"><div class="form-msg err" role="alert">Este link expirou, é inválido ou já foi usado.</div><p class="auth-links"><a class="btn btn-primary btn-block" href="recuperar-senha.html">Pedir um novo link</a></p></div>
<p class="auth-links"><a href="login.html">← Voltar ao login</a></p></div>'''
    auth_page("redefinir-senha.html", "Nova senha", red, ["assets/js/pages/auth-pages.js"])

    # ---------- 404 ----------
    nf = f'''<div class="container" style="max-width:680px"><div class="window" style="margin:50px 0"><div class="title-bar">{ico("alert", "ico-sm")}<span class="tb-title">Erro 404</span></div><div class="window-body center">
  <p class="eyebrow">CyberLeigos · Erro 404</p>
  <h1>Essa página não foi encontrada.</h1>
  <p class="muted">O endereço pode ter mudado ou estar digitado errado. Volte ao início para continuar aprendendo.</p>
  <div class="hero-actions" style="justify-content:center"><a class="btn btn-primary" href="index.html">Voltar ao CyberLeigos</a><a class="btn" href="licoes.html">Ver lições</a></div>
</div></div></div>'''
    BASE_JS = '<script>(function(){var p=location.pathname.split("/"),b=location.hostname.slice(-9)==="github.io"?"/"+p[1]+"/":"/";document.write(\'<base href="\'+location.origin+b+\'">\');})();</script>'
    page("404.html", "Página não encontrada", nf, current="", scripts=["assets/js/pages/notfound.js"], head_extra=BASE_JS)

if __name__ == "__main__":
    build(); print("páginas geradas")
