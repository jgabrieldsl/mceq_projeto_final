#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera uma apresentação de slides HTML moderna, interativa e autossuficiente (com a Figura 1 embutida em Base64)
seguindo exatamente a estrutura de 5 blocos do Roteiro de Vídeo/Apresentação (Seção 7, p. 8-9)
e o Protocolo de 1 Página (Seção 4) de MCEQ 12576 – PUC-Campinas.
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
  <title>MCEQ 12576 – Apresentação do Projeto Final | PUC-Campinas</title>
  <style>
    :root {{
      --bg-dark: #0b1120;
      --bg-card: rgba(17, 25, 45, 0.88);
      --bg-card-alt: rgba(30, 41, 69, 0.72);
      --border-subtle: rgba(148, 163, 184, 0.18);
      --accent-blue: #38bdf8;
      --accent-indigo: #6366f1;
      --accent-amber: #f59e0b;
      --accent-emerald: #10b981;
      --accent-rose: #f43f5e;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --font-mono: 'JetBrains Mono', 'Fira Code', Menlo, monospace;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: var(--font-sans);
      background: radial-gradient(circle at 12% 18%, #172554 0%, #0b1120 55%, #060a14 100%);
      color: var(--text-main);
      height: 100vh;
      width: 100vw;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      user-select: none;
    }}

    /* Top Header Bar */
    .top-bar {{
      height: 54px;
      padding: 0 32px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid var(--border-subtle);
      background: rgba(11, 17, 32, 0.85);
      backdrop-filter: blur(12px);
      z-index: 20;
      flex-shrink: 0;
    }}

    .brand {{
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 0.85rem;
      font-weight: 600;
      letter-spacing: 0.03em;
      color: var(--text-muted);
    }}

    .brand-badge {{
      background: linear-gradient(135deg, var(--accent-blue), var(--accent-indigo));
      color: #fff;
      padding: 4px 10px;
      border-radius: 6px;
      font-weight: 700;
      font-size: 0.78rem;
    }}

    .presenter-pill {{
      display: flex;
      align-items: center;
      gap: 10px;
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.35);
      padding: 5px 14px;
      border-radius: 999px;
      font-size: 0.82rem;
      font-weight: 600;
      color: var(--accent-blue);
      transition: all 0.3s ease;
    }}

    .presenter-dot {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--accent-emerald);
      box-shadow: 0 0 8px var(--accent-emerald);
    }}

    /* Slide Viewport */
    .deck-viewport {{
      flex: 1;
      position: relative;
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px 44px;
    }}

    .slide {{
      position: absolute;
      width: 100%;
      max-width: 1360px;
      height: calc(100% - 24px);
      display: flex;
      flex-direction: column;
      justify-content: center;
      opacity: 0;
      pointer-events: none;
      transform: translateX(40px) scale(0.985);
      transition: opacity 0.38s cubic-bezier(0.16, 1, 0.3, 1), transform 0.38s cubic-bezier(0.16, 1, 0.3, 1);
      padding: 12px 24px;
    }}

    .slide.active {{
      opacity: 1;
      pointer-events: auto;
      transform: translateX(0) scale(1);
    }}

    /* Typography & Layout inside slides */
    .slide-kicker {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-size: 0.82rem;
      text-transform: uppercase;
      letter-spacing: 0.11em;
      font-weight: 700;
      color: var(--accent-blue);
      margin-bottom: 8px;
    }}

    .slide-title {{
      font-size: 2.15rem;
      font-weight: 800;
      line-height: 1.18;
      margin-bottom: 12px;
      letter-spacing: -0.02em;
      background: linear-gradient(95deg, #ffffff 0%, #cbd5e1 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    .slide-subtitle {{
      font-size: 1.05rem;
      color: var(--text-muted);
      line-height: 1.5;
      margin-bottom: 22px;
      max-width: 980px;
    }}

    .grid-2 {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      width: 100%;
    }}

    .grid-3 {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 18px;
      width: 100%;
    }}

    .grid-4 {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      width: 100%;
    }}

    .card {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 14px;
      padding: 20px 22px;
      box-shadow: 0 12px 32px -12px rgba(0, 0, 0, 0.55);
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}

    .card-highlight {{
      border-color: rgba(56, 189, 248, 0.45);
      background: linear-gradient(160deg, rgba(30, 58, 138, 0.42), rgba(15, 23, 42, 0.9));
    }}

    .card-amber {{
      border-color: rgba(245, 158, 11, 0.45);
      background: linear-gradient(160deg, rgba(120, 53, 15, 0.28), rgba(15, 23, 42, 0.9));
    }}

    .card-emerald {{
      border-color: rgba(16, 185, 129, 0.45);
      background: linear-gradient(160deg, rgba(6, 78, 59, 0.32), rgba(15, 23, 42, 0.9));
    }}

    .card-title {{
      font-size: 1.02rem;
      font-weight: 700;
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
    }}

    .badge {{
      display: inline-block;
      padding: 3px 9px;
      border-radius: 6px;
      font-size: 0.72rem;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }}

    .badge-blue {{ background: rgba(56, 189, 248, 0.16); color: var(--accent-blue); border: 1px solid rgba(56, 189, 248, 0.35); }}
    .badge-emerald {{ background: rgba(16, 185, 129, 0.16); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.35); }}
    .badge-amber {{ background: rgba(245, 158, 11, 0.16); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.35); }}
    .badge-rose {{ background: rgba(244, 63, 94, 0.16); color: #fb7185; border: 1px solid rgba(244, 63, 94, 0.35); }}

    .card p, .card li {{
      font-size: 0.91rem;
      line-height: 1.52;
      color: #cbd5e1;
    }}

    .card ul {{
      padding-left: 18px;
      display: flex;
      flex-direction: column;
      gap: 7px;
    }}

    .stat-big {{
      font-size: 2.3rem;
      font-weight: 800;
      color: var(--accent-blue);
      line-height: 1.1;
      font-family: var(--font-mono);
    }}

    .stat-label {{
      font-size: 0.8rem;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.06em;
      font-weight: 600;
    }}

    /* Tables */
    table.data-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.86rem;
      margin-top: 4px;
    }}

    table.data-table th {{
      text-align: left;
      padding: 9px 11px;
      background: rgba(30, 41, 59, 0.9);
      color: var(--accent-blue);
      font-weight: 700;
      border-bottom: 2px solid rgba(56, 189, 248, 0.35);
    }}

    table.data-table td {{
      padding: 8px 11px;
      border-bottom: 1px solid var(--border-subtle);
      color: #e2e8f0;
    }}

    table.data-table tr:last-child td {{
      border-bottom: none;
      background: rgba(56, 189, 248, 0.08);
      font-weight: 600;
    }}

    .num {{
      text-align: right !important;
      font-family: var(--font-mono);
    }}

    .formula-box {{
      background: rgba(9, 14, 28, 0.85);
      border: 1px solid rgba(99, 102, 241, 0.35);
      border-left: 4px solid var(--accent-indigo);
      padding: 12px 16px;
      border-radius: 8px;
      font-family: var(--font-mono);
      font-size: 0.92rem;
      color: #e0e7ff;
    }}

    .figure-container {{
      background: #ffffff;
      border-radius: 12px;
      padding: 10px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.5);
      max-height: 490px;
    }}

    .figure-container img {{
      max-width: 100%;
      max-height: 440px;
      object-fit: contain;
      border-radius: 6px;
    }}

    /* Author cards on Slide 1 */
    .author-card {{
      background: var(--bg-card-alt);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 16px 18px;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}

    .author-name {{
      font-size: 1.05rem;
      font-weight: 700;
      color: #fff;
    }}

    .author-meta {{
      font-size: 0.82rem;
      color: var(--text-muted);
      font-family: var(--font-mono);
    }}

    /* Bottom Navigation Bar */
    .bottom-bar {{
      height: 56px;
      padding: 0 32px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-top: 1px solid var(--border-subtle);
      background: rgba(11, 17, 32, 0.9);
      backdrop-filter: blur(12px);
      z-index: 20;
      flex-shrink: 0;
    }}

    .progress-dots {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .dot {{
      width: 28px;
      height: 6px;
      border-radius: 999px;
      background: rgba(148, 163, 184, 0.25);
      cursor: pointer;
      transition: all 0.25s ease;
    }}

    .dot.active {{
      width: 48px;
      background: var(--accent-blue);
      box-shadow: 0 0 10px rgba(56, 189, 248, 0.6);
    }}

    .nav-controls {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .btn-nav {{
      background: rgba(30, 41, 59, 0.85);
      border: 1px solid var(--border-subtle);
      color: var(--text-main);
      padding: 7px 15px;
      border-radius: 8px;
      font-size: 0.84rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
    }}

    .btn-nav:hover {{
      background: rgba(56, 189, 248, 0.18);
      border-color: var(--accent-blue);
    }}

    .slide-counter {{
      font-family: var(--font-mono);
      font-size: 0.85rem;
      color: var(--text-muted);
      min-width: 75px;
      text-align: center;
    }}
  </style>
</head>
<body>

  <!-- Top Header -->
  <header class="top-bar">
    <div class="brand">
      <span class="brand-badge">PUC-CAMPINAS • 2026/2</span>
      <span>12576 – Métodos de Computação Experimental e Quantitativa (MCEQ)</span>
    </div>
    <div class="presenter-pill" id="presenter-pill">
      <span class="presenter-dot"></span>
      <span id="presenter-text">Apresentador: João Gabriel da Silva Leite (Bloco 1)</span>
    </div>
  </header>

  <!-- Main Slide Deck -->
  <main class="deck-viewport">

    <!-- SLIDE 1: CAPA + EQUIPE -->
    <section class="slide active" data-presenter="João Gabriel da Silva Leite • Abertura & Problema (0:00 – 1:15)">
      <div class="slide-kicker">Projeto Final • Artigo no Template ACM + Pacote de Reprodutibilidade</div>
      <h1 class="slide-title" style="font-size: 2.45rem; max-width: 1120px;">
        Envio de Notificações Push e Frequência Diária de Abertura de Aplicativo Móvel: Um Estudo Observacional Longitudinal
      </h1>
      <p class="slide-subtitle">
        Avaliação empírica em blocos pareados por usuário (<i>n</i> = 194 blocos; 7.503 usuários-dia ativos; 42.504 janelas de telemetria) a partir do pacote público de replicação do projeto FUTURE (OSF).
      </p>

      <div class="grid-3" style="margin-bottom: 20px;">
        <div class="author-card">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <span class="author-name">João Gabriel da Silva Leite</span>
            <span class="badge badge-blue">Bloco 1 (0:00–2:45)</span>
          </div>
          <span class="author-meta">RA: 24787392 • Engenharia de Software</span>
          <span class="author-meta">joao.gsl@puccampinas.edu.br</span>
          <span style="font-size:0.8rem; color:#94a3b8; margin-top:4px;">Problema, Adaptação da Ficha (Seção 3.3), Hipóteses H0/H1 e Proveniência OSF</span>
        </div>

        <div class="author-card">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <span class="author-name">Yuri Cardoso Balieiro</span>
            <span class="badge badge-emerald">Bloco 2 (2:45–5:45)</span>
          </div>
          <span class="author-meta">RA: 24011525 • Engenharia de Software</span>
          <span class="author-meta">yuri.cb@puccampinas.edu.br</span>
          <span style="font-size:0.8rem; color:#94a3b8; margin-top:4px;">Desenho em Blocos Pareados, Limpeza, Escolha do Teste e Resultados Confirmatórios</span>
        </div>

        <div class="author-card">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <span class="author-name">Pedro de Mello Porto Daou</span>
            <span class="badge badge-amber">Bloco 3 (5:45–8:30)</span>
          </div>
          <span class="author-meta">RA: 21010698 • Engenharia de Software</span>
          <span class="author-meta">pedro.mpd@puccampinas.edu.br</span>
          <span style="font-size:0.8rem; color:#94a3b8; margin-top:4px;">Análises Exploratórias, 4 Ameaças à Validade, Conclusão e Reprodutibilidade</span>
        </div>
      </div>

      <div class="grid-4">
        <div class="card card-highlight" style="padding: 14px 18px;">
          <span class="stat-label">Janelas Monitoradas</span>
          <span class="stat-big">42.504</span>
          <span style="font-size:0.8rem; color:#94a3b8;">201 usuários (Screen Time API)</span>
        </div>
        <div class="card card-highlight" style="padding: 14px 18px;">
          <span class="stat-label">Blocos Pareados (Usuários)</span>
          <span class="stat-big">n = 194</span>
          <span style="font-size:0.8rem; color:#94a3b8;">Com ambos os regimes de push</span>
        </div>
        <div class="card card-emerald" style="padding: 14px 18px;">
          <span class="stat-label">Diferença Média Pareada</span>
          <span class="stat-big" style="color:#34d399;">+1,11</span>
          <span style="font-size:0.8rem; color:#94a3b8;">aberturas/dia (IC 95%: [1,02; 1,20])</span>
        </div>
        <div class="card card-amber" style="padding: 14px 18px;">
          <span class="stat-label">Tamanho de Efeito (Cohen)</span>
          <span class="stat-big" style="color:#fbbf24;">d<sub>z</sub> = 1,75</span>
          <span style="font-size:0.8rem; color:#94a3b8;">t = 24,44 | p = 2,80 × 10<sup>-61</sup></span>
        </div>
      </div>
    </section>

    <!-- SLIDE 2: PROBLEMA, ADAPTAÇÃO DA FICHA (SEÇÃO 3.3) E HIPÓTESES -->
    <section class="slide" data-presenter="João Gabriel da Silva Leite • Bloco 1: Problema e Hipóteses (0:00 – 1:30)">
      <div class="slide-kicker">Bloco 1 do Roteiro • Problema, Adaptação da Ficha (Seção 3.3) e Hipóteses</div>
      <h2 class="slide-title">Do Problema Original (Semana 4) ao Protocolo com Base Pública</h2>
      <p class="slide-subtitle">
        Em Engenharia de Software móvel, o disparo de notificações <i>push</i> enfrenta um dilema arquitetural: frequência insuficiente reduz a retenção diária, enquanto o excesso provoca fadiga e revogação de permissões (Wohllebe, 2020; Mehrotra &amp; Musolesi, 2020).
      </p>

      <div class="grid-2">
        <div class="card">
          <div class="card-title">
            <span>1. Adaptação Transparente da Ficha (Seção 3.3)</span>
            <span class="badge badge-blue">Protocolo Prévio</span>
          </div>
          <ul>
            <li><b>Ficha da Semana 4:</b> Avaliava notificações <i>push</i> de PIX recebido e o número de aberturas do aplicativo bancário no mesmo dia.</li>
            <li><b>Por que adaptamos:</b> Registros bancários de PIX são proprietários e protegidos por sigilo bancário (sem base pública).</li>
            <li><b>O que foi preservado (Regra 3.3):</b> Mantivemos o mesmo mecanismo de software (entrega de <i>push</i>) e a mesma variável dependente (<b>aberturas do app no mesmo dia</b>).</li>
            <li><b>Ajuste nos níveis da VI:</b> Em dias ativos do estudo longitudinal, o servidor entregou <b>Notificação Completa (4 pushes/dia)</b> ou <b>Notificação Parcial (1 a 3 pushes/dia)</b> devido a falhas de rede/OS.</li>
          </ul>
        </div>

        <div class="card card-highlight">
          <div class="card-title">
            <span>2. Pergunta de Pesquisa &amp; Hipóteses Formais</span>
            <span class="badge badge-emerald">α = 0,05 Fixado a Priori</span>
          </div>
          <p style="font-size:0.93rem; color:#f1f5f9;">
            <b>Pergunta:</b> <i>"Em usuários de um aplicativo móvel longitudinal, dias sob regime de Notificação Completa (4 pushes/dia) apresentam maior número médio de aberturas do aplicativo no mesmo dia do que dias sob Notificação Parcial (1 a 3 pushes/dia), controlando a variabilidade individual por blocagem no usuário?"</i>
          </p>
          <div class="formula-box">
            Seja d<sub>i</sub> = Y<sub>i,Completa</sub> − Y<sub>i,Parcial</sub> a diferença intrapares no usuário i:<br><br>
            • <b>H<sub>0</sub>:</b> μ<sub>d</sub> ≤ 0 &nbsp;(μ<sub>Completa</sub> ≤ μ<sub>Parcial</sub>)<br>
            • <b>H<sub>1</sub>:</b> μ<sub>d</sub> &gt; 0 &nbsp;(μ<sub>Completa</sub> &gt; μ<sub>Parcial</sub>) — <i>Unilateral à direita</i>
          </div>
          <p style="font-size:0.83rem; color:#94a3b8;">
            <b>Justificativa Unilateral (Aula 02):</b> A literatura revisada na Semana 5 aponta direção específica positiva do estímulo <i>push</i> sobre o acionamento imediato do aplicativo.
          </p>
        </div>
      </div>
    </section>

    <!-- SLIDE 3: PROVENIÊNCIA DA BASE PÚBLICA E PIPELINE DE LIMPEZA -->
    <section class="slide" data-presenter="João Gabriel (Base OSF) & Yuri Balieiro (Limpeza e Blocagem) • (1:30 – 3:45)">
      <div class="slide-kicker">Bloco 2 do Roteiro • Base Pública (Seção 3.2) e Limpeza Reprodutível</div>
      <h2 class="slide-title">Proveniência dos Dados (OSF) e Desenho em Blocos Pareados</h2>
      <p class="slide-subtitle">
        Base pública com identificador persistente e dicionário de variáveis completo, coletada via instrumentação passiva do sistema operacional móvel (<i>Screen Time API</i> / <i>UsageStatsManager</i>).
      </p>

      <div class="grid-3">
        <div class="card">
          <div class="card-title">
            <span>Proveniência &amp; Medição</span>
            <span class="badge badge-blue">OSF: osf.io/n4sgb</span>
          </div>
          <ul>
            <li><b>Autores:</b> Dvořák, Kreidl &amp; Tancoš (2026) – Projeto <i>FUTURE</i>.</li>
            <li><b>Arquivo bruto:</b> <code>notif_data_final.dta</code> (licença aberta acadêmica).</li>
            <li><b>Escala e Período:</b> 201 usuários monitorados em 4 ondas de 2 semanas (4 janelas fixas/dia: manhã, almoço, tarde e noite = <b>42.504 janelas</b>).</li>
            <li><b>Instrumentação:</b> Sem autorrelato subjetivo — o próprio app registrou <code>notified</code>, <code>opened</code> e telemetria do smartphone (<code>screen_on</code>, <code>battery</code>).</li>
          </ul>
        </div>

        <div class="card">
          <div class="card-title">
            <span>Pipeline de Limpeza (analise.py)</span>
            <span class="badge badge-amber">Zero Edição Manual</span>
          </div>
          <ul>
            <li><b>Passo 1 (Erros de instrumentação):</b> Exclusão de <b>3 janelas</b> com código de erro <code>-666</code> em <code>time_to_open</code>, restando <b>42.501 janelas válidas</b>.</li>
            <li><b>Passo 2 (Agregação usuário-dia):</b> Consolidação por <code>(p_id, wave, day)</code> gerando <b>10.626 usuários-dia</b>.</li>
            <li><b>Passo 3 (Recorte de dias ativos):</b> Remoção de 3.123 dias inativos (0 pushes e 0 aberturas), isolando os <b>7.503 usuários-dia ativos</b> (5.168 com 4 pushes; 2.335 com 1–3 pushes).</li>
          </ul>
        </div>

        <div class="card card-highlight">
          <div class="card-title">
            <span>Por que Blocos Pareados?</span>
            <span class="badge badge-emerald">Aula 06 • n = 194</span>
          </div>
          <ul>
            <li><b>Controle de ruído entre sujeitos:</b> Cada participante tem um hábito basal distinto de uso do celular.</li>
            <li><b>O Usuário como Bloco:</b> Comparamos o <i>mesmo usuário</i> nos dois regimes: Y<sub>i,Completa</sub> vs. Y<sub>i,Parcial</sub>.</li>
            <li><b>Critério de bloco completo:</b> Dos 201 usuários, 7 tiveram apenas um dos regimes; restaram <b>n = 194 usuários pareados</b>.</li>
            <li><b>Verificação de Normalidade:</b> Shapiro-Wilk nas 194 diferenças d<sub>i</sub> resultou em <b>W = 0,9921 (p = 0,3775 &gt; 0,05)</b> → valida o <b>teste t pareado</b>!</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- SLIDE 4: RESULTADO PRINCIPAL (TABELA 1 + FIGURA 1 + TESTES) -->
    <section class="slide" data-presenter="Yuri Cardoso Balieiro • Bloco 3: Resultado Confirmatório Principal (3:45 – 5:45)">
      <div class="slide-kicker">Bloco 3 do Roteiro • Análise Confirmatória (Planejada no Protocolo)</div>
      <h2 class="slide-title" style="font-size: 1.9rem; margin-bottom: 8px;">
        Resultados Confirmatórios: Estatística Descritiva, Teste <i>t</i> Pareado e Figura 1
      </h2>

      <div class="grid-2" style="grid-template-columns: 1.22fr 0.78fr; align-items: center; gap: 22px;">
        <div style="display: flex; flex-direction: column; gap: 14px;">
          <div class="card" style="padding: 15px 18px;">
            <div class="card-title">
              <span>Tabela 1: Estatísticas Descritivas nos Blocos Pareados (n = 194 usuários)</span>
              <span class="badge badge-blue">Unidade: aberturas/dia</span>
            </div>
            <table class="data-table">
              <thead>
                <tr>
                  <th>Regime / Variável</th>
                  <th class="num">n</th>
                  <th class="num">Média</th>
                  <th class="num">DP</th>
                  <th class="num">Mediana</th>
                  <th class="num">IQR</th>
                  <th class="num">CV%</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Notificação Completa (4/dia)</td>
                  <td class="num">194</td>
                  <td class="num">2,67</td>
                  <td class="num">0,95</td>
                  <td class="num">2,95</td>
                  <td class="num">1,43</td>
                  <td class="num">35,6%</td>
                </tr>
                <tr>
                  <td>Notificação Parcial (1–3/dia)</td>
                  <td class="num">194</td>
                  <td class="num">1,56</td>
                  <td class="num">0,69</td>
                  <td class="num">1,54</td>
                  <td class="num">0,91</td>
                  <td class="num">44,5%</td>
                </tr>
                <tr>
                  <td>Diferença Pareada (d<sub>i</sub> = C − P)</td>
                  <td class="num">194</td>
                  <td class="num">+1,11</td>
                  <td class="num">0,63</td>
                  <td class="num">+1,15</td>
                  <td class="num">0,77</td>
                  <td class="num">57,0%</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="card card-emerald" style="padding: 15px 18px;">
            <div class="card-title">
              <span>Decisão Estatística e Robustez Não Paramétrica (α = 0,05)</span>
              <span class="badge badge-emerald">Rejeita H<sub>0</sub></span>
            </div>
            <ul>
              <li><b>Teste Primário (t pareado unilateral):</b> <code>t = 24,44</code> | <code>gl = 193</code> | <code>EP = 0,0455</code> | <b>p = 2,80 × 10<sup>-61</sup> &lt; 0,05</b>.</li>
              <li><b>Intervalo de Confiança (IC 95%):</b> <b>[1,02; 1,20] aberturas/dia</b> (limite inferior muito acima de zero).</li>
              <li><b>Tamanho de Efeito (Cohen):</b> <b>d<sub>z</sub> = 1,75</b> (efeito muito grande; aumento relativo de <b>+71,2%</b> nas aberturas diárias).</li>
              <li><b>Testes Alternativos do Protocolo:</b> Wilcoxon pareado (<code>T = 18.733,0</code>; <code>p = 1,14 × 10<sup>-32</sup></code>; <code>r<sub>rb</sub> = 0,981</code>) e Permutação Pareada (10.000 sorteios, semente <code>2026</code>: <code>p &lt; 0,0001</code>).</li>
            </ul>
          </div>
        </div>

        <div class="figure-container">
          <img src="data:image/png;base64,{FIG_B64}" alt="Figura 1 do Artigo" />
          <span style="color:#334155; font-size:0.74rem; font-weight:600; margin-top:6px;">
            Figura 1 do artigo (300 DPI): Eixos iniciando estritamente em zero (Cleveland, 1994).
          </span>
        </div>
      </div>
    </section>

    <!-- SLIDE 5: ANÁLISES EXPLORATÓRIAS E 4 AMEAÇAS À VALIDADE -->
    <section class="slide" data-presenter="Pedro de Mello Porto Daou • Bloco 4: Exploratórias e Ameaças à Validade (5:45 – 7:30)">
      <div class="slide-kicker">Bloco 4 do Roteiro • Honestidade Científica (Seção 9) e Ameaças à Validade (Aula 03)</div>
      <h2 class="slide-title">Análises Exploratórias e as 4 Ameaças à Validade</h2>

      <div class="grid-2">
        <div class="card">
          <div class="card-title">
            <span>Subseção 4.2: Análises Exploratórias (Fora do Protocolo)</span>
            <span class="badge badge-amber">Sem HARKing</span>
          </div>
          <ul>
            <li><b>1. Nível Usuário-Dia Independente (n<sub>1</sub> = 5.168 vs. n<sub>2</sub> = 2.335):</b>
              Média de 2,75 vs. 1,61 aberturas/dia (Welch <code>t = 40,17</code>; <code>p &lt; 0,0001</code>; IC 95% <code>[1,09; 1,20]</code>; <code>d = 0,90</code>; Vargha-Delaney <code>A = 0,75</code>).</li>
            <li><b>2. Moderadora Dia Útil vs. Fim de Semana (em dias de 4 pushes, n = 190):</b>
              Maior frequência em dias úteis (<b>2,72 ± 0,98</b>) do que no fim de semana (<b>2,45 ± 1,06</b> aberturas/dia; <code>t = 6,28</code>; <code>p = 1,11 × 10<sup>-9</sup></code>; <code>d<sub>z</sub> = 0,46</code>).</li>
            <li><b>3. Contexto do Smartphone no Disparo (Tela Ligada vs. Desligada, n = 198):</b>
              Taxa de abertura salta de <b>61,2%</b> (tela desligada) para <b>76,9%</b> quando a tela estava ligada no minuto anterior ao push (<b>+15,7 p.p.</b>; <code>t = 13,39</code>; <code>p = 8,41 × 10<sup>-30</sup></code>; <code>d<sub>z</sub> = 0,95</code>).</li>
          </ul>
        </div>

        <div class="card card-amber">
          <div class="card-title">
            <span>Seção 5: Os 4 Tipos de Ameaças à Validade (Wohlin et al., 2012)</span>
            <span class="badge badge-rose">Rigor Metodológico</span>
          </div>
          <ul>
            <li><b>Validade de Conclusão:</b> Risco de violação paramétrica ou inflação de graus de liberdade. <i>Mitigação:</i> agregação em n = 194 blocos independentes + confirmação via Wilcoxon e permutação (semente <code>2026</code>).</li>
            <li><b>Validade Interna (Principal Limitação):</b> Estudo <b>observacional</b> (sem sorteio). Falhas de entrega (1–3 pushes) podem correlacionar com bateria baixa ou modo economia. <i>Mitigação:</i> blocagem por usuário e ausência total de afirmações causais.</li>
            <li><b>Validade de Construção:</b> <code>opened</code> mede acionamento técnico do app, não engajamento cognitivo profundo. <i>Mitigação:</i> uso de telemetria objetiva (<i>Screen Time API</i>).</li>
            <li><b>Validade Externa:</b> Amostra de jovens adultos em app EMA na Europa. <i>Mitigação:</i> escopo restrito a notificações recorrentes; requer replicação em apps financeiros (PIX).</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- SLIDE 6: CONCLUSÃO, REPRODUTIBILIDADE E CHECKLIST SEÇÃO 10 -->
    <section class="slide" data-presenter="Pedro de Mello Porto Daou • Bloco 5: Conclusão e Reprodutibilidade (7:30 – 8:30)">
      <div class="slide-kicker">Bloco 5 do Roteiro • Conclusão, Próximos Passos e Pacote de Reprodutibilidade</div>
      <h2 class="slide-title">Conclusão para Engenharia de Software e Entrega Final</h2>

      <div class="grid-3">
        <div class="card card-emerald">
          <div class="card-title">
            <span>Resposta à Pergunta</span>
            <span class="badge badge-emerald">Seção 6</span>
          </div>
          <p>
            Dias com entrega completa das 4 notificações <i>push</i> estão associados a um acréscimo médio pareado de <b>+1,11 aberturas/dia</b> (IC 95% <code>[1,02; 1,20]</code>; <code>d<sub>z</sub> = 1,75</code>).
          </p>
          <p>
            <b>Implicação prática em ES:</b>
            (1) Garantir confiabilidade na entrega de <i>push</i> na camada de infraestrutura;
            (2) Adotar despacho sensível ao contexto (<i>context-aware</i>), priorizando momentos em que a tela está ativa (+15,7 p.p.).
          </p>
        </div>

        <div class="card">
          <div class="card-title">
            <span>Próximo Passo Experimental</span>
            <span class="badge badge-blue">Teste A/B Controlado</span>
          </div>
          <p>
            Para isolar confundidores de rede/sistema operacional e estabelecer <b>causalidade estrita</b>, o próximo passo é um <b>experimento controlado aleatorizado (Teste A/B)</b> em produção.
          </p>
          <p>
            Nele, o servidor sorteia aleatoriamente a cadência diária de notificações e o agendamento sensível ao estado da tela entre grupos de usuários.
          </p>
        </div>

        <div class="card card-highlight">
          <div class="card-title">
            <span>Checklist Seção 10 (100%)</span>
            <span class="badge badge-blue">Entregáveis Prontos</span>
          </div>
          <ul>
            <li>✅ <b>Artigo ACM (≤ 4 págs.):</b> <code>artigo_final_MCEQ.docx</code> sem resíduos <code>WOODSTOCK'18</code> e com Declaração de IA.</li>
            <li>✅ <b>Protocolo de 1 Página:</b> <code>protocolo_1_pagina.md</code> completo.</li>
            <li>✅ <b>Repositório Python:</b> <code>analise.py</code> com semente <code>default_rng(2026)</code>, <code>README.md</code> e dados brutos/limpos.</li>
            <li>✅ <b>Roteiro do Vídeo (≤ 10 min):</b> <code>roteiro_video.md</code> dividido entre os 3 autores.</li>
          </ul>
        </div>
      </div>
    </section>

  </main>

  <!-- Bottom Navigation -->
  <footer class="bottom-bar">
    <div class="progress-dots" id="progress-dots"></div>
    <div class="nav-controls">
      <button class="btn-nav" onclick="changeSlide(-1)">← Anterior</button>
      <span class="slide-counter" id="slide-counter">1 / 6</span>
      <button class="btn-nav" onclick="changeSlide(1)">Próximo →</button>
      <button class="btn-nav" onclick="toggleFullScreen()" title="Tela Cheia (Tecla F)">⛶ Tela Cheia</button>
    </div>
  </footer>

  <script>
    const slides = Array.from(document.querySelectorAll('.slide'));
    const dotsContainer = document.getElementById('progress-dots');
    const counterEl = document.getElementById('slide-counter');
    const presenterText = document.getElementById('presenter-text');
    let currentSlide = 0;

    slides.forEach((_, idx) => {{
      const dot = document.createElement('div');
      dot.className = 'dot' + (idx === 0 ? ' active' : '');
      dot.onclick = () => goToSlide(idx);
      dotsContainer.appendChild(dot);
    }});

    function updateUI() {{
      slides.forEach((s, i) => s.classList.toggle('active', i === currentSlide));
      Array.from(dotsContainer.children).forEach((d, i) => d.classList.toggle('active', i === currentSlide));
      counterEl.textContent = `${{currentSlide + 1}} / ${{slides.length}}`;
      presenterText.textContent = slides[currentSlide].getAttribute('data-presenter');
    }}

    function goToSlide(idx) {{
      currentSlide = (idx + slides.length) % slides.length;
      updateUI();
    }}

    function changeSlide(step) {{
      goToSlide(currentSlide + step);
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
      }} else if (e.key === 'f' || e.key === 'F') {{
        toggleFullScreen();
      }}
    }});
  </script>
</body>
</html>
"""

with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(HTML_CONTENT)

shutil.copyfile(OUT_HTML, DOWNLOADS_HTML)
print(f"Apresentação HTML gerada com sucesso em:\n - {OUT_HTML}\n - {DOWNLOADS_HTML}")
