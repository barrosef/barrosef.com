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

<div class="path" role="img" aria-label="Sete passos: o humano enuncia o pedido; o arquiteto lê e duvida, escreve o plano; o revisor objeta antes de qualquer trabalho; executores constroem dentro de fronteiras; o time de qualidade ataca o resultado; a entrega sai pelo ferramental do projeto; o humano vê funcionando e diz pronto.">
  <div class="path-step path-step-human"><span class="path-n">1</span><span class="path-name">O pedido é enunciado</span><span class="path-who">por um humano, com o quê e o porquê</span></div>
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

Era isso que eu queria desde o começo, sem saber dizer. Não um agente a quem se
manda ter cuidado, mas um projeto que já sabe como o trabalho é feito aqui,
escrito uma vez, levado de projeto em projeto, e instalado em vez de explicado. A
explicação, finalmente, fica.
