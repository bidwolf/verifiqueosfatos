# Metodologia — Verifique os Fatos

> Proposta de metodologia pública, aberta a revisão por qualquer pessoa, para que as checagens deste projeto possam ser **auditadas** por quem discorda delas — de qualquer lado.
>
> Status: **proposta** (PR). Entra em vigor quando aprovada pelo conselho editorial descrito na seção 2 e passa a valer igualmente para todas as candidaturas.

---

## 0. Por que uma metodologia

Uma checagem só vale alguma coisa se a pessoa que não gosta do resultado conseguir ver *como* ele foi produzido e *onde* contestar. Hoje o site diz "a mesma régua vale para todos", mas a régua não está escrita, a seleção das falas não é registrada e as mudanças de veredito acontecem sem rastro. Este documento escreve a régua.

Princípios, em ordem de prioridade quando conflitarem:

1. **Igualdade de tratamento** — mesma régua, mesma linguagem, mesma cobertura para todas as candidaturas.
2. **Verificabilidade** — toda checagem aponta para uma fonte que qualquer pessoa consegue abrir.
3. **Transparência** — o que foi checado, o que ficou de fora, quem checou e o que mudou são públicos.
4. **Correção** — errar é esperado; esconder o erro não é.
5. **Participação** — qualquer cidadão pode propor, revisar e contestar.
6. **Independência** — nenhuma pessoa com vínculo com campanha participa do processo editorial.

---

## 1. O que é checado e o que não é

Só recebem veredito **afirmações factuais**: números, datas, autoria de medidas, ocorrência de eventos, citações atribuídas a alguém.

**Não recebem veredito** (podem ser registradas, com o rótulo *Não verificável*, mas sem Verdadeiro/Falso):

| Tipo | Exemplo (debate Globo, 23/10/2026) |
|---|---|
| Promessa / intenção | "Vou ampliar a Zona Franca de Manaus" (Flávio) · "Vamos comprar a dívida das pessoas físicas" (Lula) |
| Opinião / previsão | "A economia verde pode render mais que gado ou café" (Lula) · "Quer expandir a legislação para animais silvestres" (Flávio) |
| Juízo de valor, insulto, adjetivo | "palácio de luxo", "virou as costas", "está tudo mais caro" (sem número) |
| Relato pessoal não documentado | "Meu pai foi salvo graças ao SUS" |

Uma promessa pode conter um **fato embutido** ("vou *criar* a Casa da Mulher Brasileira" — ela já existe desde 2015). Nesse caso checa-se o fato embutido e o texto da verificação diz exatamente isso: *a promessa não é avaliada; o programa citado já existe*.

**Mudança de posição** não é mentira. "Sou a favor da tarifa zero" dito por quem antes criticou a tarifa zero é registrado como **Contraditório** (ver escala), com as duas datas e os dois links — não como *Falso*.

---

## 2. Governança democrática

### 2.1 Conselho editorial
- Mínimo de **5 pessoas**, inscrição aberta via issue, aprovação por maioria simples do conselho atual.
- Cada integrante publica em `CONSELHO.md` uma **declaração de interesses**: filiação partidária atual ou nos últimos 4 anos, doações a campanhas, trabalho remunerado ou voluntário em campanhas, cargos comissionados. Nada disso impede participar — **esconder** impede.
- **Impedimento**: quem trabalha em qualquer campanha em disputa não checa, não revisa e não vota em método enquanto a disputa durar.
- Decisões de método são tomadas por PR neste documento, com **72 horas** de discussão aberta. **Durante um debate a régua está congelada**: nenhuma regra muda no meio do evento.

### 2.2 Duplas plurais
Toda checagem passa por **duas pessoas**: quem checa e quem revisa. Sempre que houver gente suficiente, a dupla é formada por pessoas com declarações de interesse diferentes. Um veredito **Falso** ou **Insustentável** exige revisão de duas pessoas além de quem checou.

### 2.3 Retrospectiva pública
Até 48 horas depois de cada evento, o conselho publica um **relatório de cobertura** (seção 7) e abre uma issue de retrospectiva para qualquer pessoa comentar. Vereditos contestados nessa janela têm resposta obrigatória.

---

## 3. Seleção das falas — a maior fonte de viés

A assimetria de um "placar" nasce quase sempre **antes** da checagem: na escolha do que checar. Se de um candidato se escolhem só os autoelogios fáceis de confirmar e do outro só os ataques, o resultado está decidido antes de abrir a primeira fonte.

Regras:

1. **Transcrição integral.** Todo debate é transcrito (ferramenta de reconhecimento de fala sob supervisão humana, como fazem Aos Fatos e g1). A transcrição é publicada.
2. **Fila completa.** Toda afirmação factual de **todas** as candidaturas entra numa fila pública (`fila.json`) com: `id`, candidato, horário, texto literal, tema. Entra na fila **antes** de alguém decidir se vai checar.
3. **Triagem registrada.** Cada item da fila recebe um de três estados: *checada*, *não verificável* (seção 1) ou *não checada por falta de tempo*. O estado é público. Nada "some".
4. **Paridade de cobertura.** A meta é checar a mesma **proporção** de afirmações factuais de cada candidatura. Se ao fim do evento a diferença de cobertura passar de 15 pontos percentuais, o relatório explica por quê e o placar (seção 6) é suprimido.
5. **Ordem neutra.** A fila é trabalhada em ordem cronológica, não por "qual fala rende mais".
6. **Autoelogio e ataque pesam igual.** "Criamos o MEI" e "Lula é o pai do tigrinho" são ambas afirmações factuais e ambas entram na fila.

> Teste rápido: ao fim do debate, conte quantas afirmações *verdadeiras* de cada lado foram checadas. Se um lado tem dezenas e o outro quase nenhuma, o problema não é o candidato — é a seleção.

---

## 4. Escala de vereditos

A escala atual (Verdadeiro / Falso / Parcial) obriga a jogar coisas muito diferentes no mesmo balde: exagero de 20% e invenção completa viram "Falso"; opinião e promessa viram "Parcial". A proposta é adotar a escala usada pelas agências brasileiras signatárias do IFCN (Lupa, Aos Fatos, Estadão Verifica), que já é familiar ao leitor.

| Rótulo | `c` | `r` | Quando usar | Exemplo de cada lado (23/10/2026) |
|---|---|---|---|---|
| **Verdadeiro** | 1 | `verdadeiro` | O dado confere com a fonte, no período e na base declarados. | Lula: "Flávio chamou o Bolsa Família de bolsa-farelo" · Flávio: "A taxa de juros está em torno de 14%" (Selic 13,75%) |
| **Verdadeiro, mas** (falta contexto) | 3 | `falta_contexto` | O dado confere, mas omite algo que muda a leitura. | Lula: "BR-319, uma estrada nova" (recuperação de rodovia dos anos 1970) · Flávio: "11.500 obras paradas neste governo" (lista do TCU cobre obras de 2022–24, de todos os entes) |
| **Exagerado** | 3 | `exagerado` | O número existe, mas está inflado. | Lula: "Acabamos com a fome em 2012" (saída do Mapa da Fome: 2014) · Flávio: "Lula gastou R$ 400 bi para se reeleger" (soma de impacto de medidas, não gasto executado) |
| **Subestimado** | 3 | `subestimado` | O número existe, mas é maior do que o dito. | Lula: "Herdei 6 mil obras paradas" (TCU: 8,6 mil) · Flávio: "Mais de 40 milhões vivem sob facções" (estimativas de 50–68 mi) |
| **Impreciso** | 3 | `impreciso` | Erro de data, nome, valor ou atribuição que não muda o sentido geral. | — |
| **Contraditório** | 3 | `contraditorio` | A fala contradiz posição ou fala anterior documentada da mesma pessoa. | Flávio: "Sou a favor da tarifa zero aos fins de semana" · Lula: "Sou a favor de reduzir a maioridade penal para crimes hediondos" (posição histórica contrária) |
| **Insustentável** | 2 | `insustentavel` | Não há dado público que permita confirmar nem negar. **Não é Falso.** | "O PT entregou nem 30% do que prometeu ao RS" · "Liberaram 1,1 bilhão de balas" |
| **Falso** | 2 | `falso` | Há dado público que contradiz a fala. | Lula: "O governo Bolsonaro aprovou o tigrinho" (lei de 2018, governo Temer) · Flávio: "Lula é o pai do tigrinho" (idem) |
| **Não verificável** | 4 | `nao_verificavel` | Opinião, promessa, previsão, juízo de valor (seção 1). Sem veredito. | ver seção 1 |
| **Em verificação** | 0 | `em_verificacao` | Fala registrada, checagem em andamento. Sem veredito. | — |

Regras de aplicação:

- **Ônus da prova.** Para marcar *Falso* é preciso **um dado que contradiga** a fala. Negativa do interessado (advogado, assessoria, o próprio candidato) **não refuta nada** — vira *Insustentável* ou *Em verificação*.
- **Exagero não é mentira.** 20 anos quando foram 16 é *Exagerado*. 5 mil quando foram 3,6 mil é *Exagerado*. A regra é a mesma para os dois lados.
- **Citação literal correta é Verdadeiro.** Se a pessoa disse aquilo, está documentado e o sentido não foi distorcido, o veredito é *Verdadeiro*. Contexto adicional vai no texto, não rebaixa o veredito — e, se a regra for rebaixar com contexto, ela vale para as citações que os dois lados fazem um do outro.
- **Declare a base.** Toda checagem numérica diz **série, período e denominador** ("obras federais paralisadas segundo o TCU em ago/2022"; "obras do FNDE em 2022"). Dois números diferentes podem ser ambos verdadeiros em bases diferentes; a checagem explica isso em vez de escolher a base que derruba a fala.
- **Compatibilidade.** O campo `c` continua existindo para o front atual (1 = confere, 2 = não confere, 3 = confere com ressalva, 4 = sem veredito, 0 = em verificação). O campo novo `r` guarda o rótulo detalhado e passa a ser o que aparece no card.

---

## 5. Fontes

1. **Toda checagem tem pelo menos uma fonte com link**, no campo `s`. Checagem sem link não é publicada — o validador (`scripts/validate_posts.py`) passa a exigir `s` com ao menos uma URL para `c` em {1, 2, 3}.
2. **Hierarquia de fontes:**
    1. Dado primário oficial (IBGE, Banco Central, Tesouro, TCU, DataSUS, FBSP/Atlas da Violência, Diário Oficial, inteiro teor de lei ou decisão).
    2. Checagem publicada por agência signatária do IFCN ou coalizão jornalística (Lupa, Aos Fatos, Estadão Verifica, UOL Confere, AFP Checamos, Comprova, g1 Fato ou Fake).
    3. Reportagem de veículo com redação e política de correção identificáveis.
3. **Não contam como fonte:** veículos de partido, blogs de militância, sites de campanha ("X mentiu"), redes sociais sem documento anexado, "fontes" sem URL ("G1 – título da matéria" sem link). Isso vale para os dois lados.
4. **Quem checa abre o link.** A fonte precisa dizer o que a checagem diz que ela diz. Fonte "lembrada" ou sugerida por ferramenta de IA sem conferência não é fonte.
5. **Uso de IA é declarado.** Ferramentas de IA podem transcrever, organizar a fila e rascunhar texto. **Não publicam.** Todo post rascunhado com IA leva `"ia": true` e passa pela mesma dupla de revisão. Textos com fontes inventadas são a falha mais comum dessas ferramentas — por isso a regra 4.

---

## 6. Placar ("Fatômetro") e cobertura

Um percentual de "verdade" calculado sobre falas **escolhidas à mão** não mede a honestidade do candidato; mede a seleção de quem escolheu. Por isso:

1. **Nenhum percentual único de "verdade" é exibido.**
2. O que pode ser exibido é a **distribuição de rótulos por candidatura, em números absolutos, lado a lado**, com o total de afirmações factuais registradas na fila e quantas foram checadas (exemplo abaixo).
3. O bloco só aparece quando **a cobertura dos dois lados está dentro da faixa da seção 3.4**. Fora dela, aparece o aviso "cobertura desigual — placar suprimido" e o link para a fila.
4. O bloco traz **sempre**, logo abaixo, os placares das agências independentes para o mesmo evento (seção 8), com a observação de que os números **não são somáveis** entre fontes porque cada uma usa critérios e amostras próprios.
5. A imagem compartilhável (`share.js`) **não traz percentual**; traz o rótulo da checagem, a fonte e o aviso "checagem revisável".

Exemplo (números ilustrativos):

```
Lula             — 31 afirmações factuais · 24 checadas
Verdadeiro 10 · Falta contexto 5 · Exagerado 3 · Falso 2 · Não verificável 4

Flávio Bolsonaro — 29 afirmações factuais · 22 checadas
Verdadeiro 8 · Falta contexto 6 · Exagerado 4 · Falso 3 · Não verificável 1
```

---

## 7. Processo durante um evento ao vivo

```
transcrição → fila pública (todas as falas factuais)
   → triagem (verificável? sim / não)
   → checagem (1 pessoa) → revisão (1–2 pessoas)
   → publicação com fonte → contestação aberta → errata se preciso
```

- **Publica-se só com fonte.** Se a fonte não chega em 20 minutos, o item entra como *Em verificação* (sem veredito) para o leitor saber que a fala está sendo olhada.
- **Nada é apagado.** Um item retirado vira `"c": 0` com `"e"` explicando por quê. O histórico fica.
- **Toda mudança de veredito** gera uma entrada em `"hist"` (de → para, horário, motivo) e aparece no card ("alterado de Falso para Exagerado às 23:12 — fonte X mostra …").
- **Relatório de cobertura** (até 48 h depois): por candidatura, quantas afirmações factuais, quantas checadas, distribuição de rótulos, tempo médio até publicar, contestações recebidas e aceitas, lista do que ficou de fora.

---

## 8. Checagens de outras fontes

O site exibe, para cada evento, um bloco **"O que as agências independentes concluíram"**, com:

- nome da agência, horário da última atualização que o site consultou, totais por candidatura e por rótulo **como a agência publicou**, link direto;
- aviso fixo: *critérios e amostras diferentes; os números não se somam nem se comparam diretamente*;
- inclusão **mesmo quando a conclusão da agência contraria a deste site** — isso é parte do controle de qualidade, não um constrangimento.

Critério de inclusão: signatárias do [IFCN](https://ifcncodeofprinciples.poynter.org/) com redação no Brasil e coalizões jornalísticas com método publicado. Critério de exclusão: iniciativas de campanha, partido ou militância, de qualquer lado.

Os dados ficam em `externas.json` (ver `OUTRAS-CHECAGENS.md`), mantido pelo mesmo fluxo de PR.

---

## 9. Linguagem — guia de estilo imparcial

A verificação é lida por quem vota nos dois. Ela convence pelo dado, não pelo tom.

**Estrutura fixa** (até 600 caracteres): 1. Rótulo em uma palavra. 2. O dado, com número, período e base. 3. A fonte (link em `s`). 4. Contexto, se mudar a leitura.

**Nomes.** Primeira menção: "Lula (PT)" e "Flávio Bolsonaro (PL)". Depois: "Lula" e "Flávio". Nunca "o petista", "o senador", "o ex-presidiário", "o filho". Mesmo tratamento para terceiros citados (Bolsonaro, Tarcísio, Dilma, Temer: nome e cargo à época).

**Proibido:**

- adjetivos valorativos ("impressionantes R$ 476 bilhões", "histórico", "polêmico", "esmagadora");
- atribuir intenção ("omite propositalmente", "tenta confundir", "narrativa");
- ironia, ponto de exclamação, perguntas retóricas;
- repetir o ataque de um lado como se fosse a verificação do outro.

**Obrigatório:**

- verbos neutros: "disse", "afirmou", "o dado mostra", "a lei estabelece";
- quando a fala for *Verdadeira*, dizer isso na primeira palavra — para qualquer candidato;
- quando a fala for *Falsa*, mostrar o dado que a contradiz — não a opinião de quem checou.

**Teste da troca.** Antes de publicar, troque mentalmente o nome do candidato. Se o rótulo, o tom ou a quantidade de contexto mudariam, a checagem não está pronta.

---

## 10. Contestação e direito de resposta

- Todo card tem o botão **"Contestar esta checagem"**, que abre uma issue a partir do template (`.github/ISSUE_TEMPLATE/contestar-checagem.yml`) já com o `id` do post.
- Campanhas e cidadãos usam o mesmo canal e recebem o mesmo tratamento.
- **Prazo de resposta: 24 horas** em período eleitoral. A resposta é pública na issue e, se houver mudança, no `hist` do post.
- Contestação **com fonte** que mostre erro → correção. Contestação **sem fonte** → resposta explicando o que faltou, sem alteração.
- Ninguém revisa a contestação de uma checagem que fez.

---

## 11. Dados abertos

- `posts.json` continua sendo a fonte única do front. Nenhum post é removido do arquivo; retirados viram `c: 0` + `e`.
- `fila.json` publica todas as afirmações factuais registradas, inclusive as não checadas.
- `externas.json` publica os placares das agências (seção 8).
- O histórico do git é a trilha de auditoria; o site expõe um link "ver histórico desta checagem" apontando para o `git log` do item.
- Licença dos dados: CC BY 4.0 — qualquer pessoa pode reutilizar, inclusive para auditar este projeto.

---

## 12. Mudanças propostas no esquema de `posts.json`

```json
{
  "id": 12,
  "n": 2,
  "c": 3,
  "r": "falta_contexto",
  "h": "21:48",
  "a": "Economia",
  "t": "O Brasil tem 11.500 obras paralisadas atualmente",
  "v": "Falta contexto. O TCU listou cerca de 11,5 mil obras financiadas pela União paralisadas (levantamento de 2024, obras de 2022–24). A maioria é executada por estados e municípios via convênio; a lista não separa o que começou em cada governo.",
  "s": ["https://portal.tcu.gov.br/..."],
  "e": "Rótulo alterado de Parcial para Falta contexto após revisão.",
  "hist": [{ "de": "parcial", "para": "falta_contexto", "quando": "2026-10-23T23:12-03:00", "motivo": "fonte do TCU especifica o período" }],
  "chk": ["@checador", "@revisor"],
  "ia": true
}
```

Campos novos: `r` (rótulo detalhado), `hist` (histórico de alterações), `chk` (quem checou e revisou, logins públicos), `ia` (rascunho com IA). Campo `c` ganha os valores `4` (não verificável) e `0` (em verificação); `index.html` passa a renderizá-los com os textos "Não verificável" e "Em verificação", sem cor de veredito.

Validador: `s` obrigatório para `c ∈ {1,2,3}`; `id` obrigatório e único (já exigido hoje — e hoje nenhum post tem, o que mantém o CI quebrado); `r` obrigatório e dentro da lista da seção 4.

---

## 13. Checklist antes de publicar

- [ ] A fala está na fila com horário e texto literal?
- [ ] É uma afirmação factual (não opinião, promessa ou previsão)?
- [ ] O rótulo é o mais específico da escala (não "Falso" para exagero; não "Parcial" para citação correta)?
- [ ] Série, período e base estão declarados?
- [ ] Há pelo menos um link em `s` que **eu abri** e que diz o que estou dizendo?
- [ ] A fonte é aceita pela seção 5 (nada partidário, nada sem URL)?
- [ ] O texto segue a estrutura e o guia de estilo da seção 9?
- [ ] Passou no teste da troca?
- [ ] Teve revisão de pelo menos uma outra pessoa (duas, se *Falso* ou *Insustentável*)?
- [ ] Se altera um post existente, `hist` e `e` foram preenchidos?

---

## 14. O que esta metodologia **não** resolve

- Não garante que o conselho seja plural se só um campo político se inscrever — por isso a declaração de interesses é pública e o relatório de cobertura mostra, em número, quem está sendo checado e quanto.
- Não substitui as agências profissionais; o bloco da seção 8 existe para que o leitor compare.
- Não elimina erro em tempo real. Elimina erro **escondido**.
