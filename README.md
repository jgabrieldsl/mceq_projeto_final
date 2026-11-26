# MCEQ 12576 – Projeto Final: Notificações Push e Frequência Diária de Abertura de Aplicativo Móvel

Repositório oficial de reprodutibilidade da equipe para o Projeto Final da disciplina **12576 – Métodos de Computação Experimental e Quantitativa** (PUC-Campinas – Escola Politécnica – Engenharia de Software, 2º Semestre de 2026).

**Docentes:** Prof. Dr. Wemerson D. Parreira e Prof. Dr. Leonardo N. Ferreira

## Integrantes da Equipe
- **João Gabriel da Silva Leite** (RA: 24787392) – `joao.gsl@puccampinas.edu.br`
- **Yuri Cardoso Balieiro** (RA: 24011525) – `yuri.cb@puccampinas.edu.br`
- **Pedro de Mello Porto Daou** (RA: 21010698) – `pedro.mpd@puccampinas.edu.br`

---

## 1. Pergunta de Pesquisa e Hipóteses (Protocolo)

- **Pergunta de Pesquisa (GQM):** *"Em usuários de um aplicativo móvel com coleta longitudinal, o regime de envio completo de notificações push diárias (4 notificações/dia) está associado a um maior número médio de aberturas do aplicativo no mesmo dia, em comparação ao regime de envio parcial (1 a 3 notificações/dia)?"*
- **Desenho:** Estudo empírico observacional longitudinal com **desenho pareado em blocos por usuário** (`p_id`), onde cada usuário ($n = 194$ blocos completos) é avaliado sob ambos os regimes diários de entrega de notificações push.
- **Hipótese Nula ($H_0$):** $\mu_d = 0$ (não há diferença na média populacional de aberturas do aplicativo no mesmo dia entre os regimes de notificação completa e parcial, onde $\mu_d = \mu_{\text{completa}} - \mu_{\text{parcial}}$).
- **Hipótese Alternativa ($H_1$, unilateral):** $\mu_d > 0$ (dias com regime de notificação push completa estão associados a uma maior média de aberturas do aplicativo no mesmo dia).
- **Nível de significância fixado a priori:** $\alpha = 0,05$.

---

## 2. Origem dos Dados Públicos (Proveniência e Licença)

- **Título da Base / Pacote de Reprodutibilidade:** *Effects of Questionnaire Notifications on Engagement and Attrition in an Ecological Momentary Assessment Study: Longitudinal Observational Study (FUTURE Project)*
- **Autores Originais:** Daniel Dvořák, Martin Kreidl e Martin Tancoš (2026)
- **Repositório / Identificador Persistente:** Open Science Framework (OSF) – Node ID: `n4sgb`
- **Link Direto da Fonte Original:** https://osf.io/n4sgb/
- **Link Direto de Download do Dado Bruto (`notif_data_final.dta`):** https://osf.io/download/h3u62/
- **Dicionário de Variáveis Original (`Multimedia_Appendix_9_Codebook.docx`):** https://osf.io/download/2p4kc/
- **Data de Acesso e Download:** 25/11/2026
- **Licença:** Pacote público de reprodutibilidade aberta depositado na OSF para uso e verificação acadêmica.

---

## 3. Estrutura do Repositório

```text
.
├── README.md                                    # Documentação da pergunta, proveniência e instruções
├── requirements.txt                             # Versões exatas das bibliotecas Python utilizadas
├── protocolo_1_pagina.md                        # Protocolo de 1 página (Seção 4 das Orientações)
├── analise.py                                   # Script principal executável do início ao fim (bruto -> limpo -> testes -> figura)
├── gerar_artigo_docx.py                         # Script que monta o artigo formatado no template ACM Word
├── artigo_final_MCEQ.docx                       # Artigo científico final no template ACM (≤ 4 páginas)
├── roteiro_video.md                             # Roteiro cronometrado do vídeo (≤ 10 min) dividido entre os 3 membros
├── dados/
│   ├── brutos/
│   │   └── notif_data_final.dta                 # Base bruta original da OSF (nunca editada à mão; baixada automaticamente se ausente)
│   └── limpos/
│       ├── dados_limpos_usuario_dia.csv         # 7.503 usuários-dia ativos gerados por analise.py
│       └── dados_limpos_pareados_usuario.csv    # 194 blocos (usuários pareados) gerados por analise.py
└── figuras/
    └── figura1_resultados.png                   # Figura 1 do artigo (300 DPI) gerada por analise.py
```

---

## 4. Passo a Passo para Reexecutar (Reprodutibilidade)

Qualquer pessoa de fora da equipe pode clonar este repositório e obter exatamente os mesmos números, tabelas e figuras do artigo seguindo os 3 passos abaixo no terminal (macOS / Linux / Windows):

### Passo 1: Criar e ativar um ambiente virtual Python (opcional, recomendado)
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Passo 2: Instalar as dependências listadas em `requirements.txt`
```bash
pip install -r requirements.txt
```

### Passo 3: Executar o pipeline completo de análise (`analise.py`)
```bash
python3 analise.py
```

**O que o comando `python3 analise.py` faz automaticamente:**
1. Verifica se `dados/brutos/notif_data_final.dta` existe; caso não exista, baixa diretamente da OSF (`https://osf.io/download/h3u62/`);
2. Aplica a limpeza documentada (remove as 3 janelas com código de erro `-666` de um total de 42.504 janelas), agrega os 7.503 usuários-dia ativos e os $n = 194$ usuários com blocos completos, salvando os CSVs em `dados/limpos/`;
3. Imprime no terminal todas as estatísticas descritivas (Tabela 1), o teste de normalidade de Shapiro-Wilk ($W = 0,9921, p = 0,3775$), o teste $t$ pareado unilateral ($t = 24,44, gl = 193, p = 2,80 \times 10^{-61}$), o IC 95% ($[1,02; 1,20]$), o tamanho de efeito $d_z = 1,75$, o teste alternativo de Wilcoxon ($T = 18.733,0, p = 1,14 \times 10^{-32}, r_{rb} = 0,981$), o teste de permutação com semente fixa `default_rng(2026)` ($p < 0,0001$) e as 3 análises exploratórias;
4. Gera e salva a figura `figuras/figura1_resultados.png` em alta resolução (300 DPI).
