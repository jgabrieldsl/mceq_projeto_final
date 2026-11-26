# Checklist Final de Entrega – MCEQ 12576 (Seção 10)

**Equipe:** João Gabriel da Silva Leite (RA: 24787392), Yuri Cardoso Balieiro (RA: 24011525) e Pedro de Mello Porto Daou (RA: 21010698)  
**Disciplina:** 12576 – Métodos de Computação Experimental e Quantitativa (PUC-Campinas, 2º Semestre de 2026)

---

## 1. Regras Formais (`[REGRA]` – Seção 10.1)

| # | Item do Checklist Oficial (Roteiro MCEQ, p. 11) | Status | Onde / Como foi atendido no projeto |
| :-: | :--- | :-: | :--- |
| **1** | Artigo no template ACM fornecido, com **no máximo 4 páginas incluindo referências**. | ✅ Concluído | Arquivo `artigo_final_MCEQ.docx` gerado diretamente sobre o `template_relatoriofinal.docx`, ocupando ~3,75 páginas (terminando na página 4 após a referência `[11]`). |
| **2** | Todo o **conteúdo de exemplo do template removido** (`WOODSTOCK'18`, DOI fictício, bloco de copyright, `ACM Reference Format`, referências e textos de exemplo). | ✅ Concluído | Varredura automatizada em todos os XMLs internos do `.docx` (`word/document.xml`, `header1.xml`, `header2.xml`, `docProps/app.xml`): **0 resíduos** encontrados. |
| **3** | Dados **exclusivamente de base(s) pública(s)**, com origem identificada no Método. | ✅ Concluído | Base pública do *Open Science Framework* (`https://osf.io/n4sgb/`, Dvořák et al., 2026), detalhada na Seção 3.1 com URL persistente, versão, licença acadêmica e data de acesso. |
| **4** | **Estudo observacional declarado como tal** (se for o caso), sem afirmações causais. | ✅ Concluído | Declarado explicitamente como *observacional longitudinal* no Título, Resumo, Introdução, Método, Ameaças à Validade e Conclusão, utilizando apenas linguagem associativa. |
| **5** | Ao menos **1 hipótese testada por completo**: descritiva, teste adequado, p-valor, tamanho de efeito, IC ou gráfico, interpretação. | ✅ Concluído | Seção 4.1: Tabela 1 descritiva completa + Figura 1 dupla + teste $t$ pareado unilateral ($t = 24,44$; $gl = 193$; $p = 2,80 \times 10^{-61}$) + $d_z = 1,75$ + IC 95% $[1,02;\; 1,20]$ aberturas/dia + interpretação prática em Engenharia de Software. |
| **6** | **Limitações e próximos passos** declarados. | ✅ Concluído | Seção 5 (*Ameaças à Validade*) e Seção 6 (*Conclusão e Próximos Passos*), indicando a necessidade de experimento controlado (teste A/B aleatorizado). |
| **7** | **Link do vídeo dentro do artigo**. | ⏳ Pendente (Gravação) | Já posicionado em **2 locais** do `.docx` (*Nota do Título* na pág. 1 e *Disponibilidade de Dados e Código* na pág. 4). Falta apenas substituir a URL provisória pelo link real do YouTube. |
| **8** | Vídeo no **YouTube, “não listado”, $\le 10\text{ min}$**, com todos os membros apresentando uma parte identificada. | ⏳ Pendente (Gravação) | Roteiro cronometrado de 8min30s pronto em `roteiro_video.md`, com divisão equilibrada entre João Gabriel, Yuri e Pedro. |
| **9** | **Link do vídeo testado em janela anônima**. | ⏳ Pendente (Pós-vídeo) | Testar o link do YouTube em aba anônima antes de exportar o PDF final do artigo. |
| **10** | **Repositório com dados (ou link), script/notebook e instruções**; link no artigo. | ⏳ Pendente (Upload GitHub) | Repositório 100% pronto localmente (`analise.py`, `README.md`, `requirements.txt`, `dados/brutos/`, `dados/limpos/`, `figuras/`, `protocolo_1_pagina.md`). Falta apenas subir no GitHub e colar a URL real na pág. 4 do artigo. |
| **11** | Seção **“Declaração de Uso de Inteligência Artificial”** preenchida, antes das Referências (inclusive se não houve uso). | ✅ Concluído | Seção não numerada posicionada imediatamente antes de `REFERÊNCIAS` na página 4, seguindo exatamente o modelo da Seção 9.1. |
| **12** | **Entrega via Canvas** no dia da aula. | ⏳ Pendente (Entrega) | Exportar o `.docx` final (com os links reais do GitHub e YouTube) para PDF e enviar no Canvas. |

---

## 2. Checklist de Qualidade (`[RECOMENDAÇÃO]` – Seção 10.2)

| # | Item de Qualidade (Roteiro MCEQ, p. 11) | Status | Onde / Como foi atendido no projeto |
| :-: | :--- | :-: | :--- |
| **1** | **$H_0/H_1$ do artigo coincidem com as do protocolo** (ou a mudança está declarada). | ✅ Concluído | Coincidem integralmente entre `protocolo_1_pagina.md` e a Seção 1 do artigo ($H_0: \mu_d \le 0$ vs. $H_1: \mu_d > 0$), com adaptação da Ficha da Semana 4 declarada conforme a Seção 3.3. |
| **2** | **Análises fora do protocolo estão rotuladas como exploratórias**. | ✅ Concluído | Separadas na subseção **`4.2 Análises Exploratórias`** (comparação no nível usuário-dia, efeito moderador de dia útil vs. fim de semana e estado da tela `screen_on`). |
| **3** | **Figuras com eixos, unidades e legenda; barras começando em zero**. | ✅ Concluído | `figuras/figura1_resultados.png` empilhada verticalmente em 300 DPI: ambos os painéis `(a)` e `(b)` iniciam o eixo Y estritamente em `0`, com rótulos, unidades (`aberturas/dia` e `nº de usuários`) e legenda. |
| **4** | **Ameaças à validade cobrem os quatro tipos** (conclusão, interna, construção, externa). | ✅ Concluído | Seção 5 discute separadamente Validade de Conclusão, Validade Interna, Validade de Construção e Validade Externa, incluindo as mitigações adotadas. |
| **5** | **Todas as referências existem e foram consultadas** pela equipe. | ✅ Concluído | 11 referências reais e verificáveis (`[1]` a `[11]`), integrando as 3 revisões sistemáticas da Semana 5, o pacote de dados do OSF e a bibliografia oficial da disciplina. |
| **6** | **Alguém de fora da equipe reexecutou o repositório** e obteve os mesmos números. | ✅ Concluído | Pipeline `analise.py` 100% determinístico com semente fixa `np.random.default_rng(2026)` e download automático da base bruta do OSF. |
| **7** | **Todos os membros conseguem explicar o teste escolhido e o resultado** (arguição). | ✅ Concluído | Explicação detalhada do desenho em blocos pareados, teste $t$ pareado, Wilcoxon, $d_z$ de Cohen e IC 95% incluída no `roteiro_video.md` e no `protocolo_1_pagina.md`. |

---

## 3. Auditoria Específica de Estrutura e Espaço no Template ACM (Seção 5, p. 7)

| Parte no Template ACM | Regra do Roteiro (Seção 5) | Status | Implementação no `artigo_final_MCEQ.docx` |
| :--- | :--- | :-: | :--- |
| **Título e Autores** | Título informativo; nomes, curso, PUC-Campinas, e-mails; *Title Note* (`*`) com link do vídeo. | ✅ Concluído | Título declarando variáveis e estudo observacional; 3 autores com RA, curso e e-mail institucional; *Title Note* no rodapé da 1ª coluna. |
| **`ABSTRACT` $\to$ `RESUMO`** | Traduzido para `RESUMO`; **120 a 180 palavras** contendo problema, base, método, resultado com números e limitação. | ✅ Concluído | Título `RESUMO` no estilo `AbsHead`; texto com exatas **165 palavras** cobrindo os 5 elementos exigidos. |
| **`KEYWORDS` $\to$ `PALAVRAS-CHAVE`** | Traduzido para `PALAVRAS-CHAVE`; **3 a 5 termos**. | ✅ Concluído | Título `PALAVRAS-CHAVE` no estilo `KeyWordHead`; **5 termos** separados por vírgula. |
| **`1 INTRODUÇÃO`** | Problema e relevância em ES; pergunta de pesquisa; $H_0/H_1$ explícitas; tipo de estudo. | ✅ Concluído | Seção 1 completa com adaptação da Ficha de Hipótese, pergunta, fórmulas de $H_0$ e $H_1$ e declaração de estudo observacional. |
| **`2 TRABALHOS RELACIONADOS`** | Breve: 2 a 4 estudos, incluindo o artigo de origem dos dados e revisão da Semana 5. | ✅ Concluído | Seção 2 sintetizando Wohllebe (2020), Philip & Hidayaturrahman (2024), Mehrotra & Musolesi (2020) e Dvořák et al. (2026). |
| **`3 MÉTODO`** | Base (origem, DOI, licença, medição); variáveis e unidades; limpeza; desenho; teste, $\alpha$ e justificativa; efeito e IC. | ✅ Concluído | Subseções `3.1` a `3.4` cobrindo proveniência, *Screen Time API*, limpeza dos códigos `-666`, blocagem por usuário ($n=194$) e fórmulas. |
| **`4 RESULTADOS PRELIMINARES`** | Descritiva (tabela); 1 figura; resultado com $p$-valor, efeito e IC; interpretação; separar confirmatório de exploratório. | ✅ Concluído | Subseções `4.1 Análise Confirmatória (Planejada no Protocolo)` (com Tabela 1 e Figura 1) e `4.2 Análises Exploratórias`. |
| **`5 AMEAÇAS À VALIDADE`** | Conclusão, interna, construção e externa (Semana 3), com mitigações. | ✅ Concluído | Seção 5 estruturada nos 4 tipos clássicos de Wohlin et al. (2012) com as mitigações aplicadas. |
| **`6 CONCLUSÃO E PRÓXIMOS PASSOS`** | Resposta à pergunta sem extrapolar; o que falta para um estudo completo. | ✅ Concluído | Seção 6 respondendo à pergunta com base nas evidências e propondo experimento controlado A/B. |
| **`DISPONIBILIDADE DE DADOS E CÓDIGO`** | Link do repositório, link/DOI da base, data de acesso e link do vídeo. | ✅ Concluído | Posicionada no bloco de *Acknowledgments* antes da declaração de IA. |
| **`DECLARAÇÃO DE USO DE IA`** | Obrigatória, sem número, imediatamente antes das Referências (modelo da Seção 9.1). | ✅ Concluído | Posicionada sem numeração logo acima de `REFERÊNCIAS`, especificando ferramenta, etapas e responsabilidade dos autores. |
| **`REFERENCES` $\to$ `REFERÊNCIAS`** | Traduzido para `REFERÊNCIAS`; numeradas no formato ACM; reais e verificáveis. | ✅ Concluído | 11 referências reais numeradas (`[1]` a `[11]`) no estilo `Bib_entry`. |
