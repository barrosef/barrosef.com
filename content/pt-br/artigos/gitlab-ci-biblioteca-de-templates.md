---
title: "GitLab CI para Kubernetes: uma biblioteca de templates, muitas apps, muitos clusters"
date: 2026-09-17T09:00:00-04:00
draft: false
translationKey: "gitlab-ci-template-library"
categories: ["Tecnologia"]
tags: ["gitlab-ci", "kubernetes", "devops", "entrega"]
description: "Uma arquitetura de pipelines que sobreviveu a várias apps, dois ambientes e mais de um cluster: uma biblioteca de templates versionada, pipelines de aplicação finos, um repositório de manifests que é o único a falar com o Kubernetes, e produção como promoção em vez de rebuild."
---

Três aplicações, cada uma com três ou quatro partes implantáveis. Dois
ambientes. Mais de um cluster Kubernetes, operados por times diferentes. A
primeira versão dessa entrega foi o que sempre é: um `.gitlab-ci.yml` copiado
do projeto anterior, editado até ficar verde, e nunca igual duas vezes. Um ano
depois, dois pipelines não concordavam sobre o que uma branch significava, e
uma correção em um nunca chegava aos outros.

O que segue é a arquitetura que substituiu isso. Nomes, caminhos e números são
ilustrativos; a forma é o que importa.

## A forma

<figure class="diagram"><svg viewBox="0 0 760 432" role="img" aria-label="Repositórios de aplicação incluem uma biblioteca de templates; o pipeline da aplicação constrói, publica no registry e dispara o pipeline do manifests, que aplica manifests, troca imagens e espera o rollout em cada cluster." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker><marker id="arrow-accent" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1d4e89"/></marker></defs><rect x="290" y="16" width="180" height="52" fill="#eef2f7" stroke="currentColor" stroke-width="1"/><text x="380.0" y="39.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">ci-templates</text><text x="380.0" y="54.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">templates/&lt;app&gt;/*.yml</text><text x="482" y="46" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">uma biblioteca: não roda pipeline próprio</text><rect x="20" y="104" width="110" height="52" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="75.0" y="127.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">orders</text><text x="75.0" y="142.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">.gitlab-ci.yml</text><line x1="75" y1="102" x2="330" y2="70" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 4" marker-end="url(#arrow)"/><rect x="150" y="104" width="110" height="52" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="205.0" y="127.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">billing</text><text x="205.0" y="142.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">.gitlab-ci.yml</text><line x1="205" y1="102" x2="370" y2="70" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 4" marker-end="url(#arrow)"/><rect x="280" y="104" width="110" height="52" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="335.0" y="127.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">catalog</text><text x="335.0" y="142.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">.gitlab-ci.yml</text><line x1="335" y1="102" x2="410" y2="70" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 4" marker-end="url(#arrow)"/><text x="408" y="98" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">include · ref: v2.3.0</text><text x="402" y="134" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">repositórios de aplicação — cada pipeline é um include fino</text><rect x="20" y="196" width="370" height="70" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="30" y="212" text-anchor="start" font-size="11" font-weight="600" fill="currentColor">pipeline do orders (push em release / main)</text><rect x="30" y="226" width="80" height="28" fill="#eef2f7" stroke="#c9d3e0"/><text x="70.0" y="244" text-anchor="middle" font-size="11" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">build</text><line x1="111" y1="240" x2="121" y2="240" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><rect x="122" y="226" width="80" height="28" fill="#eef2f7" stroke="#c9d3e0"/><text x="162.0" y="244" text-anchor="middle" font-size="11" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">promote</text><line x1="203" y1="240" x2="213" y2="240" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><rect x="214" y="226" width="80" height="28" fill="#eef2f7" stroke="#c9d3e0"/><text x="254.0" y="244" text-anchor="middle" font-size="11" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">deploy</text><line x1="295" y1="240" x2="305" y2="240" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><rect x="306" y="226" width="74" height="28" fill="#eef2f7" stroke="#c9d3e0"/><text x="343.0" y="244" text-anchor="middle" font-size="11" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">notify</text><polyline points="75,158 75,194" fill="none" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><text x="82" y="180" text-anchor="start" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">push</text><rect x="560" y="196" width="180" height="50" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="650.0" y="218.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">registry de imagens</text><text x="650.0" y="233.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">orders/api:&lt;sha&gt;</text><line x1="392" y1="231" x2="558" y2="221" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><text x="475" y="214" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">docker push :sha, :env</text><rect x="20" y="316" width="370" height="70" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="30" y="332" text-anchor="start" font-size="11" font-weight="600" fill="currentColor">pipeline do manifests (só roda quando disparado)</text><rect x="30" y="346" width="74" height="28" fill="#eef2f7" stroke="#c9d3e0"/><text x="67.0" y="364" text-anchor="middle" font-size="11" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">apply</text><line x1="105" y1="360" x2="115" y2="360" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><rect x="116" y="346" width="90" height="28" fill="#eef2f7" stroke="#c9d3e0"/><text x="161.0" y="364" text-anchor="middle" font-size="11" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">set image</text><line x1="207" y1="360" x2="217" y2="360" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><rect x="218" y="346" width="110" height="28" fill="#eef2f7" stroke="#c9d3e0"/><text x="273.0" y="364" text-anchor="middle" font-size="11" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">rollout status</text><polyline points="254,254 254,314" fill="none" stroke="#1d4e89" stroke-width="1.2" marker-end="url(#arrow-accent)"/><text x="262" y="282" text-anchor="start" font-size="10.5" fill="#1d4e89" font-family="IBM Plex Mono, ui-monospace, monospace">trigger</text><text x="262" y="296" text-anchor="start" font-size="10" font-weight="400" fill="#1d4e89" font-family="IBM Plex Mono, ui-monospace, monospace">IMAGE_MATRIX, strategy: depend</text><rect x="560" y="306" width="180" height="40" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="650.0" y="323.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">north</text><text x="650.0" y="338.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">cluster · namespace por ambiente</text><rect x="560" y="362" width="180" height="40" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="650.0" y="379.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">south</text><text x="650.0" y="394.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">cluster · namespace por ambiente</text><line x1="392" y1="350" x2="558" y2="326" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><text x="470" y="330" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">kubectl -n <ns></text><line x1="392" y1="362" x2="558" y2="382" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><polyline points="650,248 650,304" fill="none" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><text x="658" y="280" text-anchor="start" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">pull</text><text x="20" y="420" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">Tracejado: uma referência resolvida na criação do pipeline, não uma execução. Azul: a passagem de bastão entre os dois pipelines.</text></svg><figcaption>Três tipos de repositório, dois pipelines. Os repositórios de aplicação incluem a biblioteca; o pipeline deles constrói e entrega um mapa de imagens ao pipeline do manifests, que é o único que fala com os clusters.</figcaption></figure>

Há três tipos de repositório e só dois pipelines:

| Repositório | Guarda | Seu pipeline |
|---|---|---|
| `platform/ci-templates` | A biblioteca: uma pasta por app, quatro arquivos YAML cada | Nenhum. Ele só é `include`d |
| `orders`, `billing`, … | O código da aplicação e um `.gitlab-ci.yml` de uma dúzia de linhas | Constrói imagens, promove, dispara o pipeline do manifests, notifica |
| `platform/manifests` | Manifests do Kubernetes, `<cluster>/<app>/<env>/` | Só roda quando disparado. Aplica, troca imagens, espera o rollout |

Nada no repositório de uma aplicação sabe chegar a um cluster. Nada no
repositório de manifests sabe construir. A passagem de bastão entre os dois é
uma única variável JSON, e essa fronteira é o que mantém os dois lados
simples.

## O consumidor: uma dúzia de linhas

{{< snippet file="gitlab-ci-template-library/orders.gitlab-ci.yml" lang="yaml" >}}

O `ref` é uma tag. `main` serve para experimentar uma mudança em uma app antes
de cortar a `v2.4.0` e migrar as outras. A lista de arquivos é explícita de
propósito: **os nomes são um contrato**. Adicionar um quinto arquivo significa
que cada consumidor acrescenta uma linha; renomear um significa que cada
consumidor quebra — então arquivos são adicionados, nunca renomeados.

As flags `ENABLE_*` são como uma parte nova, ou uma versão nova do pipeline,
entra uma peça de cada vez. Uma parte com a flag desligada não tem job nenhum,
não um job pulado.

## De quatro arquivos a um pipeline

<figure class="diagram"><svg viewBox="0 0 760 362" role="img" aria-label="Quatro arquivos de template, incluídos por um arquivo curto do consumidor, expandem para um pipeline com três jobs de build, dois de trigger e um de notificação." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker><marker id="arrow-accent" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1d4e89"/></marker></defs><text x="20" y="20" text-anchor="start" font-size="11" font-weight="600" fill="currentColor">a biblioteca (templates/orders/)</text><rect x="20" y="30" width="180" height="52" fill="#eef2f7" stroke="currentColor" stroke-width="1"/><text x="110.0" y="53.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">workflow.yml</text><text x="110.0" y="68.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">stages · branch→env · retry</text><rect x="20" y="110" width="180" height="52" fill="#eef2f7" stroke="currentColor" stroke-width="1"/><text x="110.0" y="133.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">build.yml</text><text x="110.0" y="148.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">job oculto .build</text><rect x="20" y="190" width="180" height="52" fill="#eef2f7" stroke="currentColor" stroke-width="1"/><text x="110.0" y="213.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">deploy.yml</text><text x="110.0" y="228.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">job oculto .trigger</text><rect x="20" y="270" width="180" height="52" fill="#eef2f7" stroke="currentColor" stroke-width="1"/><text x="110.0" y="293.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">notify.yml</text><text x="110.0" y="308.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">notifica falha / sucesso</text><text x="250" y="20" text-anchor="start" font-size="11" font-weight="600" fill="currentColor">o consumidor</text><rect x="250" y="30" width="150" height="292" fill="#fff" stroke="currentColor"/><text x="325" y="52" text-anchor="middle" font-size="11" font-weight="600" fill="currentColor">orders/.gitlab-ci.yml</text><text x="262" y="78" text-anchor="start" font-size="9.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">include:</text><text x="262" y="93" text-anchor="start" font-size="9.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">  project: ci-templates</text><text x="262" y="108" text-anchor="start" font-size="9.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">  ref: v2.3.0</text><text x="262" y="123" text-anchor="start" font-size="9.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">  file:</text><text x="262" y="138" text-anchor="start" font-size="9.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">    - workflow.yml</text><text x="262" y="153" text-anchor="start" font-size="9.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">    - build.yml</text><text x="262" y="168" text-anchor="start" font-size="9.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">    - deploy.yml</text><text x="262" y="183" text-anchor="start" font-size="9.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">    - notify.yml</text><text x="262" y="198" text-anchor="start" font-size="9.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">variables:</text><text x="262" y="213" text-anchor="start" font-size="9.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">  ENABLE_WORKER: &quot;true&quot;</text><text x="325" y="250" text-anchor="middle" font-size="10" font-weight="400" fill="#5d6b7d">quatro linhas de include,</text><text x="325" y="265" text-anchor="middle" font-size="10" font-weight="400" fill="#5d6b7d">um bloco de variáveis —</text><text x="325" y="296" text-anchor="middle" font-size="10" font-weight="400" fill="#1d4e89">nada mais.</text><line x1="202" y1="56" x2="248" y2="60" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 4" marker-end="url(#arrow)"/><line x1="202" y1="136" x2="248" y2="136" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 4" marker-end="url(#arrow)"/><line x1="202" y1="216" x2="248" y2="216" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 4" marker-end="url(#arrow)"/><line x1="202" y1="296" x2="248" y2="296" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 4" marker-end="url(#arrow)"/><text x="225" y="48" text-anchor="middle" font-size="10" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">include</text><text x="470" y="20" text-anchor="start" font-size="11" font-weight="600" fill="currentColor">o pipeline que se materializa</text><rect x="470" y="30" width="270" height="52" fill="#fff" stroke="#c9d3e0"/><text x="480" y="48" text-anchor="start" font-size="10" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">stages: build · promote · deploy · notify</text><text x="480" y="64" text-anchor="start" font-size="10" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">release → TARGET_ENV=staging</text><text x="480" y="77" text-anchor="start" font-size="10" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">main    → TARGET_ENV=production</text><rect x="470" y="110" width="86" height="52" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="513.0" y="133.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">build_api</text><text x="513.0" y="148.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">PART=api</text><rect x="562" y="110" width="86" height="52" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="605.0" y="133.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">build_web</text><text x="605.0" y="148.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">PART=web</text><rect x="654" y="110" width="86" height="52" fill="#fff" stroke="currentColor" stroke-width="1" stroke-dasharray="5 4"/><text x="697.0" y="133.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">build_worker</text><text x="697.0" y="148.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">PART=worker</text><text x="740" y="176" text-anchor="end" font-size="10" font-weight="400" fill="#5d6b7d">paralelos; worker só com ENABLE_WORKER</text><rect x="470" y="190" width="130" height="52" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="535.0" y="213.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">deploy_north</text><text x="535.0" y="228.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">CLUSTER=north</text><rect x="610" y="190" width="130" height="52" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="675.0" y="213.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">deploy_south</text><text x="675.0" y="228.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">CLUSTER=south</text><text x="740" y="256" text-anchor="end" font-size="10" font-weight="400" fill="#5d6b7d">um trigger por cluster</text><rect x="470" y="270" width="130" height="52" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="535.0" y="293.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">notify_failure</text><text x="535.0" y="308.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">when: on_failure</text><line x1="402" y1="56" x2="468" y2="56" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><text x="435" y="48" text-anchor="middle" font-size="10.5" fill="#5d6b7d">vira</text><line x1="402" y1="136" x2="468" y2="136" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><line x1="402" y1="216" x2="468" y2="216" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><line x1="402" y1="296" x2="468" y2="296" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><text x="435" y="128" text-anchor="middle" font-size="9.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">× 3 partes</text><text x="435" y="208" text-anchor="middle" font-size="9.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">× 2 clusters</text><text x="20" y="350" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">Tracejado: um arquivo trazido pelo include. Job tracejado: criado só quando a flag está ligada.</text></svg><figcaption>Como quatro arquivos de template viram um pipeline concreto. Os jobs ocultos da biblioteca são estendidos em um job por parte e um por cluster; o arquivo do consumidor só lista includes e flags.</figcaption></figure>

### workflow.yml: o que uma branch significa

{{< snippet file="gitlab-ci-template-library/workflow.yml" lang="yaml" >}}

Três decisões moram aqui e em nenhum outro lugar. **Uma branch mapeia para
exatamente um ambiente**, e uma branch que não mapeia para nada não cria
pipeline — o `when: never` no fim não é decoração. **Retries cobrem
infraestrutura, não código**: acrescentar `script_failure` reexecutaria um
build genuinamente quebrado três vezes e esconderia o defeito atrás de um
selo verde na quarta. E **helpers de shell são compartilhados com
`!reference`**, então o retry com backoff e a checagem de existência em três
estados são escritos uma vez. Esse terceiro estado importa: uma oscilação de
rede durante um `kubectl get` era indistinguível de "não existe", e o job
seguia feliz com a premissa errada. Não conseguir saber é uma resposta em si,
e quem chama aborta nela.

### build.yml: um job oculto, um job concreto por parte

{{< snippet file="gitlab-ci-template-library/build.yml" lang="yaml" >}}

O job base faz o trabalho; cada job concreto são três variáveis. Rodam em
paralelo, já que nada em `build_web` depende de `build_api`. Toda imagem é
publicada duas vezes: como `:<sha>`, que é o que será implantado e nunca se
move, e como `:staging`, um ponteiro flutuante para "o que staging roda
agora" que o passo de promoção vai ler.

### deploy.yml: a passagem de bastão

{{< snippet file="gitlab-ci-template-library/deploy.yml" lang="yaml" >}}

`strategy: depend` faz o pai esperar o filho e falhar se ele falhar — o selo
do pipeline da aplicação diz a verdade sobre o deploy, não só sobre o build.
Um job de trigger por cluster é toda a história de multi-cluster: mesmo
repositório de manifests, mesmas variáveis, `CLUSTER` diferente.

`IMAGE_MATRIX` é o contrato através da fronteira: qual parte, qual nome de
container dentro do pod, qual imagem. O lado dos manifests não precisa de mais
nada para atualizar um deployment.

## Produção é promoção, não rebuild

<figure class="diagram"><svg viewBox="0 0 760 274" role="img" aria-label="Duas raias: a branch release constrói, publica e faz rollout em staging; a branch main pula o build, re-etiqueta o digest de staging como produção e faz o rollout dele." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker><marker id="arrow-accent" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1d4e89"/></marker></defs><text x="20" y="40" text-anchor="start" font-size="11" font-weight="600" fill="currentColor">branch release → staging</text><text x="20" y="170" text-anchor="start" font-size="11" font-weight="600" fill="currentColor">branch main → produção</text><line x1="20" y1="126" x2="740" y2="126" stroke="#c9d3e0" stroke-dasharray="3 4"/><rect x="60" y="50" width="140" height="50" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="130.0" y="72.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">build</text><text x="130.0" y="87.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">3 parts</text><line x1="202" y1="75" x2="228" y2="75" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><rect x="230" y="50" width="140" height="50" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="300.0" y="72.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">push</text><text x="300.0" y="87.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">:&lt;sha&gt; · :staging</text><line x1="372" y1="75" x2="398" y2="75" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><rect x="400" y="50" width="140" height="50" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="470.0" y="72.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">trigger</text><text x="470.0" y="87.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">matrix :&lt;sha&gt;</text><line x1="542" y1="75" x2="568" y2="75" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><rect x="570" y="50" width="140" height="50" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="640.0" y="72.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">rollout</text><text x="640.0" y="87.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">staging</text><rect x="60" y="180" width="140" height="50" fill="#fff" stroke="currentColor" stroke-width="1" stroke-dasharray="5 4"/><text x="130.0" y="202.0" text-anchor="middle" font-size="12" font-weight="400" fill="#5d6b7d">sem build</text><text x="130.0" y="217.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">estágio pulado</text><rect x="230" y="180" width="140" height="50" fill="#fff" stroke="#1d4e89" stroke-width="1"/><text x="300.0" y="202.0" text-anchor="middle" font-size="12" font-weight="600" fill="#1d4e89">promote</text><text x="300.0" y="217.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">crane tag</text><rect x="400" y="180" width="140" height="50" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="470.0" y="202.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">trigger</text><text x="470.0" y="217.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">matrix @digest</text><rect x="570" y="180" width="140" height="50" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="640.0" y="202.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">rollout</text><text x="640.0" y="217.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">production</text><line x1="202" y1="205" x2="228" y2="205" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 4" marker-end="url(#arrow)"/><line x1="372" y1="205" x2="398" y2="205" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><line x1="542" y1="205" x2="568" y2="205" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><polyline points="300.0,102 300.0,178" fill="none" stroke="#1d4e89" stroke-width="1.2" marker-end="url(#arrow-accent)"/><text x="308.0" y="144" text-anchor="start" font-size="10.5" fill="#1d4e89" font-family="IBM Plex Mono, ui-monospace, monospace">mesmo digest</text><text x="308.0" y="158" text-anchor="start" font-size="10" font-weight="400" fill="#1d4e89" font-family="IBM Plex Mono, ui-monospace, monospace">:staging → :production</text><text x="20" y="262" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">Produção nunca constrói. Ela promove a imagem que já rodou em staging, por digest, e faz o rollout dela.</text></svg><figcaption>Staging constrói; produção promove. A branch main re-etiqueta o digest de staging e o implanta — os bytes que passaram por staging são os bytes em produção.</figcaption></figure>

{{< snippet file="gitlab-ci-template-library/promote.yml" lang="yaml" >}}

A branch `main` pula o estágio de build inteiro. Reconstruir do mesmo commit
*provavelmente* produziria a mesma imagem; promover por digest produz a mesma
imagem por definição. O relatório dotenv é como os digests chegam aos jobs de
trigger — o GitLab expande `$API_REF` no `IMAGE_MATRIX` antes de entregar a
variável ao pipeline filho.

## O pipeline do manifests

Os manifests vivem por cluster, por app, por ambiente, com uma pasta
`_shared/` para o ConfigMap e o Secret que toda parte lê:

```text
platform/manifests/
└── north/
    └── orders/
        ├── _shared/
        │   ├── staging/      configmap.yaml  secret.yaml
        │   └── production/
        ├── staging/          namespace.yaml  api.yaml  web.yaml  worker.yaml
        └── production/
```

{{< snippet file="gitlab-ci-template-library/manifests.gitlab-ci.yml" lang="yaml" >}}

Quatro coisas fazem o trabalho de verdade aqui.

**Só roda quando disparado.** Um push no repositório de manifests muda
arquivos e nada mais; o cluster muda quando um pipeline de aplicação manda,
com um mapa de imagens anexado.

**`apply` e `set image` não brigam.** O manifest versionado diz
`image: …/api:staging`; o objeto vivo termina com `…/api@sha256:…`. O próximo
`apply` parece que vai reverter isso — não reverte. O apply client-side só
inclui no patch os campos que mudaram entre o último manifest aplicado e o
novo, e a linha da imagem é idêntica nos dois, então o digest definido pelo
pipeline sobrevive. Quebre essa premissa editando a tag no manifest e você
ganha um segundo rollout por deploy.

**`resource_group` serializa por alvo.** Dois pipelines para a mesma app e
ambiente entram em fila em vez de disputar. A chave do grupo inclui a app para
que `orders` e `billing` no mesmo cluster ainda implantem em paralelo.

**Um rollout que falha se explica.** `describe` e as últimas cem linhas de
log vão para a saída do job antes de ele sair vermelho — quem abre o job às
duas da manhã não deveria precisar de acesso ao cluster para ver o porquê.

## Avisando alguém

{{< snippet file="gitlab-ci-template-library/notify.yml" lang="yaml" >}}

Na falha, sempre: branch, ambiente, autor, commit, um botão. No sucesso, uma
linha do job de deploy com o digest que entrou no ar:

{{< snippet file="gitlab-ci-template-library/notify-success.sh" lang="bash" >}}

A URL do webhook é uma variável de CI/CD mascarada e protegida no projeto
consumidor; um projeto sem ela apenas registra que pulou a notificação.

## Onde mora cada configuração

| Configuração | Onde | Por que ali |
|---|---|---|
| Branch → ambiente | `workflow.yml` na biblioteca | Uma verdade para todas as apps |
| Credenciais do registry | As `CI_REGISTRY_*` do próprio GitLab | Nunca digitadas em lugar nenhum |
| Kubeconfig por cluster | Variável do tipo arquivo em `platform/manifests`, protegida | Só o pipeline do manifests alcança um cluster |
| `SLACK_WEBHOOK_URL` | Variável mascarada em cada consumidor | Cada app é dona do seu canal |
| `ENABLE_<PARTE>` | `variables:` no arquivo do consumidor | Visível no diff que liga a parte |
| Versão da biblioteca | `ref:` no `include` do consumidor | Atualização é um commit revisado, não uma surpresa |

## O que nos mordeu, para não morder você

| Sintoma | Causa | Regra |
|---|---|---|
| Deploy verde, imagem inalterada | Parte nova adicionada em `build.yml` e no `IMAGE_MATRIX`, mas o manifest não tem o label `part:`, então `set image -l` não achou nada | Adicionar uma parte toca **três** lugares: job de build, entrada no matrix, label no manifest |
| Cinco partes implantando uma após a outra | `resource_group` sem a parte ou a app na chave | A chave nomeia exatamente o que não pode se sobrepor |
| Comando falhou, sem erro, job continua | `OUT=$(cmd 2>&1)` sob `set -e`: a atribuição engole o status de saída | Use o comando como condição de um `if`, capture a saída dentro |
| Build instável "consertado" pelo retry | `script_failure` em `default.retry` | Retry para infraestrutura, nunca para código |
| Um passo pulado porque um Deployment "não existia" — existia | Oscilação de rede indistinguível de `NotFound` | Três estados, abortar no terceiro |
| Clone de um repo de 30 MB para rodar `kubectl apply` | `GIT_STRATEGY` padrão num job que nunca lê a árvore | `GIT_STRATEGY: none` quando a árvore de trabalho não é necessária |

Nada disso é GitLab exótico. É `include`, jobs ocultos, `workflow.rules`, um
trigger multi-projeto e uma variável JSON — arranjados para que adicionar a
quarta app seja uma pasta na biblioteca e uma dúzia de linhas na app, e para
que produção só rode bytes que staging já rodou.
