---
title: "Novidades do Claude Code: Fable 5.2, sessões na nuvem que se configuram sozinhas e um plano que rende mais"
seoTitle: "Novidades do Claude Code: novembro de 2026"
date: 2026-11-11T07:00:00-04:00
draft: false
translationKey: "claude-code-news-2026-11"
categories: ["Tecnologia"]
tags: ["claude-code", "desenvolvimento-com-ia"]
description: "Fable 5.2, sessões na nuvem que montam o próprio ambiente, /usage, /storage e ultrathink: o que o Claude Code lançou em novembro de 2026."
---

A newsletter do time do Claude Code chegou na terça à noite, 10 de novembro, com um
modelo novo no assunto, e eu achei que a notícia fosse o modelo. Não era bem isso,
porque ele é só um item numa lista grande, e a maior parte do que o time lançou nas
últimas semanas é menos vistosa e mais útil: sessões na nuvem que preparam o próprio
ambiente, comandos que mostram para onde o seu plano está indo e se oferecem para
corrigir, um jeito de recuperar o espaço em disco que as sessões antigas deixam para
trás e uma série de mudanças discretas que deixam as conversas longas mais baratas.
A seguir passo por tudo isso, na ordem que me parece importar para quem usa o Claude
Code todo dia, marcando o que é opinião minha e tirando o resto da newsletter e do
[changelog oficial](https://code.claude.com/docs/en/changelog).

<figure class="diagram news-fig">
  <a href="/img/claude-code-news/news-map.pt-br.svg">
    <img src="/img/claude-code-news/news-map.pt-br.svg" width="400" height="680" loading="lazy"
      alt="Mapa mental das novidades: Claude Code, novembro de 2026, no centro, com cinco ramos. Fable 5.2, mais rápido, para tarefas grandes e abertas. Ambiente na nuvem, o Claude prepara o ambiente para você. /usage e depois f, veja o que consome o plano e corrija. /storage, apague as worktrees que as sessões deixam. Ultrathink e modo automático, pense mais numa resposta e confie nos lugares certos.">
  </a>
  <figcaption>As cinco mudanças, um ramo cada; o resto do artigo segue nesta ordem.</figcaption>
</figure>

## Fable 5.2, e por que o time ainda indica o Opus

O Fable 5.2 gera as respostas até 30% mais rápido que o Fable 5.1, e o time diz que
ele é ótimo para tarefas grandes e abertas. O que mais me chamou a atenção veio no
mesmo parágrafo: para a maior parte do código do dia a dia, eles ainda começariam pelo
Opus 5.5. É quem faz a ferramenta avisando que o modelo mais novo não é,
automaticamente, o padrão certo, e isso bate com o que vejo no meu trabalho, onde
casar a tarefa com o modelo pesa mais que a data de lançamento. Para testar, troque
com `/model claude-fable-5-2`, o que pede o Claude Code na versão 2.1.321 ou mais
nova.

As regras de acesso têm data, então vale ler com calma. Nos planos Pro e Team
Standard, o Fable está incluído até 50% do seu limite semanal, até 16 de novembro;
depois disso, ele usa créditos de uso, se você tiver ativado. Quem já assinava um
plano pago antes de 9 de novembro às 10h (horário do Pacífico) pode ainda encontrar
um reset do Fable em **Settings › Usage**, na web e no app desktop, que precisa ser
usado até 16 de novembro no Pro e no Team Standard, ou até 8 de março de 2027 no
Max, no Ultra e no Team Premium. Se você está no Pro, a minha sugestão é guardar uma
tarefa grande e aberta de verdade para esta semana, porque é ali que o modelo
promete brilhar e é ali que o teste ensina mais.

<figure class="diagram news-fig">
  <a href="/img/claude-code-news/news-fable.pt-br.svg">
    <img src="/img/claude-code-news/news-fable.pt-br.svg" width="400" height="666" loading="lazy"
      alt="Por qual modelo começar: a partir da sua tarefa, o código do dia a dia vai para o Opus 5.5, conselho do time, e as tarefas grandes e abertas vão para o Fable 5.2, até 30% mais rápido que o 5.1. Abaixo, as datas do Fable: 9 de novembro às 10h do Pacífico, quem assinava antes disso pode ter um reset do Fable; 16 de novembro, acabam o teste no Pro e no Team Standard (até 50% do limite semanal) e o reset; 8 de março de 2027, prazo do reset no Max, no Ultra e no Team Premium. Para trocar, /model claude-fable-5-2, que pede a versão 2.1.321 ou mais nova.">
  </a>
  <figcaption>A escolha do modelo é o conselho do time; as datas são da newsletter de 10 de novembro de 2026.</figcaption>
</figure>

## Sessões na nuvem agora montam o próprio ambiente

As sessões na nuvem rodam a tarefa na infraestrutura da Anthropic, então dá para
começar de qualquer aparelho e deixar o trabalho seguindo em segundo plano, e a
única parte que ainda sobrava para você era preparar o ambiente: as dependências, o
acesso à rede e as chaves que o projeto precisa. Nos planos Pro, Max e Ultra, o
Claude agora faz isso também. Quando falta uma dependência, um acesso à rede ou uma
chave de API, ele avisa e mostra as mudanças para você aprovar; a chave de API vai
num formulário, de modo que o Claude nunca vê a chave; e a configuração fica salva,
para a próxima sessão começar do mesmo ambiente. Os detalhes estão na
[documentação de ambientes na nuvem](https://code.claude.com/docs/en/cloud-environments).

<figure class="diagram news-fig">
  <a href="/img/claude-code-news/news-cloud.pt-br.svg">
    <img src="/img/claude-code-news/news-cloud.pt-br.svg" width="400" height="509" loading="lazy"
      alt="O ciclo do ambiente na nuvem em quatro passos. Um, você começa a tarefa de qualquer aparelho e ela segue em segundo plano. Dois, o Claude verifica se falta dependência, acesso à rede ou chave de API. Três, você aprova as mudanças que ele mostra, e a chave vai num formulário que o Claude não vê. Quatro, o ambiente fica salvo, a próxima sessão começa no mesmo ambiente e o ciclo recomeça. Disponível no Pro, no Max e no Ultra.">
  </a>
  <figcaption>Cada ambiente salvo alimenta a próxima sessão, e é por isso que a segunda já começa pronta.</figcaption>
</figure>

Três mudanças menores do changelog vão no mesmo sentido. Desde a 2.1.318, uma
sessão na nuvem num ambiente hospedado pela Anthropic pode começar com a opção **No
repository**, para as tarefas que não precisam de código nenhum. Desde a 2.1.314, um
script de setup que falha não impede mais a sessão de começar na web, no desktop e
no celular; ela começa assim mesmo, e você resolve a falha lá dentro. E desde a
2.1.312, as rotinas que rodam na nuvem deixam você escolher o nível de esforço ao
criar ou editar, o que quer dizer que uma rotina da madrugada não precisa pensar
tanto quanto a tarefa que você está acompanhando.

## Ver para onde vai o seu plano, e corrigir

Se você já viu o limite semanal acabar mais rápido do que esperava, como eu já vi,
esta é a parte para ler duas vezes. O `/usage` no terminal já mostrava o que mais
tinha consumido o seu plano; agora mostra também como corrigir, e apertando **f** o
Claude Code manda um pedido para corrigir sozinho o que der. A
[documentação de uso](https://code.claude.com/docs/en/costs) explica o que ele mede.

Várias mudanças cortam o gasto sem perguntar nada. O Claude Code mandava a conversa
inteira a cada pedido, e para a maioria das pessoas agora manda só as mensagens
novas, e é por isso que conversas longas começam a responder mais cedo. Ele também
resume as conversas longas paradas pouco antes de o cache expirar, depois de mais ou
menos uma hora, e mostra um aviso quando faz isso: retomar uma conversa cujo cache
expirou significa processar todo o contexto de novo, e um resumo sai muito mais
barato que a conversa inteira. Dá para desligar em `/config`, e desde a 2.1.314 esse
mesmo resumo funciona no VS Code e na aba Code do app desktop, para conversas acima
de 200 mil tokens. Trocar de modelo agora pede ao modelo em que você estava para
resumir a conversa antes, quando ela é longa demais para o novo. E na 2.1.316 o time
corrigiu um gasto em que eu nunca tinha pensado: cada atualização da linha de status
no terminal relia a conversa inteira de um subagente em segundo plano, e agora
trabalha com anotações curtas, o que no teste deles, no Pro e no Max, fez as sessões
com subagentes em segundo plano gastarem cerca de 5% menos do limite.

<figure class="diagram news-fig">
  <a href="/img/claude-code-news/news-usage.pt-br.svg">
    <img src="/img/claude-code-news/news-usage.pt-br.svg" width="400" height="608" loading="lazy"
      alt="O que cada pedido envia. Antes, o primeiro pedido enviava a mensagem 1, o segundo as mensagens 1 e 2, o terceiro 1, 2 e 3: a conversa inteira toda vez. Agora cada pedido envia só a mensagem nova. Abaixo, quando uma conversa longa fica parada cerca de uma hora, o cache expira: sem o resumo, a próxima mensagem processa tudo de novo; com o resumo automático, processa só o resumo. Embaixo: rode o /usage, aperte f e o Claude corrige o que der.">
  </a>
  <figcaption>Antes e agora, pedido a pedido; o tamanho das barras é ilustrativo, não medido.</figcaption>
</figure>

## Liberar o disco que as sessões antigas deixam

Cada sessão que trabalha numa worktree própria do git deixa uma cópia do repositório
na sua máquina, e essas cópias vão se acumulando; eu mantenho uma worktree separada
para cada artigo deste site, então sei bem a rapidez com que elas se juntam. No app
desktop agora dá para ver quanto espaço as sessões e worktrees ocupam em Settings,
ou digitar `/storage`, e apagar as worktrees que você não usa faz tempo, junto com
as tarefas inativas. As sessões, as conversas e as branches continuam lá, mas o que
não foi commitado vai embora junto com a worktree, então faça o commit antes de
limpar.

<figure class="diagram news-fig">
  <a href="/img/claude-code-news/news-storage.pt-br.svg">
    <img src="/img/claude-code-news/news-storage.pt-br.svg" width="400" height="500" loading="lazy"
      alt="O que o /storage faz no app desktop. Ele apaga as worktrees sem uso faz tempo, as tarefas inativas e, junto, as mudanças sem commit, então faça o commit antes. Sessões, conversas e branches ficam.">
  </a>
  <figcaption>O que não foi commitado sai junto com a worktree, então faça o commit antes de limpar.</figcaption>
</figure>

## Pensar mais numa só vez, e confiar nos lugares certos

O **ultrathink** voltou. Escrever essa palavra no pedido aciona o nível de esforço
`xhigh` só naquela resposta, sem mudar o esforço da sessão inteira; o time é
franco em dizer que a maioria das tarefas não precisa disso e que ele vale a pena
quando o Claude está realmente travado. A
[página de configuração de modelos](https://code.claude.com/docs/en/model-config)
explica os níveis de esforço.

<figure class="diagram news-fig">
  <a href="/img/claude-code-news/news-effort.pt-br.svg">
    <img src="/img/claude-code-news/news-effort.pt-br.svg" width="400" height="290" loading="lazy"
      alt="Esforço por resposta: sete respostas no nível de esforço da sessão, marcado por uma linha tracejada, e uma resposta bem mais alta, marcada ultrathink, xhigh só nesta resposta. O esforço da sessão não muda.">
  </a>
  <figcaption>O ultrathink sobe uma resposta, não a sessão.</figcaption>
</figure>

O modo automático, por padrão, só confia na pasta em que você está trabalhando e
nos remotes do próprio repositório, o que é um bom começo até o momento em que o
Claude precisa fazer push em outro repositório do seu time ou mandar algo para um
serviço que você usa todo dia. O `/auto-mode-setup` olha o seu projeto e os comandos
que o Claude rodou nas sessões recentes ali, monta uma lista dos repositórios,
domínios e armazenamentos na nuvem em que você confia e, quando você aceita, salva em
`~/.claude/settings.json`; a
[página de modos de permissão](https://code.claude.com/docs/en/permission-modes)
explica como o modo automático decide. Do lado mais rígido, a 2.1.314 trouxe o
`permissions.blockWritesOutsideWorkingDirectories`: ligado, ele faz as ferramentas
Write, Edit e NotebookEdit recusarem qualquer caminho fora das suas pastas de
trabalho em todos os modos de permissão, tirando alguns arquivos do próprio Claude
Code. Leia o limite com o mesmo cuidado que a promessa, porém, porque ele não
restringe comandos de shell, ferramentas MCP nem hooks.

<figure class="diagram news-fig">
  <a href="/img/claude-code-news/news-trust.pt-br.svg">
    <img src="/img/claude-code-news/news-trust.pt-br.svg" width="400" height="444" loading="lazy"
      alt="Em quem o modo automático confia, em anéis. O anel de dentro, confiável por padrão: a sua pasta de trabalho e os remotes deste repositório. O anel do meio, somado pelo /auto-mode-setup: os repositórios, domínios e armazenamentos na nuvem em que você confia, salvos em ~/.claude/settings.json. Fora, todo o resto, onde o modo automático é barrado. Abaixo, a configuração blockWritesOutsideWorkingDirectories: Write, Edit e NotebookEdit ficam dentro das suas pastas de trabalho; shell, MCP e hooks não são limitados.">
  </a>
  <figcaption>O anel do meio é o que o /auto-mode-setup monta para você aceitar.</figcaption>
</figure>

## As mudanças menores

O resto da lista é curto, e uma parte muda hábitos:

| Versão | O que mudou |
|---|---|
| 2.1.318 | O Claude Code não instala mais a extensão da IDE quando é aberto no terminal da IDE; use `/ide` num terminal de fora, ou a tela de extensões do seu editor |
| 2.1.302 | Os subagentes fork, que herdam a conversa inteira, vêm ligados por padrão no app desktop e no VS Code, como já vinham no terminal |
| desktop | As mensagens que você deixou na fila numa sessão local voltam quando você reabre o app depois que ele fecha, atualiza ou trava |

## Dois hábitos do próprio time

A newsletter termina com duas práticas dos engenheiros da Anthropic, e as duas valem
a cópia. A primeira resolve o agente que para e fica esperando uma decisão que ele
não tem certeza se você tomou; um dos engenheiros dá o sinal verde logo de saída, e
conta que isso destravou um time grande de agentes (o texto original é em inglês):

> Just build and use your best judgment. Make any call that's reversible yourself,
> and check in later with the calls you made.

Em português, algo como: "Pode construir e use o seu bom senso. Toda decisão que dá
para desfazer, tome você mesmo, e depois me conte quais decisões tomou."

A segunda troca a discussão sobre se um design é flexível o bastante por um
experimento, que você pode apagar depois:

> In a separate worktree, do a throwaway build of [a feature we might add later] on
> top of this design. Don't polish it, just tell me where the design got in the way.

Ou seja: "Numa worktree separada, faça uma versão descartável de [uma feature que
talvez a gente adicione depois] em cima deste design. Não capriche, só me diga onde o
design atrapalhou."

O time também escreveu como faz code review no Claude Code, com o Claude revisando a
maior parte das mudanças antes de uma pessoa olhar, e ensinando a montar o mesmo.

## O que eu faria esta semana

Se eu tivesse que escolher, começaria atualizando o Claude Code, porque várias dessas
correções chegam sozinhas com a versão nova, e logo depois rodaria o `/usage` e
apertaria **f**, já que é a mudança que se paga no mesmo dia. Em seguida, o
`/storage` no app desktop, depois de commitar o que importa; o `/auto-mode-setup`, se
o modo automático vive parando na beira do seu próprio repositório; e, no Pro, uma
tarefa grande e aberta entregue ao Fable 5.2 antes de 16 de novembro, para você
decidir com base no que viu, e não nas notas de lançamento, se ele merece um lugar
ao lado do Opus no seu trabalho. A lista completa do que saiu está no
[changelog](https://code.claude.com/docs/en/changelog), e se você topar com um bug,
o `/feedback` dentro do Claude Code manda direto para o time.

*Fontes: "What's new in Claude Code: Fable 5.2, easier cloud setup, and more", a
newsletter do time do Claude Code de 10 de novembro de 2026; o
[changelog do Claude Code](https://code.claude.com/docs/en/changelog) (versões
2.1.302 a 2.1.321) e as páginas da documentação citadas acima, consultadas em 11 de
novembro de 2026.*
