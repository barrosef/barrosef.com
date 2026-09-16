---
title: "Quando o trabalho de um agente de IA está pronto?"
date: 2026-09-16T17:00:00-04:00
draft: false
translationKey: "when-is-an-agents-work-done"
categories: ["Tecnologia"]
tags: ["dop", "agentes-de-ia", "entrega-de-software", "decisoes-de-arquitetura"]
description: "Um agente abre um pull request em vinte minutos; uma pessoa leva uma hora para revisar. A resposta do DOP: sem verde, sem PR — e o verde tem de ser conquistado num commit, não numa árvore suja."
---

Um agente abre um pull request em vinte minutos. Uma pessoa leva uma hora para
revisá-lo direito. Ponha cinco agentes em cinco demandas e o gargalo deixa de
ser escrever o código — passa a ser a mesa do revisor. Paralelismo que para
ali só muda a fila de lugar.

O [DOP](/pt-br/sobre/) é uma plataforma que estou construindo em
que um desenvolvedor e um agente conduzem uma demanda de ponta a ponta. Duas
das suas decisões de arquitetura respondem à pergunta do título, e a resposta
é a mesma nas duas: **sem verde, sem PR** — e o verde tem de ser conquistado
com honestidade.

## O caminho da especificação até a main

<div class="path" role="img" aria-label="Sete passos: aceitação executável na especificação; o agente itera até o verde; um runner constrói o commit a partir do fonte; um crítico revisa o diff contra a especificação; o PR carrega a evidência; a fila de merge reverifica contra a main de hoje; o humano decide.">
  <div class="path-step"><span class="path-n">1</span><span class="path-name">A aceitação nasce na especificação</span><span class="path-who">executável, ou é um desejo</span></div>
  <div class="path-step"><span class="path-n">2</span><span class="path-name">O agente itera até o verde</span><span class="path-who">uma falha persistente vira pergunta, nunca um PR quebrado</span></div>
  <div class="path-step"><span class="path-n">3</span><span class="path-name">Um runner constrói o commit a partir do fonte</span><span class="path-who">não a árvore de trabalho do agente</span></div>
  <div class="path-step"><span class="path-n">4</span><span class="path-name">Um crítico revisa o diff contra a especificação</span><span class="path-who">contexto limpo, sem memória de ter escrito</span></div>
  <div class="path-step"><span class="path-n">5</span><span class="path-name">O PR carrega a evidência</span><span class="path-who">resultados, execuções, veredito, rastro</span></div>
  <div class="path-step"><span class="path-n">6</span><span class="path-name">A fila de merge reverifica</span><span class="path-who">contra a main de hoje, um por vez</span></div>
  <div class="path-step path-step-human"><span class="path-n">7</span><span class="path-name">O humano decide</span><span class="path-who">a exceção, não a regra</span></div>
</div>

## Quatro regras antes de chamar alguém

**A aceitação é executável.** Toda demanda carrega critérios que uma máquina
consegue verificar — suítes de teste, checagens derivadas da especificação. Um
critério que não executa não é critério; é um desejo, e desejos são o que o
revisor acaba conferindo na mão.

**O agente itera até o verde.** Nenhum PR abre com a aceitação falhando.
Quando uma falha persiste, ela vira um bloqueio com uma pergunta para o
humano, na caixa de atenção. Um PR quebrado nunca é o jeito de pedir ajuda.

**Um crítico revisa antes do humano.** Uma instância independente, com contexto
limpo e sem o histórico de ter escrito o código, recebe diff, especificação e
evidência e emite um veredito. É a primeira defesa contra o carimbo automático
— o revisor que já leu quatro PRs verdes hoje e vai aprovar o quinto na
confiança.

**O PR carrega a sua evidência.** Resultados da aceitação, execuções de teste,
o veredito do crítico, links para o rastro. O humano revisa a exceção, não a
regra.

## Por que o teste não pode rodar onde o agente trabalha

O agente trabalha num sandbox: sua própria microVM, sua própria árvore de
trabalho, tudo o que instalou pelo caminho. O lugar óbvio para rodar os testes
é ali mesmo. O DOP recusa, e a recusa está escrita no domínio: uma execução de
verificação precisa nomear o commit em que rodou, porque *evidência que não
diz sobre qual código rodou não é evidência*.

Um teste dentro do sandbox roda contra uma árvore suja — que não é commit
nenhum. Por isso a verificação acontece num **runner**: um ambiente efêmero
que parte do zero, puxa o commit, constrói a aplicação a partir do fonte e a
sobe. Nenhuma imagem do projeto é construída, publicada ou implantada — a
parte lenta nunca foi o build, e sim a viagem `build → push → pull` em volta
de um registry. Dependências como um banco de dados são puxadas como imagens
publicadas. Quando a execução termina, o runner morre.

O ganho é honestidade por construção: o verde fala de um commit porque rodou
num ambiente construído a partir daquele commit — o mesmo que vai ser
mesclado.

## Quem responde a qual pergunta

| A pergunta | Quem responde | Onde |
|---|---|---|
| Faz o que a especificação diz? | Os testes | No runner, sobre o commit |
| O diff é o que a especificação pediu, e nada mais? | O crítico | Um contexto limpo |
| Continua verde contra a `main` de hoje? | A fila de merge | Uma reexecução após o rebase |
| Deve ser mesclado? | O humano | O PR, com a evidência |

## Depois do verde: a fila

Três demandas rodam em paralelo e cada uma abre um PR verde — cada um testado
contra a `main` do momento em que a branch nasceu. O primeiro merge invalida
os outros dois. Na melhor hipótese, um conflito de texto; na pior, uma quebra
semântica silenciosa, em que um PR remove a checagem que o outro presumia. O
CI do PR não enxerga isso. A produção enxerga.

Então um PR verde não é mesclado; ele entra numa **fila por repositório**. A
fila reaplica cada PR sobre a `main` atual, reexecuta a verificação e mescla
um por vez. Um conflito é tarefa do agente da demanda primeiro; só uma
resolução que falhou chega ao humano, com o contexto do conflito anexado. E o
orquestrador do projeto observa quais demandas ativas tocam os mesmos
arquivos, para que a sobreposição seja sinalizada antes do PR, não depois.

## O que isso compra

| O que o humano fazia | O que o humano faz agora |
|---|---|
| Rodar os testes, ou confiar que o agente rodou | Ler um resultado que nomeia o commit |
| Ler o diff inteiro para ver se bate com o pedido | Ler o veredito do crítico e as razões |
| Adivinhar se ainda mescla limpo | Saber que foi reverificado na `main` de hoje |
| Revisar tudo | Revisar as exceções |

O DOP está em construção; isto são decisões, e é mais barato discutir com
decisões do que com código. As duas em que este artigo se apoia são públicas:
[ADR-0007, sem verde, sem PR](https://github.com/barrosef/dop/blob/main/docs/adr/0007-no-green-no-pr.md)
e [ADR-0030, a verificação constrói a partir do fonte](https://github.com/barrosef/dop/blob/main/docs/adr/0030-verification-runs-from-source.md).
