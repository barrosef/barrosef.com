---
title: "A Morte dos Tokens"
date: 2026-10-05T09:00:00-04:00
draft: false
translationKey: "death-of-tokens"
categories: ["Technology"]
tags: ["claude-code", "ai-assisted-development", "tooling", "cost", "prompt-caching", "economizando-com-ia"]
description: "Episódio 3 de Economizando com IA. Toda ferramenta que promete cortar a conta de IA mostra os tokens caindo. Abrimos a fatura linha por linha: os tokens caíram 46% e a conta subiu 14%. Onde o dinheiro mora de verdade, e por que o número que todo mundo cita deixou de significar alguma coisa."
---

*Terceiro episódio de **Economizando com IA**. O episódio 1, {{< episode 1 >}},
instalou uma ferramenta que promete uma conta mais leve enviando menos texto ao
modelo. O episódio 2, {{< episode 2 >}},
trouxe os primeiros comprovantes. Este não é mais sobre a ferramenta. É sobre o
número que toda ferramenta desse mercado mostra, e por que esse número já não
diz o que você vai pagar.*

---

Todo produto que promete cortar a sua conta de IA mostra o mesmo gráfico: uma
linha chamada **tokens** caindo. Sessenta por cento a menos. Noventa e cinco por
cento a menos. O gráfico costuma ser verdadeiro.

A fatura é outro documento. Abrimos a nossa linha por linha, em 44 dias úteis e
quatro projetos, e os dois documentos discordam. **No projeto em que enviamos
menos texto ao modelo, o texto relido caiu 46% por rodada de trabalho e o custo
por rodada subiu 14%.**

Este episódio é a anatomia dessa discordância. Se você paga IA por mês, ele
muda qual número você deve pedir à sua equipe.

## Token não é preço

Um token é mais ou menos três quartos de uma palavra. É a unidade que o
provedor conta. É também, desde 2024, **não a unidade que o provedor cobra**, e
essa é a história inteira.

Um agente de código trabalha em rodadas. Em cada rodada ele envia ao modelo a
conversa inteira até ali (toda instrução, todo arquivo que leu, todo resultado
que recebeu) e recebe uma resposta. A conversa cresce a cada rodada, então à
tarde cada rodada carrega centenas de milhares de tokens.

Enviar tudo isso a preço cheio seria ruinoso, então o provedor oferece um
acordo chamado cache. O texto que o modelo já viu pode ser **relido** por um
décimo do preço do texto novo. Em troca, na primeira vez que um trecho é
guardado, você paga um ágio para **gravá-lo**: 1,25 vez o preço do texto novo
para um cache de cinco minutos, o dobro para um de uma hora. E a **resposta**
que o modelo escreve custa cinco vezes o texto novo.

Então uma rodada de trabalho são quatro linhas na fatura, a quatro preços
diferentes:

| O que é cobrado | Preço, em relação ao texto novo |
|---|---|
| texto relido do cache | 0,1× |
| texto novo, nunca visto | 1× |
| texto gravado no cache (5 min / 1 hora) | 1,25× / 2× |
| a resposta que o modelo gera | 5× |

Um token da primeira linha vale um cinquenta avos de um token da última.
"Os tokens caíram" é uma frase sobre a soma de quatro quantidades que nunca
deveriam ter sido somadas.

## Onde estão os tokens, e onde está o dinheiro

Eis o nosso corpo de dados: 44 dias, quatro projetos, 11,9 bilhões de tokens,
US$ 10.206 a preço de lista. A primeira barra é onde estão os tokens. A segunda
é onde está o dinheiro.

<!-- FIG:SHARES -->
<figure class="diagram">
<svg viewBox="0 0 720 250" role="img" aria-label="Duas barras. Onde estão os tokens: 96% leitura de cache. Onde está o dinheiro: 50% leitura, 42% gravação, 8% respostas." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><text x="16" y="69" font-size="13.5" fill="#16233a">Onde estão os tokens</text><rect x="230.0" y="50" width="449.3" height="30" fill="#6b8ef2"/><text x="454.7" y="70" font-size="13" font-weight="700" text-anchor="middle" fill="#fff">95.6%</text><rect x="681.3" y="50" width="19.3" height="30" fill="#2a5bd7"/><rect x="702.6" y="50" width="1.5" height="30" fill="#1d7a4a"/><text x="16" y="139" font-size="13.5" fill="#16233a">Onde está o dinheiro</text><rect x="230.0" y="120" width="237.3" height="30" fill="#6b8ef2"/><text x="348.7" y="140" font-size="13" font-weight="700" text-anchor="middle" fill="#fff">50.5%</text><rect x="469.4" y="120" width="195.5" height="30" fill="#2a5bd7"/><text x="567.1" y="140" font-size="13" font-weight="700" text-anchor="middle" fill="#fff">41.6%</text><rect x="666.9" y="120" width="37.1" height="30" fill="#1d7a4a"/><rect x="230" y="178" width="12" height="12" fill="#6b8ef2"/><text x="247" y="189" font-size="12" fill="#16233a">leitura de cache</text><rect x="400" y="178" width="12" height="12" fill="#2a5bd7"/><text x="417" y="189" font-size="12" fill="#16233a">gravação em cache</text><rect x="570" y="178" width="12" height="12" fill="#1d7a4a"/><text x="587" y="189" font-size="12" fill="#16233a">respostas</text><text x="16" y="236" font-size="11" fill="#16233a">44 dias, quatro projetos, 11,9 bilhões de tokens, US$ 10.206 a preço de lista. A entrada nova é 0,03% do dinheiro e não foi desenhada.</text></svg>
<figcaption>Noventa e seis por cento do volume é releitura barata. Metade do dinheiro está lá; a outra metade está nos 4% que são gravados, e nas respostas.</figcaption>
</figure>

Noventa e seis por cento de cada token que enviamos era releitura de cache. É a
massa que uma ferramenta de compressão enxerga, e a massa que ela comprime. Ela
carrega metade do dinheiro.

A outra metade mora em dois lugares que uma contagem de tokens mal registra. As
**gravações** em cache são 4% dos tokens e 42% do dinheiro. As respostas do
próprio modelo são 0,3% dos tokens e 8% do dinheiro.

Esta é a primeira morte. Uma ferramenta que apara a barra grande só consegue
tocar metade da conta, e precisa aparar muito token barato para movê-la.

## Quatro dias, os mesmos tokens, três preços

A segunda morte é mais simples de ver. Pegue quatro dias comuns de trabalho de
um projeto, no mesmo modelo, escolhidos porque cada rodada de trabalho enviou
quase exatamente a mesma quantidade de texto ao modelo. Se token fosse preço,
os quatro dias custariam o mesmo.

<!-- FIG:DAYS -->
<figure class="diagram">
<svg viewBox="0 0 720 330" role="img" aria-label="Quatro dias de trabalho com quase os mesmos tokens por rodada, 576 a 627 mil, e um custo por rodada que vai de 34 centavos a 1 dólar e 2 centavos. A única coisa que cresceu junto com o custo foi quanto texto foi gravado no cache." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><text x="150" y="22" font-size="12" font-weight="700" fill="#16233a">tokens enviados por rodada</text><text x="470" y="22" font-size="12" font-weight="700" fill="#16233a">custo por rodada</text><text x="16" y="66" font-size="13.5" font-weight="700" fill="#16233a">dia 1</text><rect x="150" y="46" width="237" height="30" rx="4" fill="#6b8ef2"/><text x="395" y="66" font-size="13" fill="#16233a">593k</text><rect x="470" y="46" width="53" height="30" rx="4" fill="#a4252c"/><text x="531" y="66" font-size="14" font-weight="700" fill="#a4252c">US$ 0,34</text><text x="150" y="92" font-size="11" fill="#16233a" fill-opacity="0.75">dos quais gravados no cache: 3 mil</text><line x1="16" y1="102" x2="704" y2="102" stroke="#d5dde8"/><text x="16" y="132" font-size="13.5" font-weight="700" fill="#16233a">dia 2</text><rect x="150" y="112" width="230" height="30" rx="4" fill="#6b8ef2"/><text x="388" y="132" font-size="13" fill="#16233a">576k</text><rect x="470" y="112" width="79" height="30" rx="4" fill="#a4252c"/><text x="557" y="132" font-size="14" font-weight="700" fill="#a4252c">US$ 0,51</text><text x="150" y="158" font-size="11" fill="#16233a" fill-opacity="0.75">dos quais gravados no cache: 22 mil</text><line x1="16" y1="168" x2="704" y2="168" stroke="#d5dde8"/><text x="16" y="198" font-size="13.5" font-weight="700" fill="#16233a">dia 3</text><rect x="150" y="178" width="242" height="30" rx="4" fill="#6b8ef2"/><text x="400" y="198" font-size="13" fill="#16233a">605k</text><rect x="470" y="178" width="96" height="30" rx="4" fill="#a4252c"/><text x="574" y="198" font-size="14" font-weight="700" fill="#a4252c">US$ 0,62</text><text x="150" y="224" font-size="11" fill="#16233a" fill-opacity="0.75">dos quais gravados no cache: 31 mil</text><line x1="16" y1="234" x2="704" y2="234" stroke="#d5dde8"/><text x="16" y="264" font-size="13.5" font-weight="700" fill="#16233a">dia 4</text><rect x="150" y="244" width="251" height="30" rx="4" fill="#6b8ef2"/><text x="409" y="264" font-size="13" fill="#16233a">627k</text><rect x="470" y="244" width="158" height="30" rx="4" fill="#a4252c"/><text x="636" y="264" font-size="14" font-weight="700" fill="#a4252c">US$ 1,02</text><text x="150" y="290" font-size="11" fill="#16233a" fill-opacity="0.75">dos quais gravados no cache: 72 mil</text><text x="16" y="320" font-size="11" fill="#16233a">Mesmo projeto, mesmo modelo, mesma tabela de preços. Tokens a menos de 4% de diferença; custo três vezes maior.</text></svg>
<figcaption>Quatro dias, o mesmo volume de tokens, e um custo por rodada que triplica. A única linha que cresceu junto com o custo é a que os gráficos de tokens nunca mostram: quanto foi gravado no cache.</figcaption>
</figure>

O dia 1 e o dia 4 enviaram o mesmo texto, e o dia 4 custou três vezes mais. A
diferença está inteira numa linha da fatura: no dia 1, três mil tokens por
rodada foram gravados no cache; no dia 4, setenta e dois mil. Todo o resto, as
releituras e as respostas, é quase idêntico.

Nos trinta dias desse projeto nessa família de modelo, saber quantos tokens um
dia enviou explica cerca de metade do que ele custou. Saber quanto ele gravou
no cache explica quase tudo.

Nada aqui é veredito sobre ferramenta alguma. É uma descrição da fatura. A
conta segue as gravações. O volume é espectador.

## O que a ferramenta faz com essas quatro linhas

Agora a ferramenta. Um proxy se coloca entre o agente e o modelo e encurta o
que o agente envia: apara um log comprido, dobra uma listagem repetida, troca
um resultado de busca prolixo por um resumo que pode ser expandido a pedido.
Ele faz isso bem. No nosso tráfego, removeu texto exatamente como anunciado.

A pergunta é o que isso faz com a fatura. Abaixo, uma rodada de trabalho,
linha por linha, no mesmo projeto e na mesma tabela de preços: a barra cinza é
uma rodada sem o proxy, a azul é uma rodada com ele.

<!-- FIG:PAIR -->
<figure class="diagram">
<svg viewBox="0 0 720 380" role="img" aria-label="A fatura por rodada de trabalho, sem o proxy e com ele. Texto relido do cache a 0,1 vez: 543.963 tokens sem, 293.047 com, menos 46 por cento. Texto gravado no cache a 1,25 a 2 vezes: 6.273 sem, 17.759 com, mais 183 por cento. Resposta gerada a 5 vezes: 874 sem, 1.209 com, mais 38 por cento. Custo por rodada: 17,6 centavos sem, 20,1 centavos com, mais 14 por cento." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><text x="16" y="22" font-size="12" font-weight="700" fill="#16233a">linha da fatura</text><text x="250" y="22" font-size="12" font-weight="700" fill="#16233a">preço</text><text x="330" y="22" font-size="12" font-weight="700" fill="#16233a">tokens por rodada de trabalho</text><rect x="330" y="30" width="11" height="11" fill="#9aa5b5"/><text x="346" y="40" font-size="11" fill="#16233a">sem o proxy</text><rect x="470" y="30" width="11" height="11" fill="#6b8ef2"/><text x="486" y="40" font-size="11" fill="#16233a">com o proxy</text><text x="16" y="72" font-size="13.5" fill="#16233a">texto relido do cache</text><text x="250" y="72" font-size="12.5" fill="#16233a" fill-opacity="0.8">0,1×</text><rect x="330" y="58" width="250" height="18" rx="3" fill="#9aa5b5"/><text x="586" y="71" font-size="12" fill="#16233a">543.963</text><rect x="330" y="82" width="135" height="18" rx="3" fill="#6b8ef2"/><text x="471" y="95" font-size="12" fill="#16233a">293.047 <tspan font-weight="700" fill="#1d7a4a">-46%</tspan></text><line x1="16" y1="114" x2="704" y2="114" stroke="#d5dde8"/><text x="16" y="148" font-size="13.5" fill="#16233a">texto gravado no cache</text><text x="250" y="148" font-size="12.5" fill="#16233a" fill-opacity="0.8">1,25× / 2×</text><rect x="330" y="134" width="88" height="18" rx="3" fill="#9aa5b5"/><text x="424" y="147" font-size="12" fill="#16233a">6.273</text><rect x="330" y="158" width="250" height="18" rx="3" fill="#6b8ef2"/><text x="586" y="171" font-size="12" fill="#16233a">17.759 <tspan font-weight="700" fill="#a4252c">+183%</tspan></text><line x1="16" y1="190" x2="704" y2="190" stroke="#d5dde8"/><text x="16" y="224" font-size="13.5" fill="#16233a">resposta gerada</text><text x="250" y="224" font-size="12.5" fill="#16233a" fill-opacity="0.8">5×</text><rect x="330" y="210" width="181" height="18" rx="3" fill="#9aa5b5"/><text x="517" y="223" font-size="12" fill="#16233a">874</text><rect x="330" y="234" width="250" height="18" rx="3" fill="#6b8ef2"/><text x="586" y="247" font-size="12" fill="#16233a">1.209 <tspan font-weight="700" fill="#a4252c">+38%</tspan></text><line x1="16" y1="266" x2="704" y2="266" stroke="#d5dde8"/><text x="16" y="308" font-size="14" font-weight="700" fill="#16233a">custo por rodada</text><rect x="330" y="292" width="219" height="18" rx="3" fill="#9aa5b5"/><text x="555" y="305" font-size="13" font-weight="700" fill="#16233a">US$ 0,176</text><rect x="330" y="316" width="250" height="18" rx="3" fill="#a4252c"/><text x="586" y="329" font-size="13" font-weight="700" fill="#a4252c">US$ 0,201 +14%</text><text x="16" y="370" font-size="11" fill="#16233a">Mesmo projeto, mesma tabela de preços. Sem o proxy: 13 dias, 3.915 rodadas. Com ele: 2 dias, 618 rodadas.</text></svg>
<figcaption>Uma rodada de trabalho, linha por linha, sem o proxy (cinza) e com ele (azul). A linha de 0,1× caiu quase pela metade. A linha de 2× quase triplicou. A rodada custou 14% a mais.</figcaption>
</figure>

Leia de cima para baixo.

**Primeira linha, releitura, a 0,1×.** É o que o proxy comprime, e funcionou:
quase metade do volume sumiu. É o gráfico que o produto mostra para você.

**Segunda linha, gravação, a até 2×.** É o preço de comprimir. O cache do
provedor é uma promessa de que *este exato texto* será visto de novo. No
momento em que o proxy muda o texto, o provedor vê texto novo, guarda de novo
e cobra o ágio da gravação. A gravação quase triplicou.

**Terceira linha, a resposta, a 5×.** Respostas mais longas. Parte disso é o
modelo mais novo, não o proxy; está aqui porque está na fatura.

**Última linha, o total.** Um token poupado na primeira linha vale um vinte
avos de um token acrescentado na segunda. A rodada custa 14% a mais.

Nada disso é defeito no código de ninguém. Uma ferramenta cuja função é mudar
o que o modelo vê é, por construção, uma ferramenta que força regravações. Ela
economiza na linha de 0,1× e gasta na linha de 2×.

Dois dias do lado com proxy é uma amostra curta, e os dois lados rodaram em
modelos irmãos, por isso o gráfico diz "mesma tabela de preços" e não "mesmo
modelo". Vamos continuar medindo. Mas a direção se repetiu em todo corte que
fizemos, e é a mesma direção que um estudo independente encontrou em julho: em
execuções pagas e controladas do mesmo agente de código, a configuração que
cortou 38% dos tokens entregues **aumentou a conta em 6,8%**, e a correlação
entre tokens cortados e dinheiro economizado foi de 0,15. A estimativa deles
para o máximo que comprimir texto visível pode economizar, dado o peso do cache
na conta: cerca de 5%.

## O que o painel chama de economia

Se a conta sobe, por que todo usuário dessas ferramentas relata economia? Porque
o painel da própria ferramenta é o comprovante que a maioria lê, e o painel
conta de outro jeito.

<!-- FIG:DASH -->
<figure class="diagram">
<svg viewBox="0 0 720 250" role="img" aria-label="O que o painel do proxy chama de economia, e o que os contadores dele mesmo dizem que aconteceu." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><text x="16" y="28" font-size="12" font-weight="700" fill="#16233a">Dólares que o painel chama de economia</text><text x="16" y="56" font-size="13" fill="#16233a">por comprimir texto</text><rect x="300" y="40" width="11" height="24" rx="4" fill="#1d7a4a"/><text x="319" y="57" font-size="14" font-weight="700" fill="#1d7a4a">US$ 14</text><text x="16" y="92" font-size="13" fill="#16233a">desconto de cache do próprio provedor</text><rect x="300" y="76" width="400" height="24" rx="4" fill="#8a94a3"/><text x="500" y="93" font-size="14" font-weight="700" text-anchor="middle" fill="#fff">US$ 1.667</text><text x="16" y="138" font-size="12" font-weight="700" fill="#16233a">Tokens, pelos contadores do próprio proxy</text><text x="16" y="166" font-size="13" fill="#16233a">removidos pela compressão</text><rect x="300" y="150" width="252" height="24" rx="4" fill="#1d7a4a"/><text x="560" y="167" font-size="14" font-weight="700" fill="#1d7a4a">1,79 M</text><text x="16" y="202" font-size="13" fill="#16233a">perdidos em regravações que ele causou</text><rect x="300" y="186" width="400" height="24" rx="4" fill="#a4252c"/><text x="500" y="203" font-size="14" font-weight="700" text-anchor="middle" fill="#fff">2,84 M</text><text x="16" y="240" font-size="11" fill="#16233a">3.200 pedidos. O relatório do próprio proxy termina com: saldo de tokens negativo.</text></svg>
<figcaption>Em cima: os dois números que o painel soma como "economizado". Embaixo: a contabilidade da própria ferramenta, tokens removidos contra tokens perdidos nas regravações que ela causou.</figcaption>
</figure>

O painel do nosso proxy, depois de 3.200 pedidos, informou US$ 14 economizados
por compressão e US$ 1.667 economizados por cache. O segundo número é o desconto
do próprio provedor: a linha de 0,1×, que todo usuário recebe com ou sem proxy.
Apresentados lado a lado, o desconto é a manchete e a compressão é arredondamento,
e um leitor que não conhece a fatura vê uma ferramenta que economizou mil e
seiscentos dólares.

O número mais honesto está três telas abaixo, nos contadores da própria
ferramenta: ela removeu 1,79 milhão de tokens por compressão e **perdeu 2,84
milhões em regravações de cache que ela mesma causou**. O contador se chama
*saldo de tokens: negativo*. A ferramenta sabe. Só não abre com isso.

Não fomos os primeiros a notar. Um desenvolvedor que rodou a mesma ferramenta
por vários dias descobriu que US$ 47 dos seus US$ 57 "economizados" eram o
desconto do provedor, e que só 2% do tráfego dele chegou a ser comprimido. O
conselho dele foi ler o detalhamento em vez da capa. O estudo acima diz a mesma
coisa no título.

## Uma correção, no mesmo espírito

Medir isso nos custou uma lição que devemos ao leitor. Até esta semana, todo
total desta série estava **cerca de duas vezes alto demais**. O registro do
agente escreve uma linha por pedaço de resposta, e cada linha repete o custo da
resposta inteira; estávamos contando linhas. Descobrimos ao construir uma tela
que abre a conta linha por linha, onde respostas idênticas com dois segundos de
diferença pareciam erradas. Confirmamos contra um registro independente de
pedidos e recontamos tudo.

Os totais dos episódios 1 e 2 caem pela metade. As conclusões sobrevivem, porque
já estavam enunciadas por rodada e os dois lados de cada comparação estavam
inflados pelo mesmo fator. Dizemos isso aqui porque o ponto deste episódio é que
contar tokens é traiçoeiro, e nós não somos exceção.

## O que pedir no lugar

Para um gestor, um executivo ou um pequeno empresário que paga por isso, o
resultado prático é uma troca de pergunta.

**Não pergunte quantos tokens foram economizados.** É a quantidade que as
ferramentas otimizam, e a quantidade com que a fatura menos se importa.

Peça três coisas:

1. **Custo por rodada de trabalho, por modelo, por dia.** É o único número que
   sobrevive a mudanças na quantidade de trabalho, e o único em que um antes e
   depois significa alguma coisa. O nosso está numa tela que abre de um total
   até cada pedido, com a conta mostrada em cada linha.
2. **A fatia da conta que é gravação em cache.** É a linha que moveu a nossa
   conta, e a linha que nenhum gráfico de tokens mostra. Se ela sobe, algo está
   mudando o texto entre uma rodada e outra: uma ferramenta, uma pausa longa,
   uma instrução que carrega a hora do dia.
3. **Qual modelo respondeu que tipo de tarefa.** Nos nossos dias, a escolha do
   modelo moveu a conta mais do que qualquer proxy, nas duas direções. É uma
   alavanca sua e não custa nada puxar.

A ferramenta dos episódios 1 e 2 continua instalada por enquanto, num só
projeto, num teste limpo, porque dois dias não são veredito e prometemos
publicar o número para o lado que ele for. Mas a série mudou de assunto. O token
é a unidade errada, e o resto destes episódios será escrito na unidade certa.

---

*Método, em resumo. Quatro projetos, 44 dias úteis, toda resposta do modelo lida
dos registros do próprio agente e precificada pelas tarifas publicadas do
provedor, incluindo as tarifas separadas de gravação em cache de cinco minutos e
de uma hora. Respostas deduplicadas pelo id da resposta. O projeto com proxy é
comparado só consigo mesmo, por rodada, numa família de modelo e numa tabela de
preços. Dias em que o proxy rodou uma configuração depois descoberta errada
ficam fora do antes e depois e não aparecem como evidência em lugar nenhum.
Todos os valores são equivalentes a preço de lista: pagamos um plano mensal
fixo, e esta série é o estudo que fazemos antes de migrar para o uso medido.*

*Fontes: S. Weinberger e A. Hozez, "Token Reduction Is Not Cost Reduction: An
Empirical Study of End-to-End Efficiency in API-Based Coding Agents",
arXiv:2607.12161, julho de 2026. O relato de campo dos US$ 47 em US$ 57 está em
russ.cloud, junho de 2026.*
