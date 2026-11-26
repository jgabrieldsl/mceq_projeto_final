#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera a apresentação HTML com design editorial suíço/acadêmico (ACM / Nature / Keynote clean),
sem clichês visuais de IA, com muito respiro visual (9 slides bem distribuídos)
e um painel retrátil de Notas de Fala (tecla N) para ter 100% do conteúdo sem poluir a tela.
"""

import os
import base64
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FIG_PATH = os.path.join(BASE_DIR, "figuras", "figura1_resultados.png")
OUT_HTML = os.path.join(BASE_DIR, "apresentacao_MCEQ.html")
DOWNLOADS_HTML = "/Users/joao.leite/Downloads/apresentacao_MCEQ.html"

with open(FIG_PATH, "rb") as f:
    FIG_B64 = base64.b64encode(f.read()).decode("utf-8")

HTML_CONTENT = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Notificações Push e Abertura Diária de App — MCEQ 12576</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-paper: #FAF9F5;
      --bg-surface: #FFFFFF;
      --bg-subtle: #F2EFE9;
      --ink-900: #111315;
      --ink-700: #373A40;
      --ink-500: #686D76;
      --ink-300: #D8D5CE;
      --accent: #0B4F6C;
      --accent-soft: #E6F0F5;
      --accent-warm: #B84A14;
      --font-serif: 'Newsreader', Georgia, 'Times New Roman', serif;
      --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-mono: 'IBM Plex Mono', Menlo, monospace;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      background: var(--bg-paper);
      color: var(--ink-900);
      font-family: var(--font-sans);
      height: 100vh;
      width: 100vw;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      -webkit-font-smoothing: antialiased;
    }}

    /* Minimal Editorial Top Header */
    .header {{
      height: 60px;
      padding: 0 56px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid var(--ink-300);
      font-size: 0.8rem;
      color: var(--ink-500);
      flex-shrink: 0;
    }}

    .header-left {{
      display: flex;
      align-items: center;
      gap: 16px;
      font-family: var(--font-mono);
      letter-spacing: 0.02em;
    }}

    .header-divider {{
      color: var(--ink-300);
    }}

    .speaker-indicator {{
      font-family: var(--font-mono);
      font-size: 0.78rem;
      color: var(--ink-700);
      background: var(--bg-subtle);
      padding: 6px 14px;
      border-radius: 4px;
      border: 1px solid var(--ink-300);
    }}

    .speaker-indicator strong {{
      color: var(--accent);
      font-weight: 600;
    }}

    /* Viewport */
    .stage {{
      flex: 1;
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 36px 72px;
      overflow: hidden;
    }}

    .slide {{
      position: absolute;
      width: 100%;
      max-width: 1180px;
      height: calc(100% - 72px);
      display: flex;
      flex-direction: column;
      justify-content: center;
      opacity: 0;
      pointer-events: none;
      transform: translateY(10px);
      transition: opacity 0.28s ease, transform 0.28s ease;
    }}

    .slide.active {{
      opacity: 1;
      pointer-events: auto;
      transform: translateY(0);
    }}

    /* Editorial Typography */
    .section-tag {{
      font-family: var(--font-mono);
      font-size: 0.76rem;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: var(--accent);
      margin-bottom: 16px;
      font-weight: 600;
    }}

    h1.hero-title {{
      font-family: var(--font-serif);
      font-size: 3.1rem;
      font-weight: 500;
      line-height: 1.14;
      color: var(--ink-900);
      letter-spacing: -0.02em;
      max-width: 980px;
      margin-bottom: 24px;
    }}

    h2.slide-heading {{
      font-family: var(--font-serif);
      font-size: 2.35rem;
      font-weight: 500;
      line-height: 1.18;
      color: var(--ink-900);
      letter-spacing: -0.015em;
      margin-bottom: 16px;
      max-width: 920px;
    }}

    p.lead {{
      font-size: 1.12rem;
      line-height: 1.6;
      color: var(--ink-700);
      max-width: 820px;
      margin-bottom: 36px;
      font-weight: 400;
    }}

    /* Clean Grids & Dividers */
    .cols-2 {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 48px;
      align-items: start;
    }}

    .cols-3 {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 36px;
      align-items: start;
    }}

    .cols-4 {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 28px;
      align-items: start;
    }}

    .panel {{
      background: var(--bg-surface);
      border: 1px solid var(--ink-300);
      padding: 28px 30px;
      border-radius: 4px;
    }}

    .panel-accent {{
      background: var(--bg-surface);
      border: 1px solid var(--ink-300);
      border-top: 3px solid var(--accent);
      padding: 28px 30px;
      border-radius: 2px;
    }}

    .panel-label {{
      font-family: var(--font-mono);
      font-size: 0.73rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--ink-500);
      margin-bottom: 10px;
      display: block;
    }}

    .panel-title {{
      font-family: var(--font-serif);
      font-size: 1.35rem;
      font-weight: 500;
      color: var(--ink-900);
      margin-bottom: 12px;
      line-height: 1.3;
    }}

    .panel p {{
      font-size: 0.96rem;
      line-height: 1.62;
      color: var(--ink-700);
    }}

    /* Big Editorial Numbers */
    .metric-row {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      border-top: 1px solid var(--ink-900);
      border-bottom: 1px solid var(--ink-300);
      padding: 24px 0;
      gap: 32px;
    }}

    .metric-item {{
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}

    .metric-value {{
      font-family: var(--font-serif);
      font-size: 2.75rem;
      font-weight: 500;
      color: var(--ink-900);
      line-height: 1;
    }}

    .metric-value.highlight {{
      color: var(--accent);
    }}

    .metric-caption {{
      font-size: 0.85rem;
      color: var(--ink-500);
      line-height: 1.4;
    }}

    /* Booktabs Academic Table */
    table.booktabs {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.95rem;
      background: var(--bg-surface);
    }}

    table.booktabs thead th {{
      border-top: 2px solid var(--ink-900);
      border-bottom: 1px solid var(--ink-900);
      padding: 12px 14px;
      text-align: left;
      font-family: var(--font-sans);
      font-weight: 600;
      font-size: 0.84rem;
      color: var(--ink-900);
    }}

    table.booktabs tbody td {{
      padding: 13px 14px;
      border-bottom: 1px solid var(--ink-300);
      color: var(--ink-700);
    }}

    table.booktabs tbody tr:last-child td {{
      border-top: 1px solid var(--ink-900);
      border-bottom: 2px solid var(--ink-900);
      font-weight: 600;
      color: var(--ink-900);
      background: var(--bg-subtle);
    }}

    .mono-num {{
      font-family: var(--font-mono);
      text-align: right !important;
      font-size: 0.9rem;
    }}

    /* Clean Lists */
    ul.editorial-list {{
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }}

    ul.editorial-list li {{
      font-size: 0.96rem;
      line-height: 1.58;
      color: var(--ink-700);
      padding-left: 18px;
      position: relative;
    }}

    ul.editorial-list li::before {{
      content: "—";
      position: absolute;
      left: 0;
      color: var(--accent);
      font-weight: 600;
    }}

    /* Math / Hypothesis Block */
    .math-block {{
      background: var(--bg-subtle);
      border-left: 3px solid var(--ink-900);
      padding: 20px 24px;
      font-family: var(--font-serif);
      font-size: 1.22rem;
      color: var(--ink-900);
      line-height: 1.65;
      margin-top: 12px;
    }}

    /* Author Roster on Cover */
    .authors-strip {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 32px;
      padding-top: 28px;
      border-top: 1px solid var(--ink-900);
      margin-top: 12px;
    }}

    .author-box h3 {{
      font-size: 1.05rem;
      font-weight: 600;
      color: var(--ink-900);
      margin-bottom: 4px;
    }}

    .author-box p {{
      font-family: var(--font-mono);
      font-size: 0.78rem;
      color: var(--ink-500);
      line-height: 1.5;
    }}

    .author-role {{
      display: inline-block;
      margin-top: 8px;
      font-size: 0.8rem;
      color: var(--accent);
      font-weight: 500;
    }}

    /* Collapsible Speaker Notes Drawer (100% content without cluttering the slide) */
    .notes-drawer {{
      position: fixed;
      bottom: 54px;
      left: 0;
      right: 0;
      background: #16191D;
      color: #EAECEF;
      padding: 20px 72px;
      border-top: 2px solid var(--accent);
      transform: translateY(100%);
      transition: transform 0.25s ease;
      z-index: 30;
      box-shadow: 0 -10px 30px rgba(0,0,0,0.18);
    }}

    .notes-drawer.open {{
      transform: translateY(0);
    }}

    .notes-header {{
      font-family: var(--font-mono);
      font-size: 0.74rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: #7CC4E8;
      margin-bottom: 8px;
      display: flex;
      justify-content: space-between;
    }}

    .notes-body {{
      font-size: 0.94rem;
      line-height: 1.6;
      color: #D8DEE9;
      max-width: 1120px;
    }}

    /* Footer Navigation */
    .footer {{
      height: 54px;
      padding: 0 56px;
      border-top: 1px solid var(--ink-300);
      background: var(--bg-paper);
      display: flex;
      align-items: center;
      justify-content: space-between;
      z-index: 40;
      flex-shrink: 0;
    }}

    .footer-steps {{
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .step-btn {{
      border: none;
      background: transparent;
      font-family: var(--font-mono);
      font-size: 0.76rem;
      color: var(--ink-500);
      padding: 5px 10px;
      cursor: pointer;
      border-radius: 3px;
      transition: all 0.15s ease;
    }}

    .step-btn:hover {{
      color: var(--ink-900);
      background: var(--bg-subtle);
    }}

    .step-btn.active {{
      color: var(--bg-surface);
      background: var(--ink-900);
      font-weight: 600;
    }}

    .footer-actions {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .ctrl-btn {{
      background: var(--bg-surface);
      border: 1px solid var(--ink-300);
      color: var(--ink-900);
      font-family: var(--font-sans);
      font-size: 0.8rem;
      font-weight: 500;
      padding: 6px 13px;
      border-radius: 3px;
      cursor: pointer;
      transition: all 0.15s ease;
    }}

    .ctrl-btn:hover {{
      border-color: var(--ink-900);
    }}

    .ctrl-btn.active-toggle {{
      background: var(--ink-900);
      color: var(--bg-surface);
      border-color: var(--ink-900);
    }}
  </style>
</head>
<body>

  <!-- Top Editorial Bar -->
  <header class="header">
    <div class="header-left">
      <span>PUC-CAMPINAS • ENGENHARIA DE SOFTWARE</span>
      <span class="header-divider">/</span>
      <span>12576 — MCEQ (2026/2)</span>
    </div>
    <div class="speaker-indicator" id="speaker-pill">
      Apresentação: <strong>João Gabriel</strong> (0:00 – 1:15)
    </div>
  </header>

  <!-- Main Slide Stage -->
  <main class="stage">

    <!-- SLIDE 1: CAPA -->
    <section class="slide active"
      data-speaker="João Gabriel da Silva Leite • Abertura (0:00 – 1:00)"
      data-notes="Fala (João Gabriel): Olá professores. Nosso estudo avalia empiricamente a associação entre o regime diário de entrega de notificações push e a frequência de aberturas do aplicativo no mesmo dia, utilizando um desenho em blocos pareados por usuário (n = 194 blocos) a partir de 42.504 janelas monitoradas via Screen Time API no projeto longitudinal FUTURE.">
      <div class="section-tag">Relatório Final no Template ACM • Estudo Observacional Longitudinal</div>
      <h1 class="hero-title">
        Envio de Notificações Push e Frequência Diária de Abertura de Aplicativo Móvel
      </h1>
      <p class="lead">
        Análise empírica em blocos pareados por usuário (<i>n</i> = 194 usuários; 7.503 usuários-dia ativos) a partir do pacote público de replicação do projeto <i>FUTURE</i> depositado na Open Science Framework (OSF).
      </p>

      <div class="authors-strip">
        <div class="author-box">
          <h3>João Gabriel da Silva Leite</h3>
          <p>RA 24787392 • joao.gsl@puccampinas.edu.br</p>
          <span class="author-role">Parte 1 — Problema, Hipóteses e Base OSF</span>
        </div>
        <div class="author-box">
          <h3>Yuri Cardoso Balieiro</h3>
          <p>RA 24011525 • yuri.cb@puccampinas.edu.br</p>
          <span class="author-role">Parte 2 — Desenho em Blocos e Resultados</span>
        </div>
        <div class="author-box">
          <h3>Pedro de Mello Porto Daou</h3>
          <p>RA 21010698 • pedro.mpd@puccampinas.edu.br</p>
          <span class="author-role">Parte 3 — Exploratórias, Validade e Conclusão</span>
        </div>
      </div>
    </section>

    <!-- SLIDE 2: PROBLEMA E ADAPTAÇÃO DA FICHA (SEÇÃO 3.3) -->
    <section class="slide"
      data-speaker="João Gabriel da Silva Leite • Bloco 1: Problema e Adaptação (1:00 – 1:50)"
      data-notes="Fala (João Gabriel): Na revisão da Semana 5 (Wohllebe 2020; Philip 2024; Mehrotra & Musolesi 2020), vimos que notificações push são o principal gatilho externo de engajamento, mas sofrem com falhas de entrega e fadiga. Na Ficha de Hipótese da Semana 4, nosso foco era notificação de PIX recebido. Como logs bancários são protegidos por sigilo, aplicamos a regra da Seção 3.3 do roteiro: mantivemos o problema (entrega de push) e a mesma variável resposta (aberturas do aplicativo no mesmo dia), adaptando os níveis da variável independente para os regimes reais medidos na base pública.">
      <div class="section-tag">01 / Contexto e Adaptação da Ficha de Hipótese (Seção 3.3)</div>
      <h2 class="slide-heading">Do Problema em Engenharia de Software à Base Pública</h2>
      <p class="lead">
        Arquiteturas móveis dependem de serviços de mensageria assíncrona (FCM / APNs) para sustentar a retenção diária sem provocar fadiga ou revogação de permissões pelo usuário.
      </p>

      <div class="cols-2">
        <div class="panel">
          <span class="panel-label">Literatura Base (Revisão da Semana 5)</span>
          <h3 class="panel-title">O Dilema de Disparo de Push</h3>
          <ul class="editorial-list">
            <li><b>Wohllebe (2020) e Philip &amp; Hidayaturrahman (2024):</b> Notificações oportunas elevam o retorno ao aplicativo, mas o excesso gera rejeição.</li>
            <li><b>Mehrotra &amp; Musolesi (2020):</b> O efeito do alerta depende da efetiva entrega pelo sistema operacional e do contexto imediato de uso do smartphone.</li>
          </ul>
        </div>

        <div class="panel-accent">
          <span class="panel-label">Adaptação Declarada no Protocolo (Seção 3.3)</span>
          <h3 class="panel-title">O que mudou em relação à Semana 4?</h3>
          <ul class="editorial-list">
            <li><b>Ficha Original (Semana 4):</b> Avaliava notificações <i>push</i> de PIX recebido (dados bancários privados sem base pública).</li>
            <li><b>O que foi preservado:</b> O mecanismo de software (entrega de notificação <i>push</i>) e a métrica de resposta (<b>aberturas do app no mesmo dia</b>).</li>
            <li><b>Ajuste na VI:</b> Comparação entre dias ativos sob <b>Notificação Completa (4 pushes/dia)</b> versus <b>Notificação Parcial (1 a 3 pushes/dia)</b>.</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- SLIDE 3: PERGUNTA DE PESQUISA E HIPÓTESES -->
    <section class="slide"
      data-speaker="João Gabriel da Silva Leite • Bloco 1: Pergunta e Hipóteses (1:50 – 2:45)"
      data-notes="Fala (João Gabriel): Nossa pergunta de pesquisa compara a frequência diária de abertura do app entre os dois regimes de push, blocando no próprio usuário. Fixamos alfa = 0,05 antes da análise. Como a literatura prevê direção positiva (mais pushes entregues geram mais acionamentos no dia), formulamos uma hipótese alternativa unilateral à direita: mu_d > 0.">
      <div class="section-tag">02 / Protocolo Confirmatório (Seção 4)</div>
      <h2 class="slide-heading">Pergunta de Pesquisa e Hipóteses Estatísticas</h2>

      <div class="cols-2" style="margin-top: 12px;">
        <div class="panel">
          <span class="panel-label">Pergunta de Pesquisa (Modelo GQM)</span>
          <h3 class="panel-title" style="font-size: 1.45rem; line-height: 1.42;">
            “Em usuários de um aplicativo móvel com coleta longitudinal, dias sob regime de Notificação Completa (4 pushes/dia) apresentam maior número médio de aberturas do aplicativo no mesmo dia do que dias sob Notificação Parcial (1 a 3 pushes/dia)?”
          </h3>
          <p style="margin-top: 16px;">
            <b>Tipo de Estudo:</b> Observacional longitudinal (sem atribuição aleatória por sorteio; analisa-se associação empírica, não causalidade direta).
          </p>
        </div>

        <div>
          <span class="panel-label">Formulação Paramétrica Pareada (α = 0,05 fixado a priori)</span>
          <div class="math-block">
            Seja <i>d<sub>i</sub> = Y<sub>i,Completa</sub> − Y<sub>i,Parcial</sub></i> a diferença média intrapares no usuário <i>i</i>:<br><br>
            <b>H<sub>0</sub> :</b> μ<sub>d</sub> ≤ 0 &nbsp;&nbsp;(μ<sub>Completa</sub> ≤ μ<sub>Parcial</sub>)<br>
            <b>H<sub>1</sub> :</b> μ<sub>d</sub> &gt; 0 &nbsp;&nbsp;(μ<sub>Completa</sub> &gt; μ<sub>Parcial</sub>)
          </div>
          <div class="panel" style="margin-top: 18px; padding: 18px 22px;">
            <p>
              <b>Por que unilateral à direita (Aula 02)?</b> As três revisões sistemáticas da Semana 5 indicam direção específica positiva do estímulo <i>push</i> sobre o acionamento imediato do aplicativo.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- SLIDE 4: BASE PÚBLICA OSF E PIPELINE DE LIMPEZA -->
    <section class="slide"
      data-speaker="Yuri Cardoso Balieiro • Bloco 2: Base Pública e Limpeza (2:45 – 3:45)"
      data-notes="Fala (Yuri): Utilizamos o pacote de replicação do projeto FUTURE (Dvořák, Kreidl & Tancoš, 2026), depositado no OSF (osf.io/n4sgb). Diferente de questionários subjetivos, a base coletou telemetria real via Screen Time API do sistema operacional em 42.504 janelas de 201 usuários. No script analise.py, removemos 3 janelas com erro de instrumentação (-666), agregamos por usuário-dia e filtramos os 7.503 dias ativos com ao menos 1 push entregue.">
      <div class="section-tag">03 / Proveniência e Limpeza Reprodutível (Seção 3.1 e 3.3)</div>
      <h2 class="slide-heading">Base Pública (OSF) e Pipeline de Limpeza</h2>
      <p class="lead">
        Pacote de replicação de Dvořák, Kreidl &amp; Tancoš (2026) — <code>https://osf.io/n4sgb/</code> — instrumentado diretamente via API de Tempo de Uso do sistema operacional (<i>Screen Time API</i>).
      </p>

      <div class="metric-row" style="margin-bottom: 28px;">
        <div class="metric-item">
          <span class="metric-value">42.504</span>
          <span class="metric-caption">Janelas brutas no arquivo <code>notif_data_final.dta</code> (201 usuários)</span>
        </div>
        <div class="metric-item">
          <span class="metric-value">−3</span>
          <span class="metric-caption">Registros excluídos com código de erro técnico <code>-666</code> (42.501 válidas)</span>
        </div>
        <div class="metric-item">
          <span class="metric-value">7.503</span>
          <span class="metric-caption">Usuários-dia ativos (5.168 com 4 pushes; 2.335 com 1–3 pushes)</span>
        </div>
        <div class="metric-item">
          <span class="metric-value highlight">n = 194</span>
          <span class="metric-caption">Blocos completos (usuários avaliados sob ambos os regimes)</span>
        </div>
      </div>

      <div class="cols-2">
        <div class="panel" style="padding: 20px 24px;">
          <span class="panel-label">Variável Independente (Fator em 2 Níveis)</span>
          <p><b>Regime de Entrega Diária de Push:</b> Categorizado em <i>Notificação Completa</i> (4 pushes/dia entregues nas 4 janelas programadas) vs. <i>Notificação Parcial</i> (1 a 3 pushes/dia devido a restrições de rede/OS).</p>
        </div>
        <div class="panel" style="padding: 20px 24px;">
          <span class="panel-label">Variável Dependente (Resposta Quantitativa)</span>
          <p><b>Aberturas do Aplicativo no Mesmo Dia (<code>aberturas/dia</code>):</b> Soma diária de interações iniciadas (<code>opened == 1</code>, de 0 a 4 aberturas/dia), agregada pela média intrapessoal de cada regime.</p>
        </div>
      </div>
    </section>

    <!-- SLIDE 5: DESENHO EM BLOCOS E ESCOLHA DO TESTE -->
    <section class="slide"
      data-speaker="Yuri Cardoso Balieiro • Bloco 2: Desenho em Blocos e Escolha do Teste (3:45 – 4:35)"
      data-notes="Fala (Yuri): Por que escolhemos um desenho em blocos pareados por usuário (Aula 06)? Porque pessoas diferentes possuem hábitos muito distintos de uso do smartphone. Ao tratar cada usuário como seu próprio bloco (comparando os dias de 4 pushes contra os dias de 1 a 3 pushes da mesma pessoa), eliminamos a variabilidade entre indivíduos. Além disso, evitamos a pseudorreplicação de tratar 7.503 dias como independentes. O teste de Shapiro-Wilk nas 194 diferenças pareadas deu W = 0,9921 e p = 0,3775 (> 0,05), confirmando normalidade e validando o teste t pareado.">
      <div class="section-tag">04 / Desenho Experimental e Pressupostos (Seção 3.4)</div>
      <h2 class="slide-heading">Por que Blocos Pareados e Teste <i>t</i> Pareado?</h2>

      <div class="cols-3" style="margin-top: 20px;">
        <div class="panel-accent">
          <span class="panel-label">1. Controle de Variabilidade (Aula 06)</span>
          <h3 class="panel-title">O Usuário como Bloco</h3>
          <p>
            Usuários diferem drasticamente no hábito basal de checar o celular. O pareamento intrapessoal (<i>d<sub>i</sub> = Y<sub>i,Completa</sub> − Y<sub>i,Parcial</sub></i>) isola a diferença entre regimes do ruído entre sujeitos.
          </p>
        </div>

        <div class="panel-accent">
          <span class="panel-label">2. Independência das Unidades</span>
          <h3 class="panel-title">Sem Pseudorreplicação</h3>
          <p>
            Tratar 7.503 dias como independentes inflaria artificialmente os graus de liberdade. Agregar uma média por regime para cada um dos <b><i>n</i> = 194 usuários</b> garante independência entre blocos.
          </p>
        </div>

        <div class="panel-accent">
          <span class="panel-label">3. Verificação de Pressupostos</span>
          <h3 class="panel-title">Normalidade Atendida</h3>
          <p>
            O teste de <b>Shapiro-Wilk</b> sobre o vetor de diferenças <i>d<sub>i</sub></i> resultou em <b><i>W</i> = 0,9921 (<i>p</i> = 0,3775 &gt; 0,05)</b>, com assimetria <i>g<sub>1</sub></i> = −0,10, validando o <b>teste <i>t</i> pareado</b>.
          </p>
        </div>
      </div>

      <div class="panel" style="margin-top: 24px; padding: 18px 24px; display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 0.92rem; color: var(--ink-700);">
          <b>Testes Alternativos Não Paramétricos (previstos a priori no Protocolo):</b> Teste dos postos sinalizados de Wilcoxon pareado e Teste de Permutação Pareada (10.000 reamostragens com semente fixa <code>default_rng(2026)</code>).
        </span>
      </div>
    </section>

    <!-- SLIDE 6: RESULTADOS CONFIRMATÓRIOS (TABELA 1 + INFERÊNCIA) -->
    <section class="slide"
      data-speaker="Yuri Cardoso Balieiro • Bloco 3: Resultados Confirmatórios (4:35 – 5:15)"
      data-notes="Fala (Yuri): Na Tabela 1 vemos que a média de aberturas no mesmo dia subiu de 1,56 aberturas/dia no regime Parcial para 2,67 aberturas/dia no regime Completo — uma diferença média pareada de +1,11 aberturas/dia (+71,2% de aumento relativo). O teste t pareado unilateral resultou em t = 24,44 (gl = 193, p = 2,80e-61 < 0,05), rejeitando H0. O intervalo de confiança de 95% vai de 1,02 a 1,20 aberturas/dia e o tamanho de efeito de Cohen é dz = 1,75 (muito grande).">
      <div class="section-tag">05 / Resultados Confirmatórios (Seção 4.1)</div>
      <h2 class="slide-heading">Estatística Descritiva e Teste de Hipótese Principal</h2>

      <table class="booktabs" style="margin-top: 12px; margin-bottom: 28px;">
        <thead>
          <tr>
            <th>Regime / Variável (Unidade: aberturas/dia)</th>
            <th class="mono-num">n</th>
            <th class="mono-num">Média</th>
            <th class="mono-num">DP</th>
            <th class="mono-num">Mediana</th>
            <th class="mono-num">IQR (Q1–Q3)</th>
            <th class="mono-num">CV (%)</th>
            <th class="mono-num">Outliers</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Notificação Completa (4 pushes/dia)</td>
            <td class="mono-num">194</td>
            <td class="mono-num">2,67</td>
            <td class="mono-num">0,95</td>
            <td class="mono-num">2,95</td>
            <td class="mono-num">1,43 (1,97–3,40)</td>
            <td class="mono-num">35,6%</td>
            <td class="mono-num">0</td>
          </tr>
          <tr>
            <td>Notificação Parcial (1 a 3 pushes/dia)</td>
            <td class="mono-num">194</td>
            <td class="mono-num">1,56</td>
            <td class="mono-num">0,69</td>
            <td class="mono-num">1,54</td>
            <td class="mono-num">0,91 (1,09–2,00)</td>
            <td class="mono-num">44,5%</td>
            <td class="mono-num">0</td>
          </tr>
          <tr>
            <td>Diferença Pareada (d<sub>i</sub> = Completa − Parcial)</td>
            <td class="mono-num">194</td>
            <td class="mono-num">+1,11</td>
            <td class="mono-num">0,63</td>
            <td class="mono-num">+1,15</td>
            <td class="mono-num">0,77 (0,73–1,50)</td>
            <td class="mono-num">57,0%</td>
            <td class="mono-num">3</td>
          </tr>
        </tbody>
      </table>

      <div class="cols-4">
        <div class="panel" style="padding: 18px 20px;">
          <span class="panel-label">Teste t Pareado (gl = 193)</span>
          <div class="metric-value highlight" style="font-size: 2.1rem;">t = 24,44</div>
          <p style="font-size: 0.82rem; margin-top: 6px;"><i>p</i> = 2,80 × 10<sup>−61</sup> &lt; 0,05<br>Decisão: <b>Rejeita H<sub>0</sub></b></p>
        </div>
        <div class="panel" style="padding: 18px 20px;">
          <span class="panel-label">Intervalo de Confiança 95%</span>
          <div class="metric-value" style="font-size: 2.1rem;">[1,02; 1,20]</div>
          <p style="font-size: 0.82rem; margin-top: 6px;">aberturas/dia adicionais<br>(Erro padrão = 0,0455)</p>
        </div>
        <div class="panel" style="padding: 18px 20px;">
          <span class="panel-label">Tamanho de Efeito (Cohen)</span>
          <div class="metric-value highlight" style="font-size: 2.1rem;">d<sub>z</sub> = 1,75</div>
          <p style="font-size: 0.82rem; margin-top: 6px;">Magnitude muito grande<br>(+71,2% de ganho relativo)</p>
        </div>
        <div class="panel" style="padding: 18px 20px;">
          <span class="panel-label">Robustez Não Paramétrica</span>
          <div class="metric-value" style="font-size: 2.1rem;">r<sub>rb</sub> = 0,981</div>
          <p style="font-size: 0.82rem; margin-top: 6px;">Wilcoxon <i>p</i> = 1,14 × 10<sup>−32</sup><br>Permutação <i>p</i> &lt; 0,0001</p>
        </div>
      </div>
    </section>

    <!-- SLIDE 7: VISUALIZAÇÃO DE DADOS (FIGURA 1) -->
    <section class="slide"
      data-speaker="Yuri Cardoso Balieiro • Bloco 3: Figura 1 e Interpretação Visual (5:15 – 5:45)"
      data-notes="Fala (Yuri): Seguindo os princípios de qualidade gráfica de Cleveland (1994) e da Aula 04, construímos a Figura 1 com ambos os eixos verticais iniciando estritamente em zero. No painel (a), o boxplot com os 194 usuários mostra o deslocamento consistente de toda a distribuição. No painel (b), o histograma das diferenças pareadas d_i mostra que 189 dos 194 usuários (97,4%) tiveram diferença estritamente positiva, com o IC 95% [1,02; 1,20] muito distante da linha tracejada de H0 (zero).">
      <div class="section-tag">06 / Visualização de Dados (Cleveland, 1994)</div>
      <div class="cols-2" style="grid-template-columns: 0.95fr 1.05fr; align-items: center; gap: 44px;">
        <div>
          <h2 class="slide-heading" style="font-size: 2.1rem;">Leitura Visual da Distribuição e da Incerteza</h2>
          <ul class="editorial-list" style="margin-top: 20px;">
            <li><b>Eixos iniciando estritamente em zero (0):</b> Preserva a proporcionalidade visual das magnitudes e frequências sem distorção.</li>
            <li><b>Painel (a) — Deslocamento Global:</b> A mediana sobe de 1,54 para 2,95 aberturas/dia, acompanhada da dispersão individual dos 194 blocos.</li>
            <li><b>Painel (b) — Consistência Intrapessoal:</b> <b>97,4% dos usuários (189 de 194)</b> apresentaram diferença <i>d<sub>i</sub> &gt; 0</i>.</li>
            <li><b>Precisão da Estimativa:</b> A faixa sombreada do IC 95% (<code>[1,02; 1,20]</code>) situa-se inteiramente à direita da linha de referência <i>H<sub>0</sub> : μ<sub>d</sub> = 0</i>.</li>
          </ul>
        </div>

        <div style="background: #FFFFFF; border: 1px solid var(--ink-300); padding: 16px; border-radius: 4px; display: flex; justify-content: center;">
          <img src="data:image/png;base64,{FIG_B64}" alt="Figura 1 do Artigo" style="max-height: 470px; width: auto; object-fit: contain;" />
        </div>
      </div>
    </section>

    <!-- SLIDE 8: ANÁLISES EXPLORATÓRIAS E AMEAÇAS À VALIDADE -->
    <section class="slide"
      data-speaker="Pedro de Mello Porto Daou • Bloco 4: Exploratórias e Ameaças à Validade (5:45 – 7:30)"
      data-notes="Fala (Pedro): Seguindo a Seção 9 de integridade científica, separamos tudo que não estava no protocolo na subseção 4.2 Análises Exploratórias. Destaco o efeito do estado da tela (screen_on): quando o smartphone estava com a tela ligada no minuto anterior ao push, a taxa de abertura foi de 76,9% contra 61,2% com a tela desligada (+15,7 pontos percentuais, dz = 0,95). Na Seção 5, avaliamos as 4 ameaças à validade de Wohlin et al. (2012): Conclusão, Interna (a principal, por ser estudo observacional sem sorteio), Construção e Externa.">
      <div class="section-tag">07 / Honestidade Científica (Seção 4.2) e Ameaças à Validade (Seção 5)</div>
      <h2 class="slide-heading">Análises Exploratórias e Limites Metodológicos</h2>

      <div class="cols-2" style="margin-top: 12px;">
        <div class="panel">
          <span class="panel-label">Seção 4.2 — Análises Exploratórias (Fora do Protocolo)</span>
          <h3 class="panel-title">Fatores Moderadores de Contexto</h3>
          <ul class="editorial-list">
            <li><b>1. Estado da Tela no Disparo (<code>screen_on</code>, <i>n</i> = 198):</b> Taxa de abertura salta de <b>61,2%</b> (tela desligada) para <b>76,9%</b> com tela ligada no minuto anterior ao <i>push</i> (<b>+15,7 p.p.</b>; <i>t</i> = 13,39; <i>p</i> = 8,41 × 10<sup>−30</sup>; <i>d<sub>z</sub></i> = 0,95).</li>
            <li><b>2. Dia Útil vs. Fim de Semana (em dias de 4 pushes, <i>n</i> = 190):</b> Maior média em dias úteis (<b>2,72 ± 0,98</b>) do que em fins de semana (<b>2,45 ± 1,06</b> aberturas/dia; <i>t</i> = 6,28; <i>p</i> = 1,11 × 10<sup>−9</sup>; <i>d<sub>z</sub></i> = 0,46).</li>
            <li><b>3. Nível Usuário-Dia Não Pareado (<i>n<sub>1</sub></i> = 5.168 vs. <i>n<sub>2</sub></i> = 2.335):</b> Welch <i>t</i> = 40,17 (<i>p</i> &lt; 0,0001; IC 95% <code>[1,09; 1,20]</code>; <i>d</i> = 0,90; Vargha-Delaney <i>A</i> = 0,75).</li>
          </ul>
        </div>

        <div class="panel-accent">
          <span class="panel-label">Seção 5 — Os 4 Tipos de Validade (Wohlin et al., 2012)</span>
          <h3 class="panel-title">Ameaças e Mitigações Adotadas</h3>
          <ul class="editorial-list">
            <li><b>Interna (Central):</b> Estudo <i>observacional</i> (sem sorteio); entrega parcial pode correlacionar com bateria baixa ou modo offline. <i>Mitigação:</i> blocagem no usuário e linguagem estritamente associativa.</li>
            <li><b>Conclusão:</b> Risco de pseudorreplicação longitudinal. <i>Mitigação:</i> agregação em <i>n</i> = 194 blocos + Wilcoxon e permutação (semente <code>2026</code>).</li>
            <li><b>Construção:</b> <code>opened</code> mede abertura técnica, não profundidade cognitiva. <i>Mitigação:</i> telemetria objetiva via <i>Screen Time API</i>.</li>
            <li><b>Externa:</b> Coorte europeia em app EMA. <i>Mitigação:</i> não generalizar diretamente para apps bancários (PIX) sem replicação.</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- SLIDE 9: CONCLUSÃO, TESTE A/B E REPRODUTIBILIDADE -->
    <section class="slide"
      data-speaker="Pedro de Mello Porto Daou • Bloco 5: Conclusão e Reprodutibilidade (7:30 – 8:30)"
      data-notes="Fala (Pedro): Em conclusão, respondemos à pergunta de pesquisa demonstrando que a entrega completa de 4 notificações/dia está associada a +1,11 aberturas/dia (IC 95% [1,02; 1,20], dz = 1,75). Para a Engenharia de Software, isso indica que serviços de push devem priorizar confiabilidade de entrega e algoritmos context-aware que detectem quando a tela está ativa. O próximo passo para estabelecer causalidade no contexto de alertas PIX é um experimento controlado aleatorizado (Teste A/B). Todo o código e dados estão públicos no nosso GitHub.">
      <div class="section-tag">08 / Conclusão, Próximos Passos e Reprodutibilidade (Seções 6 e 8)</div>
      <h2 class="slide-heading">Síntese para Engenharia de Software e Pacote Aberto</h2>

      <div class="cols-3" style="margin-top: 20px;">
        <div class="panel-accent">
          <span class="panel-label">Resposta à Pergunta</span>
          <h3 class="panel-title">Associação Forte e Consistente</h3>
          <p>
            A entrega completa das 4 notificações <i>push</i> diárias está associada a um ganho médio pareado de <b>+1,11 aberturas/dia</b> (IC 95%: <code>[1,02; 1,20]</code>; <i>d<sub>z</sub></i> = 1,75), potencializado quando o disparo ocorre com a tela ativa (+15,7 p.p.).
          </p>
        </div>

        <div class="panel">
          <span class="panel-label">Próximo Passo para Estudo Completo</span>
          <h3 class="panel-title">Experimento Controlado (Teste A/B)</h3>
          <p>
            Para eliminar variáveis de confusão de rede/OS e estabelecer <b>inferência causal</b> no domínio financeiro (alertas PIX), propõe-se um <b>Teste A/B aleatorizado</b> sorteando o disparo imediato vs. sensível ao contexto.
          </p>
        </div>

        <div class="panel">
          <span class="panel-label">Pacote de Reprodutibilidade</span>
          <h3 class="panel-title">GitHub &amp; Template ACM</h3>
          <p style="font-family: var(--font-mono); font-size: 0.8rem; color: var(--accent); margin-bottom: 10px; word-break: break-all;">
            github.com/jgabrieldsl/mceq_projeto_final
          </p>
          <p>
            Inclui <code>analise.py</code> (semente fixa <code>default_rng(2026)</code>), base bruta OSF, CSVs limpos, protocolo de 1 página e artigo ACM (≤ 4 páginas).
          </p>
        </div>
      </div>
    </section>

  </main>

  <!-- Collapsible Speaker Notes Drawer (Toggled via 'N' key or button) -->
  <aside class="notes-drawer" id="notes-drawer">
    <div class="notes-header">
      <span>Roteiro de Fala / Cola Completa para Apresentação e Arguição (Pressione 'N' para ocultar)</span>
      <span id="notes-speaker-tag"></span>
    </div>
    <div class="notes-body" id="notes-content"></div>
  </aside>

  <!-- Bottom Minimal Footer -->
  <footer class="footer">
    <div class="footer-steps" id="footer-steps"></div>
    <div class="footer-actions">
      <button class="ctrl-btn" id="btn-notes" onclick="toggleNotes()" title="Ativar/Desativar Roteiro de Fala (Tecla N)">Roteiro de Fala (N)</button>
      <button class="ctrl-btn" onclick="changeSlide(-1)">←</button>
      <button class="ctrl-btn" onclick="changeSlide(1)">→</button>
      <button class="ctrl-btn" onclick="toggleFullScreen()" title="Tela Cheia (Tecla F)">Tela Cheia (F)</button>
    </div>
  </footer>

  <script>
    const slides = Array.from(document.querySelectorAll('.slide'));
    const stepsContainer = document.getElementById('footer-steps');
    const speakerPill = document.getElementById('speaker-pill');
    const notesDrawer = document.getElementById('notes-drawer');
    const notesContent = document.getElementById('notes-content');
    const notesSpeakerTag = document.getElementById('notes-speaker-tag');
    const btnNotes = document.getElementById('btn-notes');
    let current = 0;

    const shortLabels = [
      "01 Capa",
      "02 Problema",
      "03 Hipóteses",
      "04 Base OSF",
      "05 Método",
      "06 Tabela 1",
      "07 Figura 1",
      "08 Validade",
      "09 Conclusão"
    ];

    slides.forEach((_, idx) => {{
      const btn = document.createElement('button');
      btn.className = 'step-btn' + (idx === 0 ? ' active' : '');
      btn.textContent = shortLabels[idx] || `0${{idx + 1}}`;
      btn.onclick = () => goTo(idx);
      stepsContainer.appendChild(btn);
    }});

    function render() {{
      slides.forEach((s, i) => s.classList.toggle('active', i === current));
      Array.from(stepsContainer.children).forEach((b, i) => b.classList.toggle('active', i === current));
      const spk = slides[current].getAttribute('data-speaker') || '';
      const parts = spk.split('•');
      speakerPill.innerHTML = parts.length > 1
        ? `<strong>${{parts[0].trim()}}</strong> · ${{parts[1].trim()}}`
        : `<strong>${{spk}}</strong>`;
      notesContent.textContent = slides[current].getAttribute('data-notes') || '';
      notesSpeakerTag.textContent = `Slide ${{current + 1}} de ${{slides.length}}`;
    }}

    function goTo(idx) {{
      current = (idx + slides.length) % slides.length;
      render();
    }}

    function changeSlide(delta) {{
      goTo(current + delta);
    }}

    function toggleNotes() {{
      const isOpen = notesDrawer.classList.toggle('open');
      btnNotes.classList.toggle('active-toggle', isOpen);
    }}

    function toggleFullScreen() {{
      if (!document.fullscreenElement) {{
        document.documentElement.requestFullscreen().catch(() => {{}});
      }} else {{
        document.exitFullscreen().catch(() => {{}});
      }}
    }}

    document.addEventListener('keydown', (e) => {{
      if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') {{
        e.preventDefault();
        changeSlide(1);
      }} else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {{
        e.preventDefault();
        changeSlide(-1);
      }} else if (e.key === 'n' || e.key === 'N') {{
        toggleNotes();
      }} else if (e.key === 'f' || e.key === 'F') {{
        toggleFullScreen();
      }}
    }});

    render();
  </script>
</body>
</html>
"""

with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(HTML_CONTENT)

shutil.copyfile(OUT_HTML, DOWNLOADS_HTML)
print("Apresentação clean editorial gerada com sucesso!")
