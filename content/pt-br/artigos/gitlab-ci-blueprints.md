---
title: "GitLab CI para Kubernetes: uma biblioteca de blueprints para muitas apps e muitos clusters"
date: 2026-09-17T09:00:00-04:00
draft: false
translationKey: "gitlab-ci-blueprints"
categories: ["Tecnologia"]
tags: ["gitlab-ci", "kubernetes", "devops", "entrega"]
description: "Uma arquitetura de entrega que sobreviveu a várias apps, dois anéis e mais de um cluster: uma biblioteca de blueprints versionada, pipelines de aplicação finos, um repositório de frota que é o único a falar com o Kubernetes, e um anel live que libera o que o preview já rodou em vez de construir de novo."
aliases: ["/pt-br/artigos/gitlab-ci-biblioteca-de-templates/"]
---

Três aplicações, cada uma com três ou quatro unidades implantáveis. Dois
anéis — preview e live. Mais de um cluster Kubernetes, operados por times
diferentes. A primeira versão dessa entrega foi o que sempre é: um
`.gitlab-ci.yml` copiado do projeto anterior, editado até ficar verde, e nunca
igual duas vezes. Um ano depois, dois pipelines não concordavam sobre o que
uma branch significava, e uma correção em um nunca chegava aos outros.

O que segue é a arquitetura que substituiu isso. Nomes, caminhos e números são
ilustrativos; a forma é o que importa.

## A forma

<figure class="diagram"><svg viewBox="0 0 760 432" role="img" aria-label="Repositórios de aplicação incluem uma biblioteca de blueprints; o pipeline da aplicação assa as imagens, publica no registry e dispara o pipeline do fleet, que aplica manifests, troca imagens e espera o rollout em cada cluster." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker><marker id="arrow-accent" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1d4e89"/></marker></defs><rect x="290" y="16" width="180" height="52" fill="#eef2f7" stroke="currentColor" stroke-width="1"/><text x="380.0" y="39.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">ci-blueprints</text><text x="380.0" y="54.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">blueprints/&lt;app&gt;/*.yml</text><text x="482" y="46" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">uma biblioteca: não roda pipeline próprio</text><rect x="20" y="104" width="110" height="52" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="75.0" y="127.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">orders</text><text x="75.0" y="142.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">.gitlab-ci.yml</text><line x1="75" y1="102" x2="330" y2="70" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 4" marker-end="url(#arrow)"/><rect x="150" y="104" width="110" height="52" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="205.0" y="127.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">billing</text><text x="205.0" y="142.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">.gitlab-ci.yml</text><line x1="205" y1="102" x2="370" y2="70" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 4" marker-end="url(#arrow)"/><rect x="280" y="104" width="110" height="52" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="335.0" y="127.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">catalog</text><text x="335.0" y="142.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">.gitlab-ci.yml</text><line x1="335" y1="102" x2="410" y2="70" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 4" marker-end="url(#arrow)"/><text x="408" y="98" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">include · ref: v2.3.0</text><text x="402" y="134" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">repositórios de aplicação — cada pipeline é um include fino</text><rect x="20" y="196" width="370" height="70" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="30" y="212" text-anchor="start" font-size="11" font-weight="600" fill="currentColor">pipeline do orders (push em candidate / main)</text><rect x="30" y="226" width="80" height="28" fill="#eef2f7" stroke="#c9d3e0"/><text x="70.0" y="244" text-anchor="middle" font-size="11" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">images</text><line x1="111" y1="240" x2="121" y2="240" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><rect x="122" y="226" width="80" height="28" fill="#eef2f7" stroke="#c9d3e0"/><text x="162.0" y="244" text-anchor="middle" font-size="11" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">release</text><line x1="203" y1="240" x2="213" y2="240" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><rect x="214" y="226" width="80" height="28" fill="#eef2f7" stroke="#c9d3e0"/><text x="254.0" y="244" text-anchor="middle" font-size="11" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">delivery</text><line x1="295" y1="240" x2="305" y2="240" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><rect x="306" y="226" width="74" height="28" fill="#eef2f7" stroke="#c9d3e0"/><text x="343.0" y="244" text-anchor="middle" font-size="11" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">alerts</text><polyline points="75,158 75,194" fill="none" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><text x="82" y="180" text-anchor="start" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">push</text><rect x="560" y="196" width="180" height="50" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="650.0" y="218.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">registry de imagens</text><text x="650.0" y="233.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">orders/api:&lt;sha&gt;</text><line x1="392" y1="231" x2="558" y2="221" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><text x="475" y="214" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">docker push :sha, :ring</text><rect x="20" y="316" width="370" height="70" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="30" y="332" text-anchor="start" font-size="11" font-weight="600" fill="currentColor">pipeline do fleet (só roda quando disparado)</text><rect x="30" y="346" width="74" height="28" fill="#eef2f7" stroke="#c9d3e0"/><text x="67.0" y="364" text-anchor="middle" font-size="11" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">apply</text><line x1="105" y1="360" x2="115" y2="360" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><rect x="116" y="346" width="90" height="28" fill="#eef2f7" stroke="#c9d3e0"/><text x="161.0" y="364" text-anchor="middle" font-size="11" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">set image</text><line x1="207" y1="360" x2="217" y2="360" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><rect x="218" y="346" width="110" height="28" fill="#eef2f7" stroke="#c9d3e0"/><text x="273.0" y="364" text-anchor="middle" font-size="11" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">rollout status</text><polyline points="254,254 254,314" fill="none" stroke="#1d4e89" stroke-width="1.2" marker-end="url(#arrow-accent)"/><text x="262" y="282" text-anchor="start" font-size="10.5" fill="#1d4e89" font-family="IBM Plex Mono, ui-monospace, monospace">trigger</text><text x="262" y="296" text-anchor="start" font-size="10" font-weight="400" fill="#1d4e89" font-family="IBM Plex Mono, ui-monospace, monospace">ROLLOUT_SET · strategy: depend</text><rect x="560" y="306" width="180" height="40" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="650.0" y="323.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">north</text><text x="650.0" y="338.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">cluster · namespace por anel</text><rect x="560" y="362" width="180" height="40" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="650.0" y="379.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">south</text><text x="650.0" y="394.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">cluster · namespace por anel</text><line x1="392" y1="350" x2="558" y2="326" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><text x="470" y="330" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">kubectl -n <ns></text><line x1="392" y1="362" x2="558" y2="382" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><polyline points="650,248 650,304" fill="none" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><text x="658" y="280" text-anchor="start" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">pull</text><text x="20" y="420" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">Tracejado: uma referência resolvida na criação do pipeline, não uma execução. Azul: a passagem de bastão entre os dois pipelines.</text></svg><figcaption>Três tipos de repositório, dois pipelines. Os repositórios de aplicação incluem a biblioteca de blueprints; o pipeline deles assa as imagens e entrega um conjunto de rollout ao pipeline do fleet, que é o único que fala com os clusters.</figcaption></figure>

Há três tipos de repositório e só dois pipelines:

| Repositório | Guarda | Seu pipeline |
|---|---|---|
| `platform/ci-blueprints` | A biblioteca: uma pasta por app, cinco arquivos YAML cada | Nenhum. Ele só é `include`d |
| `orders`, `billing`, … | O código da aplicação e um `.gitlab-ci.yml` de uma dúzia de linhas | Assa imagens, libera, passa o bastão ao pipeline da frota, alerta |
| `platform/fleet` | Manifests do Kubernetes, `<cluster>/<app>/<anel>/` | Só roda quando disparado. Aplica, troca imagens, espera o rollout |

Nada no repositório de uma aplicação sabe chegar a um cluster. Nada no
repositório da frota sabe assar uma imagem. A passagem de bastão entre os
dois é uma única variável JSON, e essa fronteira é o que mantém os dois lados
simples.

## O consumidor: uma dúzia de linhas

{{< snippet file="gitlab-ci-blueprints/orders.gitlab-ci.yml" lang="yaml" >}}

O `ref` é uma tag. `main` serve para experimentar uma mudança em uma app antes
de cortar a `v2.4.0` e migrar as outras. A lista de arquivos é explícita de
propósito: **os nomes são um contrato**. Adicionar um sexto arquivo significa
que cada consumidor acrescenta uma linha; renomear um significa que cada
consumidor quebra — então arquivos são adicionados, nunca renomeados.

As flags `SHIP_*` são como uma unidade nova, ou uma versão nova da biblioteca,
entra uma peça de cada vez. Uma unidade com a flag desligada não tem job
nenhum, não um job pulado.

## De cinco arquivos a um pipeline

<figure class="diagram"><svg viewBox="0 0 760 374" role="img" aria-label="Cinco arquivos de blueprint, incluídos por um arquivo curto do consumidor, expandem para um pipeline com três jobs de bake, um de release, dois de entrega e um de alerta." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker><marker id="arrow-accent" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1d4e89"/></marker></defs><text x="20" y="20" text-anchor="start" font-size="11" font-weight="600" fill="currentColor">a biblioteca (blueprints/orders/)</text><rect x="20" y="30" width="180" height="48" fill="#eef2f7" stroke="currentColor" stroke-width="1"/><text x="110.0" y="51.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">routine.yml</text><text x="110.0" y="66.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">stages · branch→anel · retry</text><rect x="20" y="94" width="180" height="48" fill="#eef2f7" stroke="currentColor" stroke-width="1"/><text x="110.0" y="115.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">images.yml</text><text x="110.0" y="130.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">job oculto .bake</text><rect x="20" y="158" width="180" height="48" fill="#eef2f7" stroke="currentColor" stroke-width="1"/><text x="110.0" y="179.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">release.yml</text><text x="110.0" y="194.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">digest, re-tag na main</text><rect x="20" y="222" width="180" height="48" fill="#eef2f7" stroke="currentColor" stroke-width="1"/><text x="110.0" y="243.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">delivery.yml</text><text x="110.0" y="258.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">job oculto .deliver</text><rect x="20" y="286" width="180" height="48" fill="#eef2f7" stroke="currentColor" stroke-width="1"/><text x="110.0" y="307.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">alerts.yml</text><text x="110.0" y="322.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">alerta falha / sucesso</text><text x="250" y="20" text-anchor="start" font-size="11" font-weight="600" fill="currentColor">o consumidor</text><rect x="250" y="30" width="150" height="304" fill="#fff" stroke="currentColor"/><text x="325" y="52" text-anchor="middle" font-size="11" font-weight="600" fill="currentColor">orders/.gitlab-ci.yml</text><text x="262" y="78" text-anchor="start" font-size="9.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">include:</text><text x="262" y="93" text-anchor="start" font-size="9.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">  project: ci-blueprints</text><text x="262" y="108" text-anchor="start" font-size="9.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">  ref: v2.3.0</text><text x="262" y="123" text-anchor="start" font-size="9.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">  file:</text><text x="262" y="138" text-anchor="start" font-size="9.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">    - routine.yml</text><text x="262" y="153" text-anchor="start" font-size="9.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">    - images.yml</text><text x="262" y="168" text-anchor="start" font-size="9.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">    - release.yml</text><text x="262" y="183" text-anchor="start" font-size="9.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">    - delivery.yml</text><text x="262" y="198" text-anchor="start" font-size="9.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">    - alerts.yml</text><text x="262" y="213" text-anchor="start" font-size="9.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">variables:</text><text x="262" y="228" text-anchor="start" font-size="9.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">  SHIP_WORKER: &quot;true&quot;</text><text x="325" y="268" text-anchor="middle" font-size="10" font-weight="400" fill="#5d6b7d">quatro linhas de include,</text><text x="325" y="283" text-anchor="middle" font-size="10" font-weight="400" fill="#5d6b7d">um bloco de variáveis —</text><text x="325" y="312" text-anchor="middle" font-size="10" font-weight="400" fill="#1d4e89">nada mais.</text><line x1="202" y1="54.0" x2="248" y2="60" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 4" marker-end="url(#arrow)"/><line x1="202" y1="118.0" x2="248" y2="118.0" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 4" marker-end="url(#arrow)"/><line x1="202" y1="182.0" x2="248" y2="182.0" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 4" marker-end="url(#arrow)"/><line x1="202" y1="246.0" x2="248" y2="246.0" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 4" marker-end="url(#arrow)"/><line x1="202" y1="310.0" x2="248" y2="310.0" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 4" marker-end="url(#arrow)"/><text x="225" y="46" text-anchor="middle" font-size="10" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">include</text><text x="470" y="20" text-anchor="start" font-size="11" font-weight="600" fill="currentColor">o pipeline que se materializa</text><rect x="470" y="30" width="270" height="48" fill="#fff" stroke="#c9d3e0"/><text x="480" y="46" text-anchor="start" font-size="10" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">images · release · delivery · alerts</text><text x="480" y="60" text-anchor="start" font-size="10" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">candidate → RING=preview</text><text x="480" y="72" text-anchor="start" font-size="10" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">main      → RING=live</text><rect x="470" y="94" width="86" height="48" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="513.0" y="115.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">bake_api</text><text x="513.0" y="130.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">UNIT=api</text><rect x="562" y="94" width="86" height="48" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="605.0" y="115.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">bake_web</text><text x="605.0" y="130.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">UNIT=web</text><rect x="654" y="94" width="86" height="48" fill="#fff" stroke="currentColor" stroke-width="1" stroke-dasharray="5 4"/><text x="697.0" y="115.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">bake_worker</text><text x="697.0" y="130.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">UNIT=worker</text><text x="740" y="154" text-anchor="end" font-size="10" font-weight="400" fill="#5d6b7d">paralelos; worker só com SHIP_WORKER</text><rect x="470" y="158" width="130" height="48" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="535.0" y="179.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">release</text><text x="535.0" y="194.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">crane · dotenv</text><text x="740" y="186.0" text-anchor="end" font-size="10" font-weight="400" fill="#5d6b7d">um job, todas as unidades</text><rect x="470" y="222" width="130" height="48" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="535.0" y="243.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">deliver_north</text><text x="535.0" y="258.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">CLUSTER=north</text><rect x="610" y="222" width="130" height="48" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="675.0" y="243.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">deliver_south</text><text x="675.0" y="258.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">CLUSTER=south</text><text x="740" y="282" text-anchor="end" font-size="10" font-weight="400" fill="#5d6b7d">um trigger por cluster</text><rect x="470" y="286" width="130" height="48" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="535.0" y="307.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">alert_failure</text><text x="535.0" y="322.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">when: on_failure</text><line x1="402" y1="54.0" x2="468" y2="54.0" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><text x="435" y="46.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d">vira</text><line x1="402" y1="118.0" x2="468" y2="118.0" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><line x1="402" y1="182.0" x2="468" y2="182.0" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><line x1="402" y1="246.0" x2="468" y2="246.0" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><line x1="402" y1="310.0" x2="468" y2="310.0" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><text x="435" y="110.0" text-anchor="middle" font-size="9.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">× 3 unidades</text><text x="435" y="238.0" text-anchor="middle" font-size="9.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">× 2 clusters</text><text x="20" y="362" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">Tracejado: um arquivo trazido pelo include. Job tracejado: criado só quando a flag de envio está ligada.</text></svg><figcaption>Como cinco arquivos de blueprint viram um pipeline concreto. Os jobs ocultos da biblioteca são estendidos em um job por unidade e um por cluster; o arquivo do consumidor só lista includes e flags.</figcaption></figure>

### routine.yml: o que uma branch significa

{{< snippet file="gitlab-ci-blueprints/routine.yml" lang="yaml" >}}

Três decisões moram aqui e em nenhum outro lugar. **Uma branch mapeia para
exatamente um anel**, e uma branch que não mapeia para nada não cria pipeline
— o `when: never` no fim do bloco `workflow:` não é decoração. **Retries
cobrem infraestrutura, não código**: acrescentar `script_failure` reexecutaria
um bake genuinamente quebrado três vezes e esconderia o defeito atrás de um
selo verde na quarta. E **a biblioteca de shell é compartilhada com
`!reference`**, então o retry com backoff e a sonda de três estados são
escritos uma vez. Esse terceiro estado importa: uma oscilação de rede durante
um `kubectl get` era indistinguível de "ausente", e o job seguia com a
premissa errada. Não conseguir saber é uma resposta em si, e quem chama para
nela.

### images.yml: um job oculto, um job concreto por unidade

{{< snippet file="gitlab-ci-blueprints/images.yml" lang="yaml" >}}

O job oculto faz o trabalho; cada job concreto são duas variáveis. Rodam em
paralelo, já que nada em `bake_web` depende de `bake_api`. Toda imagem é
publicada duas vezes: como `:<sha>`, que é o que será implantado e nunca se
move, e como `:preview`, um ponteiro flutuante para "o que o anel preview roda
agora" que o passo de release vai ler.

### delivery.yml: a passagem de bastão

{{< snippet file="gitlab-ci-blueprints/delivery.yml" lang="yaml" >}}

`strategy: depend` faz o pai esperar o filho e falhar se ele falhar — o selo
do pipeline da aplicação diz a verdade sobre o rollout, não só sobre o bake.
Um job de entrega por cluster é toda a história de multi-cluster: mesmo
repositório de frota, mesmas variáveis, `CLUSTER` diferente.

`ROLLOUT_SET` é o contrato através da fronteira: qual unidade, qual nome de
container dentro do pod, qual imagem. O lado da frota não precisa de mais
nada para atualizar um deployment.

## Live é release, não rebuild

<figure class="diagram"><svg viewBox="0 0 760 274" role="img" aria-label="Duas raias: a branch candidate assa, publica e faz rollout no anel preview; a branch main pula o bake, re-etiqueta o digest de preview como live e faz o rollout dele." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker><marker id="arrow-accent" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1d4e89"/></marker></defs><text x="20" y="40" text-anchor="start" font-size="11" font-weight="600" fill="currentColor">branch candidate → anel preview</text><text x="20" y="170" text-anchor="start" font-size="11" font-weight="600" fill="currentColor">branch main → anel live</text><line x1="20" y1="126" x2="740" y2="126" stroke="#c9d3e0" stroke-dasharray="3 4"/><rect x="60" y="50" width="140" height="50" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="130.0" y="72.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">bake</text><text x="130.0" y="87.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">3 units</text><line x1="202" y1="75" x2="228" y2="75" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><rect x="230" y="50" width="140" height="50" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="300.0" y="72.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">push</text><text x="300.0" y="87.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">:&lt;sha&gt; · :preview</text><line x1="372" y1="75" x2="398" y2="75" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><rect x="400" y="50" width="140" height="50" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="470.0" y="72.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">trigger</text><text x="470.0" y="87.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">set :&lt;sha&gt;</text><line x1="542" y1="75" x2="568" y2="75" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><rect x="570" y="50" width="140" height="50" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="640.0" y="72.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">roll out</text><text x="640.0" y="87.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">preview</text><rect x="60" y="180" width="140" height="50" fill="#fff" stroke="currentColor" stroke-width="1" stroke-dasharray="5 4"/><text x="130.0" y="202.0" text-anchor="middle" font-size="12" font-weight="400" fill="#5d6b7d">sem bake</text><text x="130.0" y="217.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">estágio pulado</text><rect x="230" y="180" width="140" height="50" fill="#fff" stroke="#1d4e89" stroke-width="1"/><text x="300.0" y="202.0" text-anchor="middle" font-size="12" font-weight="600" fill="#1d4e89">release</text><text x="300.0" y="217.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">crane tag</text><rect x="400" y="180" width="140" height="50" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="470.0" y="202.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">trigger</text><text x="470.0" y="217.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">set @digest</text><rect x="570" y="180" width="140" height="50" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="640.0" y="202.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">roll out</text><text x="640.0" y="217.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">live</text><line x1="202" y1="205" x2="228" y2="205" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 4" marker-end="url(#arrow)"/><line x1="372" y1="205" x2="398" y2="205" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><line x1="542" y1="205" x2="568" y2="205" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><polyline points="300.0,102 300.0,178" fill="none" stroke="#1d4e89" stroke-width="1.2" marker-end="url(#arrow-accent)"/><text x="308.0" y="144" text-anchor="start" font-size="10.5" fill="#1d4e89" font-family="IBM Plex Mono, ui-monospace, monospace">mesmo digest</text><text x="308.0" y="158" text-anchor="start" font-size="10" font-weight="400" fill="#1d4e89" font-family="IBM Plex Mono, ui-monospace, monospace">:preview → :live</text><text x="20" y="262" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">O anel live nunca assa. Ele libera a imagem que já rodou em preview, por digest, e faz o rollout dela.</text></svg><figcaption>Preview assa; live libera. A branch main re-etiqueta o digest de preview e faz o rollout — os bytes que rodaram em preview são os bytes que entram no ar.</figcaption></figure>

{{< snippet file="gitlab-ci-blueprints/release.yml" lang="yaml" >}}

A branch `main` pula o estágio de bake inteiro. Reconstruir do mesmo commit
*provavelmente* produziria a mesma imagem; liberar por digest produz a mesma
imagem por definição. O relatório dotenv é como os digests chegam aos jobs de
entrega — o GitLab expande `$API_IMAGE` dentro do `ROLLOUT_SET` antes de
entregar a variável ao pipeline filho.

## O pipeline da frota

Os manifests vivem por cluster, por app, por anel, com uma pasta `common/`
para o ConfigMap e o Secret que toda unidade lê. Os namespaces seguem uma
convenção, `<app>-<anel>`, então ninguém precisa declará-los:

```text
platform/fleet/
└── north/
    └── orders/
        ├── common/
        │   ├── preview/      configmap.yaml  secret.yaml
        │   └── live/
        ├── preview/          api.yaml  web.yaml  worker.yaml
        └── live/
```

{{< snippet file="gitlab-ci-blueprints/fleet.gitlab-ci.yml" lang="yaml" >}}

Quatro coisas fazem o trabalho de verdade aqui.

**Só roda quando disparado.** Um push no repositório da frota muda arquivos e
nada mais; o cluster muda quando um pipeline de aplicação manda, com um
conjunto de rollout anexado.

**`apply` e `set image` não brigam.** O manifest versionado diz
`image: …/api:preview`; o objeto vivo termina com `…/api@sha256:…`. O próximo
`apply` parece que vai reverter isso — não reverte. O apply client-side só
inclui no patch os campos que mudaram entre o último manifest aplicado e o
novo, e a linha da imagem é idêntica nos dois, então o digest definido pelo
pipeline sobrevive. Quebre essa premissa editando a tag no manifest e você
ganha um segundo rollout por entrega.

**`resource_group` serializa por alvo.** Dois pipelines para a mesma app e
anel entram em fila em vez de disputar. A chave do grupo inclui a app para que
`orders` e `billing` no mesmo cluster ainda façam rollout em paralelo.

**Um rollout que falha se explica.** `describe` e as últimas cem linhas de
log vão para a saída do job antes de ele sair vermelho — quem abre o job às
duas da manhã não deveria precisar de acesso ao cluster para ver o porquê.

## Avisando alguém

{{< snippet file="gitlab-ci-blueprints/alerts.yml" lang="yaml" >}}

Na falha, sempre: branch, anel, autor, commit, um botão. No sucesso, uma linha
do job de rollout com o digest que entrou no ar:

{{< snippet file="gitlab-ci-blueprints/alert-success.sh" lang="bash" >}}

A URL do webhook é uma variável de CI/CD mascarada e protegida no projeto
consumidor; um projeto sem ela apenas registra que pulou o alerta.

## Onde mora cada configuração

| Configuração | Onde | Por que ali |
|---|---|---|
| Branch → anel | `routine.yml` na biblioteca | Uma verdade para todas as apps |
| Credenciais do registry | As `CI_REGISTRY_*` do próprio GitLab | Nunca digitadas em lugar nenhum |
| Kubeconfig por cluster | Variável do tipo arquivo em `platform/fleet`, protegida | Só o pipeline da frota alcança um cluster |
| `SLACK_WEBHOOK_URL` | Variável mascarada em cada consumidor | Cada app é dona do seu canal |
| `SHIP_<UNIDADE>` | `variables:` no arquivo do consumidor | Visível no diff que liga a unidade |
| Versão da biblioteca | `ref:` no `include` do consumidor | Atualização é um commit revisado, não uma surpresa |

## O que nos mordeu, para não morder você

| Sintoma | Causa | Regra |
|---|---|---|
| Rollout verde, imagem inalterada | Unidade nova adicionada em `images.yml` e no `ROLLOUT_SET`, mas o manifest não tem o label `unit:`, então `set image -l` não achou nada | Adicionar uma unidade toca **três** lugares: job de bake, entrada no conjunto, label no manifest |
| Cinco unidades fazendo rollout uma após a outra | `resource_group` sem a app na chave | A chave nomeia exatamente o que não pode se sobrepor |
| Comando falhou, sem erro, job continua | `OUT=$(cmd 2>&1)` sob `set -e`: a atribuição engole o status de saída | Use o comando como condição de um `if`, capture a saída dentro |
| Bake instável "consertado" pelo retry | `script_failure` em `default.retry` | Retry para infraestrutura, nunca para código |
| Um passo pulado porque um Deployment "estava ausente" — não estava | Oscilação de rede indistinguível de `NotFound` | Três estados, parar no terceiro |
| Clone de um repo de 30 MB para rodar `kubectl apply` | `GIT_STRATEGY` padrão num job que nunca lê a árvore | `GIT_STRATEGY: none` quando a árvore de trabalho não é necessária |

Nada disso é GitLab exótico. É `include`, jobs ocultos, regras de `workflow:`,
um trigger multi-projeto e uma variável JSON — arranjados para que adicionar a
quarta app seja uma pasta na biblioteca e uma dúzia de linhas na app, e para
que o anel live só rode bytes que o preview já rodou.
