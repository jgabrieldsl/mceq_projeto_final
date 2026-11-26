#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera o artigo final MCEQ 12576 no template oficial da ACM (template_relatoriofinal.docx),
corrigindo:
1. Largura da Tabela 1 ajustada exatamente à largura da coluna da ACM (3.30 polegadas), sem cortar bordas;
2. Rótulos matemáticos limpos na Figura 1 (d_i em itálico sem underscore);
3. Espaço no nome dos autores e e-mails sem quebra de linha no bloco de 3 colunas;
4. Densidade e detalhamento calibrados para preencher harmonicamente as 4 páginas do template ACM.
"""

import os
import zipfile
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import docx
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = "/Users/joao.leite/Downloads/template_relatoriofinal.docx"
OUTPUT_DOCX = os.path.join(BASE_DIR, "artigo_final_MCEQ.docx")
FIG_PATH = os.path.join(BASE_DIR, "figuras", "figura1_resultados.png")
PAIRED_CSV = os.path.join(BASE_DIR, "dados", "limpos", "dados_limpos_pareados_usuario.csv")


def regenerar_figura_empilhada():
    """
    Gera a Figura 1 com os painéis (a) e (b) empilhados verticalmente na largura exata
    de 1 coluna da ACM, deixando os textos grandes, nítidos e com notação matemática limpa ($d_i$).
    """
    df_p = pd.read_csv(PAIRED_CSV)
    c_u = df_p["Completa (4 pushes/dia)"].values
    p_u = df_p["Parcial (1-3 pushes/dia)"].values
    d_u = df_p["dif_completa_menos_parcial"].values
    rng = np.random.default_rng(2026)

    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.size": 8.5,
        "axes.titlesize": 9.0,
        "axes.labelsize": 8.5,
        "xtick.labelsize": 8.0,
        "ytick.labelsize": 8.0,
    })

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(3.4, 3.85), dpi=300)

    # Painel (a): Boxplot comparativo com dispersão individual (eixo Y iniciando em 0)
    dados_grupos = [p_u, c_u]
    labels_grupos = ["Notificação Parcial\n(1 a 3 pushes/dia)", "Notificação Completa\n(4 pushes/dia)"]
    cores = ["#9ecae1", "#3182bd"]

    bp = ax1.boxplot(
        dados_grupos,
        tick_labels=labels_grupos,
        widths=0.42,
        patch_artist=True,
        showmeans=True,
        meanprops={"marker": "D", "markerfacecolor": "#d95f02", "markeredgecolor": "black", "markersize": 4.8},
        medianprops={"color": "#08306b", "linewidth": 1.6},
        boxprops={"edgecolor": "#08306b", "linewidth": 0.9},
        whiskerprops={"color": "#08306b", "linewidth": 0.9},
        capprops={"color": "#08306b", "linewidth": 0.9},
    )
    for patch, cor in zip(bp["boxes"], cores):
        patch.set_facecolor(cor)
        patch.set_alpha(0.75)

    for idx, valores in enumerate(dados_grupos, start=1):
        jitter = rng.uniform(-0.11, 0.11, size=len(valores))
        ax1.scatter(
            np.full_like(valores, idx) + jitter,
            valores,
            color="#08306b",
            alpha=0.25,
            s=9,
            zorder=3,
        )

    ax1.set_ylim(0, 4.35)
    ax1.set_ylabel("Aberturas no dia (aberturas/dia)")
    ax1.set_title("(a) Aberturas diárias por regime de push (n = 194 blocos)")
    ax1.grid(axis="y", linestyle="--", alpha=0.4)
    ax1.plot([], [], "D", color="#d95f02", markeredgecolor="black", markersize=4.8, label="Média amostral")
    ax1.plot([], [], "-", color="#08306b", linewidth=1.6, label="Mediana (Q2)")
    ax1.legend(loc="lower right", frameon=True, fontsize=7.5)

    # Painel (b): Histograma das diferenças intrapares d_i (eixo Y iniciando em 0)
    ax2.hist(d_u, bins=14, color="#3182bd", edgecolor="white", alpha=0.85)
    media_d = np.mean(d_u)
    ax2.axvline(0, color="#636363", linestyle=":", linewidth=1.3, label=r"$H_0$: dif. = 0,00")
    ax2.axvline(media_d, color="#d95f02", linestyle="--", linewidth=1.5, label=f"Média: +{media_d:.2f}")
    ax2.axvspan(1.022, 1.201, color="#fdb863", alpha=0.38, label="IC 95%: [1,02; 1,20]")

    ax2.set_ylim(bottom=0)
    ax2.set_xlabel(r"Diferença intrapares $d_i$ (aberturas/dia)")
    ax2.set_ylabel("Frequência (nº de usuários)")
    ax2.set_title(r"(b) Distribuição das diferenças pareadas ($d_i$)")
    ax2.grid(axis="y", linestyle="--", alpha=0.4)
    ax2.legend(loc="upper left", frameon=True, fontsize=7.5)

    plt.tight_layout()
    plt.savefig(FIG_PATH, dpi=300, bbox_inches="tight")
    plt.close(fig)


def set_cell_margins(cell, top=22, bottom=22, left=22, right=22):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for m, val in [("top", top), ("bottom", bottom), ("left", left), ("right", right)]:
        node = OxmlElement(f"w:{m}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        tcMar.append(node)
    tcPr.append(tcMar)


def set_table_horizontal_borders_and_width(table, total_in=3.30):
    """Aplica bordas estilo booktabs e trava a largura da tabela na largura de 1 coluna da ACM (3.30 pol)."""
    tblPr = table._tbl.tblPr
    tblW = OxmlElement("w:tblW")
    tblW.set(qn("w:w"), str(int(total_in * 1440)))
    tblW.set(qn("w:type"), "dxa")
    tblPr.append(tblW)

    borders = OxmlElement("w:tblBorders")
    for b_name, val, sz in [
        ("top", "single", "8"),
        ("bottom", "single", "8"),
        ("left", "none", "0"),
        ("right", "none", "0"),
        ("insideH", "single", "4"),
        ("insideV", "none", "0"),
    ]:
        b = OxmlElement(f"w:{b_name}")
        b.set(qn("w:val"), val)
        b.set(qn("w:sz"), sz)
        b.set(qn("w:space"), "0")
        b.set(qn("w:color"), "000000")
        borders.append(b)
    tblPr.append(borders)


def fill_author(p, full_name, dept, org, city_line, email):
    p.clear()
    r1 = p.add_run(full_name)
    r1.style = "FirstName"
    p.add_run("\n")
    r3 = p.add_run(dept)
    r3.style = "OrgDiv"
    p.add_run("\n")
    r4 = p.add_run(org)
    r4.style = "OrgName"
    p.add_run("\n")
    r5 = p.add_run(city_line)
    r5.style = "City"
    p.add_run("\n")
    r6 = p.add_run(email)
    r6.style = "Email"
    r6.font.size = Pt(8.5)


def build_docx():
    regenerar_figura_empilhada()
    doc = docx.Document(TEMPLATE_PATH)

    # 1. Título (P0)
    p_title = doc.paragraphs[0]
    p_title.clear()
    p_title.add_run(
        "Envio de Notificações Push e Frequência Diária de Abertura de Aplicativo Móvel: Um Estudo Empírico em Blocos*"
    )

    # Remove P1 (Subtitle)
    p_sub = doc.paragraphs[1]
    p_sub._element.getparent().remove(p_sub._element)

    # P2, P3, P4 = Authors (3 cols) - com espaço explícito e e-mail em 8.5pt para não quebrar linha
    fill_author(
        doc.paragraphs[2],
        "João G. S. Leite",
        "Engenharia de Software (RA: 24787392)",
        "PUC-Campinas",
        "Campinas, SP, Brasil",
        "joao.gsl@puccampinas.edu.br",
    )
    fill_author(
        doc.paragraphs[3],
        "Yuri C. Balieiro",
        "Engenharia de Software (RA: 24011525)",
        "PUC-Campinas",
        "Campinas, SP, Brasil",
        "yuri.cb@puccampinas.edu.br",
    )
    fill_author(
        doc.paragraphs[4],
        "Pedro M. P. Daou",
        "Engenharia de Software (RA: 21010698)",
        "PUC-Campinas",
        "Campinas, SP, Brasil",
        "pedro.mpd@puccampinas.edu.br",
    )

    # Remove P6 (AuthNotes sem sectPr)
    p_authnotes = doc.paragraphs[6]
    p_authnotes._element.getparent().remove(p_authnotes._element)

    # Remove parágrafos de exemplo a partir de P7
    for p in list(doc.paragraphs[7:]):
        p._element.getparent().remove(p._element)

    for t in list(doc.tables):
        t._element.getparent().remove(t._element)

    def add_head(style_name, number_str, title_str):
        p = doc.add_paragraph(style=style_name)
        if number_str:
            r_num = p.add_run(number_str)
            r_num.style = "Label"
            p.add_run("\u2003" + title_str)
        else:
            p.add_run(title_str)
        return p

    def add_para(text, style_name="Para"):
        p = doc.add_paragraph(style=style_name)
        p.add_run(text)
        return p

    # Nota do Título (Title Note - link do vídeo conforme Seção 5)
    p_tn = doc.add_paragraph(style="footnote text")
    p_tn.add_run(
        "* Nota do título (Title Note): Vídeo da equipe (YouTube, não listado, ≤ 10 min): "
        "https://youtu.be/INSERIR_LINK_YOUTUBE_NAO_LISTADO | Repositório de código e dados: "
        "https://github.com/joaoleite/mceq-notificacoes-push-2026"
    )

    # RESUMO (165 palavras - estritamente dentro de 120 a 180 palavras da Seção 5)
    add_head("AbsHead", None, "RESUMO")
    resumo_texto = (
        "Notificações push são amplamente empregadas em aplicativos móveis para estimular o engajamento imediato. "
        "Contudo, revisões sistemáticas apontam escassez de estudos com telemetria real que comparem regimes de entrega "
        "de notificações sobre a frequência diária de abertura do aplicativo. Este artigo avalia se o envio completo de "
        "notificações push diárias está associado a um maior número de aberturas do aplicativo no mesmo dia, comparado à "
        "entrega parcial. Utilizou-se a base pública observacional longitudinal do projeto FUTURE (OSF, n4sgb), contendo "
        "42.504 janelas de medição de 201 usuários. Adotou-se desenho pareado em blocos por usuário (n = 194 blocos "
        "completos; α = 0,05), contrastando dias com notificação completa (4 pushes/dia) contra parcial (1–3 pushes/dia) "
        "via teste t pareado e Wilcoxon. Dias com notificação completa apresentaram média de 2,67 (DP = 0,95) contra "
        "1,56 (DP = 0,69) aberturas/dia (+1,11 aberturas/dia; IC 95%: [1,02; 1,20]; t = 24,44; p = 2,80 × 10⁻⁶¹; "
        "dz = 1,75). Por tratar-se de estudo observacional, as conclusões restringem-se à associação estatística, sem "
        "inferência causal."
    )
    add_para(resumo_texto, "Abstract")

    # PALAVRAS-CHAVE (5 termos)
    add_head("KeyWordHead", None, "PALAVRAS-CHAVE")
    add_para(
        "Notificações push, engajamento móvel, engenharia de software empírica, desenho em blocos pareado, telemetria.",
        "KeyWords",
    )

    # 1 INTRODUÇÃO
    add_head("Head1", "1", "INTRODUÇÃO")
    add_para(
        "Em Engenharia de Software para dispositivos móveis, serviços de notificação assíncrona (mobile push notifications) "
        "constituem componentes arquiteturais críticos para retenção e engajamento [7, 9]. Em aplicativos financeiros — como "
        "alertas transacionais instantâneos de PIX recebido — e em plataformas móveis de monitoramento contínuo, a política "
        "de disparo deve estimular a abertura imediata do aplicativo sem provocar fadiga, interrupção excessiva ou "
        "desinstalação [6, 9]. Embora amplamente adotadas na indústria, regras de envio de notificações costumam ser "
        "definidas de maneira informal ou ad hoc, contrariando os princípios da Engenharia de Software Baseada em "
        "Evidências (EBSE) [1, 5]."
    )
    add_para(
        "A motivação original desta equipe partiu da investigação sobre o impacto de notificações push de PIX recebido na "
        "frequência diária de aberturas de um aplicativo bancário. Como registros transacionais bancários são protegidos "
        "por sigilo comercial e bancário, aplicou-se a diretriz metodológica de adaptação a dados públicos reais de "
        "telemetria móvel [4], documentada no protocolo do projeto antes da análise. Preservando o mecanismo técnico de "
        "interesse (envio de notificação push) e a métrica primária de resposta no mesmo dia (número de aberturas diárias "
        "do aplicativo registradas por timestamp), formulou-se a seguinte pergunta de pesquisa estruturada pela abordagem "
        "Goal-Question-Metric (GQM) [1]: \"Em usuários de um aplicativo móvel com coleta longitudinal, o regime de envio "
        "completo de notificações push diárias (4 notificações/dia) está associado a um maior número médio de aberturas do "
        "aplicativo no mesmo dia, em comparação ao regime de envio parcial (1 a 3 notificações/dia)?\""
    )
    add_para(
        "Seguindo o método hipotético-dedutivo e fixando a priori o nível de significância α = 0,05 sobre a diferença "
        "populacional média intrapares (μd = μcompleta − μparcial), estabeleceram-se: Hipótese Nula (H0: μd = 0), "
        "postulando ausência de diferença no número médio de aberturas diárias do aplicativo entre os regimes de "
        "notificação completa e parcial; e Hipótese Alternativa unilateral (H1: μd > 0), postulando que o regime de "
        "notificação completa está associado a uma maior média de aberturas no mesmo dia. Por tratar-se de um estudo "
        "empírico observacional conduzido sobre dados secundários públicos, todas as conclusões expressam associação "
        "estatística e não relações de causa e efeito."
    )

    # 2 TRABALHOS RELACIONADOS
    add_head("Head1", "2", "TRABALHOS RELACIONADOS")
    add_para(
        "Três revisões sistemáticas localizadas no mapeamento prévio da literatura fundamentam diretamente a lacuna deste "
        "estudo. Wohllebe [9], em revisão sistemática seguindo o protocolo PRISMA sobre 17 estudos primários acerca da "
        "frequência de notificações push, identificou que a literatura depende predominantemente de questionários e "
        "comportamento autorreportado, apontando a escassez de análises baseadas em telemetria real de abertura do "
        "aplicativo (app analytics). Philip e Hidayaturrahman [7], ao revisarem 12 estudos sobre estratégias de "
        "engajamento móvel, destacaram que, embora notificações push figurem entre as práticas recomendadas, faltam "
        "comparações quantitativas controladas que mensurem o efeito de diferentes regimes de entrega. Por sua vez, "
        "Mehrotra e Musolesi [6], em survey sobre sistemas inteligentes de notificação, demonstraram que a receptividade "
        "do usuário depende fortemente do contexto de uso do smartphone no momento do alerta, como o estado de atividade "
        "da tela e o período da semana."
    )
    add_para(
        "No âmbito de bases públicas de telemetria móvel, Dvořák, Kreidl e Tancoš [4] conduziram um estudo observacional "
        "longitudinal no projeto FUTURE com 201 usuários de smartphone, disponibilizando os paradados brutos de "
        "notificações push e aberturas do aplicativo com resolução de milissegundos. Enquanto o artigo original [4] "
        "empregou modelos de sobrevivência de Cox para avaliar a latência até a resposta e a taxa de desistência "
        "(dropout) entre ondas de coleta, o presente artigo reutiliza essa base pública sob um delineamento distinto: "
        "avalia o efeito intrapares da completude diária de notificações push sobre a quantidade de aberturas do "
        "aplicativo no mesmo dia, além de testar variáveis moderadoras de contexto."
    )

    # 3 MÉTODO
    add_head("Head1", "3", "MÉTODO")
    add_para(
        "Proveniência e Instrumentação da Base Pública. Utilizou-se o pacote público de reprodutibilidade depositado por "
        "Dvořák, Kreidl e Tancoš [4] no repositório Open Science Framework (OSF, identificador persistente: "
        "https://osf.io/n4sgb/, arquivo bruto notif_data_final.dta e dicionário Multimedia_Appendix_9_Codebook.docx, "
        "acessados em 25/11/2026 sob licença pública de reprodutibilidade acadêmica). O estudo monitorou 201 participantes "
        "ao longo de quatro ondas (bursts) de 14 dias cada (entre maio de 2021 e maio de 2022), com até 4 janelas diárias "
        "programadas de questionários no aplicativo Android (Manhã, Diário I, Diário II e Noite), totalizando 42.504 "
        "janelas de medição. A coleta foi instrumentada automaticamente em segundo plano via API do Android, gravando os "
        "timestamps em milissegundos da entrega da notificação push, da abertura do aplicativo pelo usuário e do tempo de "
        "tela ligada no minuto imediatamente anterior ao disparo."
    )
    add_para(
        "Variáveis e Limpeza Reprodutível. No nível de usuário-dia ativo, operacionalizaram-se as seguintes variáveis: "
        "(i) Variável Independente (VI): regime diário de entrega de notificações push (notified_windows), com dois níveis "
        "— Notificação Completa (4 pushes entregues/dia) e Notificação Parcial (1 a 3 pushes entregues/dia, ocorrendo "
        "quando falhas de conectividade, aparelho desligado ou restrições do sistema operacional impediram parte das "
        "entregas diárias); (ii) Variável Dependente (VD): número de aberturas do aplicativo no mesmo dia (daily_opens, "
        "medida em aberturas/dia, variando de 0 a 4, obtida pela soma diária de janelas com opened_bin == '1'); "
        "(iii) Variáveis de Controle: mesmo aplicativo instrumentado, teto fixo de 4 janelas programadas por dia e "
        "restrição a dias ativos (notified_windows ≥ 1); e (iv) Variáveis Moderadoras (avaliadas na Seção 4.2): período "
        "da semana (is_weekend: dia útil vs. fim de semana) e estado da tela do smartphone no minuto anterior ao disparo "
        "(screen_on: tela ligada vs. desligada). O script automatizado em Python (analise.py) carrega a base bruta sem "
        "edição manual e remove 3 janelas (0,007% das 42.504) registradas com o código '-666' (erro conhecido de log "
        "documentado no Codebook original [4]). As 42.501 janelas válidas resultaram em 10.626 usuários-dia. Em 3.123 "
        "usuários-dia nos quais nenhuma notificação foi entregue (0 pushes), ocorreram 0 aberturas do aplicativo em 100% "
        "dos casos — confirmando que o uso depende do gatilho da notificação, mas gerando variância nula. Assim, o "
        "contraste analítico concentrou-se nos 7.503 usuários-dia ativos (5.168 completos e 2.335 parciais)."
    )
    add_para(
        "Desenho em Blocos e Escolha do Teste Estatístico. Como a propensão basal a interagir com o smartphone varia "
        "fortemente entre indivíduos (fator de perturbação conhecido e controlável), adotou-se um desenho pareado em "
        "blocos, no qual cada usuário (p_id) atua como seu próprio bloco submetido a ambos os regimes ao longo do estudo "
        "[8]. Dos 201 usuários, 7 foram excluídos da análise pareada por apresentarem observações em apenas um regime "
        "(blocos incompletos), resultando em n = 194 blocos completos. Para cada usuário i (i = 1, ..., 194), calculou-se "
        "a diferença média intrapares di = x̄completa,i − x̄parcial,i, cancelando a variação interindividual do erro "
        "experimental. A premissa de normalidade das diferenças di foi avaliada pelo teste de Shapiro-Wilk, obtendo-se "
        "W = 0,9921 e p = 0,3775 > 0,05. Atendida a normalidade, aplicou-se o teste t pareado unilateral (α = 0,05) [8], "
        "complementado pelo teste de permutação pareado (10.000 réplicas com semente fixa default_rng(2026)) e pelo teste "
        "não paramétrico de postos sinalizados de Wilcoxon (definido a priori no protocolo como teste alternativo). "
        "Relatam-se o tamanho de efeito padronizado para amostras pareadas (dz = d̄ / sd) [2, 3], a correlação "
        "posto-bisserial (rrb) e o Intervalo de Confiança bilateral de 95% (IC 95%) para a diferença média."
    )

    # 4 RESULTADOS PRELIMINARES
    add_head("Head1", "4", "RESULTADOS PRELIMINARES")
    add_head("Head2", "4.1", "Análise Confirmatória (Protocolo)")
    add_para(
        "A Tabela 1 sintetiza as estatísticas descritivas de tendência central (média e mediana), dispersão (desvio "
        "padrão, intervalo interquartil e coeficiente de variação) para os 194 usuários pareados. As médias e medianas "
        "são altamente consistentes nos dois grupos e na diferença intrapares di (média = +1,11 vs. mediana = +1,15 "
        "aberturas/dia; coeficiente de assimetria g1 = −0,10), evidenciando distribuição simétrica. Pela regra de Tukey "
        "(1,5 × IQR), não foram detectados outliers nos regimes isolados e apenas 3 blocos (1,5%) apresentaram diferenças "
        "di moderadamente extremas, mantidas na análise por representarem variação legítima de comportamento."
    )

    # TABELA 1 (Largura exata de 3.30 pol para caber perfeitamente em 1 coluna da ACM sem cortar nada)
    p_tcap = doc.add_paragraph(style="TableCaption")
    r_tlbl = p_tcap.add_run("Tabela 1:")
    r_tlbl.bold = True
    p_tcap.add_run(" Estatística descritiva das aberturas diárias do app por regime de notificação push (n = 194 usuários pareados).")

    table = doc.add_table(rows=4, cols=7)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_horizontal_borders_and_width(table, total_in=3.30)

    col_widths = [Inches(1.12), Inches(0.28), Inches(0.38), Inches(0.35), Inches(0.42), Inches(0.35), Inches(0.40)]
    headers = ["Regime / Variável", "n", "Média", "DP", "Med.", "IQR", "CV%"]
    rows_data = [
        ["Completa (4/dia)", "194", "2,67", "0,95", "2,95", "1,43", "35,6"],
        ["Parcial (1–3/dia)", "194", "1,56", "0,69", "1,54", "0,91", "44,5"],
        ["Diferença (di)", "194", "+1,11", "0,63", "+1,15", "0,77", "57,0"],
    ]

    for row in table.rows:
        for idx, w in enumerate(col_widths):
            row.cells[idx].width = w

    for col_idx, h_text in enumerate(headers):
        cell = table.cell(0, col_idx)
        set_cell_margins(cell, top=22, bottom=22, left=20, right=20)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT if col_idx == 0 else WD_ALIGN_PARAGRAPH.RIGHT
        run = p.add_run(h_text)
        run.bold = True
        run.font.size = Pt(7.5)
        run.font.name = "Linux Libertine"

    for row_idx, r_list in enumerate(rows_data, start=1):
        for col_idx, val_text in enumerate(r_list):
            cell = table.cell(row_idx, col_idx)
            set_cell_margins(cell, top=18, bottom=18, left=20, right=20)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if col_idx == 0 else WD_ALIGN_PARAGRAPH.RIGHT
            run = p.add_run(val_text)
            run.font.size = Pt(7.5)
            run.font.name = "Linux Libertine"

    # FIGURA 1 (Empilhada, 3.25 pol de largura)
    p_fig = doc.add_paragraph(style="Para")
    p_fig.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_fig = p_fig.add_run()
    run_fig.add_picture(FIG_PATH, width=Inches(3.25))

    p_fcap = doc.add_paragraph(style="FigureCaption")
    r_flbl = p_fcap.add_run("Figura 1:")
    r_flbl.style = "Label"
    p_fcap.add_run(
        " (a) Boxplot e dispersão individual das aberturas diárias por regime de notificação; "
        "(b) histograma das diferenças intrapares di com média (+1,11) e IC 95% ([1,02; 1,20] aberturas/dia)."
    )

    add_para(
        "O teste t pareado unilateral demonstrou diferença estatisticamente significativa (t = 24,44; gl = 193; "
        "EP = 0,0455; p = 2,80 × 10⁻⁶¹ < α = 0,05), levando à rejeição categórica de H0. O resultado foi integralmente "
        "confirmado pelo teste de permutação pareado (p < 0,0001) e pelo teste alternativo de Wilcoxon (T = 18.733,0; "
        "p = 1,14 × 10⁻³²; rrb = 0,981). O Intervalo de Confiança de 95% situa o aumento médio real entre 1,02 e 1,20 "
        "aberturas adicionais por dia, excluindo com ampla folga o valor nulo (Figura 1b). O tamanho de efeito atingiu "
        "dz = 1,75, classificado como muito grande (dz > 0,80) [2, 3]. Sob a ótica prática de Engenharia de Software, a "
        "entrega integral das 4 notificações diárias está associada a um ganho relativo de 71,2% nas aberturas do "
        "aplicativo (+1,11 sobre 1,56 aberturas/dia), evidenciando que falhas de entrega de push degradam severamente o "
        "engajamento diário."
    )

    add_head("Head2", "4.2", "Análises Exploratórias")
    add_para(
        "Em conformidade com as diretrizes de integridade científica contra p-hacking e HARKing [10], realizaram-se três "
        "testes adicionais fora da hipótese primária do protocolo, rotulados explicitamente como exploratórios: "
        "(1) Comparação por usuário-dia independente (5.168 dias completos vs. 2.335 dias parciais): o teste t de Welch "
        "confirmou a superioridade do regime completo (2,71 ± 1,38 vs. 1,56 ± 1,02 aberturas/dia; t = 40,17; gl = 5928,3; "
        "p < 0,0001; IC 95%: [1,09; 1,20]; d de Cohen = 0,90; A de Vargha-Delaney = 0,75). "
        "(2) Efeito moderador do dia da semana (avaliado nos dias com 4 notificações, n = 190 blocos pareados): dias "
        "úteis apresentaram maior média de aberturas do que finais de semana (2,72 ± 0,98 vs. 2,45 ± 1,06 aberturas/dia; "
        "t pareado = 6,28; gl = 189; p = 1,11 × 10⁻⁹; IC 95%: [0,19; 0,36]; dz = 0,46, efeito moderado). "
        "(3) Efeito moderador do estado da tela no disparo (n = 198 blocos pareados): notificações entregues quando a "
        "tela do smartphone já estava ativa no minuto anterior obtiveram taxa média de abertura de 76,9% ± 24,4%, contra "
        "61,2% ± 23,9% com a tela desligada (t pareado = 13,39; gl = 197; p = 8,41 × 10⁻³⁰; IC 95%: [+13,4; +18,0] "
        "pontos percentuais; dz = 0,95), comprovando a eficácia de arquiteturas de disparo sensíveis ao contexto [6]."
    )

    # 5 AMEAÇAS À VALIDADE
    add_head("Head1", "5", "AMEAÇAS À VALIDADE")
    add_para(
        "Seguindo a classificação de Wohlin et al. [11], discutem-se as quatro categorias de ameaças e suas mitigações: "
        "(1) Validade de Conclusão: o risco de violação de pressupostos paramétricos ou de falsos positivos por múltiplos "
        "testes foi mitigado testando formalmente a normalidade (Shapiro-Wilk, p = 0,3775), confirmando a decisão com "
        "Wilcoxon e permutação, e separando a hipótese confirmatória das análises exploratórias (relatando todos os 4 "
        "testes executados e todas as exclusões: 3 janelas com erro '-666' e 7 blocos incompletos). "
        "(2) Validade Interna: como o regime parcial ou completo não foi atribuído por sorteio, variáveis de confusão "
        "(ex.: o usuário desligar o aparelho em dias de menor disponibilidade pessoal) podem explicar parte da diferença "
        "observada; mitigou-se a heterogeneidade entre indivíduos mediante blocagem pareada por usuário e adoção de "
        "linguagem estritamente associativa (não causal). "
        "(3) Validade de Construto: receber 4 notificações proporciona mecanicamente mais oportunidades de reação no dia "
        "do que receber 1 a 3 notificações; mitigou-se essa limitação avaliando também a taxa percentual de conversão por "
        "notificação individual na Seção 4.2. "
        "(4) Validade Externa: os dados provêm de adolescentes tchecos utilizando um aplicativo de questionários (EMA), "
        "não permitindo generalização direta para adultos utilizando aplicativos bancários (transações PIX) sem "
        "replicação específica no domínio financeiro."
    )

    # 6 CONCLUSÃO E PRÓXIMOS PASSOS
    add_head("Head1", "6", "CONCLUSÃO E PRÓXIMOS PASSOS")
    add_para(
        "Em resposta à pergunta de pesquisa, conclui-se que o regime de envio completo de notificações push (4/dia) está "
        "associado a um aumento estatisticamente significativo e de grande magnitude prática (+1,11 aberturas/dia; IC 95%: "
        "[1,02; 1,20]; dz = 1,75) na frequência de aberturas do aplicativo no mesmo dia em comparação ao envio parcial, "
        "sendo positivamente moderado por disparos realizados com a tela ativa (+15,7 p.p.) e em dias úteis (+0,27 "
        "aberturas/dia). Para evoluir estes resultados preliminares para um estudo completo no domínio financeiro, "
        "propõe-se conduzir um experimento controlado aleatorizado (teste A/B) em protótipo instrumentado de alertas PIX, "
        "sorteando o disparo imediato versus agrupado para estabelecer inferência causal."
    )

    # DISPONIBILIDADE DE DADOS E CÓDIGO
    add_head("AckHead", None, "DISPONIBILIDADE DE DADOS E CÓDIGO")
    add_para(
        "A base pública original encontra-se depositada na Open Science Framework (OSF) em https://osf.io/n4sgb/ "
        "(acessada em 25/11/2026) [4]. O repositório completo da equipe contendo o protocolo, o script Python "
        "reprodutível (analise.py), os arquivos de dados limpos e as instruções passo a passo de reexecução está "
        "disponível em: https://github.com/jgabrieldsl/mceq_projeto_final. O vídeo de apresentação da equipe "
        "(YouTube, não listado, ≤ 10 min) pode ser acessado em: https://youtu.be/INSERIR_LINK_YOUTUBE_NAO_LISTADO.",
        "AckPara",
    )

    # DECLARAÇÃO DE USO DE INTELIGÊNCIA ARTIFICIAL
    add_head("AckHead", None, "DECLARAÇÃO DE USO DE INTELIGÊNCIA ARTIFICIAL")
    add_para(
        "Na elaboração deste trabalho, a ferramenta de Inteligência Artificial generativa Antigravity (Google DeepMind) "
        "foi utilizada nas seguintes etapas: (i) apoio na localização da base pública com identificador persistente na "
        "plataforma OSF; (ii) estruturação e depuração do script Python (analise.py) para limpeza reprodutível, execução "
        "dos testes estatísticos (SciPy/Statsmodels) e geração da Figura 1 (Matplotlib); e (iii) revisão textual e "
        "adequação estilística ao template da ACM. Todos os números, tabelas e figuras foram produzidos pela execução "
        "real do código sobre os dados brutos e conferidos pela equipe. Os autores declaram ter revisado integralmente o "
        "conteúdo gerado e assumem total responsabilidade pela precisão, originalidade e integridade científica do "
        "trabalho.",
        "AckPara",
    )

    # REFERÊNCIAS
    add_head("ReferenceHead", None, "REFERÊNCIAS")
    refs = [
        "[1]\tVictor R. Basili and H. Dieter Rombach. 1988. The TAME project: towards improvement-oriented software environments. IEEE Transactions on Software Engineering 14, 6 (1988), 758–773.",
        "[2]\tJacob Cohen. 1988. Statistical Power Analysis for the Behavioral Sciences (2nd ed.). Lawrence Erlbaum Associates, Hillsdale, NJ.",
        "[3]\tVigdis By Kampenes, Tore Dybå, Jo E. Hannay, and Dag I. K. Sjøberg. 2007. A systematic review of effect size in software engineering experiments. Information and Software Technology 49, 11–12 (2007), 1073–1086. DOI: https://doi.org/10.1016/j.infsof.2007.02.015",
        "[4]\tDaniel Dvořák, Martin Kreidl, and Martin Tancoš. 2026. Effects of Questionnaire Notifications on Engagement and Attrition in an Ecological Momentary Assessment Study: Longitudinal Observational Study. Reproducibility Package and Dataset. Open Science Framework (OSF). https://osf.io/n4sgb/",
        "[5]\tBarbara Ann Kitchenham, Tore Dybå, and Magne Jørgensen. 2004. Evidence-based software engineering. In Proceedings of the 26th International Conference on Software Engineering (ICSE ’04). IEEE Computer Society, Washington, DC, 273–281.",
        "[6]\tAbhinav Mehrotra and Mirco Musolesi. 2020. Intelligent Notification Systems. Synthesis Lectures on Mobile and Pervasive Computing. Morgan & Claypool Publishers, San Rafael, CA. DOI: https://doi.org/10.2200/S00965ED1V01Y201911MPC014",
        "[7]\tSherly Philip and Hidayaturrahman. 2024. Effective Approaches for User Engagement Improvement in Mobile Health Applications: A Comprehensive Literature Analysis. Jurnal EMACS (Engineering, MAthematics and Computer Science) 6, 3 (2024), 185–191. DOI: https://doi.org/10.21512/emacsjournal.v6i3.11837",
        "[8]\tDouglas C. Montgomery and George C. Runger. 2018. Applied Statistics and Probability for Engineers (7th ed.). John Wiley & Sons, Hoboken, NJ.",
        "[9]\tAtilla Wohllebe. 2020. Consumer Acceptance of App Push Notifications: Systematic Review on the Influence of Frequency. International Journal of Interactive Mobile Technologies (iJIM) 14, 13 (2020), 36–47. DOI: https://doi.org/10.3991/ijim.v14i13.14563",
        "[10]\tRonald L. Wasserstein and Nicole A. Lazar. 2016. The ASA’s statement on p-values: context, process, and purpose. The American Statistician 70, 2 (2016), 129–133. DOI: https://doi.org/10.1080/00031305.2016.1154108",
        "[11]\tClaes Wohlin, Per Runeson, Martin Höst, Magnus C. Ohlsson, Björn Regnell, and Anders Wesslén. 2012. Experimentation in Software Engineering. Springer, Berlin, Heidelberg.",
    ]
    for r_str in refs:
        add_para(r_str, "Bib_entry")

    doc.core_properties.title = "Envio de Notificações Push e Frequência Diária de Abertura de Aplicativo Móvel"
    doc.core_properties.author = "João Gabriel da Silva Leite; Yuri Cardoso Balieiro; Pedro de Mello Porto Daou"
    doc.core_properties.subject = "MCEQ 12576 - Projeto Final - PUC-Campinas"

    temp_docx = OUTPUT_DOCX + ".tmp"
    doc.save(temp_docx)

    with zipfile.ZipFile(temp_docx, "r") as zin, zipfile.ZipFile(OUTPUT_DOCX, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            content = zin.read(item.filename)
            if item.filename in ("word/header1.xml", "word/header2.xml", "docProps/app.xml"):
                text_xml = content.decode("utf-8")
                text_xml = text_xml.replace("WOODSTOCK’18, ", "MCEQ 12576 – Projeto Final, ")
                text_xml = text_xml.replace("June,", "2º Semestre")
                text_xml = text_xml.replace(" 2018, El Paso, Texas USA", " de 2026, PUC-Campinas")
                text_xml = text_xml.replace("F. Surname et al.", "J. G. S. Leite, Y. C. Balieiro e P. M. P. Daou")
                text_xml = text_xml.replace("Insert Your Title Here", "Notificações Push e Frequência Diária de Abertura de App")
                content = text_xml.encode("utf-8")
            zout.writestr(item, content)

    os.remove(temp_docx)
    print(f"Artigo atualizado com sucesso em: {OUTPUT_DOCX}")


if __name__ == "__main__":
    build_docx()
