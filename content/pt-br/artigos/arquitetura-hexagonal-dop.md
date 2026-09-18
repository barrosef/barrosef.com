---
title: "Arquitetura hexagonal onde ela compensa: como o DOP mantém os fornecedores atrás de ports"
date: 2026-09-18T08:00:00-04:00
draft: false
translationKey: "hexagonal-architecture-dop"
categories: ["Tecnologia"]
tags: ["dop", "arquitetura-hexagonal", "go", "decisoes-de-arquitetura", "nuvem"]
description: "O núcleo do DOP roda no Cloud Run e num cluster k3s sem mudar uma linha do domínio. O que torna isso verdade não é a estrutura de pastas: dois adapters por port desde o primeiro dia, uma suíte de contrato que todo adapter passa e um teste que quebra o build quando o domínio importa infraestrutura — com o código."
---

O núcleo do DOP precisa rodar em dois lugares que não concordam em nada. No
Google Cloud Run, um segredo mora no Secret Manager e a identidade vem do
Firebase. Num cluster k3s, um segredo é um Secret do Kubernetes e a identidade
vem do provedor OIDC que o cluster tiver. Some a lista que cresce com o
produto — armazenamento de objetos, um broker de mensagens, o executor que
roda o sandbox de um agente, o host git que recebe o pull request — e acoplar
o domínio a qualquer um deles significaria uma reescrita por ambiente.

Arquitetura hexagonal — ports e adapters — é a resposta de manual. É também o
padrão que mais frequentemente termina como o nome de uma pasta: um pacote
`interfaces/`, uma implementação por interface, e um domínio que continua
sabendo o que é um bucket. Este artigo é sobre a versão que o
[DOP](https://dop-t.com/) roda: onde a hexagonal valeu a pena, o que ela
custa, e as três disciplinas que a impedem de apodrecer. O código é real — os
trechos vêm do `dop-core`, o núcleo em Go da plataforma, aparados para
leitura.

## A forma

<figure class="diagram"><svg viewBox="0 0 720 464" role="img" aria-label="O BFF e a CLI chegam a um hexágono azul-marinho rotulado internal/domain por uma borda gRPC; à direita, ports desenhados como tomadas na borda do hexágono ligam-se a fileiras de chips de adapters, agrupados em ports de infraestrutura escolhidos no boot e ports de provedor escolhidos por requisição; uma faixa de raiz de composição embaixo." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="h-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#16233a"/></marker><marker id="h-navy" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#1d4e89"/></marker><marker id="h-forbid" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#b3261e"/></marker><marker id="h-muted" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#5d6b7d"/></marker></defs><rect x="16" y="60" width="190" height="330" rx="10" fill="#eef2f7" stroke="#d5dde8" stroke-width="1"/><text x="32" y="84" text-anchor="start" font-size="12.5" font-weight="600" fill="#5d6b7d">aciona o domínio</text><rect x="420" y="60" width="284" height="330" rx="10" fill="#eef2f7" stroke="#d5dde8" stroke-width="1"/><text x="436" y="84" text-anchor="start" font-size="12.5" font-weight="600" fill="#5d6b7d">acionado pelo domínio</text><polygon points="258.0,138.5 354.0,138.5 402.0,222.0 354.0,305.5 258.0,305.5 210.0,222.0" fill="#1d4e89" stroke="#173d6e" stroke-width="1.5"/><text x="306" y="192" text-anchor="middle" font-size="14.5" font-weight="600" fill="#fff">internal/domain</text><text x="306" y="211" text-anchor="middle" font-size="11" font-weight="400" fill="#cfe0f5">modelo · casos de uso · ports</text><text x="306" y="236" text-anchor="middle" font-size="10.5" font-weight="400" fill="#e8f0fa" font-family="IBM Plex Mono, ui-monospace, monospace">demand · delivery</text><text x="306" y="252" text-anchor="middle" font-size="10.5" font-weight="400" fill="#e8f0fa" font-family="IBM Plex Mono, ui-monospace, monospace">execution · resource</text><text x="306" y="268" text-anchor="middle" font-size="10.5" font-weight="400" fill="#e8f0fa" font-family="IBM Plex Mono, ui-monospace, monospace">identity · …</text><rect x="32" y="104" width="110" height="50" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="87.0" y="126.0" text-anchor="middle" font-size="13" font-weight="600" fill="#16233a">dop-api</text><text x="87.0" y="143.0" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">BFF Python</text><rect x="32" y="176" width="110" height="50" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="87.0" y="198.0" text-anchor="middle" font-size="13" font-weight="600" fill="#16233a">dop-cmd</text><text x="87.0" y="215.0" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">CLI</text><rect x="150" y="138" width="50" height="56" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="175.0" y="163.0" text-anchor="middle" font-size="13" font-weight="600" fill="#16233a">borda</text><text x="175.0" y="180.0" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">gRPC</text><path d="M 142,129 L 150,152" fill="none" stroke="#16233a" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-ink)"/><path d="M 142,201 L 150,180" fill="none" stroke="#16233a" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-ink)"/><path d="M 200,166 L 204,214" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/><rect x="204" y="216" width="12" height="12" rx="2" fill="#fff" stroke="#1d4e89" stroke-width="1.6"/><text x="32" y="262" text-anchor="start" font-size="11.5" font-weight="400" fill="#5d6b7d">O BFF e a CLI chegam ao</text><text x="32" y="279" text-anchor="start" font-size="11.5" font-weight="400" fill="#5d6b7d">domínio só por gRPC —</text><text x="32" y="296" text-anchor="start" font-size="11.5" font-weight="400" fill="#5d6b7d">o único adapter primário.</text><text x="436" y="108" text-anchor="start" font-size="11.5" font-weight="600" fill="#1d4e89">infraestrutura · no boot, um ativo</text><text x="436" y="280" text-anchor="start" font-size="11.5" font-weight="600" fill="#1d4e89">provedores · por requisição, vários ativos</text><path d="M 368.7701149425287,152 C 398.38505747126436,152 398.38505747126436,132 428,132" fill="none" stroke="#1d4e89" stroke-width="1.2" stroke-linecap="round"/><rect x="356.7701149425287" y="147" width="10" height="10" rx="2" fill="#fff" stroke="#1d4e89" stroke-width="1.6"/><text x="436" y="136" text-anchor="start" font-size="11.5" font-weight="600" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">SecretStore</text><rect x="524" y="121" width="54" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="551.0" y="136" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">memory</text><rect x="584" y="121" width="35" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="601.5" y="136" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">k8s</text><rect x="625" y="121" width="35" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="642.5" y="136" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">gcp</text><path d="M 382.5632183908046,176 C 405.2816091954023,176 405.2816091954023,166 428,166" fill="none" stroke="#1d4e89" stroke-width="1.2" stroke-linecap="round"/><rect x="370.5632183908046" y="171" width="10" height="10" rx="2" fill="#fff" stroke="#1d4e89" stroke-width="1.6"/><text x="436" y="170" text-anchor="start" font-size="11.5" font-weight="600" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">EventBus</text><rect x="502" y="155" width="54" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="529.0" y="170" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">memory</text><rect x="562" y="155" width="41" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="582.5" y="170" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">nats</text><path d="M 396.35632183908046,200 C 412.17816091954023,200 412.17816091954023,200 428,200" fill="none" stroke="#1d4e89" stroke-width="1.2" stroke-linecap="round"/><rect x="384.35632183908046" y="195" width="10" height="10" rx="2" fill="#fff" stroke="#1d4e89" stroke-width="1.6"/><text x="436" y="204" text-anchor="start" font-size="11.5" font-weight="600" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">IdentityProvider</text><rect x="559" y="189" width="67" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="592.5" y="204" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">firebase</text><rect x="632" y="189" width="41" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="652.5" y="204" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">oidc</text><path d="M 407.85057471264366,224 C 417.92528735632186,224 417.92528735632186,234 428,234" fill="none" stroke="#1d4e89" stroke-width="1.2" stroke-linecap="round"/><rect x="395.85057471264366" y="219" width="10" height="10" rx="2" fill="#fff" stroke="#1d4e89" stroke-width="1.6"/><text x="436" y="238" text-anchor="start" font-size="11.5" font-weight="600" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">SandboxLauncher</text><rect x="552" y="223" width="54" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="579.0" y="238" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">docker</text><rect x="612" y="223" width="35" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="629.5" y="238" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">k8s</text><path d="M 394.0574712643678,248 C 411.0287356321839,248 411.0287356321839,304 428,304" fill="none" stroke="#1d4e89" stroke-width="1.2" stroke-linecap="round"/><rect x="382.0574712643678" y="243" width="10" height="10" rx="2" fill="#fff" stroke="#1d4e89" stroke-width="1.6"/><text x="436" y="308" text-anchor="start" font-size="11.5" font-weight="600" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">GitProvider</text><rect x="524" y="293" width="54" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="551.0" y="308" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">github</text><rect x="584" y="293" width="54" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="611.0" y="308" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">gitlab</text><path d="M 380.264367816092,272 C 404.132183908046,272 404.132183908046,338 428,338" fill="none" stroke="#1d4e89" stroke-width="1.2" stroke-linecap="round"/><rect x="368.264367816092" y="267" width="10" height="10" rx="2" fill="#fff" stroke="#1d4e89" stroke-width="1.6"/><text x="436" y="342" text-anchor="start" font-size="11.5" font-weight="600" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">AgentProvider</text><rect x="538" y="327" width="73" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="574.5" y="342" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">anthropic</text><rect x="617" y="327" width="54" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="644.0" y="342" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">openai</text><path d="M 366.4712643678161,296 C 397.235632183908,296 397.235632183908,372 428,372" fill="none" stroke="#1d4e89" stroke-width="1.2" stroke-linecap="round"/><rect x="354.4712643678161" y="291" width="10" height="10" rx="2" fill="#fff" stroke="#1d4e89" stroke-width="1.6"/><text x="436" y="376" text-anchor="start" font-size="11.5" font-weight="600" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">Mailer</text><rect x="488" y="361" width="41" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="508.5" y="376" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">smtp</text><rect x="535" y="361" width="67" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="568.5" y="376" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">sendgrid</text><rect x="16" y="404" width="688" height="44" rx="10" fill="#fff" stroke="#b9c5d4" stroke-width="1" stroke-dasharray="6 5"/><text x="32" y="431" text-anchor="start" font-size="13" font-weight="600" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">internal/app</text><text x="140" y="431" text-anchor="start" font-size="12" font-weight="400" fill="#5d6b7d">a raiz de composição — conhece as duas pontas; a configuração escolhe cada adapter</text></svg><figcaption>As três regiões do dop-core. O domínio declara os ports (as tomadas nas suas bordas); cada pacote de adapter se liga a uma; a raiz de composição faz a ligação, por configuração. As duas famílias à direita têm ciclos de vida opostos.</figcaption></figure>

Três regiões. `internal/domain` é dono do modelo e declara os ports — o
cofre, o provedor de identidade, o barramento de eventos, o executor, os
repositórios — no seu próprio vocabulário. `internal/adapter` tem um pacote
por tecnologia: Secret Manager e Secret do Kubernetes atrás da mesma
interface, NATS JetStream e um barramento em memória atrás de outra, GitHub e
GitLab atrás de uma terceira. `internal/app` é a raiz de composição: o único
lugar que conhece as duas pontas, onde um valor de configuração escolhe qual
adapter preenche qual port. Do outro lado, o servidor gRPC é o adapter
primário; o BFF em Python e a CLI chegam ao domínio por ele e por nada mais.

Nada disso é novo. O que importa é uma distinção que o diagrama faz e a
maioria das bases de código hexagonais não faz.

## Duas famílias de ports

| | Ports de infraestrutura | Ports de provedor de domínio |
|---|---|---|
| Exemplos | `SecretStore`, `IdentityProvider`, `ObjectStore`, `EventBus`, repositórios | `GitProvider`, `AgentProvider`, `Mailer` |
| Quem escolhe | O ambiente de implantação | A configuração da conta |
| Quando | Uma vez, no boot | A cada requisição |
| Quantos ativos | Um | Vários ao mesmo tempo |

Elas se parecem — uma interface Go, N implementações — e têm ciclos de vida
opostos. Um port de infraestrutura é escolhido pela implantação: uma vez, no
boot, um adapter ativo pela vida do processo. Um port de provedor de domínio
é escolhido pelos dados da conta: a cada requisição, vários adapters ativos
ao mesmo tempo, porque um workspace tem um repositório no GitHub e outro no
GitLab e os dois têm que funcionar. Confundir as duas é o erro típico deste
desenho — um provedor git escolhido por variável de ambiente funciona na demo
e falha, em silêncio, no primeiro cliente com dois hosts. A seção sobre o
provedor git, mais abaixo, mostra como a família por requisição fica em
código.

## Um port na linguagem do domínio

{{< snippet file="hexagonal-dop/ports_secretstore.go" lang="go" >}}

Quatro verbos. `SecretRef` é opaco de propósito: o domínio nunca vê um
caminho no Secret Manager nem um namespace no Kubernetes. `SecretValue` não
consegue se imprimir, e é assim que a garantia 6 sobrevive a um `%v`
descuidado. E as garantias estão escritas no port, numeradas, porque são elas
que a suíte de contrato testa — a interface diz quais são os métodos; o
comentário diz o que eles prometem.

Repare no que não está lá: versões. O Secret Manager tem, um Secret do
Kubernetes não tem, e uma capacidade que não mapeia entre adapters fica fora
do port. Se um dia for necessária, entra como capacidade opcional que o
domínio nunca presume.

O caso de uso do outro lado do port sabe exatamente isto:

{{< snippet file="hexagonal-dop/resource_set_credential.go" lang="go" >}}

O domínio monta uma referência a partir dos próprios identificadores e chama
`Put`. Ordena o cofre antes da linha por uma razão que ele mesmo escreve, e
não sabe nada sobre para onde os bytes vão.

## Dois adapters desde o primeiro dia

A primeira disciplina: um port com um único adapter é um chute, e sai com o
formato do fornecedor que o inspirou. Por isso o adapter local não é "para
depois" — é escrito junto com o port, e é a prova de que o port está certo.

{{< snippet file="hexagonal-dop/secretstore_memory.go" lang="go" >}}

Cinquenta linhas, e não é um mock: copia os bytes na entrada e na saída para
que quem chama não altere o cofre por acidente, e passa exatamente os mesmos
testes que o adapter do GCP. O barramento de eventos em memória é a mesma
história com mais em jogo — entrega numa goroutine, com backoff, teto de
tentativas e a mesma política de mensagem envenenada do JetStream, porque um
dublê que entregasse de forma síncrona e perfeita esconderia os bugs que só
aparecem com entrega assíncrona.

A raiz de composição escolhe entre eles por configuração:

{{< snippet file="hexagonal-dop/wire.go" lang="go" >}}

`Deps` guarda ports, nunca tipos concretos, e esse `switch` é o único
condicional sobre backend em toda a base de código. É assim que "escolhido no
boot, um ativo" fica na prática.

## A suíte de contrato é o que torna isso verdade

A segunda disciplina. Dois adapters que passam cada um nos próprios testes
são dois adapters; dois adapters que passam nos *mesmos* testes são
substituíveis. O DOP mantém uma suíte por port em `test/contract`, escrita
contra as garantias numeradas do port:

{{< snippet file="hexagonal-dop/contract_secretstore.go" lang="go" >}}

O comentário do topo registra a armadilha. A primeira versão desta suíte
usava nomes de conta fixos e passava — contra o dublê em memória, onde cada
subteste ganha um cofre novo. Contra um backend real o mesmo cofre persiste
entre subtestes, e o segredo deixado pelo subteste 1 quebrou o subteste 5. A
suíte tinha sido escrita em cima do dublê e carregava uma premissa que só o
dublê satisfazia; nenhum adapter real passaria, e nenhum estava sendo
executado. Identificadores únicos por execução consertaram a suíte. Rodá-la
contra a coisa real foi o que achou o bug — e é a razão do arquivo seguinte:

{{< snippet file="hexagonal-dop/contract_secretstore_test.go" lang="go" >}}

<figure class="diagram"><svg viewBox="0 0 720 392" role="img" aria-label="A suíte de contrato do SecretStore se abre em três adapters: memória sempre, k8s quando um cluster responde, GCP atrás de uma build tag; embaixo, três colunas para domínio, adapter e SDKs, com setas permitidas do adapter para o domínio e para os SDKs, e uma seta tracejada vermelha proibida do domínio para o adapter." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="h-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#16233a"/></marker><marker id="h-navy" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#1d4e89"/></marker><marker id="h-forbid" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#b3261e"/></marker><marker id="h-muted" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#5d6b7d"/></marker></defs><rect x="16" y="44" width="190" height="70" rx="6" fill="#1d4e89" stroke="#173d6e" stroke-width="1.2"/><text x="111.0" y="76.0" text-anchor="middle" font-size="13" font-weight="600" fill="#fff">SecretStoreSuite</text><text x="111.0" y="93.0" text-anchor="middle" font-size="11" font-weight="400" fill="#cfe0f5">seis garantias numeradas</text><text x="111" y="132" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">test/contract/secretstore.go</text><path d="M 206,79 L 240,79 L 262,46 L 282,46" fill="none" stroke="#1d4e89" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><rect x="284" y="24" width="110" height="44" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="339.0" y="51.0" text-anchor="middle" font-size="13" font-weight="600" fill="#16233a">memory</text><text x="408" y="51" text-anchor="start" font-size="12" font-weight="400" fill="#5d6b7d">sempre</text><path d="M 206,79 L 240,79 L 262,98 L 282,98" fill="none" stroke="#1d4e89" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><rect x="284" y="76" width="110" height="44" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="339.0" y="103.0" text-anchor="middle" font-size="13" font-weight="600" fill="#16233a">k8s</text><text x="408" y="103" text-anchor="start" font-size="12" font-weight="400" fill="#5d6b7d">quando um cluster responde</text><path d="M 206,79 L 240,79 L 262,150 L 282,150" fill="none" stroke="#1d4e89" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><rect x="284" y="128" width="110" height="44" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2" stroke-dasharray="6 5"/><text x="339.0" y="155.0" text-anchor="middle" font-size="13" font-weight="600" fill="#16233a">gcp</text><text x="408" y="155" text-anchor="start" font-size="12" font-weight="400" fill="#5d6b7d">atrás de uma build tag, quando há credencial</text><text x="284" y="194" text-anchor="start" font-size="12" font-weight="600" fill="#1d4e89">uma função, três alvos</text><rect x="16" y="226" width="688" height="150" rx="10" fill="#eef2f7" stroke="#d5dde8" stroke-width="1"/><text x="32" y="250" text-anchor="start" font-size="12.5" font-weight="600" fill="#5d6b7d">a fronteira, guardada por dois testes em todo go test ./...</text><rect x="40" y="262" width="150" height="52" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="115.0" y="285.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">internal/domain</text><text x="115.0" y="302.0" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">declara os ports</text><rect x="290" y="262" width="150" height="52" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="365.0" y="285.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">internal/adapter</text><text x="365.0" y="302.0" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">os implementa</text><rect x="540" y="262" width="150" height="52" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="615.0" y="285.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">SDKs</text><text x="615.0" y="302.0" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">pgx · nats · gcp · k8s</text><path d="M 440,288 L 538,288" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><text x="489" y="280" text-anchor="middle" font-size="10.5" font-weight="400" fill="#1d4e89">permitido</text><path d="M 290,276 L 192,276" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><text x="241" y="268" text-anchor="middle" font-size="10.5" font-weight="400" fill="#1d4e89">implementa</text><path d="M 192,300 L 290,300" fill="none" stroke="#b3261e" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="6 5" marker-end="url(#h-forbid)"/><text x="241" y="322" text-anchor="middle" font-size="10.5" font-weight="600" fill="#b3261e">nunca</text><text x="40" y="350" text-anchor="start" font-size="11.5" font-weight="400" fill="#5d6b7d">TestTheDomainDoesNotImportInfrastructure — nada sob internal/domain importa um adapter ou um SDK.</text><text x="40" y="366" text-anchor="start" font-size="11.5" font-weight="400" fill="#5d6b7d">TestOnlyAppKnowsTheAdapters — fora de internal/app, nada importa internal/adapter.</text></svg><figcaption>O que mantém o padrão verdadeiro ao longo do tempo. Em cima: uma suíte de contrato roda contra todo adapter. Embaixo: a fronteira de imports — adapters podem conhecer o domínio e os SDKs; o domínio não conhece nenhum dos dois — imposta por testes que quebram o build.</figcaption></figure>

A mesma função, três alvos: o adapter em memória sempre, o Kubernetes quando
um cluster responde, o Secret Manager atrás de uma build tag quando existe
credencial. O aviso acima do teste do GCP é merecido: o emulador é mais
permissivo que o Google em nove pontos documentados, e um deles é a primeira
garantia do port.

## Quando o adapter não consegue cumprir a promessa, o adapter paga

O `SecretStore` promete read-after-write. A promessa nasceu do adapter
Kubernetes, onde ela vale — desde que o adapter leia pela API e não por um
volume montado, que o kubelet sincroniza mais ou menos uma vez por minuto. O
adapter do GCP não conseguiu cumpri-la como estava escrita. O Google é
explícito: só a leitura *por número de versão* é fortemente consistente,
enquanto o alias `latest` converge "tipicamente em minutos, mas pode levar
algumas horas". E `SecretRef` é plano; não há onde guardar uma versão.

O modo de falha é o pior que um cofre pode ter. No GCP real, um `Get` logo
depois de um `Put` podia devolver `(nil, nil)` — que, pelo port, significa
"não existe". Uma credencial recém-escrita pareceria ausente, em silêncio, e
quem chamou concluiria que a integração nunca foi configurada. No emulador o
mesmo caso passa em dez milissegundos.

<figure class="diagram"><svg viewBox="0 0 720 454" role="img" aria-label="Duas raias para SecretStore.Put: o adapter em memória escreve num map e retorna; o adapter Secret Manager cria uma versão, confirma por número, espera o alias latest com retries, destrói versões antigas e retorna, ou recusa com KindUnavailable passado o teto." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="h-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#16233a"/></marker><marker id="h-navy" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#1d4e89"/></marker><marker id="h-forbid" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#b3261e"/></marker><marker id="h-muted" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#5d6b7d"/></marker></defs><rect x="16" y="16" width="250" height="48" rx="6" fill="#1d4e89" stroke="#173d6e" stroke-width="1.2"/><text x="141.0" y="37.0" text-anchor="middle" font-size="13" font-weight="600" fill="#fff">SecretStore.Put</text><text x="141.0" y="54.0" text-anchor="middle" font-size="11" font-weight="400" fill="#cfe0f5">a promessa: read-after-write</text><rect x="16" y="88" width="688" height="88" rx="10" fill="#eef2f7" stroke="#d5dde8" stroke-width="1"/><text x="32" y="112" text-anchor="start" font-size="12.5" font-weight="600" fill="#5d6b7d">adapter em memória</text><rect x="32" y="122" width="150" height="40" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="107.0" y="147.0" text-anchor="middle" font-size="12.5" font-weight="400" fill="#16233a">map[key] = copy</text><path d="M 182,142 L 208,142" fill="none" stroke="#16233a" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-ink)"/><rect x="210" y="122" width="110" height="40" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="265.0" y="147.0" text-anchor="middle" font-size="12.5" font-weight="400" fill="#16233a">return nil</text><text x="340" y="147" text-anchor="start" font-size="12" font-weight="400" fill="#5d6b7d" font-style="italic">aqui a promessa não custa nada</text><rect x="16" y="192" width="688" height="246" rx="10" fill="#eef2f7" stroke="#d5dde8" stroke-width="1"/><text x="32" y="216" text-anchor="start" font-size="12.5" font-weight="600" fill="#5d6b7d">adapter Secret Manager</text><rect x="32" y="226" width="138" height="52" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="101.0" y="249.0" text-anchor="middle" font-size="12.5" font-weight="500" fill="#16233a">AddSecretVersion</text><text x="101.0" y="266.0" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">versão n criada</text><path d="M 172,252 L 186,252" fill="none" stroke="#16233a" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-ink)"/><rect x="188" y="226" width="138" height="52" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="257.0" y="249.0" text-anchor="middle" font-size="12.5" font-weight="500" fill="#16233a">confirm v = n</text><text x="257.0" y="266.0" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">por número — forte</text><path d="M 328,252 L 342,252" fill="none" stroke="#16233a" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-ink)"/><rect x="344" y="226" width="138" height="52" rx="6" fill="#1d4e89" stroke="#173d6e" stroke-width="1.2"/><text x="413.0" y="249.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#fff">await latest ≥ n</text><text x="413.0" y="266.0" text-anchor="middle" font-size="11" font-weight="400" fill="#cfe0f5">alias — eventual</text><path d="M 484,252 L 498,252" fill="none" stroke="#16233a" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-ink)"/><rect x="500" y="226" width="138" height="52" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="569.0" y="249.0" text-anchor="middle" font-size="12.5" font-weight="500" fill="#16233a">destroyOlder</text><text x="569.0" y="266.0" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">material antigo destruído</text><path d="M 640,252 L 654,252" fill="none" stroke="#16233a" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-ink)"/><rect x="656" y="226" width="34" height="52" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="673.0" y="257.0" text-anchor="middle" font-size="16" font-weight="600" fill="#16233a">✓</text><path d="M 374,280 L 374,302 L 356,302 L 356,282" fill="none" stroke="#1d4e89" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><text x="346" y="306" text-anchor="end" font-size="11" font-weight="400" fill="#1d4e89" font-family="IBM Plex Mono, ui-monospace, monospace">retry · 25 ms → 1 s · ≤ 30 s</text><path d="M 458,280 L 458,338" fill="none" stroke="#1d4e89" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="6 5" marker-end="url(#h-navy)"/><rect x="378" y="340" width="160" height="44" rx="6" fill="#fff" stroke="#1d4e89" stroke-width="1.2"/><text x="458.0" y="359.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#1d4e89">KindUnavailable</text><text x="458.0" y="376.0" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">passado o teto</text><text x="458" y="404" text-anchor="middle" font-size="11.5" font-weight="400" fill="#5d6b7d">escrita aceita, read-after-write não confirmado:</text><text x="458" y="420" text-anchor="middle" font-size="11.5" font-weight="400" fill="#5d6b7d">um erro que alguém lê, não um Get dizendo "não existe".</text></svg><figcaption>O mesmo Put por dois adapters. Em memória a promessa é de graça. No Secret Manager o adapter confirma por número de versão, espera o alias alcançar — o passo destacado — e, passado o teto, recusa em vez de mentir.</figcaption></figure>

Três saídas estavam na mesa. Afrouxar a garantia para "eventualmente
consistente" empurra um laço de releitura para cada chamador, e o chamador
não consegue distinguir "ainda não" de "nunca". Guardar o valor em cache no
processo depois do `Put` cria um segundo lugar onde a credencial existe, com
a própria invalidação — troca um problema de consistência por um de
segurança. Ler por número de versão é o caminho fortemente consistente, mas
exige que o `Put` devolva um identificador que o chamador guarda; isso muda o
port, não um adapter, e ficou registrado como evolução possível em vez de
rejeitado.

A decisão foi que a garantia se mantém e o adapter paga:

{{< snippet file="hexagonal-dop/secretstore_gcp_await.go" lang="go" >}}

Confirmar a escrita por número de versão, depois esperar o `latest`
alcançar, com um teto, e se não convergir, recusar com um erro explícito.
Recusar é a parte que importa: um `Put` que devolve sucesso enquanto o `Get`
seguinte diz "não encontrado" produz uma integração silenciosamente quebrada;
um `Put` que falha produz um erro que alguém lê. O resíduo também está
escrito — um `Put` no GCP é mais lento e pode falhar por não-convergência,
comportamento que o emulador nunca reproduz, então o teste local não cobre
esse caminho.

É aqui que a hexagonal paga o próprio aluguel. O domínio nunca soube que o
Secret Manager tem um alias, o caso de uso não mudou uma linha, e o lugar
onde a semântica do fornecedor foi absorvida é uma função num adapter.

## A família por requisição: o provedor git

Um pull request vai para o host onde o repositório mora, e o token que o abre
pertence à integração da conta. O domínio de entrega declara o que precisa e
quem resolve:

{{< snippet file="hexagonal-dop/delivery_gitprovider.go" lang="go" >}}

Duas interfaces. `GitProvider` é o vocabulário do domínio de entrega — abrir,
rebase, merge, e se o host tem uma fila de merge própria em cima da qual a
fila do DOP pode orquestrar. `GitProviders` resolve qual delas serve um dado
repositório. O resolvedor é implementado na raiz de composição, porque é o
único lugar autorizado a conhecer as três pontas:

{{< snippet file="hexagonal-dop/app_gitproviders.go" lang="go" >}}

<figure class="diagram"><svg viewBox="0 0 720 290" role="img" aria-label="O domínio de entrega chama For com conta e repositório; dentro da raiz de composição três passos resolvem repositório, integração e cofre; um adapter GitHub ou GitLab é devolvido por chamada; o cofre é lido dentro do resolvedor." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="h-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#16233a"/></marker><marker id="h-navy" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#1d4e89"/></marker><marker id="h-forbid" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#b3261e"/></marker><marker id="h-muted" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#5d6b7d"/></marker></defs><rect x="16" y="60" width="160" height="64" rx="6" fill="#1d4e89" stroke="#173d6e" stroke-width="1.2"/><text x="96.0" y="89.0" text-anchor="middle" font-size="13" font-weight="600" fill="#fff">domain/delivery</text><text x="96.0" y="106.0" text-anchor="middle" font-size="11" font-weight="400" fill="#cfe0f5">abre o PR</text><path d="M 176,92 L 206,92" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><text x="96" y="146" text-anchor="middle" font-size="11" font-weight="400" fill="#1d4e89" font-family="IBM Plex Mono, ui-monospace, monospace">For(account, repo)</text><rect x="208" y="24" width="320" height="172" rx="10" fill="#eef2f7" stroke="#d5dde8" stroke-width="1"/><text x="224" y="48" text-anchor="start" font-size="12.5" font-weight="600" fill="#5d6b7d">internal/app · gitProviders.For</text><rect x="222" y="56" width="92" height="52" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="268.0" y="79.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">repositório</text><text x="268.0" y="96.0" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">→ integração</text><path d="M 316,82 L 320,82" fill="none" stroke="#16233a" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/><rect x="322" y="56" width="92" height="52" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="368.0" y="79.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">integração</text><text x="368.0" y="96.0" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">→ provedor</text><path d="M 416,82 L 420,82" fill="none" stroke="#16233a" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/><rect x="422" y="56" width="92" height="52" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="468.0" y="79.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">cofre</text><text x="468.0" y="96.0" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">→ token</text><text x="222" y="138" text-anchor="start" font-size="11.5" font-weight="600" fill="#1d4e89">resolvido a cada requisição</text><text x="222" y="156" text-anchor="start" font-size="11.5" font-weight="400" fill="#5d6b7d">provedor desconhecido: recusa,</text><text x="222" y="172" text-anchor="start" font-size="11.5" font-weight="400" fill="#5d6b7d">nunca um default</text><rect x="548" y="36" width="156" height="52" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="626.0" y="59.0" text-anchor="middle" font-size="13" font-weight="600" fill="#16233a">GitHub</text><text x="626.0" y="76.0" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">GraphQL · merge queue</text><rect x="548" y="108" width="156" height="52" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="626.0" y="131.0" text-anchor="middle" font-size="13" font-weight="600" fill="#16233a">GitLab</text><text x="626.0" y="148.0" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">REST · merge trains</text><path d="M 528,82 L 546,62" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><path d="M 528,110 L 546,134" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><text x="632" y="180" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d" font-style="italic">o token chega pronto</text><path d="M 468,110 L 468,224" fill="none" stroke="#16233a" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-ink)"/><text x="476" y="214" text-anchor="start" font-size="11" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">Get(ref)</text><rect x="388" y="226" width="160" height="48" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="468.0" y="247.0" text-anchor="middle" font-size="13" font-weight="600" fill="#16233a">ports.SecretStore</text><text x="468.0" y="264.0" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">lido aqui, no core</text><text x="16" y="232" text-anchor="start" font-size="12" font-weight="400" fill="#5d6b7d">O domínio de entrega nunca fica sabendo que o GitHub existe.</text><text x="16" y="250" text-anchor="start" font-size="12" font-weight="400" fill="#5d6b7d">O adapter git nunca fica sabendo que existe um cofre.</text><text x="16" y="268" text-anchor="start" font-size="12" font-weight="400" fill="#5d6b7d">O domínio de recursos nunca fica sabendo que PRs existem.</text></svg><figcaption>Um port por requisição. O domínio de entrega pede um provedor por repositório; a raiz de composição resolve integração e credencial e devolve um adapter pronto — GitHub para um repositório, GitLab para o seguinte.</figcaption></figure>

Repositório → integração → credencial → adapter, a cada requisição. O adapter
git recebe um token pronto e nunca fica sabendo que existe um cofre; o
domínio de entrega nunca fica sabendo que o GitHub existe; o domínio de
recursos nunca fica sabendo que pull requests existem. Um provedor
desconhecido é uma recusa, não um default, porque abrir um PR no lugar errado
é pior do que não abrir. O port do provedor de agente — Anthropic ou OpenAI,
escolhido por conta — tem exatamente a mesma forma.

## A fronteira é um teste

A terceira disciplina é a mais barata e a mais pulada. Uma regra que mora no
README dura até o primeiro prazo. A do DOP mora na suíte de testes:

{{< snippet file="hexagonal-dop/architecture_test.go" lang="go" >}}

Faça o parse dos imports de todo arquivo sob `internal/domain`; falhe em
qualquer pacote de adapter ou SDK de fornecedor. Um segundo teste percorre
todo o resto de `internal/` e falha se qualquer coisa além da raiz de
composição importar um adapter. Os dois rodam em todo `go test ./...`, então
a fronteira quebra o build antes de quebrar o desenho.

## O que custa, e onde não vale o esforço

Dois adapters por port, escritos e mantidos, desde o primeiro commit. Uma
suíte de contrato por port, e a infraestrutura para rodá-la contra os
backends reais, não só contra os emuladores. Uma indireção a mais em toda
chamada de infraestrutura. E o recurso mais forte de um fornecedor — versões
de segredo, IAM por segredo, custom claims do Firebase — inacessível ao
domínio por construção. Esse último é o preço, e é deliberado.

As mesmas regras dizem onde o padrão não compensa. Duas alternativas foram
consideradas para a plataforma como um todo e rejeitadas: acoplar ao GCP
agora e portar depois — "depois" é quando o acoplamento já se espalhou, e
rodar num cluster local era requisito de desenvolvimento, não ambição — e uma
biblioteca multi-cloud genérica, que entrega o denominador comum dos
fornecedores *da biblioteca*, não do domínio, e troca um acoplamento por
outro. Mas dentro da fronteira, o DOP não põe um port na frente de consultas
Postgres que só vão rodar no Postgres, não abstrai a borda gRPC e não
embrulha o logger. Um port vale a pena onde o segundo adapter é real: um
segundo ambiente, um segundo host que o cliente pode escolher, um teste que
precisa rodar sem infraestrutura. Onde o segundo adapter é imaginário, a
interface é o nome de uma pasta.

A hexagonal, no fim, é uma regra contábil: o domínio não paga nada ao
fornecedor, e o adapter paga o que o fornecedor cobrar. As três disciplinas
são o que mantém os livros honestos.
