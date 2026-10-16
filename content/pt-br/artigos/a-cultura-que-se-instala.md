---
title: "A Cultura que se Instala"
date: 2026-10-16T17:00:00-04:00
draft: false
translationKey: "foreman-culture"
categories: ["Tecnologia"]
tags: ["agentes-de-ia", "entrega-de-software", "cultura-de-engenharia", "foreman", "dop"]
description: "Todo projeto AI-first começava com a mesma explicação sobre quem decide, quem constrói e quem confere. O foreman escreve isso uma vez e instala em dois passos."
---

Todo projeto que conduzi com um agente de IA ao teclado começou do mesmo jeito,
e durante muito tempo eu não percebi que começava. Antes da primeira linha de
código havia uma conversa sobre como o trabalho iria acontecer: quem decide o que
um pedido realmente pede, quem escreve a mudança, quem olha para ela com olho
desconfiado, quando o agente deve parar e perguntar em vez de adivinhar, e o que
"pronto" significa para quem está pagando. Eu tinha essa conversa comigo mesmo,
depois com o agente, depois de novo no projeto seguinte, e a cada vez ela saía um
pouco diferente, porque morava em quem tinha feito o projeto anterior, e essa
pessoa estava cansada, ou com pressa, ou simplesmente tinha esquecido metade.

O agente, enquanto isso, fazia o que agentes fazem quando as regras chegam tarde
ou incompletas: preenchia as lacunas com o seu melhor palpite. Às vezes o palpite
era bom. Às vezes ele revisava o próprio trabalho e aprovava, o que não é uma
revisão, mas o mesmo raciocínio concordando consigo mesmo; às vezes rodava um
teste à mão de um jeito que ninguém conseguiria repetir; às vezes me fazia uma
pergunta que eu já tinha respondido em outro projeto, e às vezes não fazia a única
pergunta que importava. Nada disso era culpa do agente. O jeito de trabalhar nunca
tinha sido escrito, então não havia nada para ele seguir.

Esta é a história de como aquela conversa virou um documento, de como o documento
virou algo que se instala em dois passos, e do que sai do outro lado: um jeito de
construir e entregar software que corre AI-first do pedido ao código em
funcionamento, com o humano decidindo nos portões e em nenhum outro lugar.

## Escrever uma vez

Numa plataforma de um cliente, depois de meses disso, a conversa finalmente virou
um documento, e o documento se revelou feito de três camadas que eu vinha
misturando desde sempre.

A primeira camada são as **regras**, escritas para qualquer agente, num arquivo
que não nomeia fornecedor nem modelo. Ele diz, em frases simples, que quem decide
não executa, que quem executa só toca no que a tarefa nomeia, que o plano passa por
alguém cujo trabalho é objetar antes que qualquer pessoa comece a construir, que o
resultado é atacado depois por um time que não o escreveu, e que existe exatamente
um portão humano, que fica depois de o trabalho estar no ar e não antes. Diz
também a coisa que fez toda a diferença numa tarde ruim: não pergunte nada que
você mesmo possa decidir. Uma pergunta ao humano é uma interrupção, para ser gasta
só quando as regras realmente não cobrem o caso.

A segunda camada são os **papéis**, quatro, escritos como contratos e não como
programas. Um arquiteto, que lê o pedido, duvida dele, o confronta com o código,
escreve o que vai mudar e por quê, e divide o trabalho. Um revisor, que trabalha no
mesmo nível do arquiteto, porque um revisor um degrau abaixo só consegue revisar
ortografia, e cujo sucesso se mede em objeções que mudaram o plano, nunca em planos
aprovados depressa. Executores, que recebem uma fronteira e devolvem o que
encontraram, incluindo a linha que diz que esbarraram em algo que não lhes pediram
para tocar. E um time de qualidade com um líder próprio, que decide o que os testes
precisam cobrir e qual pode ser o tamanho do ataque, e que reporta uma fraqueza
mesmo quando ela não é defeito deste trabalho em particular. Os papéis puxam uns
contra os outros de propósito, e quando discordam o arquiteto decide e escreve o
porquê, para que a mesma objeção não volte um mês depois sem que ninguém saiba
dizer o que foi feito dela.

A terceira camada é a que eu nunca tinha separado, e é onde a cultura encontra o
projeto: cinco **registros** de fatos que uma cultura não tem como saber sozinha.
Quais bases de código existem e como se relacionam. Como o trabalho viaja pelos
ramos até um ambiente em funcionamento, e o que "entregue" significa ali. Como a
aplicação sobe, desce e é testada. Onde um pedido mora enquanto está sendo
trabalhado, e qual evento o move de um estado ao seguinte. E como a qualidade se
sustenta, quais camadas de teste uma mudança deve, e com quais ferramentas. As
regras diziam algo desconfortável sobre esses cinco: se qualquer um deles falta,
você para. Não começa um pedido, não adivinha a convenção, não a infere do código.
Diz qual registro está faltando, e espera.

Essa regra era o ponto. Era também o problema, para quem chegava.

## Transformar em algo que se instala

Uma cultura que para quando falta um registro é uma cultura que, num projeto
novo, para imediatamente. Escrever os cinco registros à mão me custou boa parte de
uma semana na primeira plataforma, com a história do projeto diante dos olhos.
Ninguém adotando o jeito de trabalhar pela primeira vez faria isso, e eu não
queria explicar tudo de novo. Então o documento virou uma ferramenta, e a
ferramenta se chama **foreman**, o nome em inglês do papel do arquiteto: aquele
que decide e não executa. Ela é [pública](https://github.com/barrosef/foreman), e
adotá-la são dois passos. O primeiro instala. O segundo, executado dentro de
qualquer projeto, faz o resto.

<!-- fig:layers -->
<figure class="diagram"><svg viewBox="0 0 720 430" role="img" aria-label="Diagrama do que o foreman instala: uma faixa superior com três passagens, detecta, pergunta e escreve; uma zona à esquerda com a cultura, regras, quatro papéis e o mecanismo mais cinco agentes; uma zona à direita com os cinco registros, cada um marcado como detectado, respondido ou padrão." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="h-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#16233a"/></marker><marker id="h-navy" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#1d4e89"/></marker><marker id="h-muted" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#5d6b7d"/></marker><marker id="h-gold" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#b7791f"/></marker></defs><rect x="16" y="16" width="688" height="84" rx="10" fill="#eef2f7" stroke="#d5dde8" stroke-width="1"/><text x="32" y="38" text-anchor="start" font-size="12" font-weight="600" fill="#5d6b7d">a instalação, em três passagens</text><rect x="32" y="40" width="196" height="48" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="130.0" y="61.0" text-anchor="middle" font-size="13" font-weight="600" fill="#16233a">detecta</text><text x="130.0" y="78.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">lê só o que o projeto versiona</text><rect x="262" y="40" width="196" height="48" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="360.0" y="61.0" text-anchor="middle" font-size="13" font-weight="600" fill="#16233a">pergunta</text><text x="360.0" y="78.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">até cinco, resposta já marcada</text><rect x="492" y="40" width="196" height="48" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="590.0" y="61.0" text-anchor="middle" font-size="13" font-weight="600" fill="#16233a">escreve</text><text x="590.0" y="78.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">nunca por cima do que já existia</text><path d="M 230,64 L 258,64" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><path d="M 460,64 L 488,64" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><rect x="16" y="118" width="330" height="296" rx="10" fill="#eef2f7" stroke="#d5dde8" stroke-width="1"/><text x="32" y="140" text-anchor="start" font-size="12" font-weight="600" fill="#5d6b7d">a cultura · idêntica em todo projeto</text><rect x="32" y="144" width="298" height="54" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="181.0" y="162.0" text-anchor="middle" font-size="13" font-weight="600" fill="#16233a">as regras</text><text x="181.0" y="178.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">princípios, o ciclo,</text><text x="181.0" y="192.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">um portão humano</text><rect x="32" y="206" width="298" height="54" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="181.0" y="224.0" text-anchor="middle" font-size="13" font-weight="600" fill="#16233a">quatro papéis como contratos</text><text x="181.0" y="240.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">arquiteto · revisor ·</text><text x="181.0" y="254.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">executores · time de qualidade</text><rect x="32" y="268" width="298" height="54" rx="6" fill="#1d4e89" stroke="#173d6e" stroke-width="1.2"/><text x="181.0" y="286.0" text-anchor="middle" font-size="13" font-weight="600" fill="#fff">o mecanismo</text><text x="181.0" y="302.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#cfe0f5">papéis → agentes ·</text><text x="181.0" y="316.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#cfe0f5">capacidade e esforço por papel</text><text x="181" y="344" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">cinco agentes, copiados, seus para ajustar</text><rect x="40" y="352" width="56" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="68.0" y="367" text-anchor="middle" font-size="9.5" font-weight="400" fill="#16233a">reviewer</text><rect x="102" y="352" width="45" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="124.5" y="367" text-anchor="middle" font-size="9.5" font-weight="400" fill="#16233a">reader</text><rect x="153" y="352" width="51" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="178.5" y="367" text-anchor="middle" font-size="9.5" font-weight="400" fill="#16233a">builder</text><rect x="210" y="352" width="51" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="235.5" y="367" text-anchor="middle" font-size="9.5" font-weight="400" fill="#16233a">qa lead</text><rect x="267" y="352" width="45" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="289.5" y="367" text-anchor="middle" font-size="9.5" font-weight="400" fill="#16233a">tester</text><rect x="362" y="118" width="342" height="296" rx="10" fill="#eef2f7" stroke="#d5dde8" stroke-width="1"/><text x="378" y="140" text-anchor="start" font-size="12" font-weight="600" fill="#5d6b7d">o projeto · preenchido na instalação</text><rect x="378" y="144" width="310" height="38" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="533.0" y="160.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">repositórios</text><text x="533.0" y="177.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">o que existe e como se relaciona</text><rect x="378" y="186" width="310" height="38" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="533.0" y="202.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">entrega</text><text x="533.0" y="219.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">ramos, pull requests, o que é DEV</text><rect x="378" y="228" width="310" height="38" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="533.0" y="244.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">ambiente</text><text x="533.0" y="261.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">subir, derrubar, testar</text><rect x="378" y="270" width="310" height="38" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="533.0" y="286.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">demandas</text><text x="533.0" y="303.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">onde um pedido mora, como se move</text><rect x="378" y="312" width="310" height="38" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="533.0" y="328.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">qualidade</text><text x="533.0" y="345.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">camadas de teste, o time, relatórios</text><text x="378" y="370" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">cada valor diz como foi preenchido:</text><rect x="378" y="376" width="64" height="22" rx="11" fill="#1d4e89" stroke="#1d4e89" stroke-width="1"/><text x="410.0" y="391" text-anchor="middle" font-size="10" font-weight="400" fill="#fff">detectado</text><rect x="448" y="376" width="70" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="483.0" y="391" text-anchor="middle" font-size="10" font-weight="400" fill="#16233a">respondido</text><rect x="524" y="376" width="47" height="22" rx="11" fill="#eef2f7" stroke="#b9c5d4" stroke-width="1"/><text x="547.5" y="391" text-anchor="middle" font-size="10" font-weight="400" fill="#5d6b7d">padrão</text><path d="M 590,92 L 590,112" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/></svg><figcaption>O que dois passos deixam para trás. A cultura, à esquerda, é a mesma em todo projeto e não nomeia fornecedor; os cinco registros, à direita, são do projeto, preenchidos na instalação com o que foi detectado, respondido ou assumido por padrão, e editados livremente depois.</figcaption></figure>

O que "o resto" significa é a parte de que mais me orgulho, porque inverte a regra
sem quebrá-la. O foreman primeiro lê o projeto, o que lhe é permitido desde que
leia só o que o projeto versiona: encontra as peças e como estão costuradas, quais
ramos existem e o que a história recente diz sobre como o time trabalha, os
comandos que sobem as coisas e rodam os testes, se as mensagens de commit estão em
inglês ou em português, se há um lugar onde as decisões já são registradas. Depois
pergunta, e pergunta o mínimo que consegue. No máximo cinco perguntas, uma por
registro, em linguagem simples, cada uma com a resposta que detectou já marcada
como recomendada, e a primeira de todas oferece aceitar todos os padrões de uma
vez. Então escreve os cinco registros, preenchidos, com cada valor detectado,
respondido ou assumido por padrão, e cada registro diz na primeira página como foi
preenchido, para que ninguém mais tarde confunda um padrão com uma decisão que
alguém tomou sobre o seu projeto.

O agente que abre o projeto na manhã seguinte encontra os cinco registros no
lugar, e a regra que diz "se algum falta, você para" está satisfeita sem que
ninguém tenha sido parado. O projeto edita os registros sempre que discorda,
porque são arquivos comuns dentro da sua própria base de código, e o foreman
nunca mais pergunta. Mudar um registro é editar um arquivo.

### Como o próprio foreman foi construído

Quero contar esta parte porque o foreman foi construído do jeito que a cultura
diz que software deve ser construído, e a tarde que isso levou foi o melhor
argumento que já vi a favor da cultura.

Começou com um documento de design, e antes que eu escrevesse uma linha da
ferramenta, um leitor que nunca tinha visto a conversa recebeu esse documento com
uma única pergunta: o que você ainda precisaria saber para construir isto? Vieram
quatro perguntas de volta, e três eram reais. Uma delas, sobre o que acontece
quando a ferramenta encontra um projeto feito de várias bases de código em vez de
uma, mudou o design.

Depois veio um plano em que cada peça chegava com o seu teste primeiro. A detecção
da forma do projeto, a entrevista, a escrita de arquivos dentro do projeto de
outra pessoa sem jamais sobrescrever um byte que já estava lá: cada uma existiu
como um teste falhando antes de existir como código, e o teste foi visto falhando,
para que quando passasse houvesse um motivo para acreditar nele. No fim eram cento
e noventa e cinco dessas verificações, e elas rodam contra quatro pequenos projetos
de mentira, construídos do zero a cada vez: um vazio, um comum, um feito de várias
peças com os detalhes incômodos que projetos reais têm, e um que já tinha passado
pela ferramenta.

Então um revisor que não tinha visto nada daquilo leu o todo. Encontrou um jeito de
a ferramenta quebrar no tipo mais comum de notebook, e mais dez defeitos que
valiam a correção, e cada um deles foi corrigido na mesma tarde, cada um com o seu
próprio teste escrito antes. Eu não reli o meu trabalho e chamei isso de revisão;
a cultura não permite, e tinha razão.

E então o primeiro cliente encontrou mais três. Antes que um único arquivo fosse
escrito nele, o foreman leu o [DOP](/pt-br/sobre/), a plataforma que estou
construindo, que tem a forma oposta à do projeto em que a cultura nasceu: seis
peças em vez de uma, três linguagens de programação, duas dúzias de decisões de
arquitetura já registradas, e um modelo inteiramente diferente fazendo o papel de
revisor. A leitura encontrou um projeto que mencionava os números das próprias
decisões nas mensagens de commit e foi confundido com um que usava um sistema de
chamados; um projeto com um lugar para ocorrências que nunca tinha guardado
nenhuma; e uma base de código de topo que só movia ponteiros e documentação, e
portanto não era o tipo de lugar onde código muda, o que a ferramenta se recusava
a acreditar. Três correções, três testes, mais uma versão, e então a instalação,
que me fez exatamente uma pergunta, porque aceitei os padrões, e deixou os
registros que passei meia hora refinando à mão em seguida.

## Um pedido, de ponta a ponta

Com a cultura instalada, é por isto que um pedido passa, e é aqui que o humano
aparece.

<!-- fig:roles -->
<figure class="diagram"><svg viewBox="0 0 720 420" role="img" aria-label="Diagrama do ciclo: um humano enuncia o pedido; o arquiteto, ao centro, envia o plano ao revisor e recebe objeções, despacha um leitor e um construtor com tarefas delimitadas, aciona o líder de qualidade que despacha testadores, entrega pelo ferramental do projeto em DEV, onde o humano vê funcionando e diz pronto." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="h-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#16233a"/></marker><marker id="h-navy" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#1d4e89"/></marker><marker id="h-muted" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#5d6b7d"/></marker><marker id="h-gold" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#b7791f"/></marker></defs><rect x="250" y="16" width="220" height="46" rx="6" fill="#1d4e89" stroke="#173d6e" stroke-width="1.2"/><text x="360.0" y="36.0" text-anchor="middle" font-size="13" font-weight="600" fill="#fff">o pedido</text><text x="360.0" y="53.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#cfe0f5">por um humano: o quê e o porquê</text><path d="M 360,62 L 360,146" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><text x="368" y="108" text-anchor="start" font-size="11" font-weight="600" fill="#1d4e89">1 ler e duvidar</text><rect x="248" y="150" width="224" height="80" rx="6" fill="#1d4e89" stroke="#173d6e" stroke-width="1.2"/><text x="360.0" y="181.0" text-anchor="middle" font-size="14" font-weight="600" fill="#fff">o arquiteto</text><text x="360.0" y="197.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#cfe0f5">lê, duvida, especifica, divide, julga</text><text x="360.0" y="211.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#cfe0f5">o único que vê o pedido inteiro</text><rect x="16" y="120" width="168" height="60" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="100.0" y="141.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">o revisor</text><text x="100.0" y="157.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">objeta antes de qualquer trabalho</text><text x="100.0" y="171.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">no mesmo nível do arquiteto</text><path d="M 276,150 L 276,96 L 100,96 L 100,116" fill="none" stroke="#16233a" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-ink)"/><text x="188" y="90" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">2 o plano</text><path d="M 184,160 L 244,160" fill="none" stroke="#5d6b7d" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="6 5" marker-end="url(#h-muted)"/><text x="214" y="198" text-anchor="middle" font-size="10" font-weight="400" fill="#5d6b7d">3 objeções</text><rect x="16" y="270" width="232" height="124" rx="10" fill="#eef2f7" stroke="#d5dde8" stroke-width="1"/><text x="32" y="292" text-anchor="start" font-size="12" font-weight="600" fill="#5d6b7d">executores</text><rect x="32" y="296" width="200" height="42" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="132.0" y="314.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">leitor</text><text x="132.0" y="331.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">uma pergunta delimitada</text><rect x="32" y="344" width="200" height="42" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="132.0" y="362.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">construtor</text><text x="132.0" y="379.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">uma mudança delimitada</text><path d="M 290,230 L 290,256 L 132,256 L 132,266" fill="none" stroke="#16233a" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-ink)"/><text x="298" y="252" text-anchor="start" font-size="11" font-weight="400" fill="#5d6b7d">4 uma tarefa com fronteira</text><rect x="520" y="84" width="184" height="150" rx="10" fill="#eef2f7" stroke="#d5dde8" stroke-width="1"/><text x="536" y="106" text-anchor="start" font-size="12" font-weight="600" fill="#5d6b7d">time de qualidade</text><rect x="536" y="110" width="152" height="46" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="612.0" y="130.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">o líder</text><text x="612.0" y="147.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">dimensiona e dá o veredito</text><rect x="536" y="176" width="48" height="40" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="560.0" y="201.0" text-anchor="middle" font-size="10.5" font-weight="500" fill="#16233a">testador</text><path d="M 612,156 L 560,172" fill="none" stroke="#5d6b7d" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-muted)"/><rect x="588" y="176" width="48" height="40" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="612.0" y="201.0" text-anchor="middle" font-size="10.5" font-weight="500" fill="#16233a">testador</text><path d="M 612,156 L 612,172" fill="none" stroke="#5d6b7d" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-muted)"/><rect x="640" y="176" width="48" height="40" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="664.0" y="201.0" text-anchor="middle" font-size="10.5" font-weight="500" fill="#16233a">testador</text><path d="M 612,156 L 664,172" fill="none" stroke="#5d6b7d" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-muted)"/><path d="M 440,150 L 440,133 L 532,133" fill="none" stroke="#16233a" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-ink)"/><text x="486" y="126" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">5 atacar</text><path d="M 395,230 L 395,296" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><text x="403" y="266" text-anchor="start" font-size="11" font-weight="600" fill="#1d4e89">6 entregar</text><rect x="300" y="300" width="190" height="50" rx="6" fill="#fff" stroke="#1d4e89" stroke-width="1.2"/><text x="395.0" y="322.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">o ferramental do projeto</text><text x="395.0" y="339.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">entrega, com o veredito anexado</text><rect x="526" y="300" width="90" height="50" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="571.0" y="322.0" text-anchor="middle" font-size="13" font-weight="600" fill="#16233a">DEV</text><text x="571.0" y="339.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">onde roda</text><path d="M 490,325 L 522,325" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><rect x="526" y="362" width="178" height="44" rx="6" fill="#1d4e89" stroke="#173d6e" stroke-width="1.2"/><text x="615.0" y="381.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#fff">o humano</text><text x="615.0" y="398.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#cfe0f5">vê funcionando · diz pronto</text><path d="M 571,350 L 571,358" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><text x="640" y="358" text-anchor="start" font-size="11" font-weight="600" fill="#1d4e89">7 · 8</text></svg><figcaption>Os quatro papéis em torno de um pedido. O humano o enuncia e, no fim, diz que está pronto; nada no meio espera permissão. O revisor objeta antes de qualquer trabalho, os executores nunca alargam uma tarefa, o time de qualidade nunca corrige o que encontra, e a entrega sai pelo ferramental do próprio projeto.</figcaption></figure>
  <div class="path-step"><span class="path-n">2</span><span class="path-name">O arquiteto lê e duvida</span><span class="path-who">confronta o pedido com o código, escreve o que muda e como se divide</span></div>
  <div class="path-step"><span class="path-n">3</span><span class="path-name">O revisor objeta</span><span class="path-who">antes que alguém construa; uma aprovação rápida é uma falha</span></div>
  <div class="path-step"><span class="path-n">4</span><span class="path-name">Executores constroem dentro de fronteiras</span><span class="path-who">uma tarefa cada; o inesperado volta, não se resolve</span></div>
  <div class="path-step"><span class="path-n">5</span><span class="path-name">O time de qualidade ataca</span><span class="path-who">um líder dimensiona a rodada; um vermelho causado pelo produto fica vermelho</span></div>
  <div class="path-step"><span class="path-n">6</span><span class="path-name">A entrega sai pelo ferramental</span><span class="path-who">com o veredito do time anexado</span></div>
  <div class="path-step path-step-human"><span class="path-n">7</span><span class="path-name">O humano vê funcionando</span><span class="path-who">e diz pronto; nada mais encerra</span></div>
</div>

Dois dos sete passos são do humano, e são o primeiro e o último. No meio, o
arquiteto não pergunta se pode prosseguir; anuncia o que decidiu e por quê, na
tela, para que uma pessoa lendo por cima do ombro possa redirecionar cedo se
quiser, e fora isso segue em frente. O revisor não é assistente do arquiteto e
não aprova por padrão. Os executores não alargam a tarefa, por mais tentadora que
seja a refatoração dois arquivos adiante. O time de qualidade não corrige o que
encontra. E "pronto" não significa que os testes passaram, o que é uma
precondição e não uma entrega; significa que a pessoa que pediu viu a coisa
funcionando onde ela deve rodar, e disse isso.

Cada papel trabalha também no nível de capacidade e de esforço que merece, o que a
cultura chama de senioridade e débito para nunca precisar nomear um fornecedor: o
arquiteto e o revisor no topo, porque um revisor abaixo do arquiteto revisa
ortografia; os executores mais abaixo, porque uma tarefa sem julgamento restante
não precisa de julgamento; o líder de qualidade onde o arquiteto o colocar,
tendendo ao capaz, porque um líder que só roda o que você especificou não encontra
nada que você já não soubesse. O arquivo de mecanismo, o único que nomeia os
modelos, é do projeto para editar, e no DOP a linha do revisor já aponta para algo
diferente do padrão.

## Ferramentas, não disciplina

Há mais um princípio nas regras, e foi o que mais demorei a entender. *A
governança se honra pelo ferramental, não pela disciplina.*

Todo projeto tem um punhado de operações que acontecem dezenas de vezes por dia e
precisam acontecer sempre do mesmo jeito: subir o ambiente e derrubá-lo, rodar os
testes de uma peça ou de todas, mover o pedido de um estado ao seguinte, abrir a
entrega. Um agente fará cada uma delas à mão se você deixar, e fará de um jeito
ligeiramente diferente a cada vez, porque é isso que fazer à mão significa. Dizer
a ele que tenha cuidado não ajuda; ele estava tendo cuidado. O que ajuda é dar ao
projeto uma ferramenta com um verbo para cada uma dessas operações, escrever no
registro de ambiente quais verbos existem, e enunciar uma regra só: quando a
ferramenta tem um verbo para uma ação, a ação não acontece fora dela. Um verbo
que falta é uma lacuna a reportar, não um convite a improvisar, e se a ferramenta
não consegue subir o ambiente, o trabalho para e avisa, em vez de encontrar outro
caminho.

<!-- fig:tooling -->
<figure class="diagram"><svg viewBox="0 0 720 376" role="img" aria-label="Diagrama da cultura encontrando o ferramental: os papéis enviam comandos à ferramenta do projeto, que sozinha age sobre o ambiente local, sobre a entrega e sobre os estados do pedido; a entrega chega a DEV, onde o humano vê o trabalho e diz pronto. Cada alvo é nomeado por um registro." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="h-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#16233a"/></marker><marker id="h-navy" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#1d4e89"/></marker><marker id="h-muted" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#5d6b7d"/></marker><marker id="h-gold" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#b7791f"/></marker></defs><rect x="16" y="96" width="190" height="180" rx="10" fill="#eef2f7" stroke="#d5dde8" stroke-width="1"/><text x="32" y="118" text-anchor="start" font-size="12" font-weight="600" fill="#5d6b7d">os papéis</text><rect x="32" y="122" width="158" height="42" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="111.0" y="140.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">arquiteto</text><text x="111.0" y="157.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">decide, entrega</text><rect x="32" y="172" width="158" height="42" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="111.0" y="190.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">construtores</text><text x="111.0" y="207.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">mudam o código</text><rect x="32" y="222" width="158" height="42" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="111.0" y="240.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">time de qualidade</text><text x="111.0" y="257.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">conduz o ataque</text><rect x="258" y="104" width="204" height="150" rx="8" fill="#1d4e89" stroke="#173d6e" stroke-width="1.2"/><text x="360" y="132" text-anchor="middle" font-size="14" font-weight="600" fill="#fff">a ferramenta do projeto</text><text x="360" y="150" text-anchor="middle" font-size="10.5" font-weight="400" fill="#cfe0f5">um verbo por ação</text><line x1="276" y1="162" x2="444" y2="162" stroke="#5b8fd6" stroke-width="1"/><text x="360" y="184" text-anchor="middle" font-size="11.5" font-weight="400" fill="#fff" font-family="IBM Plex Mono, ui-monospace, monospace">subir · derrubar · testar</text><text x="360" y="206" text-anchor="middle" font-size="11.5" font-weight="400" fill="#fff" font-family="IBM Plex Mono, ui-monospace, monospace">logs · ramificar · entregar</text><text x="360" y="228" text-anchor="middle" font-size="11.5" font-weight="400" fill="#fff" font-family="IBM Plex Mono, ui-monospace, monospace">mover o pedido</text><path d="M 206,186 L 254,186" fill="none" stroke="#16233a" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-ink)"/><text x="230" y="178" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">comandos</text><rect x="258" y="292" width="204" height="46" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="360.0" y="312.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">o ambiente local</text><text x="360.0" y="329.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">subir, derrubar, testar, reiniciar</text><path d="M 360,254 L 360,288" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><text x="372" y="276" text-anchor="start" font-size="10" font-weight="600" fill="#b7791f">registro de ambiente</text><rect x="510" y="24" width="194" height="50" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="607.0" y="46.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">a entrega</text><text x="607.0" y="63.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">ramos, pull requests, DEV</text><path d="M 462,130 L 486,130 L 486,49 L 506,49" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><text x="606" y="88" text-anchor="middle" font-size="10" font-weight="600" fill="#b7791f">registro de entrega</text><rect x="510" y="128" width="194" height="50" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="607.0" y="150.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">o pedido</text><text x="607.0" y="167.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">move-se por eventos de entrega</text><path d="M 462,170 L 486,170 L 486,153 L 506,153" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><text x="606" y="192" text-anchor="middle" font-size="10" font-weight="600" fill="#b7791f">registro de demandas</text><rect x="510" y="228" width="194" height="52" rx="6" fill="#1d4e89" stroke="#173d6e" stroke-width="1.2"/><text x="607.0" y="251.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#fff">o humano</text><text x="607.0" y="268.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#cfe0f5">vê funcionando em DEV, diz pronto</text><path d="M 690,76 L 690,224" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="6 5" marker-end="url(#h-navy)"/><text x="360" y="362" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">um verbo que falta é uma lacuna a reportar, não motivo para improvisar</text></svg><figcaption>Governança pelo ferramental, não pela disciplina. Toda operação repetitiva é um verbo de uma ferramenta que o projeto possui; os registros dizem quais verbos existem e em que cada um toca. Quando a ferramenta tem um verbo para uma ação, a ação nunca acontece à mão.</figcaption></figure>

No DOP isso é agora o próximo trabalho, e a própria cultura é quem o faz. A
plataforma tem uma ferramenta operacional que foi escrita para outro cliente e
está sendo reconstruída para carregar exatamente os verbos que o registro de
ambiente nomeia: subir, derrubar, estado, logs, testar, reiniciar, uma peça de
cada vez. O briefing que inicia esse trabalho foi escrito no dia em que a cultura
foi instalada, e diz à sessão do arquiteto o que os registros já decidiram, em que
ordem vêm as peças, quais sete coisas precisam ser verdadeiras para o trabalho ser
aceito, e as cinco que ele não deve fazer, entre elas construir qualquer coisa que
os registros não nomeiem. O agente vai lê-lo do jeito que lê qualquer pedido: com
dúvida, e depois com um plano a que outra pessoa tem o direito de objetar
primeiro.

## Três coisas, e nada mais

Olhando para trás, para tudo por que um pedido passa, do momento em que alguém o
enuncia ao momento em que diz que está pronto, cada passo se revela apoiado em uma
de três coisas, e só três. A **cultura** diz quem decide o quê: as regras, os
quatro papéis e os cinco registros, escritos uma vez e levados de projeto em
projeto, para que nenhum passo dependa de quem por acaso estava na sala. A
**ferramenta** faz o que precisa ser feito sempre do mesmo jeito, subir e derrubar
o ambiente, rodar os testes, mover o pedido, abrir a entrega, um verbo por ação,
para que nenhum passo dependa do cuidado de um agente. E a **rotina** é o próprio
ciclo, ler e duvidar, especificar, objetar, executar, atacar, entregar, validar,
fechar, na mesma ordem para todo pedido, para que nenhum passo dependa de alguém
lembrar o que vem depois. Cultura, ferramenta e rotina sustentam o todo, da
primeira linha de um pedido ao código rodando onde deve rodar, e quando uma das
três falta as outras duas não a substituem, que é por isso que os registros param
o agente quando estão ausentes e por isso que um verbo que falta é reportado em
vez de contornado.

## O que sai do outro lado

O que sai é um jeito de construir software que corre AI-first de ponta a ponta, e
em que hoje confio mais do que no jeito que ele substituiu. O agente é autônomo
entre os portões: não pergunta se pode prosseguir, anuncia o que decidiu e segue,
e o trabalho de um dia já não espera que uma pessoa esteja disponível para
responder a uma pergunta que as regras já tinham respondido. A qualidade não é
uma esperança, mas um acordo, escrito no pedido como linhas de aceitação que um
teste prova, objetado antes que alguém construa, atacado depois por um time que
não escreveu o código, e levado pela entrega com o veredito anexado. O humano
decide exatamente onde um humano deve decidir: no começo, o que se quer e por
quê; no fim, se funciona; e nos poucos outros lugares que os registros nomeiam,
onde uma decisão sobre o trabalho é dele e não do agente. Tudo o que fica no meio
pertence à cultura, à ferramenta e à rotina.

Era isso que eu queria desde os meus primeiros projetos AI-first, sem saber
dizer: não um agente a quem se manda ter cuidado, mas um projeto que já sabe como
o trabalho é feito aqui, escrito uma vez, instalado em vez de explicado, e capaz
de levar um pedido de uma ideia a software em funcionamento enquanto as pessoas
envolvidas decidem só o que é delas decidir. A explicação, finalmente, fica, e a
qualidade fica com ela.
