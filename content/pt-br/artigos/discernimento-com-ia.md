---
title: "Olhe antes de confiar: Discernimento, o terceiro D da Fluência em IA"
seoTitle: "Como avaliar a resposta da IA: produto, processo e desempenho"
date: 2026-11-27T10:00:00-04:00
draft: false
translationKey: "ai-fluency-discernment"
categories: ["Tecnologia"]
tags: ["ai-fluency", "ia-generativa"]
description: "Episódio 4 de Fluência em IA. O Discernimento, a arte de julgar o que a IA devolve: se o resultado está certo, se o raciocínio por trás dele se sustenta e se o jeito como ela trabalha com você está funcionando."
---

*Quarto episódio de **Fluência em IA**, uma série que percorre o AI Fluency
Framework uma competência por vez. O [episódio 1](/pt-br/artigos/fluencia-em-ia-em-mapa/)
desenhou o mapa inteiro, o [episódio 2](/pt-br/artigos/delegacao-com-ia/) percorreu
a Delegação, a decisão tomada antes de digitar, e o [episódio 3](/pt-br/artigos/descricao-com-ia/)
percorreu a Descrição, o que você digita; este é sobre o que você faz com a resposta.*

---

É sexta de manhã, e o cupom da Black Friday tem de estar no ar na segunda. Na
quinta à noite você mandou para a IA um pedido de dar orgulho, que dizia o que
você queria receber, pedia os casos de borda antes de qualquer código e mandava o
assistente ser breve, perguntar em vez de chutar e apontar os furos do seu plano.
Ela listou os casos de borda, você acrescentou o cliente que abre duas abas do
navegador e aplica o cupom nas duas, e foi dormir enquanto ela escrevia o código.
A resposta que espera por você agora é tudo o que um desenvolvedor cansado quer
ler: "Pronto. O cupom BLACKFRIDAY está no checkout e os 14 testes passam", seguida
de um resumo caprichado, uma lista arrumada dos arquivos alterados e uma fileira
verde de testes, e a tentação é fazer o merge, fechar o notebook e aproveitar o
resto do dia.

É exatamente dessa tentação que trata a próxima competência. O AI Fluency
Framework, criado por Rick Dakan, Joseph Feller e a Anthropic, chama essa
habilidade de **Discernimento**: avaliar com precisão a utilidade dos resultados e
dos comportamentos da IA, ou, nas palavras mais completas do glossário do
framework, avaliar com cuidado e senso crítico os resultados, os processos, os
comportamentos e as interações da IA, o que inclui julgar qualidade, precisão e
adequação e decidir o que melhorar. A Descrição era tirar da sua cabeça o que
estava lá e colocar na caixa de texto, e o Discernimento é o movimento contrário,
pegar o que saiu da caixa e comparar com o que você sabe, que é justamente a
única coisa a que a IA nunca teve acesso.

## O ramo, de perto

<figure class="diagram fluency-map fluency-map--main">
  <a href="/img/ai-fluency/discernment-map.pt-br.svg">
    <picture>
      <source media="(max-width: 1099px)" srcset="/img/ai-fluency/discernment-map-narrow.pt-br.svg">
      <img src="/img/ai-fluency/discernment-map.pt-br.svg" width="1200" height="770" loading="lazy"
        alt="Mapa mental do Discernimento, a terceira competência do AI Fluency Framework: julgar o que volta, e como chegou lá. Três ramos. Discernimento do produto, o resultado, correto, adequado, coerente e relevante, com as perguntas: está certo ou só arrumado, é o que eu pedi, o que faria isso quebrar. Discernimento do processo, como a IA chegou ao resultado, com as perguntas: cada passo faz sentido, o que ela pulou ou supôs, eu pensaria assim. Discernimento do desempenho, como a IA se comporta enquanto vocês trabalham, com as perguntas: o jeito dela me serve, ela perguntou ou chutou, ela só concorda comigo.">
    </picture>
  </a>
  <figcaption>Baseado no AI Fluency Framework © 2025 Rick Dakan, Joseph Feller e Anthropic, CC BY-NC-SA 4.0. As habilidades são do framework e os resumos de uma linha condensam as suas definições; as perguntas em volta são leitura minha. Compartilhado sob a mesma licença. Toque ou clique para abrir em tamanho real.</figcaption>
</figure>

Se o mapa parece conhecido, é de propósito. O Discernimento se divide nas mesmas
três linhas da Descrição, produto, processo e desempenho, e assim cada coisa que
você pediu na quinta vira algo a conferir na sexta: o resultado que você descreveu
agora é um resultado a julgar, os passos que você pediu agora são um raciocínio a
acompanhar, e o jeito como você pediu que a IA se comportasse agora é um
comportamento que você pode observar. As perguntas em volta de cada habilidade são
minhas, as que acho mais úteis quando uma resposta parece pronta, e, como as do
episódio anterior, servem menos como formulário e mais como um jeito de pegar
aquilo que uma olhada rápida deixa passar.

## Discernimento do produto: está certo, ou só arrumado?

O **discernimento do produto** é avaliar a qualidade do que a IA produz, e o
framework cita quatro qualidades a observar: precisão, adequação, coerência e
relevância. A dificuldade é que um assistente moderno entrega respostas que se
saem muito bem nas qualidades que se veem de relance, já que o código vem bem
formatado, os nomes fazem sentido e o resumo parece escrito por um colega
cuidadoso, enquanto a qualidade que mais importa, se aquilo faz a coisa certa para
o seu negócio, só pode ser julgada por quem conhece o negócio. Então você faz a
única coisa que a IA não podia fazer por você, que é testar o cupom do jeito que
um cliente de verdade faria: aplica o cupom, troca a forma de pagamento para Pix e
vê os dois descontos se somarem, exatamente o que a sua regra proíbe.

O que torna o momento instrutivo é a nota que veio junto com o código, que dizia,
numa frase calma e segura, que a soma era impossível porque o desconto do Pix é
sempre aplicado depois do cupom. O glossário do framework tem uma palavra para
isso, alucinação, quando a IA afirma com segurança algo plausível que não é
verdade, e a lição não é que o assistente mente, mas que a segurança do texto não
diz nada sobre a precisão dele. Uma afirmação que importa, daquelas de que o resto
da mudança depende, merece ser conferida no código ou no comportamento real, por
mais razoável que pareça.

## Discernimento do processo: o raciocínio se sustenta?

O **discernimento do processo** é avaliar como a IA chegou ao resultado,
procurando erros de lógica, falhas de atenção ou passos de raciocínio
inadequados, e é aqui que o pedido de quinta, para explicar o plano antes de cada
mudança, se paga, porque o plano agora está na tela para você ler. Lendo com o
erro da soma em mente, você vê onde ela errou: o plano confere a regra uma vez só,
no momento em que o cupom entra, e nunca mais, como se o carrinho não pudesse
mudar depois. Isso é um erro de lógica no raciocínio, não um erro de digitação no
código, e explica por que os testes não pegaram nada, já que a mesma IA escreveu
os catorze a partir da mesma suposição, e a fileira verde prova que o código faz o
que a IA acreditava, o que é bem diferente do que o negócio precisa.

O plano também mostra uma falha de atenção, do tipo que um revisor humano comete
num dia longo: ele nunca menciona a compra sem cadastro, em que o cliente compra
sem criar conta, e aí a regra de um uso por cliente não tem cliente para contar.
Nada no código está errado ali; alguma coisa simplesmente falta, e o que falta é o
mais difícil de ver numa resposta pronta, porque nada na tela aponta para isso.
Ler o raciocínio, e não só o resultado, é o jeito de encontrar, e é também por isso
que pedir à IA que mostre o raciocínio, na Descrição, e questionar esse
raciocínio, no Discernimento, são duas metades do mesmo hábito.

## Discernimento do desempenho: o jeito dela está funcionando para você?

O **discernimento do desempenho** é avaliar como a IA se comporta durante a
interação, considerando se o jeito como ela se comunica funciona para o que você
precisa, e é aquele em que quase ninguém pensa, embora o pedido de quinta tenha
deixado tudo fácil de conferir. Você pediu respostas curtas e recebeu três páginas,
pediu que ela perguntasse quando uma regra estivesse confusa e ela chutou como
arredondar o desconto, e pediu para ouvir sobre os furos do seu plano e não ouviu
nada, embora o plano tivesse pelo menos dois. Nada disso é defeito de caráter da
máquina, já que os assistentes tendem, por padrão, a respostas longas e
concordantes, mas perceber isso importa, porque um assistente que sempre concorda
com você é agradável de trabalhar e péssimo no serviço que você deu a ele.

O discernimento do desempenho alimenta direto a descrição do desempenho: quando
você percebe que o assistente está chutando em vez de perguntar, você diz de novo,
com mais firmeza, ou manda ele listar as suposições antes de escrever qualquer
coisa, e numa tarefa longa confere de novo depois de um tempo, porque o
comportamento tende a voltar ao padrão conforme a conversa cresce.

## O que a revisão pegou

<figure class="diagram fluency-map fluency-map--split">
  <a href="/img/ai-fluency/discernment-review.pt-br.svg">
    <img src="/img/ai-fluency/discernment-review.pt-br.svg" width="400" height="683" loading="lazy"
      alt="A resposta da IA e o que a revisão pegou. O que voltou: pronto, o cupom BLACKFRIDAY está no checkout e os 14 testes passam. O que a revisão pegou, em quatro partes. Produto: troque a forma de pagamento depois do cupom, e ele soma com o desconto do Pix. Processo: o plano confere a regra uma vez só, quando o cupom entra, e os 14 testes partem da mesma suposição. Processo: ela pulou a compra sem cadastro, onde um uso por cliente não tem cliente para contar. Desempenho: três páginas depois de você pedir algo curto, um chute sobre arredondamento em vez de uma pergunta, e nenhum furo apontado no seu plano.">
  </a>
  <figcaption>Um exemplo; as etiquetas são leitura minha das três habilidades de Discernimento do AI Fluency Framework, CC BY-NC-SA 4.0.</figcaption>
</figure>

Junte as três habilidades e a resposta animada de uma linha da sexta de manhã vira
a revisão da figura, quatro achados que levaram talvez vinte minutos e que
levariam bem mais tempo no sábado depois da Black Friday, com clientes de verdade e
estornos de verdade no meio. Um achado é sobre o produto, dois são sobre o processo
que o produziu e um é sobre o jeito como a IA trabalhou com você, e só o primeiro
apareceria numa olhada rápida na tela; os outros três exigiram que você lesse o
raciocínio e lembrasse do que tinha pedido.

## O que a pesquisa mostra

<figure class="diagram fluency-map fluency-map--split">
  <a href="/img/ai-fluency/discernment-index.pt-br.svg">
    <img src="/img/ai-fluency/discernment-index.pt-br.svg" width="400" height="554" loading="lazy"
      alt="Gráfico de barras do The AI Fluency Index, parcela de 9.830 conversas no Claude.ai. Percebe contexto faltando 20,3%. Questiona raciocínio fraco 15,8%. Confere fatos que importam 8,7%. Com e sem idas e vindas: percebe contexto faltando 22,8% contra 5,7%; questiona raciocínio fraco 17,9% contra 3,2%.">
  </a>
  <figcaption>Fonte: The AI Fluency Index, Anthropic, fevereiro de 2026, uma amostra de conversas de janeiro de 2026, que chama estes de os três comportamentos de discernimento. Rótulos encurtados por mim.</figcaption>
</figure>

O AI Fluency Index da Anthropic, o estudo publicado em fevereiro de 2026 que
classificou comportamentos de fluência em 9.830 conversas no Claude.ai, mediu três
comportamentos que ele agrupa como discernimento, e os três são raros. Em cerca de
uma conversa a cada cinco, 20,3%, as pessoas perceberam que podia faltar contexto
à IA; em 15,8% questionaram um raciocínio que não se sustentava; e em apenas 8,7%
conferiram os fatos e as afirmações que importavam. Comparado aos comportamentos de
descrição do episódio anterior, em que metade das conversas deixava claro o
objetivo, julgar a resposta acaba sendo bem menos comum do que pedi-la.

O mesmo padrão de antes aparece quando o estudo compara as conversas que tiveram
idas e vindas com as que pararam na primeira resposta, só que mais forte. Quem
refinou percebeu contexto faltando em 22,8% das conversas, contra 5,7% de quem não
refinou, e questionou o raciocínio em 17,9% contra 3,2%, o que os autores descrevem
como 5,6 vezes mais chance de questionar o raciocínio do Claude e 4 vezes mais
chance de identificar contexto faltando. Como sempre neste estudo, são
correlações, e os autores têm o cuidado de dizer que as pessoas podem muito bem
estar avaliando o resultado fora da conversa, testando ou usando, o que os
classificadores não enxergam. Para quem desenvolve, essa ressalva é real, já que
rodar o código é uma forma de discernimento, mas só conta quando os testes são
seus, ou pelo menos foram lidos por você, e não os catorze que a IA escreveu a
partir da própria suposição.

<figure class="diagram fluency-map fluency-map--split">
  <a href="/img/ai-fluency/discernment-finished.pt-br.svg">
    <img src="/img/ai-fluency/discernment-finished.pt-br.svg" width="400" height="630" loading="lazy"
      alt="Quando o trabalho parece pronto, conversas em que a IA produziu código ou um documento contra as em que não produziu. Percebe contexto faltando 15,8% contra 21,0%. Questiona raciocínio fraco 13,0% contra 16,2%. Confere fatos que importam 5,5% contra 9,2%. A hora de parar, três perguntas: isso está correto, falta alguma coisa, esse raciocínio se sustenta.">
  </a>
  <figcaption>Fonte: The AI Fluency Index, Anthropic, fevereiro de 2026; as três perguntas são conselho do próprio estudo. Rótulos encurtados por mim.</figcaption>
</figure>

O achado mais útil para este episódio é aquele com que o episódio anterior
terminou. Nas conversas em que a IA produziu um artefato, como código ou um
documento, as pessoas descreveram o pedido com mais cuidado no começo, e mesmo
assim os três comportamentos de discernimento caíram: perceber contexto faltando
foi de 21% para 15,8%, questionar o raciocínio de 16,2% para 13% e conferir fatos
de 9,2% para 5,5%. Os autores sugerem que resultados caprichados, com cara de
prontos, podem fazer outras perguntas parecerem desnecessárias, e dizem isso numa
frase simples: se o trabalho parece pronto, as pessoas podem tratá-lo como
pronto. O conselho deles para esse momento é igualmente simples: quando a IA
produz algo que parece bom, pare e pergunte se está correto, se falta alguma coisa
e se o raciocínio se sustenta, três perguntas que, na minha leitura, casam direitinho
com os três comportamentos que eles mediram.

## O laço que se fecha na sexta

<figure class="diagram fluency-map fluency-map--split">
  <a href="/img/ai-fluency/discernment-loop.pt-br.svg">
    <img src="/img/ai-fluency/discernment-loop.pt-br.svg" width="400" height="578" loading="lazy"
      alt="O laço Descrição–Discernimento na sexta de manhã, quatro passos num anel: descrever, o pedido de quinta; a IA responde, código e 14 testes verdes; discernir, ele soma com o desconto do Pix; refinar, conferir de novo quando o pagamento muda. No meio: 5,6 vezes mais chance de questionar o raciocínio com idas e vindas.">
  </a>
  <figcaption>O laço é do AI Fluency Framework, CC BY-NC-SA 4.0; a razão é do The AI Fluency Index, Anthropic, 2026. Os passos são um exemplo.</figcaption>
</figure>

O episódio 3 desenhou a Descrição e o Discernimento como um laço só, a habilidade
do dia a dia de trabalhar com IA, e a sexta de manhã é esse laço se fechando. A
descrição de quinta produziu código e catorze testes verdes, o discernimento de
sexta encontrou o desconto somado, a conferência única e o cliente sem cadastro, e
cada achado vira uma linha da próxima descrição: conferir a regra de novo sempre
que a forma de pagamento mudar, cobrir a compra sem cadastro pelo e-mail, escrever
os testes dos dois casos antes de mexer no código e listar todas as suposições
antes de escrever qualquer coisa. A segunda rodada volta mais perto, você julga de
novo, e em algum momento da terceira a resposta não está só arrumada, está certa.

## De volta à sexta de manhã

Repasse a manhã mais uma vez. A resposta chegou com cara de pronta, e em vez de
tratá-la como pronta você testou do jeito que um cliente faria, leu o plano do
jeito que um revisor faria e comparou o comportamento do assistente com o que você
tinha pedido, e isso transformou um animado "os 14 testes passam" em quatro
correções concretas e num fim de semana bem mais tranquilo. As mesmas três
perguntas, está certo, o raciocínio se sustenta e o jeito dela está funcionando
para mim, valem do mesmo jeito para uma migração de banco de dados, o resumo de um
contrato ou um relatório de mercado, e os autores do Index fazem uma observação
que vale guardar: conforme a IA fica melhor em produzir resultados caprichados, a
capacidade de avaliá-los fica mais valiosa, e não menos.

O que o Discernimento não resolve sozinho é quem responde pelo cupom quando ele
entrar no ar na segunda, quem precisa saber que uma IA escreveu a maior parte dele
e se a ferramenta que você usou era a certa para confiar o código de pagamento. Esse
é o assunto do último episódio, sobre a Diligência: responder pelo resultado, da
criação à transparência e à implantação.

*Fontes: o [AI Fluency Framework](https://www-cdn.anthropic.com/b383cf6baddbfc72fdf8b0ed533a518e2872d531.pdf)
e o [Key Terminology Cheat Sheet](https://www-cdn.anthropic.com/4396730ed190e691a3712cf2fd6bfe35509deca2.pdf)
da Anthropic, © 2025 Rick Dakan, Joseph Feller e Anthropic, CC BY-NC-SA 4.0; o curso
[AI Fluency: Framework & Foundations](https://anthropic.skilljar.com/ai-fluency-framework-foundations);
e o [The AI Fluency Index](https://www.anthropic.com/research/AI-fluency-index)
(Swanson, Bent, Ludwig, Dakan e Feller, fevereiro de 2026). Este artigo é um
explicador independente, não uma publicação da Anthropic.*
