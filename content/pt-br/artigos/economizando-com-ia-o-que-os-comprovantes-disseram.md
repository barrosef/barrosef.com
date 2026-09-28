---
title: "Uma ferramenta para gastar menos com IA aumentou a minha conta"
seoTitle: "Uma ferramenta para gastar menos com IA aumentou a conta"
date: 2026-09-28T09:00:00-04:00
draft: false
translationKey: "headroom-receipts"
categories: ["Technology"]
tags: ["claude-code", "headroom", "ai-assisted-development", "tooling", "cost", "economizando-com-ia"]
description: "Episódio 2. Economizou US$ 439 e cerca de US$ 1.200 voltaram em outra linha da mesma fatura — e a régua que eu escrevi antes era cega ali."
---

*Segundo episódio de **Economizando com IA**. O primeiro — {{< episode 1 >}} —
descreveu o que a ferramenta promete e a configurou. Este traz o que os
comprovantes dizem. Na semana que vem, o episódio três: a mesma ferramenta,
configurada como a documentação dela descreve, e não como eu improvisei.*

---

Há oito dias eu coloquei um proxy entre o meu agente de código e o modelo,
escrevi as regras do teste antes da primeira requisição passar, e prometi
publicar o que os comprovantes dissessem. É isto.

A versão curta: **economizou US$ 439, e cerca de US$ 1.200 voltaram em outra
linha da mesma fatura.**

As duas metades são reais. Entender como as duas podem ser verdade ao mesmo tempo
é o ponto inteiro deste episódio, e vale mais que qualquer um dos dois números.

<!-- FIG:BALANCE -->
<figure class="diagram">
<svg viewBox="0 0 720 210" role="img" aria-label="Três barras: 439 dólares economizados, cerca de 1.200 dólares pagos a mais, deixando cerca de 750 dólares negativos." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><text x="16" y="54" font-size="13.5" fill="#16233a">Economizou em texto enviado</text><rect x="300" y="36" width="110" height="26" rx="5" fill="#1d7a4a"/><text x="422" y="55" font-size="16" font-weight="700" fill="#1d7a4a">+$439</text><text x="16" y="104" font-size="13.5" fill="#16233a">Pagou a mais em regravação</text><rect x="300" y="86" width="300" height="26" rx="5" fill="#a4252c"/><text x="612" y="105" font-size="16" font-weight="700" fill="#a4252c">−$1.200</text><line x1="300" y1="124" x2="700" y2="124" stroke="#d5dde8"/><text x="16" y="154" font-size="13.5" fill="#16233a">Saldo, seis dias</text><rect x="300" y="136" width="188" height="26" rx="5" fill="#a4252c" opacity="0.85"/><text x="500" y="155" font-size="16" font-weight="700" fill="#a4252c">−$750</text><text x="16" y="198" font-size="11" fill="#16233a">US$ 439 é medido. Os outros dois são estimativa — três recortes põem o excesso entre US$ 1.110 e US$ 1.271.</text></svg>
<figcaption>Os seis dias, como extrato. A economia é real e a linha abaixo dela é maior.</figcaption>
</figure>

## O que ela fez, exatamente como anunciado

Seis dias de trabalho comum. 3.994 requisições, cada uma registrada com o que
entrou antes do proxy tocar e o que saiu depois.

**6,4% menos texto enviado ao modelo.** No `claude-opus-5`, que concentra 91% do
que eu gasto, a contabilidade do próprio proxy põe a economia em **US$ 438,94**.
Não é estimativa de fornecedor nem conta minha — é a ferramenta prestando contas
do próprio trabalho, e o meu registro de requisições concorda com ela.

O editor fez o serviço. Encurtou o dossiê antes de ele sair pela porta.

## E a fatura foi para o outro lado

Aqui está a parte que eu não vi chegando.

Um agente não tem memória, então cada passo reenvia a conversa inteira. O
provedor guarda essa conversa e cobra muito pouco para lê-la de volta — um
décimo da tarifa base. Guardar de novo custa **1,25×** a tarifa base. Entre
reaproveitar o que está guardado e guardar outra vez há um fator de **doze e
meio**, pelas mesmas palavras.

<!-- FIG:PRICE -->
<figure class="diagram">
<svg viewBox="0 0 720 210" role="img" aria-label="Duas barras comparando preços: reaproveitar o contexto guardado custa uma unidade, guardar de novo custa doze e meia." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><text x="16" y="62" font-size="14" font-weight="600" fill="#16233a">Reaproveitar o guardado</text><rect x="250" y="44" width="32" height="30" rx="6" fill="#1d4e89"/><text x="296" y="65" font-size="17" font-weight="700" fill="#1d4e89">1×</text><text x="16" y="136" font-size="14" font-weight="600" fill="#16233a">Guardar de novo</text><rect x="250" y="118" width="400" height="30" rx="6" fill="#a4252c"/><text x="664" y="139" font-size="17" font-weight="700" fill="#a4252c">12.5×</text><text x="16" y="26" font-size="11" fill="#5d6b7d">preço pelas mesmas palavras</text><text x="16" y="196" font-size="11" fill="#16233a">Leitura de cache custa 0,10× a tarifa base; escrita custa 1,25×.</text></svg>
<figcaption>As mesmas palavras, dois preços. Tudo que reescreve o começo da mensagem move tokens da coluna barata para a cara.</figcaption>
</figure>

O proxy encolhe a mensagem editando o **começo** dela: as definições de
ferramenta, o catálogo, as instruções que vêm antes de tudo. E o começo da
mensagem é exatamente o que o cache usa como chave. Mude um byte ali e nada
depois pode ser reaproveitado. A conversa inteira é guardada de novo, na tarifa
cara.

Pior: o quanto ele apara varia de requisição para requisição — vinte e oito
ferramentas diferidas numa chamada, vinte e uma na seguinte, seis na outra. O
prefixo nunca assenta. Então o cache nunca tem chance de se pagar.

O que isso parece, dia a dia:

<!-- FIG:DAILY -->
<figure class="diagram">
<svg viewBox="0 0 720 300" role="img" aria-label="Gráfico de barras de vinte e um dias úteis. Os quinze antes do proxy ficam entre 0,4 e 7,6 por cento; os seis depois vão de 13,1 a 37,5 por cento." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><rect x="60.0" y="239.4" width="26.7" height="10.6" fill="#c9d3df" rx="2"/><rect x="90.7" y="245.3" width="26.7" height="4.7" fill="#c9d3df" rx="2"/><rect x="121.3" y="231.8" width="26.7" height="18.2" fill="#c9d3df" rx="2"/><rect x="152.0" y="236.5" width="26.7" height="13.5" fill="#c9d3df" rx="2"/><rect x="182.7" y="245.9" width="26.7" height="4.1" fill="#c9d3df" rx="2"/><rect x="213.3" y="247.7" width="26.7" height="2.3" fill="#c9d3df" rx="2"/><rect x="244.0" y="243.0" width="26.7" height="7.0" fill="#c9d3df" rx="2"/><rect x="274.7" y="246.5" width="26.7" height="3.5" fill="#c9d3df" rx="2"/><rect x="305.3" y="241.2" width="26.7" height="8.8" fill="#c9d3df" rx="2"/><rect x="336.0" y="244.7" width="26.7" height="5.3" fill="#c9d3df" rx="2"/><rect x="366.7" y="235.9" width="26.7" height="14.1" fill="#c9d3df" rx="2"/><rect x="397.3" y="225.4" width="26.7" height="24.6" fill="#c9d3df" rx="2"/><rect x="428.0" y="224.2" width="26.7" height="25.8" fill="#c9d3df" rx="2"/><rect x="458.7" y="238.9" width="26.7" height="11.1" fill="#c9d3df" rx="2"/><rect x="489.3" y="205.4" width="26.7" height="44.6" fill="#c9d3df" rx="2"/><rect x="520.0" y="173.1" width="26.7" height="76.9" fill="#a4252c" rx="2"/><rect x="550.7" y="157.9" width="26.7" height="92.1" fill="#a4252c" rx="2"/><rect x="581.3" y="118.6" width="26.7" height="131.4" fill="#a4252c" rx="2"/><rect x="612.0" y="30.0" width="26.7" height="220.0" fill="#a4252c" rx="2"/><rect x="642.7" y="52.3" width="26.7" height="197.7" fill="#a4252c" rx="2"/><rect x="673.3" y="119.2" width="26.7" height="130.8" fill="#a4252c" rx="2"/><line x1="60" y1="250" x2="700" y2="250" stroke="#d5dde8" stroke-width="1.5"/><line x1="518.0" y1="22" x2="518.0" y2="250" stroke="#5d6b7d" stroke-width="1" stroke-dasharray="4 3"/><text x="524.0" y="18" font-size="11" fill="#5d6b7d">proxy ligado</text><text x="52" y="38" text-anchor="end" font-size="10.5" fill="#5d6b7d">40%</text><text x="52" y="137" text-anchor="end" font-size="10.5" fill="#5d6b7d">20%</text><text x="52" y="254" text-anchor="end" font-size="10.5" fill="#5d6b7d">0%</text><text x="60" y="270" font-size="10.5" fill="#5d6b7d">quinze dias antes</text><text x="700" y="270" text-anchor="end" font-size="10.5" fill="#5d6b7d">seis dias depois</text><text x="60" y="290" font-size="11" fill="#16233a">Guardado de novo, como fração do que foi reaproveitado — uma barra por dia.</text></svg>
<figcaption>A razão entre contexto guardado de novo e contexto reaproveitado, por dia. A mediana dos quinze dias anteriores era 1,9%; os seis dias seguintes correram entre 13% e 37%.</figcaption>
</figure>

É o mecanismo inteiro. Menos texto, mais dinheiro, nenhuma contradição.

## As regras que escrevi antes de medir

O episódio um se comprometeu com três números por antecipação, justamente para
que eu não pudesse torcê-los depois. Eis o placar.

| A regra que eu fixei | O que os comprovantes dizem | |
|---|---|---|
| Tokens por requisição caírem **15% ou mais** | **6,4%** | não |
| Re-leituras e recuperações subirem **no máximo um quinto** | re-leituras **caíram 31%**; recuperações foram 28 eventos em 3.994 requisições | sim |
| Latência acrescentada abaixo de **4 segundos** no percentil noventa | **9,5 segundos** (p99: 31s) | não |

Duas de três falharam, e a regra que eu escrevi dizia o que fazer nesse caso:
voltar ao modo cache ou à compactação sem perda, e dizer isso em voz alta. Estou
dizendo.

## A parte que de fato me ensinou algo

Olhe de novo para a linha do meio. Ela passou.

As re-leituras não subiram — **caíram**, quase um terço. As recuperações foram
erro de arredondamento. Pela letra da minha própria regra, o critério foi
atendido; e se eu tivesse olhado só para o que disse que ia olhar, teria
concluído que o editor estava se comportando bem.

Enquanto isso, as re**gravações** por requisição subiram **527%**.

Construí uma regra para me impedir de mover a trave, e a regra tinha um ponto
cego exatamente onde o dinheiro foi. Eu estava vigiando a metade barata do cache
e não tinha escrito nada sobre a metade cara.

Se você levar uma coisa deste episódio, leve essa. Não é "proxy de compressão é
ruim" — não é. **A medição que você desenha antes do experimento é ela mesma uma
hipótese, e pode estar errada de um jeito que o experimento não vai te contar.**
A minha estava.

## Onde ela funciona

A mesma ferramenta, a mesma semana, três modelos diferentes:

<!-- FIG:MODEL -->
<figure class="diagram">
<svg viewBox="0 0 720 250" role="img" aria-label="Três barras horizontais: Opus economiza 5,4 por cento e é 91 por cento do gasto; Sonnet economiza 32,6 por cento e é 3 por cento; Haiku economiza 44,1 por cento e é 0,3 por cento." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><text x="16" y="56" font-size="14" font-weight="600" fill="#16233a">Opus</text><text x="16" y="73" font-size="10.5" fill="#5d6b7d">fatia do gasto: 91%</text><rect x="130" y="40" width="420" height="28" rx="6" fill="#eef2f7"/><rect x="130" y="40" width="45" height="28" rx="6" fill="#1d7a4a"/><text x="566" y="60" font-size="15" font-weight="700" fill="#1d7a4a">−5,4%</text><rect x="646" y="46" width="109" height="16" rx="3" fill="#a4252c"/><text x="16" y="118" font-size="14" font-weight="600" fill="#16233a">Sonnet</text><text x="16" y="135" font-size="10.5" fill="#5d6b7d">fatia do gasto: 3%</text><rect x="130" y="102" width="420" height="28" rx="6" fill="#eef2f7"/><rect x="130" y="102" width="274" height="28" rx="6" fill="#1d7a4a"/><text x="566" y="122" font-size="15" font-weight="700" fill="#1d7a4a">−32,6%</text><rect x="646" y="108" width="4" height="16" rx="3" fill="#a4252c"/><text x="16" y="180" font-size="14" font-weight="600" fill="#16233a">Haiku</text><text x="16" y="197" font-size="10.5" fill="#5d6b7d">fatia do gasto: 0.3%</text><rect x="130" y="164" width="420" height="28" rx="6" fill="#eef2f7"/><rect x="130" y="164" width="370" height="28" rx="6" fill="#1d7a4a"/><text x="566" y="184" font-size="15" font-weight="700" fill="#1d7a4a">−44,1%</text><rect x="646" y="170" width="3" height="16" rx="3" fill="#a4252c"/><text x="130" y="28" font-size="10.5" fill="#5d6b7d">texto economizado</text><text x="646" y="28" font-size="10.5" fill="#5d6b7d">fatia do gasto</text><text x="16" y="238" font-size="11" fill="#16233a">Ela rende de seis a oito vezes mais nos modelos que quase não pesam na conta.</text></svg>
<figcaption>Texto economizado por modelo contra a fatia de gasto de cada um. A barra verde é a economia; a vermelha é onde o dinheiro está.</figcaption>
</figure>

De seis a oito vezes mais eficaz nos modelos baratos do que no caro — e o caro é
onde está praticamente todo o dinheiro.

Isso não é defeito da ferramenta, é descasamento entre onde ela alcança e onde o
meu gasto mora. Minhas sessões no modelo grande são longas, e o que as enche é a
conversa acumulada, não a saída das ferramentas. No período inteiro, resultado de
ferramenta foi **menos de 1% do tráfego**. Um proxy que comprime saída de
ferramenta não move um número dominado pela conversa sendo relida.

Em trabalho curto, barato e descartável — um subagente que lê três arquivos e
responde — ela vai muito bem.

## O que eu não rodei

Preciso ser direto sobre o alcance deste veredito, porque ele é mais estreito que
a manchete.

Rodei a configuração básica: subir o proxy, apontar o agente para ele, proteger
conteúdo de arquivo da compressão, truncar descrição de ferramenta. Foi o que o
episódio um descreveu, e foi o que eu medi.

Não é o que a documentação descreve. Quatro capacidades da ferramenta nunca foram
ligadas, e uma delas reduz a **resposta** em vez da pergunta — o lado da saída,
que no modelo caro custa cinco vezes o que custa a entrada, e que no meu caso
nunca produziu uma única medição. O roteamento também está incompleto: algumas
das minhas sessões passaram por fora do proxy, o que significa que estes números
subestimam o tráfego e superestimam a parte do dano que cabe à ferramenta, ao
mesmo tempo.

Então isto é uma leitura da minha configuração. Não é um veredito sobre a
ferramenta.

## Antes de comprar eficiência para o seu gasto com IA

Cinco perguntas, na ordem em que eu gostaria de tê-las feito.

**Qual unidade ela otimiza, e é essa a unidade da sua fatura?** Token,
requisição, janela de contexto e dólar são quatro coisas diferentes, e uma
otimização pode ganhar numa e perder em outra.

**Se ela mexe no começo do prompt, meça o cache.** Qualquer coisa que reescreva o
prefixo invalida tudo depois dele. Acompanhe guardado-de-novo contra
reaproveitado, não só volume total.

**Compare dinheiro em dias comparáveis.** Minha primeira tentativa de análise
anunciou 18% de melhora, que evaporou assim que controlei como os dias estavam
estruturados. Porcentagem de texto é fácil e enganosa; dólar por unidade
comparável de trabalho é difícil e honesto.

**Aponte para onde o gasto realmente está.** Se 90% da sua conta é um modelo, uma
ferramenta que brilha nos outros 10% não vai aparecer na fatura.

**Defina um teto antes de ligar qualquer coisa.** Eu não tinha nenhum. Uma
otimização que custa mais em silêncio é exatamente o modo de falha que um teto
pega.

## Episódio três

Na semana que vem, a mesma ferramenta, configurada como a documentação dela
descreve: o redutor de saída ligado, o roteamento tornado durável para que toda
sessão passe mesmo por ele, o trabalho apontado para os modelos onde ela já
performa, e um teto de gasto definido.

Aí eu meço de novo e publico esse número também, para o lado que ele for. Se ele
merecer a cadeira, eu digo. Ainda não mereceu.

*Versões: Headroom 0.36.5, Claude Code 2.1.278, setembro de 2026. Os números vêm
das minhas próprias transcrições do Claude Code e do log de requisições do proxy,
num projeto real que não é o assunto e não é nomeado. Os US$ 439 e as
porcentagens são medidos; os ~US$ 1.200 e o saldo de ~−US$ 750 são estimativa —
três recortes independentes põem o excesso entre US$ 1.110 e US$ 1.271, e 290
pausas de mais de uma hora no período quebram o cache por conta própria, o que
faz desse valor um teto do que o proxy sozinho custou.*
