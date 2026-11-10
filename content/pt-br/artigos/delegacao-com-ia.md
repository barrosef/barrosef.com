---
title: "Antes de digitar: Delegação, o primeiro D da Fluência em IA"
seoTitle: "Delegação com IA: o que entregar à IA, e o que manter"
date: 2026-11-10T11:00:00-04:00
draft: false
translationKey: "ai-fluency-delegation"
categories: ["Tecnologia"]
tags: ["ai-fluency", "ia-generativa"]
description: "Episódio 2 de Fluência em IA. A Delegação, a decisão tomada antes do pedido: conhecer o problema, conhecer a ferramenta e dividir o trabalho para que cada lado faça o que faz melhor."
---

*Segundo episódio de **Fluência em IA**, uma série que percorre o AI Fluency
Framework uma competência por vez. O [episódio 1](/pt-br/artigos/fluencia-em-ia-em-mapa/)
desenhou o mapa inteiro; este percorre o seu primeiro ramo.*

---

Imagine uma quinta-feira à noite com uma feature para entregar na segunda. A
loja virtual precisa de uma regra nova de cupom no checkout a tempo da Black
Friday, e tudo o que você precisa saber sobre ela está espalhado entre o ticket,
umas conversas no chat, uma planilha do financeiro e as suas anotações de três
reuniões. A semana foi puxada e sobrou pouca energia, então você abre um
assistente de IA e digita algo como "coloque a regra do cupom no nosso
checkout". A resposta chega em segundos e tem cara de código pronto: uma função
bem arrumada, alguns testes e até comentários. Olhando com calma, porém, ela
chama uma função de pagamento que o seu sistema nunca teve, foi escrita para uma
versão antiga da biblioteca que vocês usam e deixa o cupom somar com o desconto
do Pix, justamente o que o financeiro disse na segunda reunião que não podia
acontecer de jeito nenhum. Os testes passam só porque conferem o que o código
faz, e não o que o negócio pediu, e lá se vai boa parte do fim de semana
desfazendo aquilo.

Nessa hora a vontade é culpar o pedido e procurar um jeito melhor de perguntar,
o que é uma habilidade de verdade e o assunto do próximo episódio. Só que o
problema daquela cena começou um passo antes, antes de qualquer palavra ser
digitada, no momento em que você entregou o trabalho inteiro, inclusive as
partes que só você podia fazer. O AI Fluency Framework, criado por Rick Dakan,
Joseph Feller e pela Anthropic, chama esse passo de **Delegação**: definir
objetivos e decidir se, quando e como usar a IA, o que na prática quer dizer
decidir que trabalho fica com as pessoas, que trabalho vai para a IA e como
dividir entre as duas. Das quatro competências do mapa, é, na minha leitura, a
que costuma vir primeiro e a mais fácil de pular, porque pular dá a impressão de
que você está ganhando tempo.

## O ramo, de perto

<figure class="diagram fluency-map fluency-map--main">
  <a href="/img/ai-fluency/delegation-map.pt-br.svg">
    <picture>
      <source media="(max-width: 1099px)" srcset="/img/ai-fluency/delegation-map-narrow.pt-br.svg">
      <img src="/img/ai-fluency/delegation-map.pt-br.svg" width="1200" height="770" loading="lazy"
        alt="Mapa mental da Delegação, a primeira competência do AI Fluency Framework: decidir se, quando e como trazer a IA. Três ramos. Consciência do problema, seu objetivo e o trabalho antes da IA, com as perguntas: como fica o trabalho pronto, para quem é e o que está em jogo, o que eu sei que a IA não sabe. Consciência da plataforma, o que esta IA faz bem e seus limites, com as perguntas: em que esta ferramenta é boa, o que ela não sabe ou não vê, onde ela pode chutar. Delegação de tarefas, dividir o trabalho pelos pontos fortes, com as perguntas: que partes pedem o meu julgamento, que partes a IA faz ou rascunha, e automação, ampliação ou agência.">
    </picture>
  </a>
  <figcaption>Baseado no AI Fluency Framework © 2025 Rick Dakan, Joseph Feller e Anthropic, CC BY-NC-SA 4.0. As habilidades são do framework e os resumos de uma linha condensam as suas definições; as perguntas em volta delas são leitura minha. Compartilhado sob a mesma licença. Toque ou clique para abrir em tamanho real.</figcaption>
</figure>

O framework divide a Delegação em três habilidades, e o mapa coloca, em volta de
cada uma, as perguntas que eu me pego fazendo quando as pratico. As habilidades
são do framework e os resumos de uma linha condensam as suas definições; já as
perguntas são minhas, uma porta de entrada e não parte do texto oficial. Lidos a
partir do alto, à esquerda, e seguindo para a direita e para baixo, os ramos vão
do trabalho para a ferramenta e depois para a divisão entre os dois, que é também
a ordem em que as decisões costumam acontecer.

## Consciência do problema: saber o que você está pedindo de verdade

O framework define a **consciência do problema** como entender com clareza os
seus objetivos e o tipo de trabalho antes de envolver a IA. Parece óbvio até
você reparar como isso escapa fácil quando o prazo aperta, porque o objetivo na
cena do checkout nunca foi "uma feature de cupom"; era uma promoção de Black
Friday que não podia comer a margem, ou seja, um cupom que não soma com o
desconto do Pix, um uso por cliente e um checkout que não pode ficar mais lento
no dia de maior movimento do ano. Dito assim, o trabalho muda de cara, porque
boa parte dele passa a ser amarrar regras e casos de borda que só a equipe
conhece, e muito pouco dele é digitar código.

As perguntas do mapa são um atalho para chegar lá. Como fica o trabalho pronto,
a ponto de você reconhecê-lo quando o vir, como faz um bom critério de aceite?
Para quem é, e o que quebra se der errado? E o que eu sei que a IA não sabe, a
história do código, o que ficou decidido naquela reunião, a regra que ninguém
escreveu, coisas que nenhum sistema vai adivinhar sozinho? A própria pesquisa da
Anthropic mostra que esse passo está longe de ser regra. No AI Fluency Index, um
estudo publicado em fevereiro de 2026 que classificou comportamentos de fluência
em 9.830 conversas no Claude.ai, o comportamento que eu leio como o mais próximo
da consciência do problema, deixar claro o objetivo antes de pedir ajuda,
apareceu em mais ou menos metade delas, 51,1%. Na outra metade, o objetivo nunca
foi posto em palavras antes do pedido, do mesmo jeito que naquela quinta-feira.

## Consciência da plataforma: conhecer o colega a quem você passa a tarefa

A segunda habilidade, a **consciência da plataforma**, é entender o que os
diferentes sistemas de IA conseguem e não conseguem fazer, e para isso não é
preciso ser especialista. É mais ou menos o que você gostaria de saber sobre um
colega novo e competente no primeiro dia na equipe antes de lhe passar uma
tarefa: no que ele é bom, o que ele ainda não tem como saber e onde costuma
chutar. O próprio glossário do framework dá nome aos limites. Um modelo tem uma
**data de corte do conhecimento**, depois da qual ele não sabe nada do mundo por
conta própria, e é por isso que pode escrever código para uma versão de
biblioteca mais antiga do que a sua. Tem uma **janela de contexto**, um limite de
quanta informação consegue levar em conta de uma vez, que muda de um modelo para
outro. E pode **alucinar**, afirmando com toda a confiança algo que parece certo
e está simplesmente errado, como uma função que tem tudo para existir e não
existe.

Cada um desses limites vira direto uma decisão de delegação. A IA da cena do
checkout não via o seu repositório, a não ser que você mostrasse o código
envolvido, então chutou uma função de pagamento em vez de usar a de verdade; e
não sabia nada das três reuniões, então não tinha como saber que o cupom não
podia somar. As ferramentas também são diferentes entre si, porque umas
conseguem ler o projeto inteiro, rodar os testes ou consultar a documentação,
enquanto outras só enxergam o que você cola no chat, de modo que a mesma tarefa
pode ser uma boa delegação para um sistema e uma furada para outro. Consciência
da plataforma é só o costume de perguntar, antes de entregar alguma coisa, se
esta ferramenta é a certa para esta parte do trabalho.

## Delegação de tarefas: dividir o trabalho pelos pontos fortes

A terceira habilidade, a **delegação de tarefas**, é onde as duas primeiras se
encontram: dividir o trabalho entre pessoas e IA com critério, aproveitando o
que cada lado faz melhor. A aula da Anthropic sobre o tema traz uma frase que eu
acho útil, a de que delegar bem exige conhecer o assunto e também entender o que
a IA consegue fazer. Na minha leitura, é por isso que uma desenvolvedora com anos
de casa no sistema de pagamentos delega esse trabalho melhor do que alguém que
chegou na semana passada, e por isso que ela, mesmo experiente, ainda precisa
conhecer a ferramenta para a divisão ficar boa.

<figure class="diagram fluency-map fluency-map--split">
  <a href="/img/ai-fluency/delegation-split.pt-br.svg">
    <img src="/img/ai-fluency/delegation-split.pt-br.svg" width="400" height="734" loading="lazy"
      alt="Mapa mental de uma tarefa dividida: uma regra nova no checkout no centro e os seus seis passos em volta. Um, definir o que é pronto, a regra e os critérios de aceite: você. Dois, mostrar o código envolvido e o que as reuniões decidiram: você. Três, pensar a solução e os casos de borda: juntos, ampliação. Quatro, escrever o código e os testes a partir do plano combinado: IA, automação. Cinco, revisar cada linha e rodar os testes: você. Seis, aprovar e subir para produção: você.">
  </a>
  <figcaption>Um exemplo de delegação de tarefas; a divisão é minha, não do framework. As formas de trabalho são do AI Fluency Framework, CC BY-NC-SA 4.0.</figcaption>
</figure>

A figura refaz a regra do checkout com a tarefa no centro e o trabalho dividido
em seis passos em volta, no sentido do relógio a partir do alto, bem parecido
com o exercício que o curso da Anthropic passa aos alunos: pegar um projeto com
várias etapas, quebrar em tarefas e planejar quais você faz sozinho e quais faz
com a IA. Na minha divisão, definir o que é pronto, a regra e os critérios de
aceite, fica com você, porque depende do que foi combinado com o negócio, e o
mesmo vale para mostrar o código envolvido e o que as reuniões decidiram, porque
isso está no seu repositório e nas suas anotações, e não no modelo. Pensar a
solução e os casos de borda se faz junto, como uma conversa. Escrever o código e
os testes a partir do plano combinado vai para a IA, que é rápida e não se cansa
justamente nisso. Revisar cada linha e rodar os testes volta para você, e no fim
aprovar e subir para produção também, já que a mudança vai ao ar com o seu nome.
Não tem nada de sofisticado nessa lista, e a graça está aí: a mesma ferramenta,
recebendo o quarto passo em vez do trabalho inteiro, entrega algo que você
consegue usar de verdade.

## Escolher como, e escolher não delegar

As marcações da figura levam à última decisão do ramo. O framework descreve três
formas de pessoas e IA trabalharem juntas: a **automação**, em que a IA executa
uma tarefa específica seguindo as suas instruções; a **ampliação**, em que vocês
pensam juntos, num vai e vem em que os dois contribuem; e a **agência**, em que
você prepara a IA para trabalhar sozinha em seu nome. Na minha leitura, escolher
entre elas faz parte do "como" de "se, quando e como", e por isso é assunto da
Delegação, e o mesmo trabalho pode pedir uma forma diferente a cada passo, como
acontece na regra do checkout. O AI Fluency Index viu que a forma de fluência
mais comum foi a ampliação, usar a IA como parceira para pensar em vez de jogar
o trabalho inteiro no colo dela. Viu também que só cerca de uma conversa em cada
dez, 10,1%, tinha a pessoa perguntando à IA como ela faria antes de mandar
fazer, o que, na minha leitura, talvez seja a pergunta de delegação mais barata
que existe, igual a pedir o plano a um colega antes de pedir o código.

O "se" dessa definição merece um parágrafo só para ele, porque delegar inclui
decidir ficar com parte do trabalho. Algumas partes de uma tarefa pedem um
julgamento que é seu, como qual regra de negócio vale quando duas batem de
frente ou que desenho a equipe vai ter de carregar por anos; outras carregam uma
responsabilidade que não dá para passar adiante, como o que sobe para produção;
e outras, sobretudo para quem está começando, existem justamente para você
aprender o sistema fazendo, e aí entregá-las à IA é perder o sentido da tarefa.
Uma boa delegação deixa essas partes com você de propósito, e não por descuido,
e muitas vezes são as partes que você guarda que fazem valer a pena as que você
entrega.

## O laço que traz você de volta

O episódio 1 mostrou a Delegação ligada à Diligência num dos dois laços do
framework, o das decisões estratégicas e éticas sobre o uso da IA. Na minha
leitura, o laço se fecha porque responder pelo resultado ensina o que delegar da
próxima vez: o fim de semana caçando uma função que nunca existiu é exatamente o
que faz você mostrar o código de verdade para a IA, e guardar as regras de
negócio com você, na próxima feature. A Delegação não é, portanto, uma decisão
tomada uma vez e esquecida na gaveta, mas uma que você revê cada vez que um
resultado volta, e o quinto episódio, sobre a Diligência, vai percorrer a outra
metade desse laço.

## De volta à quinta-feira à noite

Volte ao checkout e repasse a noite com o ramo na cabeça. Antes de abrir o
assistente, você gasta alguns minutos anotando para que a regra serve de verdade
e como vai saber que ela funciona; lembra que a ferramenta não enxerga o seu
repositório nem as suas reuniões, então decide mostrar o código envolvido e
levar as regras você mesmo; divide o trabalho, pensa a solução e os casos de
borda junto com a IA, deixa com ela a primeira versão do código e dos testes e
fica com a revisão. O pedido que você enfim digita não tem nada de genial, e
mesmo assim chega muito mais longe, porque a decisão por trás dele, tomada antes
de digitar e chamada pelo framework de Delegação, foi boa, e essa decisão
funciona do mesmo jeito para uma migração de banco, uma correção de bug, uma
revisão de código ou uma especificação técnica, e também fora do código.

O que ela não diz é como falar o que você precisa depois de decidir pedir, e
esse é o assunto do próximo episódio, sobre a Descrição: como descrever o
produto que você quer, o processo que a IA deve seguir e o jeito como ela deve
trabalhar com você.

*Fontes: o [AI Fluency Framework](https://www-cdn.anthropic.com/b383cf6baddbfc72fdf8b0ed533a518e2872d531.pdf)
e o [Key Terminology Cheat Sheet](https://www-cdn.anthropic.com/4396730ed190e691a3712cf2fd6bfe35509deca2.pdf)
da Anthropic, © 2025 Rick Dakan, Joseph Feller e Anthropic, CC BY-NC-SA 4.0; o
curso [AI Fluency: Framework & Foundations](https://anthropic.skilljar.com/ai-fluency-framework-foundations);
e [The AI Fluency Index](https://www.anthropic.com/research/AI-fluency-index)
(Swanson, Bent, Ludwig, Dakan e Feller, fevereiro de 2026). Este artigo é uma
explicação independente, não uma publicação da Anthropic.*
