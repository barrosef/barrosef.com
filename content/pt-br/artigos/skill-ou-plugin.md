---
title: "Skill ou plugin? Como empacotar o que o Claude precisa saber"
seoTitle: "Skill ou plugin? Como escolher no Claude Code"
date: 2026-10-30T17:00:00-04:00
draft: false
translationKey: "skill-or-plugin"
categories: ["Tecnologia"]
tags: ["claude-code", "plugins", "agentes-de-ia"]
description: "Skills guardam conhecimento; plugins o distribuem. Um guia para escolher entre skill pessoal, commit no repositório e plugin no Claude Code."
---

Na terceira vez que digitei as mesmas instruções no Claude Code (como escrevemos
as notas de versão, quais seções elas precisam ter, o tom que usamos com os
clientes), parei no meio da frase, porque repetir aquilo tinha virado o trabalho
de verdade. A solução parecia óbvia: empacotar de uma vez. O que não era óbvio era
a embalagem, já que o Claude Code oferece dois nomes que soam como rivais, skill e
plugin, e quase todo mundo com quem conversei escolhe um por instinto e descobre,
algumas semanas depois, que resolveu um problema diferente do que tinha.

A confusão é compreensível, porque um plugin pode conter skills, e uma skill faz
boa parte do que as pessoas constroem plugins para fazer. Mas os dois respondem a
perguntas diferentes. Este artigo é sobre separar essas perguntas, para que, da
próxima vez que você se pegar repetindo algo para o Claude, saiba onde aquilo deve
morar.

## Duas respostas para duas perguntas diferentes

Uma **skill** é uma unidade de conhecimento. É uma pasta com um arquivo `SKILL.md`
cujo frontmatter a descreve e cujo corpo diz ao Claude como fazer alguma coisa,
mais os arquivos de referência ou scripts que ajudem. O Claude recorre a ela quando
o seu pedido combina com a descrição, ou você mesmo a executa como `/nome-da-skill`.
A pergunta dela é *"como o Claude deve fazer isto?"*

Um **plugin** é uma unidade de distribuição. É um diretório que o Claude Code
instala e carrega como uma peça só, normalmente a partir de um marketplace, e que
pode levar skills junto com subagentes, hooks, servidores MCP e outros componentes,
tudo sob um nome e uma versão. A pergunta dele é *"como esta configuração chega a
outras pessoas e a outros projetos, e continua igual em todos eles?"*

Entre os dois há uma opção que muitos desenvolvedores ignoram e que resolve mais
casos do que qualquer um deles: o próprio repositório. O Claude Code lê a pasta
`.claude/` do projeto, então skills em `.claude/skills/`, subagentes em
`.claude/agents/`, hooks em `.claude/settings.json` e servidores MCP em `.mcp.json`
chegam a todos que clonam o repositório, sem plugin nenhum. Isso dá três lugares,
e não dois, e o resto deste artigo é sobre escolher entre eles.

## Que problema cada um resolve

Uma skill resolve o problema de um assistente capaz que não conhece o *seu* jeito
de fazer as coisas. O formato das suas notas de versão, o checklist que você roda
antes de uma migração, o jeito como o seu time nomeia feature flags: nada disso
está no modelo, e colar tudo a cada vez é cansativo e inconsistente. Uma skill
escreve isso uma vez, e o Claude Code é econômico com ela, porque só a descrição
fica no contexto do Claude, para que ele saiba que a skill existe, enquanto o corpo
completo carrega quando ela é de fato usada. É por isso que uma skill longa e
detalhada quase não custa nada até o momento em que é necessária.

Um plugin resolve outro problema: uma configuração que funciona na sua máquina e
precisa funcionar, de forma idêntica, em outro lugar. Quando os seus hábitos no
Claude Code já somam algumas skills, um subagente revisor, um hook que roda um
formatador depois de cada edição e um servidor MCP para o seu gerenciador de
tarefas, a parte difícil deixa de ser escrever qualquer um deles; passa a ser levar
tudo isso a um colega, ou ao próximo repositório, num estado igual ao seu, e saber
que versão ele tem quando algo se comporta diferente.

## Onde cada um mora, e quem recebe

O lugar onde você salva uma skill decide quem a recebe, e essa é a forma mais
prática de pensar a escolha. Uma skill em `~/.claude/skills/` é pessoal: ela vai
com você para todos os projetos da sua máquina, e ninguém mais a vê. Uma skill em
`.claude/skills/` do projeto pertence àquele repositório, e o conselho da
documentação é simplesmente commitá-la para que o seu time também a receba; o
mesmo vale para subagentes em `.claude/agents/`, para hooks no `.claude/settings.json`
compartilhado e para servidores MCP em `.mcp.json`, então um time já consegue
compartilhar uma configuração completa via `git pull`. Quando duas skills têm o
mesmo nome, a pessoal vence a do projeto, o que vale lembrar quando um colega diz
que o seu `/deploy` se comporta diferente do dele.

Um plugin mora em outro lugar. Normalmente ele é buscado num marketplace (um repositório ou
pasta com um `marketplace.json` que lista plugins) para o armazenamento de plugins
do próprio Claude Code, e você escolhe um escopo ao instalá-lo: para você em todos
os projetos, ou para um repositório, em que as configurações commitadas o declaram
e cada colaborador ainda o instala na própria máquina. As skills dele aparecem sob
o nome dele, como `/nome-do-plugin:nome-da-skill`, e é assim que dois plugins podem
trazer cada um uma skill `review` sem pisar um no outro.

## O que só um plugin faz

É tentador responder "hooks" ou "agentes", mas seria errado, já que cada um desses
componentes também funciona sozinho. Tirando algumas peças que só existem dentro de
um plugin, a mais útil delas um servidor de linguagem que dá ao Claude os
diagnósticos do seu editor, o que um plugin acrescenta não é uma capacidade nova,
e sim um novo tipo de alcance. Ele deixa uma configuração viajar
como uma unidade só para muitos repositórios de uma vez, onde commitar `.claude/`
significaria copiar os mesmos arquivos em cada um e torcer para que as cópias nunca
se distanciem. Ele dá uma versão a essa configuração, para que as pessoas fiquem
numa versão conhecida até você publicar a próxima, e dá a elas um jeito de receber
a próxima, com um único comando de atualização, ou automaticamente quando ativam a
atualização automática do seu marketplace (ela começa desligada para qualquer
marketplace que não seja da Anthropic), em vez de um diff para aplicar à mão. Ele ainda tira os seus nomes do caminho dos
outros por meio do prefixo do plugin, o que importa assim que a sua configuração
encontra a de outras pessoas.

## O que um plugin cobra de você

Nada disso sai de graça, e quando empacotei as regras de trabalho do meu próprio
time como plugin, porque elas precisavam chegar a todos os repositórios que temos,
paguei cada um desses custos. Primeiro mudam os nomes: uma skill
que era `/deploy` vira `/meu-plugin:deploy`, e quem tinha o hábito de digitar a
versão curta precisa ser avisado. Depois muda a presença, porque um plugin ativo
faz parte de toda sessão, e não só das sessões em que você o usa: as descrições
das skills e agentes que o Claude pode invocar ficam no contexto a cada turno, os
hooks dele disparam nos seus eventos e os servidores MCP dele rodam, tudo com as
suas permissões, então um plugin instalado "por via das dúvidas" nunca está de fato
parado. E então vem o trabalho de quem publica, e não só usa: um manifesto para
manter correto, uma versão para aumentar de propósito, um marketplace para manter
e a pergunta, a cada mudança, de quem vai recebê-la e quando. Para um único
repositório, tudo isso é custo sem retorno, porque o `git pull` já faz a
distribuição.

Uma skill, em comparação, custa um arquivo. Você pode editá-la no meio de uma
sessão e o Claude Code aplica a mudança sem reiniciar, e quando ela se mostra
errada, você corrige num lugar só. A contrapartida é o alcance: uma skill vai
exatamente até onde vai a pasta em que você a salvou.

## Decidir em menos de um minuto

<div class="path" role="img" aria-label="Três perguntas em ordem: é só para mim, então uma skill pessoal em ~/.claude/skills; é para todos neste repositório, então commite em .claude no repositório; precisa chegar a outros repositórios ou pessoas como uma unidade versionada, então um plugin.">
  <div class="path-step"><span class="path-n">1</span><span class="path-name">É só para mim?</span><span class="path-who">uma skill pessoal em <code>~/.claude/skills/</code></span></div>
  <div class="path-step"><span class="path-n">2</span><span class="path-name">É para todos neste repositório?</span><span class="path-who">commite <code>.claude/</code> (skills, agentes, hooks) e o <code>.mcp.json</code></span></div>
  <div class="path-step path-step-human"><span class="path-n">3</span><span class="path-name">Precisa ir além deste repositório?</span><span class="path-who">um plugin: uma unidade, uma versão, atualizações por marketplace</span></div>
</div>

A escolha, portanto, se resume a uma pergunta feita de três jeitos, e ela nunca é
"qual é mais poderoso?", e sim "até onde isto precisa ir?". Quando o conhecimento é
só seu, como uma rotina de depuração que ninguém mais usa, é uma skill pessoal, e
você deveria escrevê-la hoje. Quando ele pertence a um projeto e todos que
trabalham ali devem compartilhá-lo, como acabou sendo o caso das minhas notas de
versão, junto com o checklist de revisão daquele repositório, o subagente revisor
e o hook que formata cada edição, commite em `.claude/` (com o `.mcp.json` na raiz
para servidores MCP compartilhados), porque o repositório já é o melhor canal de
distribuição que aquele time tem; as instruções de notas de versão que eu vivia
redigitando viraram `.claude/skills/release-notes/`, e ninguém naquele projeto as
digitou de novo. E quando a
mesma configuração precisa chegar a muitos repositórios ou a muitas pessoas,
continuar idêntica em todos eles e mudar só quando você decidir, esse é o momento,
e o único momento, de construir um plugin.

A ordem importa tanto quanto a regra. Quase tudo o que vale empacotar nasce como
uma skill que uma pessoa achou útil, vira alguns arquivos que um time commita, e
só merece um plugin quando cresce além do repositório em que nasceu; a
documentação até mostra como converter uma configuração em `.claude/` num plugin
quando esse dia chega. Comece pelo menor lugar que alcança todos que precisam, e
deixe que aquilo que você construiu diga quando precisa de um lugar maior.
