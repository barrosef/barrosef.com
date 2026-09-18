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

<figure class="diagram"><svg viewBox="0 0 760 432" role="img" aria-label="O BFF e a CLI chegam ao hexágono do domínio por uma borda gRPC; do outro lado, ports de infraestrutura escolhidos no boot e ports de provedor escolhidos por requisição listam seus adapters; uma faixa de raiz de composição embaixo liga as duas pontas." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker><marker id="arrow-accent" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1d4e89"/></marker></defs><text x="20" y="30" text-anchor="start" font-size="11" font-weight="600" fill="currentColor">quem aciona o domínio</text><rect x="20" y="60" width="140" height="46" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="90.0" y="80.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">dop-api</text><text x="90.0" y="95.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">BFF Python · REST+SSE</text><rect x="20" y="122" width="140" height="46" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="90.0" y="142.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">dop-cmd</text><text x="90.0" y="157.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">CLI · v0.7.1</text><rect x="190" y="60" width="80" height="108" fill="#eef2f7" stroke="currentColor" stroke-width="1"/><text x="230.0" y="118.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">borda gRPC</text><text x="230" y="154" text-anchor="middle" font-size="9" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">internal/app/grpc</text><line x1="162" y1="83" x2="188" y2="90" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><text x="175" y="72" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">gRPC</text><line x1="162" y1="145" x2="188" y2="138" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><line x1="272" y1="114" x2="296" y2="114" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><polygon points="320,40 450,40 474,190 450,340 320,340 296,190" fill="#eef2f7" stroke="currentColor" stroke-width="1.2"/><text x="385" y="70" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">internal/domain</text><text x="385" y="86" text-anchor="middle" font-size="10" font-weight="400" fill="#5d6b7d">modelo · casos de uso · ports</text><text x="385" y="116" text-anchor="middle" font-size="10.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">demand</text><text x="385" y="133" text-anchor="middle" font-size="10.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">delivery</text><text x="385" y="150" text-anchor="middle" font-size="10.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">execution</text><text x="385" y="167" text-anchor="middle" font-size="10.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">resource</text><text x="385" y="184" text-anchor="middle" font-size="10.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">identity</text><text x="385" y="201" text-anchor="middle" font-size="10.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">event</text><text x="385" y="218" text-anchor="middle" font-size="10.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">workflow</text><text x="385" y="235" text-anchor="middle" font-size="10.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">…</text><text x="385" y="264" text-anchor="middle" font-size="10" font-weight="600" fill="#1d4e89">os PORTS</text><text x="385" y="278" text-anchor="middle" font-size="9.5" font-weight="400" fill="#1d4e89">na linguagem do domínio</text><text x="385" y="292" text-anchor="middle" font-size="9" font-weight="400" fill="#1d4e89" font-family="IBM Plex Mono, ui-monospace, monospace">domain/ports</text><text x="385" y="304" text-anchor="middle" font-size="9" font-weight="400" fill="#1d4e89" font-family="IBM Plex Mono, ui-monospace, monospace">delivery.GitProvider …</text><text x="500" y="30" text-anchor="start" font-size="11" font-weight="600" fill="currentColor">o que o domínio aciona</text><text x="500" y="56" text-anchor="start" font-size="10" font-weight="600" fill="#1d4e89">infraestrutura — escolhidos no boot, um ativo</text><circle cx="455" cy="70" r="3" fill="#1d4e89"/><text x="500" y="74" text-anchor="start" font-size="10.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">SecretStore</text><text x="740" y="74" text-anchor="end" font-size="10" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">memory · k8s · gcp</text><circle cx="458" cy="90" r="3" fill="#1d4e89"/><text x="500" y="94" text-anchor="start" font-size="10.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">EventBus</text><text x="740" y="94" text-anchor="end" font-size="10" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">memory · nats</text><circle cx="461" cy="110" r="3" fill="#1d4e89"/><text x="500" y="114" text-anchor="start" font-size="10.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">IdentityProvider</text><text x="740" y="114" text-anchor="end" font-size="10" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">firebase · oidc</text><circle cx="464" cy="130" r="3" fill="#1d4e89"/><text x="500" y="134" text-anchor="start" font-size="10.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">ObjectStore</text><text x="740" y="134" text-anchor="end" font-size="10" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">fs · gcs</text><circle cx="468" cy="150" r="3" fill="#1d4e89"/><text x="500" y="154" text-anchor="start" font-size="10.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">SandboxLauncher</text><text x="740" y="154" text-anchor="end" font-size="10" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">docker · k8s</text><circle cx="471" cy="170" r="3" fill="#1d4e89"/><text x="500" y="174" text-anchor="start" font-size="10.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">repositories</text><text x="740" y="174" text-anchor="end" font-size="10" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">postgres</text><text x="500" y="212" text-anchor="start" font-size="10" font-weight="600" fill="#1d4e89">provedores de domínio — por requisição, vários ativos</text><circle cx="468" cy="226" r="3" fill="#1d4e89"/><text x="500" y="230" text-anchor="start" font-size="10.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">GitProvider</text><text x="740" y="230" text-anchor="end" font-size="10" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">github · gitlab</text><circle cx="465" cy="246" r="3" fill="#1d4e89"/><text x="500" y="250" text-anchor="start" font-size="10.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">AgentProvider</text><text x="740" y="250" text-anchor="end" font-size="10" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">anthropic · openai</text><circle cx="462" cy="266" r="3" fill="#1d4e89"/><text x="500" y="270" text-anchor="start" font-size="10.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">Mailer</text><text x="740" y="270" text-anchor="end" font-size="10" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">smtp · sendgrid</text><circle cx="459" cy="286" r="3" fill="#1d4e89"/><text x="500" y="290" text-anchor="start" font-size="10.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">SMSer</text><text x="740" y="290" text-anchor="end" font-size="10" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">twilio · zenvia</text><text x="500" y="318" text-anchor="start" font-size="9.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">internal/adapter/<tecnologia></text><text x="500" y="332" text-anchor="start" font-size="10" font-weight="400" fill="#5d6b7d">um pacote por fornecedor</text><rect x="20" y="364" width="720" height="34" fill="#fff" stroke="currentColor" stroke-dasharray="5 4"/><text x="30" y="385" text-anchor="start" font-size="11" font-weight="600" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">internal/app</text><text x="122" y="385" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">a raiz de composição: o único lugar que conhece as duas pontas — a configuração escolhe o adapter de cada port</text><text x="20" y="420" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">Esquerda: adapters primários chegam ao domínio via gRPC. Direita: os adapters de cada port. Ponto azul: um port na borda do hexágono.</text></svg><figcaption>As três regiões do dop-core. O domínio declara os ports; os adapters os implementam, uma tecnologia por pacote; a raiz de composição os liga por configuração. As duas famílias à direita têm ciclos de vida opostos.</figcaption></figure>

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

<figure class="diagram"><svg viewBox="0 0 760 318" role="img" aria-label="A suíte de contrato do SecretStore se abre em três adapters, memória sempre, k8s quando um cluster responde, GCP atrás de uma build tag; abaixo, duas setas cortadas mostram que o domínio não pode importar adapters e os SDKs dos adapters não chegam ao domínio." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker><marker id="arrow-accent" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1d4e89"/></marker></defs><rect x="20" y="40" width="190" height="70" fill="#eef2f7" stroke="currentColor" stroke-width="1"/><text x="115.0" y="72.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">SecretStoreSuite</text><text x="115.0" y="87.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">as seis garantias numeradas</text><text x="115" y="124" text-anchor="middle" font-size="9.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">test/contract/secretstore.go</text><rect x="300" y="30" width="150" height="38" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="375.0" y="46.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">memory</text><text x="375.0" y="61.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">go test ./...</text><line x1="212" y1="75" x2="298" y2="49" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><text x="460" y="53" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">sempre</text><rect x="300" y="76" width="150" height="38" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="375.0" y="92.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">k8s</text><text x="375.0" y="107.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">-run SecretStore</text><line x1="212" y1="75" x2="298" y2="95" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><text x="460" y="99" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">quando um cluster responde</text><rect x="300" y="122" width="150" height="38" fill="#fff" stroke="currentColor" stroke-width="1" stroke-dasharray="5 4"/><text x="375.0" y="138.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">gcp</text><text x="375.0" y="153.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">-tags=integration</text><line x1="212" y1="75" x2="298" y2="141" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><text x="460" y="145" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">quando existe credencial (emulador ou GCP real)</text><text x="300" y="172" text-anchor="start" font-size="10.5" font-weight="400" fill="#1d4e89">uma função, três alvos: substituibilidade de fato, não de intenção</text><line x1="20" y1="192" x2="740" y2="192" stroke="#c9d3e0" stroke-dasharray="3 4"/><text x="20" y="214" text-anchor="start" font-size="11" font-weight="600" fill="currentColor">dois testes guardam a fronteira em todo go test ./...</text><rect x="20" y="226" width="150" height="40" fill="#eef2f7" stroke="currentColor" stroke-width="1"/><text x="95.0" y="243.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">internal/domain</text><text x="95.0" y="258.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d">declara os ports</text><rect x="320" y="226" width="150" height="40" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="395.0" y="243.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">internal/adapter</text><text x="395.0" y="258.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d">os implementa</text><rect x="590" y="226" width="150" height="40" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="665.0" y="243.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">vendor SDKs</text><text x="665.0" y="258.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">pgx · nats · gcp · k8s</text><line x1="172" y1="246" x2="318" y2="246" stroke="#1d4e89" stroke-width="1.2" stroke-dasharray="5 4" marker-end="url(#arrow-accent)"/><text x="245" y="240" text-anchor="middle" font-size="14" font-weight="700" fill="#1d4e89">✕</text><line x1="472" y1="246" x2="588" y2="246" stroke="#1d4e89" stroke-width="1.2" stroke-dasharray="5 4" marker-end="url(#arrow-accent)"/><text x="530" y="240" text-anchor="middle" font-size="14" font-weight="700" fill="#1d4e89">✕</text><text x="20" y="290" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">TestTheDomainDoesNotImportInfrastructure: nenhum arquivo sob internal/domain importa um adapter ou SDK de fornecedor.</text><text x="20" y="305" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">TestOnlyAppKnowsTheAdapters: fora de internal/app, nada importa internal/adapter.</text></svg><figcaption>O que mantém o padrão verdadeiro ao longo do tempo: uma suíte de contrato que todo adapter passa, e dois testes de import que quebram o build quando a fronteira é cruzada.</figcaption></figure>

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

<figure class="diagram"><svg viewBox="0 0 760 396" role="img" aria-label="Duas raias para SecretStore.Put: o adapter em memória escreve num map e retorna; o adapter GCP cria uma versão, confirma por número, espera o alias latest com backoff, destrói versões antigas e retorna, ou recusa com KindUnavailable passado o teto." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker><marker id="arrow-accent" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1d4e89"/></marker></defs><rect x="20" y="20" width="200" height="46" fill="#eef2f7" stroke="currentColor" stroke-width="1"/><text x="120.0" y="40.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">SecretStore.Put</text><text x="120.0" y="55.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">promessa: read-after-write</text><text x="20" y="100" text-anchor="start" font-size="11" font-weight="600" fill="currentColor">adapter em memória</text><rect x="20" y="110" width="130" height="40" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="85.0" y="134.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">map[key] = copy</text><line x1="152" y1="130" x2="188" y2="130" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><rect x="190" y="110" width="90" height="40" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="235.0" y="134.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">return nil</text><text x="300" y="134" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">aqui a promessa é de graça</text><line x1="20" y1="168" x2="740" y2="168" stroke="#c9d3e0" stroke-dasharray="3 4"/><text x="20" y="192" text-anchor="start" font-size="11" font-weight="600" fill="currentColor">adapter GCP Secret Manager</text><rect x="20" y="204" width="130" height="48" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="85.0" y="225.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">AddSecretVersion</text><text x="85.0" y="240.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d">versão n criada</text><line x1="152" y1="228" x2="168" y2="228" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><rect x="170" y="204" width="130" height="48" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="235.0" y="225.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">confirm v=n</text><text x="235.0" y="240.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d">por número: forte</text><line x1="302" y1="228" x2="318" y2="228" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><rect x="320" y="204" width="130" height="48" fill="#fff" stroke="#1d4e89" stroke-width="1"/><text x="385.0" y="225.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">await latest ≥ n</text><text x="385.0" y="240.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d">alias: eventual</text><line x1="452" y1="228" x2="468" y2="228" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><rect x="470" y="204" width="130" height="48" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="535.0" y="225.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">destroyOlder</text><text x="535.0" y="240.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d">material antigo destruído</text><line x1="602" y1="228" x2="618" y2="228" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><rect x="620" y="204" width="120" height="48" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="680.0" y="232.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">return nil</text><polyline points="340,254 340,272 326,272 326,256" fill="none" stroke="#1d4e89" stroke-width="1.2" marker-end="url(#arrow-accent)"/><text x="350" y="276" text-anchor="start" font-size="9.5" font-weight="400" fill="#1d4e89" font-family="IBM Plex Mono, ui-monospace, monospace">retry · backoff 25 ms → 1 s · ≤ SECRET_PROPAGATION_SECONDS</text><polyline points="430,254 430,298" fill="none" stroke="#1d4e89" stroke-width="1.2" stroke-dasharray="5 4" marker-end="url(#arrow-accent)"/><rect x="355" y="300" width="150" height="40" fill="#fff" stroke="#1d4e89" stroke-width="1"/><text x="430.0" y="317.0" text-anchor="middle" font-size="12" font-weight="600" fill="#1d4e89">KindUnavailable</text><text x="430.0" y="332.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d">passado o teto</text><text x="515" y="316" text-anchor="start" font-size="9.5" font-weight="400" fill="#5d6b7d">escrita aceita, read-after-write não confirmado:</text><text x="515" y="330" text-anchor="start" font-size="9.5" font-weight="400" fill="#5d6b7d">um erro que alguém lê, não um Get dizendo "não existe".</text><text x="20" y="384" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">Azul: o passo que só existe porque o alias do fornecedor é eventualmente consistente. Tracejado: a saída quando não converge.</text></svg><figcaption>O mesmo Put por dois adapters. Em memória a promessa não custa nada; no Secret Manager o adapter confirma por número de versão, espera o alias e recusa em vez de mentir.</figcaption></figure>

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

<figure class="diagram"><svg viewBox="0 0 760 278" role="img" aria-label="O domínio de entrega chama For com conta e repo; dentro da raiz de composição o repositório dá a integração, a integração dá o provedor, o cofre dá o token; um adapter GitHub ou GitLab é devolvido por chamada." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker><marker id="arrow-accent" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1d4e89"/></marker></defs><rect x="20" y="60" width="170" height="60" fill="#eef2f7" stroke="currentColor" stroke-width="1"/><text x="105.0" y="87.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">domain/delivery</text><text x="105.0" y="102.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">PRs · rebase · merge</text><line x1="192" y1="90" x2="208" y2="90" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><text x="105" y="138" text-anchor="middle" font-size="10" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">→ For(account, repo)</text><rect x="210" y="20" width="330" height="150" fill="#fff" stroke="currentColor" stroke-dasharray="5 4"/><text x="220" y="38" text-anchor="start" font-size="11" font-weight="600" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">internal/app · gitProviders.For</text><rect x="224" y="52" width="92" height="40" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="270.0" y="69.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">1 · repo</text><text x="270.0" y="84.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d">→ id da integração</text><line x1="318" y1="72" x2="336" y2="72" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><rect x="338" y="52" width="92" height="40" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="384.0" y="69.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">2 · integration</text><text x="384.0" y="84.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d">→ provedor</text><line x1="432" y1="72" x2="450" y2="72" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><rect x="452" y="52" width="78" height="40" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="491.0" y="69.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">3 · vault</text><text x="491.0" y="84.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d">→ token</text><text x="360" y="122" text-anchor="middle" font-size="10" font-weight="400" fill="#1d4e89">resolvido a CADA requisição: dois hosts, os dois funcionam</text><text x="360" y="152" text-anchor="middle" font-size="10" font-weight="400" fill="#5d6b7d">provedor desconhecido → recusa, nunca um default</text><rect x="590" y="36" width="150" height="44" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="665.0" y="55.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">gitprovider.GitHub</text><text x="665.0" y="70.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d">REST + GraphQL, merge queue</text><rect x="590" y="100" width="150" height="44" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="665.0" y="119.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">gitprovider.GitLab</text><text x="665.0" y="134.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d">REST, merge trains</text><line x1="542" y1="72" x2="588" y2="58" stroke="#1d4e89" stroke-width="1.2" marker-end="url(#arrow-accent)"/><line x1="542" y1="100" x2="588" y2="122" stroke="#1d4e89" stroke-width="1.2" marker-end="url(#arrow-accent)"/><rect x="414" y="200" width="150" height="40" fill="#eef2f7" stroke="currentColor" stroke-width="1"/><text x="489.0" y="217.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">ports.SecretStore</text><text x="489.0" y="232.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">lido AQUI, no core</text><polyline points="522,94 522,198" fill="none" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><text x="528" y="150" text-anchor="start" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">Get(ref)</text><text x="20" y="200" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">o domínio de entrega nunca fica sabendo que o GitHub existe;</text><text x="20" y="216" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">o adapter git nunca fica sabendo que existe um cofre;</text><text x="20" y="232" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">o domínio de recursos nunca fica sabendo que PRs existem.</text><text x="20" y="266" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">Azul: o adapter escolhido para esta chamada. O cofre é lido na raiz de composição e o token é entregue pronto.</text></svg><figcaption>Um port por requisição. O domínio de entrega pede um provedor por repositório; a raiz de composição resolve integração e credencial e devolve um adapter pronto.</figcaption></figure>

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
