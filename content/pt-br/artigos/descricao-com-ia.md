---
title: "Diga o que você quer: Descrição, o segundo D da Fluência em IA"
seoTitle: "Como descrever para a IA: produto, processo e desempenho"
date: 2026-11-17T12:00:00-04:00
draft: false
translationKey: "ai-fluency-description"
categories: ["Tecnologia"]
tags: ["ai-fluency", "ia-generativa"]
description: "Episódio 3 de Fluência em IA. A Descrição, a arte de dizer o que você precisa: o resultado que quer receber, o caminho que a IA deve seguir e o jeito como ela deve trabalhar com você."
---

*Terceiro episódio de **Fluência em IA**, uma série que percorre o AI Fluency
Framework uma competência por vez. O [episódio 1](/pt-br/artigos/fluencia-em-ia-em-mapa/)
desenhou o mapa inteiro e o [episódio 2](/pt-br/artigos/delegacao-com-ia/) percorreu
a Delegação, a decisão tomada antes de digitar; este é sobre o que você digita.*

---

Vamos voltar àquela quinta-feira à noite, com o cupom da Black Friday para
entregar na segunda. Da última vez você fez a parte difícil antes de abrir o
assistente: anotou para que a regra serve de verdade, lembrou que a ferramenta
não enxerga o seu repositório nem as suas reuniões e decidiu ficar com as regras
do negócio e com a revisão, deixando para a IA a primeira versão do código e dos
testes. Agora o cursor está piscando numa caixa vazia, e o velho hábito continua
ali, pronto para digitar "coloque a regra do cupom no nosso checkout" e torcer
pelo melhor. Desta vez a decisão por trás do pedido é boa, só que uma boa decisão
mal explicada ainda vai parar no lugar errado, porque a IA só sabe o que você
coloca em palavras, e tudo o que fica de fora ela preenche com um chute que soa
razoável e quase sempre é mediano.

O AI Fluency Framework, criado por Rick Dakan, Joseph Feller e a Anthropic, chama
essa habilidade de **Descrição**: descrever bem os objetivos para obter da IA
comportamentos e resultados úteis, ou, nas palavras do glossário do framework,
comunicar-se bem com sistemas de IA, deixando claro o resultado esperado,
orientando o caminho que a IA segue e dizendo como ela deve se comportar durante
o trabalho. É a competência que a maioria das pessoas conhece pelo nome popular,
escrever prompts, e o framework faz algo muito útil com ela: divide o pedido em
três perguntas que você responde uma de cada vez, e assim um bom prompt deixa de
depender de inspiração e passa a depender de não esquecer nada.

## O ramo, de perto

<figure class="diagram fluency-map fluency-map--main">
  <a href="/img/ai-fluency/description-map.pt-br.svg">
    <picture>
      <source media="(max-width: 1099px)" srcset="/img/ai-fluency/description-map-narrow.pt-br.svg">
      <img src="/img/ai-fluency/description-map.pt-br.svg" width="1200" height="770" loading="lazy"
        alt="Mapa mental da Descrição, a segunda competência do AI Fluency Framework: dizer o que você precisa, para a IA entregar. Três ramos. Descrição do produto, o resultado, com formato, público e estilo, e as perguntas: o que deve voltar e em que forma, quem vai ler ou rodar isso, tenho um exemplo do que é bom. Descrição do processo, como a IA aborda o seu pedido, e as perguntas: que passos e em que ordem, que contexto e regras ela precisa, pensar antes ou responder direto. Descrição do desempenho, como a IA se comporta enquanto vocês trabalham, e as perguntas: curta ou detalhada, me questionar ou me apoiar, perguntar ou supor.">
    </picture>
  </a>
  <figcaption>Baseado no AI Fluency Framework © 2025 Rick Dakan, Joseph Feller e Anthropic, CC BY-NC-SA 4.0. As habilidades são do framework e os resumos de uma linha condensam as suas definições; as perguntas em volta são leitura minha. Compartilhado sob a mesma licença. Toque ou clique para abrir em tamanho cheio.</figcaption>
</figure>

As três habilidades do mapa são do framework, e elas dividem o pedido por uma
linha fácil de guardar depois que você a enxerga: o que você quer receber, como a
IA deve chegar lá e como ela deve se comportar com você no caminho. As perguntas
em volta de cada habilidade são minhas, as que eu acabo repassando antes de
apertar enter, e funcionam menos como um formulário a preencher e mais como uma
lista que pega aquilo que você estava prestes a esquecer.

## Descrição do produto: o que deve voltar

A **descrição do produto** é definir o que você quer em termos de resultado,
formato, público e estilo, e é a parte que quase todo mundo já faz, mesmo que
pela metade. "Coloque a regra do cupom" diz qual é o produto, mas deixa a IA
decidir que tipo de mudança é essa, que arquivos ela mexe, se vem com testes e
em que forma tudo deve chegar, então ela responde com o que um desenvolvedor
qualquer escreveria para uma loja qualquer, que é justamente o que você não tem.
Dizer o que deve voltar, a mudança, os testes junto e uma notinha sobre o que
ficou de fora, já estreita bastante o chute, e dizer para quem é estreita ainda
mais, porque um código que um colega vai revisar amanhã e um rascunho que você
vai jogar fora hoje à noite não se escrevem do mesmo jeito.

A ferramenta mais subestimada desta parte é o exemplo. O glossário do framework
chama isso de few-shot, ensinar a IA mostrando exemplos do padrão que você quer,
e num sistema o exemplo quase sempre já existe: um cupom que segue o padrão da
casa, um teste escrito do jeito que o time gosta, uma mensagem de erro no tom do
produto. Apontar para um desses faz mais do que um parágrafo de adjetivos,
porque mostra à IA como é o bom no seu mundo em vez de pedir que ela imagine. As
regras também moram aqui, e são a parte que só você sabe: um uso por cliente,
nunca somando com o desconto do Pix e nada que deixe o checkout mais lento no dia
mais movimentado do ano.

## Descrição do processo: como chegar lá

A **descrição do processo** é definir como a IA aborda o seu pedido, por exemplo
dando a ela um passo a passo para seguir, e é onde a decisão que você tomou na
Delegação vira palavras. Você decidiu da última vez que os casos de borda seriam
pensados juntos antes de qualquer código, então o processo que você descreve diz
exatamente isso: primeiro liste os casos de borda que você enxerga, depois espere
a minha resposta, e só então escreva o código e os testes. Essa única frase
transforma uma resposta comprida, que você teria de desembaraçar sozinho, numa
conversa curta em que o seu conhecimento entra na hora em que ele faz falta.

O processo também é o lugar do contexto, que em software quer dizer mostrar o
código envolvido em vez de descrevê-lo de cabeça, e o lugar de pedir que a IA
raciocine antes de responder. O glossário tem nome para os dois hábitos: o
chain-of-thought, incentivar a IA a resolver o problema passo a passo, e o
pensar primeiro, pedir explicitamente que ela mostre o raciocínio antes da
resposta final. Na prática eles são tão simples quanto "me explique o seu plano
antes de mudar qualquer coisa", e fazem diferença porque um plano que você lê em
trinta segundos é o lugar mais barato para pegar uma suposição errada, muito
antes de ela ficar enterrada em duzentas linhas de código bem arrumado.

## Descrição do desempenho: como ela deve trabalhar com você

A **descrição do desempenho** é definir o comportamento da IA durante o trabalho
em conjunto, por exemplo se ela deve ser curta ou detalhada, se deve questionar
ou apoiar, e é a parte que quase todo mundo pula. Sem ela o assistente volta ao
jeito padrão, que puxa para respostas longas, um tom educado e uma disposição de
tapar qualquer buraco com uma suposição em vez de uma pergunta. Esse jeito padrão
serve para alguns momentos e atrapalha em outros: numa quinta à noite, com pouca
energia sobrando, você talvez queira respostas curtas, com certeza quer ser
perguntado em vez de ver a IA chutar quando uma regra está confusa, e bem pode
querer ouvir quando o seu próprio plano tem um furo, coisa que um assistente
prestativo raramente vai dizer sem que você peça.

O glossário do framework traz mais uma ferramenta que, na minha leitura, mora
neste ramo: o papel ou persona, pedir que a IA adote um personagem, um nível de
experiência ou um jeito de falar. "Revise isto como o desenvolvedor que cuida do
nosso sistema de pagamento há cinco anos" muda aquilo em que a IA presta atenção
e a franqueza com que ela fala, e isso também é uma forma de descrever o
desempenho.

## O mesmo pedido, antes e depois

<figure class="diagram fluency-map fluency-map--split">
  <a href="/img/ai-fluency/description-prompt.pt-br.svg">
    <img src="/img/ai-fluency/description-prompt.pt-br.svg" width="400" height="821" loading="lazy"
      alt="O pedido do checkout antes e depois. Antes: coloque a regra do cupom no nosso checkout. Depois, em seis partes. Produto: crie um cupom de Black Friday no checkout, seguem o CouponService e o código de preços que ele usa. Produto: um uso por cliente, ele nunca soma com o desconto do Pix. Produto: siga o cupom BEMVINDO10, que já usa o nosso padrão. Processo: primeiro liste os casos de borda e espere o meu ok, depois escreva o código e os testes. Processo: explique o seu raciocínio antes de cada mudança. Desempenho: seja breve; se uma regra estiver confusa, pergunte em vez de chutar, e me avise se o meu plano tiver furo.">
  </a>
  <figcaption>Um exemplo; as etiquetas são leitura minha das três habilidades de Descrição do AI Fluency Framework, CC BY-NC-SA 4.0.</figcaption>
</figure>

Junte as três habilidades e aquela frase solta da quinta à noite vira o pedido da
figura, que é mais longo mas nada sofisticado. Metade dele é produto, porque é ali
que mora o que você sabe do negócio: o que construir, o código envolvido, as
regras que ninguém mais conhece e um cupom existente para copiar. Duas linhas são
processo, pedindo primeiro os casos de borda e o raciocínio antes de cada
mudança, e uma linha é desempenho, pedindo respostas curtas, perguntas no lugar
de chutes e franqueza sobre o plano. Nada disso exige vocabulário especial, e
tudo já estava na sua cabeça; a única coisa que a Descrição acrescenta é o hábito
de tirar isso da cabeça e colocar na caixa antes que a IA comece a preencher o
seu silêncio por conta própria.

## A caixa de ferramentas

<figure class="diagram fluency-map fluency-map--split">
  <a href="/img/ai-fluency/description-toolbox.pt-br.svg">
    <img src="/img/ai-fluency/description-toolbox.pt-br.svg" width="400" height="716" loading="lazy"
      alt="Mapa mental das técnicas de prompt, agrupadas por habilidade. Descrição do produto: restrições de saída, formato, tamanho e estrutura; exemplos (few-shot), mostrar o que é bom. Descrição do processo: passo a passo, quebrar a tarefa em etapas; pensar primeiro, raciocínio antes da resposta. Descrição do desempenho: papel ou persona, com quem ela deve soar.">
  </a>
  <figcaption>Termos do AI Fluency Key Terminology Cheat Sheet, CC BY-NC-SA 4.0; o agrupamento por habilidade é leitura minha.</figcaption>
</figure>

As técnicas de prompt que circulam pela internet cabem direitinho nos mesmos três
ramos, e esse é um bom motivo para aprender primeiro os ramos e depois as
técnicas. O glossário do framework dá nome a cinco delas, e na minha leitura elas
se agrupam assim: as restrições de saída, dizer o formato, o tamanho e a
estrutura que você precisa, e os exemplos servem ao produto; o passo a passo e o
pensar primeiro dão forma ao processo; e o papel ou persona dá forma, sobretudo,
ao desempenho. Vista assim, uma técnica nunca é um fim em si mesma, e sim a
resposta para uma das perguntas do mapa, o que também mostra quando não vale a
pena usá-la: uma pergunta rápida não precisa de persona, e um rascunho
descartável não precisa de formato.

## O que a pesquisa mostra

<figure class="diagram fluency-map fluency-map--split">
  <a href="/img/ai-fluency/description-index.pt-br.svg">
    <img src="/img/ai-fluency/description-index.pt-br.svg" width="400" height="744" loading="lazy"
      alt="Gráfico de barras do The AI Fluency Index, parcela de 9.830 conversas no Claude.ai. Deixa claro o objetivo, 51,1%. Dá exemplos do que é bom, 41,1%. Especifica o formato, 30,0%. Define o jeito de interagir, 30,0%. Diz o tom e o estilo, 22,7%. Define o público, 17,6%. Com e sem idas e vindas: deixa claro o objetivo, 54,5% contra 30,9%; dá exemplos, 44,4% contra 21,8%; especifica o formato, 32,4% contra 16,1%.">
  </a>
  <figcaption>Fonte: The AI Fluency Index, Anthropic, fevereiro de 2026, com uma amostra de conversas de janeiro de 2026. Agrupar estes comportamentos como Descrição é leitura minha.</figcaption>
</figure>

O AI Fluency Index da Anthropic, o estudo publicado em fevereiro de 2026 que
classificou comportamentos de fluência em 9.830 conversas no Claude.ai, mostra
com que frequência as pessoas de fato fazem essas coisas, e o retrato é
desigual. Os comportamentos que eu leio como Descrição aparecem numa ordem bem
clara: mais ou menos metade das conversas deixou claro o objetivo antes de pedir
ajuda, 51,1%, umas quatro em dez deram um exemplo do que é bom, 41,1%, três em
dez disseram o formato que precisavam, e as mesmas três em dez disseram à IA
como queriam que ela interagisse, que é o que o estudo tem de mais próximo da
descrição do desempenho. Tom e estilo apareceram em 22,7% das conversas e o
público em só 17,6%, ou seja, quanto mais longe do produto está a habilidade,
menos as pessoas se dão ao trabalho de descrevê-la.

A segunda metade da figura é a mais interessante. Nas conversas em que as
pessoas foram e voltaram refinando o resultado, que foram 85,7% delas, cada um
desses comportamentos de descrição apareceu muito mais do que nas conversas que
pararam na primeira resposta: deixar claro o objetivo, 54,5% contra 30,9%,
exemplos, 44,4% contra 21,8%, e formato, 32,4% contra 16,1%. O estudo mostra
correlação, não causa, e eu não tiraria mais do que isso dali, mas combina com o
que a maioria de nós aprende fazendo: quem descreve bem costuma continuar a
conversa, e quem continua a conversa acaba descrevendo melhor.

O estudo também traz um alerta. Nas conversas em que a IA produziu algo
concreto, como código ou um documento, as pessoas descreveram mais no começo,
porém ficaram menos propensas a notar que faltava contexto, a conferir fatos ou
a questionar o raciocínio da IA depois, e os autores observam que esse controle
maior na largada não veio acompanhado de mais avaliação. Em outras palavras, um
pedido bem descrito pode deixar a resposta com cara de pronta, e é exatamente aí
que entra a próxima competência.

## O laço que mantém tudo honesto

<figure class="diagram fluency-map fluency-map--split">
  <a href="/img/ai-fluency/description-loop.pt-br.svg">
    <img src="/img/ai-fluency/description-loop.pt-br.svg" width="400" height="550" loading="lazy"
      alt="O laço Descrição–Discernimento, quatro passos num anel: descrever o produto, o processo e o desempenho; a IA responde com um rascunho, um plano ou código; discernir se está certo e como chegou ali; refinar e descrever de novo, melhor. No meio: 85,7% das conversas tiveram idas e vindas.">
  </a>
  <figcaption>O laço é do AI Fluency Framework, CC BY-NC-SA 4.0; a parcela é do The AI Fluency Index, Anthropic, 2026.</figcaption>
</figure>

O episódio 1 mostrou a Descrição ligada ao Discernimento num dos dois laços do
framework, o que cuida do trabalho do dia a dia com a IA, momento a momento.
Você descreve, a IA responde, você julga o que voltou e como ela chegou ali, e o
que você aprende com esse julgamento entra na próxima descrição, então um prompt
raramente sai certo de primeira, e nem precisa. Na quinta à noite o laço poderia
ser assim: a IA lista os casos de borda, você percebe que ela esqueceu o cliente
que abre duas abas do navegador e aplica o cupom nas duas, e a próxima descrição
inclui esse caso, que a IA nunca teria adivinhado e de que você nunca teria
lembrado sem ver a lista.

## De volta à quinta-feira à noite

Repasse a noite mais uma vez. A decisão por trás do pedido foi tomada na
Delegação, então o pedido que você digita agora diz o que você quer receber e
aponta o código e o cupom a copiar, pede os casos de borda antes de qualquer
código e o raciocínio antes de cada mudança, e diz à IA para ser breve, perguntar
em vez de chutar e apontar os furos do seu plano. Ele leva talvez três minutos a
mais para escrever do que a frase solta, e salva o fim de semana, não porque as
palavras sejam mágicas, mas porque a IA deixou de preencher o seu silêncio com um
chute mediano. As mesmas três perguntas, o que deve voltar, como chegar lá e como
trabalhar comigo, valem do mesmo jeito para uma migração de banco de dados, uma
revisão de código ou uma especificação técnica, e valem igualmente fora do
código.

O que a Descrição não consegue fazer sozinha é dizer se a resposta presta, e o
Index sugere que um pedido bem descrito torna essa pergunta mais fácil de
esquecer. Esse é o assunto do próximo episódio, sobre o Discernimento: como
julgar o produto, o processo e o desempenho que voltam da IA.

*Fontes: o [AI Fluency Framework](https://www-cdn.anthropic.com/b383cf6baddbfc72fdf8b0ed533a518e2872d531.pdf)
e o [Key Terminology Cheat Sheet](https://www-cdn.anthropic.com/4396730ed190e691a3712cf2fd6bfe35509deca2.pdf)
da Anthropic, © 2025 Rick Dakan, Joseph Feller e Anthropic, CC BY-NC-SA 4.0; o curso
[AI Fluency: Framework & Foundations](https://anthropic.skilljar.com/ai-fluency-framework-foundations);
e o [The AI Fluency Index](https://www.anthropic.com/research/AI-fluency-index)
(Swanson, Bent, Ludwig, Dakan e Feller, fevereiro de 2026). Este artigo é um
explicador independente, não uma publicação da Anthropic.*
