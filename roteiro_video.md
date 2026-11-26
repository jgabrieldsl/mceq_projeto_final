# Roteiro Cronometrado do Vídeo da Equipe (Máx. 10 Minutos)

**Disciplina:** MCEQ 12576 – Métodos de Computação Experimental e Quantitativa (PUC-Campinas – 2º Semestre de 2026)  
**Regras Críticas (Seção 7):**
- Duração máxima: **10:00 minutos** (sugestão abaixo fechando em **8:30 min**, com **1:30 min de folga** para transições);
- Publicar no **YouTube** como **"Não listado"** (nunca como "Privado");
- **Todos os 3 membros devem apresentar uma parte identificada** (dizer o nome ao começar sua fala);
- Colar o link definitivo do YouTube no `artigo_final_MCEQ.docx` (na Nota do Título da pág. 1 e na seção *Disponibilidade de Dados e Código* da pág. 4) e **testar o link em uma janela anônima** antes de exportar o PDF final.

---

## Divisão Equilibrada entre os 3 Integrantes

| Integrante | Blocos que apresenta | Tempo estimado |
| :--- | :--- | :---: |
| **1. João Gabriel da Silva Leite** | Bloco 1 (Problema, Adaptação do Protocolo e Hipóteses) + Bloco 2 (Parte A: Base Pública OSF e Proveniência) | ~2 min 45 s |
| **2. Yuri Cardoso Balieiro** | Bloco 2 (Parte B: Limpeza, Desenho em Blocos e Escolha do Teste) + Bloco 3 (Resultado Principal, Figura 1 e Decisão de Engenharia) | ~3 min 15 s |
| **3. Pedro de Mello Porto Daou** | Bloco 4 (Análises Exploratórias e as 4 Ameaças à Validade) + Bloco 5 (Conclusão, Reprodutibilidade e Próximos Passos) | ~2 min 30 s |

---

## Fala Passo a Passo (Pronta para Apresentar)

### BLOCO 1: Problema, Pergunta e Hipóteses (0:00 – 1:15) — *João Gabriel*
- **Na tela:** Slide ou topo do artigo mostrando Título, Autores e Seção 1 (Introdução) + Protocolo de 1 página.
- **Fala sugerida (João Gabriel):**
  > "Olá professores Wemerson e Leonardo, meu nome é **João Gabriel da Silva Leite**, e junto com o **Yuri Cardoso Balieiro** e o **Pedro de Mello Porto Daou** vou apresentar nosso projeto final sobre o envio de notificações push e a frequência diária de abertura de aplicativos móveis.
  >
  > Na Semana 4, nossa Ficha de Hipótese partiu do problema prático de alertas push de PIX recebido em aplicativos bancários. Na revisão da literatura da Semana 5, analisamos as revisões sistemáticas de Wohllebe (2020), Philip e Hidayaturrahman (2024) e Mehrotra e Musolesi (2020), que apontaram duas grandes lacunas: a maioria dos estudos usa questionários subjetivos em vez de telemetria real de abertura do app, e faltam comparações controladas entre regimes de envio.
  >
  > Como logs bancários reais de PIX são protegidos por sigilo comercial, aplicamos a regra da Seção 3.3 do roteiro e adaptamos nosso protocolo — antes de rodar qualquer teste — para uma base pública real de telemetria móvel na OSF, mantendo o mesmo mecanismo (notificação push) e a mesma variável de resposta (aberturas do app no mesmo dia).
  >
  > Nossa **pergunta de pesquisa (GQM)** é: *Em usuários de um aplicativo móvel com coleta longitudinal, o regime de envio completo de notificações push diárias (4 notificações/dia) está associado a um maior número médio de aberturas do aplicativo no mesmo dia, em comparação ao regime de envio parcial (1 a 3 notificações/dia)?*
  >
  > Definimos a priori, com $\alpha = 0,05$, sobre a diferença média intrapares $\mu_d = \mu_{\text{completa}} - \mu_{\text{parcial}}$:
  > - **$H_0: \mu_d = 0$** (não há diferença na média de aberturas diárias entre os regimes completo e parcial);
  > - **$H_1: \mu_d > 0$** (unilateral: dias com notificação completa estão associados a maior média de aberturas no mesmo dia)."

---

### BLOCO 2 (Parte A): Base Pública e Proveniência (1:15 – 2:45) — *João Gabriel*
- **Na tela:** Seção 3 do artigo (Método) + página da base na OSF (`https://osf.io/n4sgb/`) ou `README.md` do repositório.
- **Fala sugerida (João Gabriel):**
  > "Sobre a **base pública escolhida**: utilizamos o pacote de reprodutibilidade de Dvořák, Kreidl e Tancoš (2026), depositado com identificador persistente na Open Science Framework (`osf.io/n4sgb`), sob licença aberta para reprodução acadêmica.
  >
  > Os autores originais monitoraram **201 usuários** de smartphone Android durante 4 ondas de 14 dias, com até 4 janelas diárias de notificação push, totalizando **42.504 janelas** medidas automaticamente via API do Android com precisão de milissegundos.
  >
  > Como ninguém sorteou em quais dias o usuário receberia todas as 4 notificações ou apenas 1 a 3 (o que dependia de conectividade ou aparelho ligado), declaramos nosso estudo explicitamente como **observacional**, utilizando apenas linguagem de associação estatística e nunca de causalidade. Agora passo a palavra para o Yuri explicar a limpeza, o desenho em blocos e os resultados."

---

### BLOCO 2 (Parte B): Limpeza, Desenho em Blocos e Teste (2:45 – 4:15) — *Yuri Cardoso Balieiro*
- **Na tela:** Script `analise.py` e Tabela 1 do artigo.
- **Fala sugerida (Yuri):**
  > "Olá professores, meu nome é **Yuri Cardoso Balieiro**. Vou detalhar nossa limpeza reprodutível, o desenho experimental e o resultado principal.
  >
  > No nosso script `analise.py`, carregamos o arquivo bruto `notif_data_final.dta` sem nenhuma edição manual. Primeiro, removemos **3 janelas** (0,007% da base) marcadas no dicionário de variáveis dos autores com o código `-666`, que indica erro de gravação de timestamp.
  >
  > Em seguida, agregamos as 42.501 janelas válidas nos **10.626 usuários-dia**. Observamos que nos **3.123 dias** em que nenhuma notificação push foi entregue (0 pushes), houve **zero aberturas** em 100% dos casos — o que mostra que o usuário só abre o app quando estimulado pelo push, mas gera variância zero. Por isso, focamos nos **7.503 usuários-dia ativos** (de 1 a 4 pushes entregues).
  >
  > Como cada pessoa tem um hábito diferente de uso do celular (fator de perturbação conhecido), aplicamos a técnica de **blocagem (desenho pareado)** vista na Aula 07: cada usuário (`p_id`) é um **bloco** comparado contra si mesmo nos dias em que recebeu **Notificação Completa (4 pushes/dia)** versus **Notificação Parcial (1 a 3 pushes/dia)**. Dos 201 usuários, 7 não tinham observações nos dois regimes e foram excluídos, restando **$n = 194$ blocos completos**.
  >
  > Para escolher o teste, calculamos as diferenças intrapares $d_i$ de cada um dos 194 usuários e verificamos a normalidade com **Shapiro-Wilk**, obtendo $W = 0,9921$ e $p = 0,3775 > 0,05$. Como a normalidade foi atendida, aplicamos o **teste $t$ pareado unilateral** a $\alpha = 0,05$, além de confirmar com o teste de permutação (10.000 réplicas, semente `2026`) e com o teste alternativo não paramétrico de **Wilcoxon** que havíamos registrado no protocolo."

---

### BLOCO 3: Resultado Principal e Decisão de Engenharia (4:15 – 6:00) — *Yuri Cardoso Balieiro*
- **Na tela:** Tabela 1 e **Figura 1** do artigo em destaque.
- **Fala sugerida (Yuri):**
  > "Olhando para a **Tabela 1** e para a **Figura 1**, que construímos seguindo os princípios de Cleveland (eixos começando estritamente em zero, sem distorção 3D e exibindo a dispersão individual):
  >
  > - No Painel (a), vemos que sob **Notificação Parcial (1–3 pushes/dia)**, os usuários abriram o aplicativo em média **1,56 vezes ao dia** ($\text{DP} = 0,69$; mediana = $1,54$; $\text{IQR} = 0,91$). Já sob **Notificação Completa (4 pushes/dia)**, a média subiu para **2,67 aberturas/dia** ($\text{DP} = 0,95$; mediana = $2,95$; $\text{IQR} = 1,43$).
  > - No Painel (b), vemos o histograma das diferenças intrapares $d_i$: a distribuição é simétrica (assimetria $g_1 = -0,10$), centrada em um ganho médio de **$+1,11$ aberturas/dia** ($\text{DP} = 0,63$).
  > - O **teste $t$ pareado unilateral** resultou em $t = 24,44$, com $193$ graus de liberdade e **$p = 2,80 \times 10^{-61} < 0,05$**, rejeitando categoricamente $H_0$ (confirmado por Wilcoxon com $p = 1,14 \times 10^{-32}$ e permutação com $p < 0,0001$).
  > - O **Intervalo de Confiança de 95%** para o aumento médio vai de **$1,02$ a $1,20$ aberturas adicionais por dia**, bem distante do zero, e o tamanho de efeito padronizado foi **$d_z = 1,75$**, que é muito grande segundo Cohen (acima de 0,80).
  >
  > **Traduzindo para uma decisão de Engenharia de Software:** garantir a entrega das 4 notificações diárias está associado a um aumento relativo de **71,2%** nas aberturas diárias do aplicativo. Ou seja, falhas técnicas na entrega de push derrubam severamente o engajamento diário. Passo agora a palavra para o Pedro."

---

### BLOCO 4: Análises Exploratórias e Ameaças à Validade (6:00 – 7:30) — *Pedro de Mello Porto Daou*
- **Na tela:** Subseção 4.2 (Análises Exploratórias) e Seção 5 (Ameaças à Validade) do artigo.
- **Fala sugerida (Pedro):**
  > "Olá professores, meu nome é **Pedro de Mello Porto Daou**. Vou apresentar nossas análises exploratórias, as ameaças à validade e a conclusão.
  >
  > Seguindo as regras de integridade científica contra *p-hacking* e *HARKing*, separamos na Seção 4.2 três análises que não faziam parte da hipótese primária do protocolo:
  > 1. Primeiro, testamos os 7.503 usuários-dia ativos como amostras independentes via **teste $t$ de Welch** e **Mann-Whitney**, confirmando a mesma diferença ($+1,15$ aberturas/dia; $t = 40,17$; $p < 0,0001$; $d = 0,90$; $A = 0,75$).
  > 2. Segundo, avaliamos a moderadora **dia da semana** nos dias com 4 pushes ($n = 190$ blocos): dias úteis tiveram média maior de aberturas que finais de semana ($2,72$ vs. $2,45$ aberturas/dia; $t = 6,28$; $p = 1,11 \times 10^{-9}$; $d_z = 0,46$).
  > 3. Terceiro, avaliamos o **estado da tela do celular no minuto anterior ao disparo** ($n = 198$ blocos): quando a notificação chegou com a tela ligada, a taxa média de abertura foi de **76,9%** contra **61,2%** com a tela desligada ($+15,7$ pontos percentuais; $t = 13,39$; $p = 8,41 \times 10^{-30}$; $d_z = 0,95$).
  >
  > Na **Seção 5**, discutimos os quatro tipos de **ameaças à validade** (Wohlin et al., 2012):
  > - **Conclusão:** mitigamos testando a normalidade (Shapiro-Wilk), confirmando com Wilcoxon e permutação, e relatando todos os 4 testes feitos e todas as exclusões (3 janelas com erro `-666` e 7 blocos incompletos).
  > - **Interna:** como é um estudo observacional sem sorteio, fatores de confusão (como o usuário estar com o celular desligado em dias mais ocupados) impedem conclusões causais. Mitigamos a variação entre indivíduos com a blocagem por usuário e mantendo linguagem associativa.
  > - **Construto:** receber 4 notificações oferece mais oportunidades mecânicas de abrir o app do que receber 1 a 3; mitigamos isso avaliando também a taxa percentual de abertura por notificação na análise da tela ativa.
  > - **Externa:** a base vem de adolescentes tchecos em um app de questionários (EMA), o que impede generalizar diretamente para usuários adultos de apps bancários e alertas de PIX sem um estudo específico no setor financeiro."

---

### BLOCO 5: Conclusão e Reprodutibilidade (7:30 – 8:30) — *Pedro de Mello Porto Daou*
- **Na tela:** Seção 6 (Conclusão), Disponibilidade de Dados e Código e Repositório da Equipe.
- **Fala sugerida (Pedro):**
  > "Concluindo nosso trabalho: respondemos à pergunta de pesquisa demonstrando que o regime completo de notificações push (4/dia) está associado a um aumento médio de **$+1,11$ aberturas/dia** ($\text{IC 95\%}: [1,02; 1,20]$; $d_z = 1,75$), e que disparar notificações quando a tela está ativa eleva a conversão em $15,7$ pontos percentuais.
  >
  > Como **próximo passo** para transformar estes resultados preliminares em um estudo completo no domínio bancário, propomos realizar um experimento controlado aleatorizado (teste A/B) em um protótipo de carteira digital, sorteando o envio imediato versus agrupado de alertas PIX.
  >
  > Todo o nosso código Python (`analise.py`), o arquivo `requirements.txt`, o `README.md` passo a passo e os dados limpos estão disponíveis no repositório cujo link consta no artigo, permitindo reproduzir todos os números e a Figura 1 com um único comando. Muito obrigado!"
