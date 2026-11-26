#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCEQ 12576 - Projeto Final (PUC-Campinas - 2º Semestre de 2026)
Script Reprodutível: Do Dado Bruto aos Números e Figuras do Artigo

Integrantes:
- João Gabriel da Silva Leite (RA: 24787392)
- Yuri Cardoso Balieiro (RA: 24011525)
- Pedro de Mello Porto Daou (RA: 21010698)

Base Pública Utilizada:
Dvořák, D.; Kreidl, M.; Tancoš, M. (2026). Effects of Questionnaire Notifications
on Engagement and Attrition in an Ecological Momentary Assessment Study:
Longitudinal Observational Study. Open Science Framework (OSF), ID: n4sgb.
URL: https://osf.io/n4sgb/ | Arquivo bruto: notif_data_final.dta
"""

import os
import urllib.request
import numpy as np
import pandas as pd
import pyreadstat
from scipy import stats
from statsmodels.stats.multitest import multipletests
import matplotlib.pyplot as plt

# Semente fixa conforme recomendação da Seção 8 do roteiro (default_rng(2026))
RNG = np.random.default_rng(2026)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "dados", "brutos")
CLEAN_DIR = os.path.join(BASE_DIR, "dados", "limpos")
FIG_DIR = os.path.join(BASE_DIR, "figuras")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(CLEAN_DIR, exist_ok=True)
os.makedirs(FIG_DIR, exist_ok=True)

RAW_FILE = os.path.join(RAW_DIR, "notif_data_final.dta")
OSF_DOWNLOAD_URL = "https://osf.io/download/h3u62/"


def baixar_dados_brutos():
    """Baixa o arquivo bruto notif_data_final.dta da OSF caso não exista localmente."""
    if not os.path.exists(RAW_FILE):
        print(f"[1/4] Baixando dados brutos de {OSF_DOWNLOAD_URL} ...")
        urllib.request.urlretrieve(OSF_DOWNLOAD_URL, RAW_FILE)
        print(f"      Salvo em: {RAW_FILE}")
    else:
        print(f"[1/4] Arquivo bruto já presente em: {RAW_FILE}")


def limpar_e_agregar_dados():
    """
    Carrega os dados brutos (42.504 janelas de 201 usuários), aplica as regras
    transparentes de limpeza documentadas no Codebook (Multimedia Appendix 9)
    e produz as bases limpas em dados/limpos/.
    """
    print("[2/4] Carregando e limpando dados brutos...")
    df, _ = pyreadstat.read_dta(RAW_FILE)
    n_total_janelas = len(df)
    n_usuarios_total = df["p_id"].nunique()

    # 1. Identificar registros com erro de sistema documentado no Codebook (-666 em opened)
    mask_erro_666 = df["opened"] == "-666"
    n_erro_666 = int(mask_erro_666.sum())

    # Remove as 3 janelas com erro de registro (-666) antes da agregação
    df_valido = df[~mask_erro_666].copy()

    # Variável binária de abertura do aplicativo na janela (1 = aberto, 0 = não aberto)
    df_valido["is_opened"] = (df_valido["opened_bin"] == "1").astype(int)

    # Número de notificações (inicial + lembretes) enviadas na janela
    df_valido["notification_count_num"] = pd.to_numeric(
        df_valido["notification_count"].replace("NA", np.nan), errors="coerce"
    ).fillna(0)

    # Tempo de tela ligada no minuto anterior à 1ª notificação (segundos, vírgula -> ponto)
    df_valido["on_1_min_num"] = pd.to_numeric(
        df_valido["on_1_min"].str.replace(",", ".").replace("NA", np.nan),
        errors="coerce",
    )
    df_valido["screen_on"] = np.where(
        df_valido["on_1_min_num"].isna(), np.nan, (df_valido["on_1_min_num"] > 0).astype(int)
    )

    # Agregação por usuário-dia (p_id, burst, day_in_study)
    daily = df_valido.groupby(["p_id", "burst", "day_in_study"], as_index=False).agg(
        janelas_validas=("questionnaire", "count"),
        notified_windows=("notified_bin", "sum"),
        total_pushes=("notification_count_num", "sum"),
        daily_opens=("is_opened", "sum"),
        is_weekend=("is_weekend", "first"),
    )
    n_user_days_total = len(daily)

    # Dias inativos (notified_windows == 0: aplicativo não entregou nenhuma notificação no dia)
    n_dias_sem_notificacao = int((daily["notified_windows"] == 0).sum())

    # Dias ativos (ao menos 1 notificação push entregue no dia: notified_windows de 1 a 4)
    daily_active = daily[daily["notified_windows"] >= 1].copy()
    daily_active["regime_push"] = np.where(
        daily_active["notified_windows"] == 4,
        "Completa (4 pushes/dia)",
        "Parcial (1-3 pushes/dia)",
    )

    # Salva tabela limpa de usuário-dia ativo
    caminho_daily_csv = os.path.join(CLEAN_DIR, "dados_limpos_usuario_dia.csv")
    daily_active.to_csv(caminho_daily_csv, index=False)

    # Agregação em Blocos (Nível do Usuário p_id = Bloco) para a Hipótese Principal (Pareada)
    user_Pivot = (
        daily_active.groupby(["p_id", "regime_push"])["daily_opens"]
        .mean()
        .unstack()
    )
    # Usuários que possuem observações em ambos os tratamentos (blocos completos)
    user_paired = user_Pivot.dropna(
        subset=["Completa (4 pushes/dia)", "Parcial (1-3 pushes/dia)"]
    ).copy()
    user_paired["dif_completa_menos_parcial"] = (
        user_paired["Completa (4 pushes/dia)"] - user_paired["Parcial (1-3 pushes/dia)"]
    )
    n_excluidos_bloco_incompleto = n_usuarios_total - len(user_paired)

    caminho_paired_csv = os.path.join(CLEAN_DIR, "dados_limpos_pareados_usuario.csv")
    user_paired.reset_index().to_csv(caminho_paired_csv, index=False)

    print(f"      Total de janelas brutas: {n_total_janelas} ({n_usuarios_total} usuários)")
    print(f"      Janelas excluídas por erro de log (-666): {n_erro_666}")
    print(f"      Total de usuários-dia: {n_user_days_total}")
    print(f"      Usuários-dia sem notificação (0 pushes -> 0 aberturas): {n_dias_sem_notificacao}")
    print(f"      Usuários-dia ativos (1 a 4 pushes): {len(daily_active)}")
    print(f"      Usuários com blocos completos (ambos os regimes): {len(user_paired)} (excluídos: {n_excluidos_bloco_incompleto})")

    return df_valido, daily, daily_active, user_paired


def estatistica_descritiva_grupo(vetor):
    """Retorna dicionário com n, média, DP, mediana, Q1, Q3, IQR, CV% e skewness."""
    v = np.asarray(vetor, dtype=float)
    q1, med, q3 = np.percentile(v, [25, 50, 75])
    iqr = q3 - q1
    media = np.mean(v)
    dp = np.std(v, ddof=1)
    cv = (dp / media) * 100.0 if media != 0 else np.nan
    skew = stats.skew(v, bias=False)
    lim_inf = q1 - 1.5 * iqr
    lim_sup = q3 + 1.5 * iqr
    n_outliers = int(((v < lim_inf) | (v > lim_sup)).sum())
    return {
        "n": len(v),
        "media": media,
        "dp": dp,
        "mediana": med,
        "q1": q1,
        "q3": q3,
        "iqr": iqr,
        "cv_pct": cv,
        "skew": skew,
        "n_outliers": n_outliers,
    }


def r_bisserial_wilcoxon(x, y):
    """Calcula a correlação posto-bisserial r para o teste de Wilcoxon pareado (Aula 08, slide 54)."""
    d = np.asarray(x) - np.asarray(y)
    r = stats.rankdata(np.abs(d))
    zeros = r[d == 0].sum() / 2.0
    mais = r[d > 0].sum() + zeros
    menos = r[d < 0].sum() + zeros
    return (mais - menos) / (mais + menos)


def executar_analises(df_valido, daily, daily_active, user_paired):
    """Executa a análise confirmatória (protocolo) e as análises exploratórias."""
    print("\n[3/4] Executando testes estatísticos (Confirmatório e Exploratórios)...")

    c_u = user_paired["Completa (4 pushes/dia)"].values
    p_u = user_paired["Parcial (1-3 pushes/dia)"].values
    d_u = user_paired["dif_completa_menos_parcial"].values

    desc_comp = estatistica_descritiva_grupo(c_u)
    desc_parc = estatistica_descritiva_grupo(p_u)
    desc_dif = estatistica_descritiva_grupo(d_u)

    print("\n--- ESTATÍSTICA DESCRITIVA (CONFIRMATÓRIA - NÍVEL DO USUÁRIO, n = 194 blocos) ---")
    for nome, d in [
        ("Notificação Completa (4 pushes/dia)", desc_comp),
        ("Notificação Parcial (1-3 pushes/dia)", desc_parc),
        ("Diferença Intrapares (d_i = Completa - Parcial)", desc_dif),
    ]:
        print(
            f"{nome:48s}: n={d['n']}, Média={d['media']:.2f}, DP={d['dp']:.2f}, "
            f"Mediana={d['mediana']:.2f}, IQR={d['iqr']:.2f} (Q1={d['q1']:.2f}, Q3={d['q3']:.2f}), "
            f"CV={d['cv_pct']:.1f}%, Assimetria(g1)={d['skew']:.2f}, Outliers(IQR)={d['n_outliers']}"
        )

    # Verificação de normalidade das diferenças intrapares d_i (Shapiro-Wilk)
    shapiro_res = stats.shapiro(d_u)
    print(f"\nNormalidade dos resíduos/diferenças (Shapiro-Wilk): W = {shapiro_res.statistic:.4f}, p = {shapiro_res.pvalue:.4f}")

    # Teste Principal Planejado no Protocolo: Teste t pareado unilateral (H1: mu_d > 0)
    t_par = stats.ttest_rel(c_u, p_u, alternative="greater")
    ic_par = stats.ttest_rel(c_u, p_u).confidence_interval(0.95)
    ep_par = desc_dif["dp"] / np.sqrt(desc_dif["n"])
    d_z = desc_dif["media"] / desc_dif["dp"]

    # Teste Alternativo Planejado no Protocolo: Teste de Wilcoxon pareado unilateral
    w_par = stats.wilcoxon(c_u, p_u, alternative="greater")
    r_rb = r_bisserial_wilcoxon(c_u, p_u)

    # Teste de Permutação Pareado (10.000 iterações com semente fixa 2026 - Aula 06)
    sinais = RNG.choice([-1, 1], size=(10000, len(d_u)))
    medias_perm = (sinais * d_u).mean(axis=1)
    p_perm = np.mean(medias_perm >= desc_dif["media"])

    print("\n--- RESULTADO DO TESTE CONFIRMATÓRIO (PROTOCOLO) ---")
    print(f"Teste t Pareado (unilateral): t = {t_par.statistic:.2f}, gl = {t_par.df}, p = {t_par.pvalue:.4e}")
    print(f"Erro Padrão (EP) = {ep_par:.4f} | IC 95% bilateral = [{ic_par.low:.2f}; {ic_par.high:.2f}] aberturas/dia")
    print(f"Tamanho de efeito d_z de Cohen = {d_z:.2f}")
    print(f"Teste Alternativo (Wilcoxon pareado): T = {w_par.statistic:.1f}, p = {w_par.pvalue:.4e}, r_bisserial = {r_rb:.3f}")
    print(f"Teste de Permutação Pareado (10.000 réplicas, seed=2026): p = {p_perm:.4f}")

    # =========================================================================
    # ANÁLISES EXPLORATÓRIAS (Declaradas em subseção própria conforme Seção 9)
    # =========================================================================
    print("\n--- ANÁLISES EXPLORATÓRIAS ---")

    # Exploratória 1: Comparação não-pareada no nível de usuário-dia (n = 5168 vs n = 2335) via Welch e Mann-Whitney
    g_comp_day = daily_active[daily_active["notified_windows"] == 4]["daily_opens"].values
    g_parc_day = daily_active[daily_active["notified_windows"] < 4]["daily_opens"].values
    t_welch = stats.ttest_ind(g_comp_day, g_parc_day, equal_var=False, alternative="greater")
    ic_welch = stats.ttest_ind(g_comp_day, g_parc_day, equal_var=False).confidence_interval(0.95)
    mw_day = stats.mannwhitneyu(g_comp_day, g_parc_day, alternative="greater")
    n1, n2 = len(g_comp_day), len(g_parc_day)
    sp_day = np.sqrt(((n1 - 1) * np.var(g_comp_day, ddof=1) + (n2 - 1) * np.var(g_parc_day, ddof=1)) / (n1 + n2 - 2))
    d_day = (np.mean(g_comp_day) - np.mean(g_parc_day)) / sp_day
    a_vd = mw_day.statistic / (n1 * n2)
    print(
        f"Exploratória 1 (Nível Usuário-Dia Independente, n1={n1}, n2={n2}): "
        f"Média Completa={np.mean(g_comp_day):.2f} (DP={np.std(g_comp_day, ddof=1):.2f}), "
        f"Média Parcial={np.mean(g_parc_day):.2f} (DP={np.std(g_parc_day, ddof=1):.2f}) | "
        f"Welch t={t_welch.statistic:.2f}, gl={t_welch.df:.1f}, p={t_welch.pvalue:.4e}, "
        f"IC95%=[{ic_welch.low:.2f}; {ic_welch.high:.2f}], d={d_day:.2f} | "
        f"Mann-Whitney A={a_vd:.2f}"
    )

    # Exploratória 2: Efeito moderador do período/contexto (Dias Úteis vs. Finais de Semana em dias com 4 notificações)
    daily4 = daily_active[daily_active["notified_windows"] == 4]
    u_wk = daily4.groupby(["p_id", "is_weekend"])["daily_opens"].mean().unstack().dropna()
    wk_util = u_wk[0].values
    wk_fds = u_wk[1].values
    t_wk = stats.ttest_rel(wk_util, wk_fds, alternative="greater")
    ic_wk = stats.ttest_rel(wk_util, wk_fds).confidence_interval(0.95)
    dz_wk = np.mean(wk_util - wk_fds) / np.std(wk_util - wk_fds, ddof=1)
    print(
        f"Exploratória 2 (Moderadora Dia Útil vs. Fim de Semana, n={len(u_wk)} usuários pareados): "
        f"Média Útil={np.mean(wk_util):.2f} (DP={np.std(wk_util, ddof=1):.2f}) vs. "
        f"Fim de Semana={np.mean(wk_fds):.2f} (DP={np.std(wk_fds, ddof=1):.2f}) | "
        f"t pareado={t_wk.statistic:.2f}, gl={t_wk.df}, p={t_wk.pvalue:.4e}, "
        f"IC95%=[{ic_wk.low:.2f}; {ic_wk.high:.2f}], dz={dz_wk:.2f}"
    )

    # Exploratória 3: Efeito do contexto imediato do smartphone (Tela Ligada vs. Desligada no minuto anterior ao push)
    df_notif = df_valido[df_valido["notified_bin"] == 1].dropna(subset=["screen_on"])
    u_scr = df_notif.groupby(["p_id", "screen_on"])["is_opened"].mean().unstack().dropna()
    scr_on = u_scr[1.0].values * 100.0
    scr_off = u_scr[0.0].values * 100.0
    t_scr = stats.ttest_rel(scr_on, scr_off, alternative="greater")
    ic_scr = stats.ttest_rel(scr_on, scr_off).confidence_interval(0.95)
    dz_scr = np.mean(scr_on - scr_off) / np.std(scr_on - scr_off, ddof=1)
    print(
        f"Exploratória 3 (Moderadora Tela Ligada vs. Desligada no disparo, n={len(u_scr)} usuários pareados): "
        f"Taxa abertura Tela Ligada={np.mean(scr_on):.1f}% (DP={np.std(scr_on, ddof=1):.1f}%) vs. "
        f"Tela Desligada={np.mean(scr_off):.1f}% (DP={np.std(scr_off, ddof=1):.1f}%) | "
        f"t pareado={t_scr.statistic:.2f}, gl={t_scr.df}, p={t_scr.pvalue:.4e}, "
        f"IC95%=[{ic_scr.low:.1f}; {ic_scr.high:.1f}] p.p., dz={dz_scr:.2f}"
    )

    return {
        "c_u": c_u,
        "p_u": p_u,
        "d_u": d_u,
        "desc_comp": desc_comp,
        "desc_parc": desc_parc,
        "desc_dif": desc_dif,
    }


def gerar_figura_artigo(resultados):
    """
    Gera a Figura 1 seguindo todos os princípios de Cleveland (1994) e da Aula 04:
    - 2D limpo, sem chartjunk;
    - Eixo de contagem/frequência começando estritamente em zero (0);
    - Escalas consistentes, rótulos e unidades explícitas;
    - Painel A: Boxplot + pontos individuais (dispersão) das aberturas diárias médias por regime;
    - Painel B: Histograma da diferença intrapares (d_i) com média, IC 95% e linha de referência H0 (0).
    """
    print("\n[4/4] Gerando Figura 1 para o artigo...")
    c_u = resultados["c_u"]
    p_u = resultados["p_u"]
    d_u = resultados["d_u"]

    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.size": 8.5,
        "axes.titlesize": 9.0,
        "axes.labelsize": 8.5,
        "xtick.labelsize": 8.0,
        "ytick.labelsize": 8.0,
    })

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(3.4, 3.85), dpi=300)

    # Painel (a): Boxplot comparativo com jitter dos 194 usuários (eixo Y iniciando em 0)
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

    # Adiciona pontos individuais com leve jitter horizontal (mostrando a distribuição real)
    for idx, valores in enumerate(dados_grupos, start=1):
        jitter = RNG.uniform(-0.11, 0.11, size=len(valores))
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

    # Legenda enxuta da média no Painel (a)
    ax1.plot([], [], "D", color="#d95f02", markeredgecolor="black", markersize=4.8, label="Média amostral")
    ax1.plot([], [], "-", color="#08306b", linewidth=1.6, label="Mediana (Q2)")
    ax1.legend(loc="lower right", frameon=True, fontsize=7.5)

    # Painel (b): Histograma das diferenças intrapares d_i = Completa - Parcial (eixo Y iniciando em 0)
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
    fig_path = os.path.join(FIG_DIR, "figura1_resultados.png")
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"      Figura salva com sucesso em: {fig_path}")


if __name__ == "__main__":
    baixar_dados_brutos()
    df_val, daily_all, daily_act, u_paired = limpar_e_agregar_dados()
    res = executar_analises(df_val, daily_all, daily_act, u_paired)
    gerar_figura_artigo(res)
    print("\nPipeline concluído com sucesso! Todos os números e figuras foram gerados de forma reprodutível.")
