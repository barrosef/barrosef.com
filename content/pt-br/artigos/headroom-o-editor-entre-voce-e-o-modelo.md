---
title: "Headroom: o editor entre você e o modelo"
date: 2026-09-20T16:30:00-04:00
draft: false
translationKey: "headroom-editor"
categories: ["Tecnologia"]
tags: ["claude-code", "headroom", "desenvolvimento-com-ia", "ferramentas", "custo"]
description: "Cada requisição a um agente de código reenvia a conversa inteira. O Headroom é um proxy local que a edita na saída. O que ele promete, como instalar no Linux, no macOS e no Windows, e as regras de um teste que começa amanhã em projetos reais."
---

Imagine um mensageiro que leva um dossiê entre você e um especialista. Cada
vez que você acrescenta uma página, ele vai até lá e lê para o especialista o
arquivo inteiro, desde a primeira folha — a página nova e as quatrocentas
anteriores —, porque o especialista não guarda nada entre uma visita e outra.
E o especialista cobra por palavra.

Uma conversa com um modelo de linguagem é isso. Ele não tem memória: cada
requisição carrega tudo o que já foi dito, e a conta soma tudo, todas as
vezes. Em um projeto real que examinei na semana passada, trinta dias de
sessões do Claude Code enviaram **3,6 bilhões de tokens** de entrada à API.
Noventa e oito por cento vieram do cache do provedor, a um décimo do preço. A
requisição média ainda assim carregava **meio milhão de tokens** de contexto
— o dossiê, lido em voz alta mais uma vez.

O Headroom propõe pôr um editor na porta.

## O que é o editor

O [Headroom](https://github.com/headroomlabs-ai/headroom) é um proxy de
código aberto (Apache 2.0) que roda na sua própria máquina. Você aponta o
agente para `http://127.0.0.1:8787` em vez da API; o proxy lê cada
requisição, edita e repassa o resultado. Nada sai do seu computador além do
que já sairia. Ele fala os formatos da Anthropic, da OpenAI e do Gemini, de
modo que o mesmo processo atende Claude Code, Codex, Cursor, Aider e mais uma
dúzia de agentes.

Para o Claude Code em particular, três peças chegam juntas:

- **o proxy**, o editor propriamente dito;
- **um plugin**, dois hooks que verificam, no início da sessão (e antes de
  cada comando de shell), se o proxy está vivo — e o sobem se não estiver;
- **um servidor MCP**, três ferramentas que o modelo pode chamar:
  `headroom_compress`, `headroom_stats` e a que importa, `headroom_retrieve`.

## O que ele faz com o dossiê

<figure class="diagram">
<svg viewBox="0 0 720 330" role="img" aria-label="O Claude Code envia a conversa inteira a um proxy Headroom local; dentro dele quatro estágios rodam em ordem: roteador de conteúdo, compressores, alinhador de cache, adiamento de esquemas de ferramentas; a requisição editada segue para a API da Anthropic. Abaixo do proxy, um cofre CCR guarda todo original; uma seta de recuperação volta ao Claude Code pelo servidor MCP." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="hd-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#16233a"/></marker><marker id="hd-navy" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#1d4e89"/></marker><marker id="hd-muted" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#5d6b7d"/></marker></defs><rect x="16" y="92" width="118" height="76" rx="10" fill="#eef2f7" stroke="#d5dde8"/><text x="75" y="124" text-anchor="middle" font-size="14" font-weight="600" fill="#16233a">Claude Code</text><text x="75" y="143" text-anchor="middle" font-size="11" fill="#5d6b7d">o mensageiro</text><line x1="134" y1="130" x2="176" y2="130" stroke="#16233a" stroke-width="1.5" marker-end="url(#hd-ink)"/><text x="155" y="147" text-anchor="middle" font-size="10.5" fill="#5d6b7d">dossiê</text><text x="155" y="159" text-anchor="middle" font-size="10.5" fill="#5d6b7d">inteiro</text><rect x="178" y="48" width="376" height="164" rx="12" fill="#1d4e89" stroke="#173d6e" stroke-width="1.5"/><text x="366" y="72" text-anchor="middle" font-size="14.5" font-weight="600" fill="#fff">Headroom proxy · 127.0.0.1:8787</text><text x="366" y="88" text-anchor="middle" font-size="11" fill="#cfe0f5">o editor</text><g font-size="11.5" fill="#16233a"><rect x="192" y="104" width="82" height="66" rx="8" fill="#eef2f7"/><text x="233" y="130" text-anchor="middle" font-weight="600">roteador</text><text x="233" y="146" text-anchor="middle" font-size="10" fill="#5d6b7d">que bloco</text><text x="233" y="159" text-anchor="middle" font-size="10" fill="#5d6b7d">é este?</text><rect x="284" y="104" width="82" height="66" rx="8" fill="#eef2f7"/><text x="325" y="130" text-anchor="middle" font-weight="600">comprime</text><text x="325" y="146" text-anchor="middle" font-size="10" fill="#5d6b7d">JSON · logs</text><text x="325" y="159" text-anchor="middle" font-size="10" fill="#5d6b7d">código · prosa</text><rect x="376" y="104" width="82" height="66" rx="8" fill="#eef2f7"/><text x="417" y="130" text-anchor="middle" font-weight="600">cache</text><text x="417" y="146" text-anchor="middle" font-size="10" fill="#5d6b7d">congela o que</text><text x="417" y="159" text-anchor="middle" font-size="10" fill="#5d6b7d">já foi decorado</text><rect x="468" y="104" width="72" height="66" rx="8" fill="#eef2f7"/><text x="504" y="130" text-anchor="middle" font-weight="600">ferramentas</text><text x="504" y="146" text-anchor="middle" font-size="10" fill="#5d6b7d">esquemas</text><text x="504" y="159" text-anchor="middle" font-size="10" fill="#5d6b7d">sob demanda</text></g><line x1="274" y1="137" x2="284" y2="137" stroke="#cfe0f5" stroke-width="1.5"/><line x1="366" y1="137" x2="376" y2="137" stroke="#cfe0f5" stroke-width="1.5"/><line x1="458" y1="137" x2="468" y2="137" stroke="#cfe0f5" stroke-width="1.5"/><text x="366" y="196" text-anchor="middle" font-size="10.5" fill="#cfe0f5">todo corte com perda deixa um marcador  ‹‹ccr:hash››</text><line x1="554" y1="130" x2="596" y2="130" stroke="#16233a" stroke-width="1.5" marker-end="url(#hd-ink)"/><text x="575" y="118" text-anchor="middle" font-size="10.5" fill="#5d6b7d">editado</text><rect x="598" y="92" width="106" height="76" rx="10" fill="#eef2f7" stroke="#d5dde8"/><text x="651" y="124" text-anchor="middle" font-size="14" font-weight="600" fill="#16233a">Anthropic</text><text x="651" y="143" text-anchor="middle" font-size="11" fill="#5d6b7d">API · o modelo</text><rect x="284" y="244" width="164" height="60" rx="10" fill="#fff" stroke="#1d4e89" stroke-width="1.5" stroke-dasharray="5 3"/><text x="366" y="268" text-anchor="middle" font-size="13" font-weight="600" fill="#1d4e89">cofre CCR</text><text x="366" y="286" text-anchor="middle" font-size="10.5" fill="#5d6b7d">todo original, SQLite local</text><line x1="366" y1="212" x2="366" y2="242" stroke="#1d4e89" stroke-width="1.5" marker-end="url(#hd-navy)"/><text x="378" y="232" text-anchor="start" font-size="10.5" fill="#1d4e89">guarda</text><path d="M284,274 L75,274 L75,170" fill="none" stroke="#5d6b7d" stroke-width="1.5" stroke-dasharray="4 3" marker-end="url(#hd-muted)"/><text x="180" y="266" text-anchor="middle" font-size="10.5" fill="#5d6b7d">headroom_retrieve (MCP)</text><text x="180" y="290" text-anchor="middle" font-size="10.5" fill="#5d6b7d">quando o modelo precisa do original</text></svg>
<figcaption>O caminho da requisição com o Headroom no meio. Quatro estágios editam a conversa; todo corte com perda é guardado no cofre CCR e pode ser recuperado pelo modelo por meio do servidor MCP.</figcaption>
</figure>

Quatro movimentos, nesta ordem.

**Ele lê antes de cortar.** Um roteador de conteúdo classifica cada bloco da
conversa — a saída de uma ferramenta, um log, um JSON, um arquivo-fonte, a
sua própria prosa — e escolhe o compressor adequado. JSON recebe um
compactador estrutural que preserva a forma e descarta a repetição. Logs e
tabelas recebem compactação nativa do formato, sem perda. Código passa por uma
etapa ciente da árvore sintática, que mantém assinaturas e descarta corpos que
o modelo já viu. Prosa vai para um pequeno modelo treinado que conserva as
frases que carregam peso. Blocos que aparecem duas vezes em turnos diferentes
seguem uma vez só.

**Todo corte deixa um recibo.** É esta a parte que torna o resto aceitável.
Quando um compressor descarta algo, ele guarda o original em um cofre SQLite
local e deixa um marcador no lugar: `<<ccr:hash>>`. Se o modelo precisar
depois do que foi cortado, chama `headroom_retrieve` com o hash e recebe o
original de volta. O Headroom chama isso de CCR — *compress, cache,
retrieve*. A contagem de recuperações é o sinal de alarme: se cresce, o editor
está cortando coisas de que o especialista realmente precisava.

**Ele nunca reescreve uma página que o especialista já decorou.** Os
provedores guardam em cache o prefixo de uma conversa e cobram um décimo pela
parte que já têm. Um editor que reordena páginas antigas quebra esse cache e
custa mais do que economiza. O Headroom acompanha qual prefixo o provedor já
viu e o congela.

**Ele deixa o catálogo de ferramentas na porta.** Uma sessão do Claude Code
com alguns servidores MCP pode carregar centenas de definições de ferramentas
— esquemas que o modelo lê em toda requisição e usa em quase nenhuma. Com a
busca de ferramentas ligada, só os nomes viajam; o esquema é buscado quando o
modelo estende a mão para aquela ferramenta. Não é invenção do Headroom — é
um recurso do Claude Code —, mas o proxy faz questão dele por um motivo que
vale conhecer: no momento em que você define um `ANTHROPIC_BASE_URL`
próprio, o Claude Code deixa de adiar os esquemas, a menos que
`ENABLE_TOOL_SEARCH=true` também esteja definido. Passe por qualquer proxy sem
essa variável e o seu contexto se enche de catálogo.

## Dois modos, uma tensão

O editor pode ser tímido ou ousado.

No **modo cache**, o padrão, ele só toca no turno mais recente. Toda página
anterior fica byte a byte como o provedor a guardou. Seguro, barato e — por
desenho — pequeno: a maior parte de uma conversa longa é página antiga, e
página antiga é intocável.

No **modo token**, ele pode voltar e reescrever turnos anteriores. O dossiê
encurta; o cache do provedor para aquela requisição é quebrado e refeito.
Troca-se uma falha de cache pontual por um arquivo permanentemente menor. A
estimativa do próprio Headroom é que isso estende uma sessão em um quarto a um
terço antes de o contexto lotar.

Aprendi a diferença do jeito honesto. Por quatro dias o proxy rodou em um
projeto real em modo cache, por acidente — um processo iniciado à mão havia
ignorado o modo que eu tinha configurado. Pouco mais de 700 milhões de tokens
passaram por ele. O compressor de mensagens removeu 1,7 milhão: um quarto de
um por cento. O painel anunciava, animado, milhares de dólares em "economia
de cache" — que era o cache do provedor, anterior ao proxy, que não lhe deve
nada. A única camada que fez força de verdade foi o catálogo de ferramentas:
29,6 milhões de tokens de esquemas mantidos fora da janela de contexto.

Um quarto de um por cento não é um veredito sobre o Headroom. É um veredito
sobre rodá-lo no modo errado e confiar em um painel. Por isso o teste recomeça
amanhã, em modo token, com as regras escritas antes.

## A configuração, como fiz hoje

A CLI se instala do mesmo jeito em qualquer sistema — uma ferramenta Python
3.13 em ambiente próprio:

{{< snippet file="headroom-editor/install.sh" lang="bash" >}}

O passo 2 é o caminho portátil: `headroom install apply` cria um proxy que
sobrevive a reinicializações e, de quebra, aplica as salvaguardas do teste. No
Linux ele vira um serviço de usuário do systemd; no macOS, um agente do
launchd; no Windows, uma entrada no Agendador de Tarefas (a ferramenta
converte o preset de serviço por você). O passo 3 escreve `ANTHROPIC_BASE_URL`
e `ENABLE_TOOL_SEARCH` no `.claude/settings.local.json` do projeto, junto com
os hooks que mantêm o proxy vivo. O `headroom doctor` diz, em uma tabela, se o
proxy está de pé, se o Claude está de fato roteado e se o seu shell o está
contornando.

Por baixo do capô, no Linux, são três arquivos pequenos — e eu prefiro ser
dono deles. Os ajustes vivem em um lugar só:

{{< snippet file="headroom-editor/proxy.env" lang="ini" >}}

O serviço os lê e reinicia o proxy se ele cair:

{{< snippet file="headroom-editor/headroom.service" lang="ini" >}}

E um *wrapper* abre o Claude através do proxy. O `claude` puro fica intocado
de propósito — é o grupo de controle:

{{< snippet file="headroom-editor/clh" lang="bash" >}}

O gêmeo para Windows é um script PowerShell no seu `PATH`; o proxy fica vivo
pela tarefa agendada do passo 2:

{{< snippet file="headroom-editor/clh.ps1" lang="powershell" >}}

Se preferir não usar *wrapper*, é isto que o `headroom init claude` escreve
no projeto — as mesmas duas variáveis, mais o hook:

{{< snippet file="headroom-editor/settings.local.json" lang="json" >}}

Uma nota sobre `--dangerously-skip-permissions`: essa flag é escolha minha,
na minha máquina, onde o agente trabalha dentro de repositórios git que posso
restaurar. Deixe-a de fora se essa não for a sua situação.

## As regras do teste

Dois princípios, acordados antes de a primeira requisição passar.

**Economizar o máximo, perder o mínimo — e saber o que se perdeu.**
Compressão com perda continua sendo perda; afirmar que nada é afetado seria
desonesto. O que o teste exige é que toda perda seja *aceitável* (não altera o
resultado do trabalho), *previsível* (as regras do que nunca é cortado são
conhecidas de antemão) e *auditável* (o que foi cortado pode ser contado e
recuperado).

**Deixar a evidência decidir.** Antes e depois são medidos na mesma fonte, e a
regra para manter, aprofundar ou abandonar a configuração é escrita antes de
os dados chegarem. O gráfico decide, não a impressão.

Na prática, as salvaguardas são estas:

| Salvaguarda | Por quê |
|---|---|
| **Edição ousada**<br>`HEADROOM_MODE=token` | A alavanca que nunca foi testada. |
| **Arquivos são sagrados**<br>`HEADROOM_PROTECT_TOOL_RESULTS=Read,Edit,Write` | O que o agente leu ou escreveu nunca é comprimido com perda; ele nunca edita a partir de um resumo. |
| **Catálogo mais curto**<br>`HEADROOM_TOOL_DESC_MAX_CHARS=200` | Descrições de ferramentas truncadas na primeira frase — barato e previsível. |
| **Prosa conservadora**<br>`HEADROOM_TARGET_RATIO` indefinido | O compressor de prosa mantém o seu próprio limiar cauteloso. |
| **Todo corte recuperável**<br>CCR ligado (padrão) | Sem `--no-ccr`; as recuperações são o alarme. |
| **Um recibo por requisição**<br>`HEADROOM_LOG_FILE=…/requests.jsonl` | Tokens antes e depois, leituras e escritas de cache, latência, quais transformações rodaram. |

E a medição, em três fontes que não dependem umas das outras: os transcripts
do Claude Code, que registram o que a API de fato cobrou por requisição; o
log de requisições do próprio proxy, que registra o que ele afirma ter feito;
e o coletor de uso da assinatura, que registra quanto da cota semanal do plano
foi realmente consumido. Dois projetos, três fases cada — sem proxy, modo
cache, modo token —, com pelo menos cinco dias úteis na última.

A regra fica fixada agora, para que eu não possa dobrá-la depois: **manter e
aprofundar** se os tokens cobrados por requisição caírem quinze por cento ou
mais, se releituras e recuperações não subirem mais de um quinto e se a
latência acrescentada pelo proxy ficar abaixo de quatro segundos no
nonagésimo percentil. Fora disso, voltar ao modo cache ou à compactação sem
perda — e dizer isso.

## O que vem a seguir

O editor sentou-se na cadeira hoje à noite. Em alguns dias publico o que os
recibos dizem: tokens por requisição em cada fase, leituras contra escritas de
cache, até onde uma sessão se estende antes de lotar, quantas vezes o modelo
pediu um original de volta e quanto o proxy custou em segundos. Se o editor
merecer a cadeira, eu digo. Se não merecer, digo também.

*Versões: Headroom 0.36.5, Claude Code 2.1.278, em setembro de 2026. Os
números acima vêm de um projeto real em que trabalho; o projeto não é o
assunto e não é nomeado.*
