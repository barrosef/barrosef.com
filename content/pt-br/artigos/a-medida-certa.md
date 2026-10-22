---
title: "A Medida Certa"
seoTitle: "Como escolher o modelo de IA e o esforço para cada tarefa de software"
date: 2026-10-22T08:00:00-04:00
draft: false
translationKey: "right-fit"
categories: ["Tecnologia"]
tags: ["agentes-de-ia", "custo", "gestão", "entrega-de-software", "claude-code", "economizando-com-ia"]
description: "Episódio 5 de Economizando com IA. Qual modelo, com qual esforço, para qual tipo de pedido de software — endpoints, bugs, refatoração, testes, revisão de código, arquitetura — e como um líder com subagentes faz essa escolha por você, para que a eficiência deixe de depender de alguém se lembrar de escolher."
---

*Quinto episódio de **Economizando com IA**. Os episódios 1 a 3 ({{< episode 1 >}},
{{< episode 2 >}}, {{< episode 3 >}}) testaram uma ferramenta que enviava menos
tokens e deixou a conta mais pesada; o episódio 4, {{< episode 4 >}}, passou a gerir
modelos e mediu a economia. Este é sobre como escolher.*

---

O episódio 4 terminou com uma planilha ainda aberta na minha tela, e ela
continuou aberta por um motivo que só entendi alguns dias depois. A medição
tinha nos dito, centavo por centavo, quanto gastamos a mais deixando o modelo
mais caro fazer tudo; o que ela não sabia dizer era como escolher certo da
próxima vez que um pedido chegasse, e da vez seguinte, sem precisar abrir a
planilha de novo. Uma fatura é um veredito sobre o passado, enquanto o que um
gestor de TI precisa na segunda-feira de manhã é uma regra para o futuro.

Por isso este episódio é diferente dos quatro anteriores, e prefiro dizer logo
no começo a deixá-lo emprestar a autoridade deles: é um guia, não uma medição.
Os fatos sobre os modelos vêm da própria documentação da Anthropic, os poucos
números sobre o nosso trabalho são os que o episódio 4 já publicou, e o resto é
o critério que fomos construindo enquanto pagávamos pelos nossos erros. Use-o
como ponto de partida para conferir contra o seu próprio trabalho, como a
própria documentação recomenda.

## Duas alavancas, não uma

Costumamos imaginar a escolha de um modelo de IA como uma única alavanca, do barato
e fraco ao caro e forte, puxada até onde o orçamento deixa; na verdade são duas
alavancas, e a maior parte da eficiência mora no jeito como elas se combinam.

A primeira alavanca é o **modelo**, que define o quanto o trabalhador é capaz. O
Claude vem em quatro tamanhos que importam para software: o Haiku, o menor e
mais rápido; o Sonnet, o burro de carga do dia a dia; o Opus, o sênior; e o
Fable, o modelo mais capaz que a Anthropic vende de forma ampla. Os preços de
tabela são mais distantes do que a maioria imagina, porque, pela mesma
quantidade de texto lido ou escrito, o Opus cobra quarenta vezes o que o Haiku
cobra, e o Fable cobra duas vezes e meia o que o Opus cobra, o que coloca um
fator de cem entre o trabalhador mais barato e o mais caro do mesmo time.

A segunda alavanca é o **esforço**, que define quanto tempo o trabalhador pensa
antes de agir e quantos passos ele se permite pelo caminho. Ele tem cinco
posições, que o produto chama de low, medium, high, xhigh e max, e vale para
tudo o que o modelo produz: o raciocínio, as ações que ele executa nos seus
sistemas e a explicação que escreve no fim. Com esforço baixo o modelo vai
direto ao ponto; no topo ele explora, confere duas vezes e explica. Esforço é
um sinal, não um orçamento, insiste a documentação: mesmo no nível mais baixo o
modelo ainda pensa quando o problema é de fato difícil, só que pensa menos.

Junte as duas alavancas e aparece uma possibilidade que contraria a intuição. Como
o Haiku custa quarenta vezes menos por palavra que o Opus, um Haiku com tempo
para pensar bastante ainda pode custar uma fração de um Opus pensando pouco, e
num trabalho que está ao seu alcance vai entregar o mesmo resultado. O modelo
barato com espaço para pensar é, muitas vezes, a escolha eficiente. Há só uma
pegadinha, e ela molda toda a segunda metade deste artigo: o Haiku mantém esse
preço apenas enquanto a conversa que recebe continua curta, abaixo de uns cem
mil tokens, a unidade em que o provedor conta o texto, ou mais ou menos um
livro de trezentas páginas; passando disso, o preço sobe cinco vezes e ele fica
só oito vezes mais barato que o Opus. O Haiku é o trabalhador certo para um
serviço pequeno e bem definido, entregue inteiro, e o errado para uma sessão
longa que não para de crescer.

## O preço do trabalho pronto, não do pedido

Uma ideia muda a maneira de ler a matriz de seis pedidos que vem a seguir. O jeito natural de comparar modelos é
pelo custo de um único pedido, e essa é quase sempre a comparação errada,
porque uma tentativa barata que precisa ser refeita não é barata, e uma cara
que acerta de primeira muitas vezes é a pechincha. O que importa é o custo do
trabalho pronto, contadas todas as tentativas e todas as horas de atenção.

É por isso que a eficiência escapa pelos dois lados da medida certa. Acima
dela, você está **pagando a mais**, comprando um critério de que o trabalho não
precisava e recebendo de volta só uma conta maior. Abaixo dela, o modelo está
**fraco demais**, o que parece economia até o retrabalho chegar, e retrabalho
é a linha mais cara de qualquer conta, porque paga as duas tentativas e quem
precisou perceber o erro. Os testes de programação da própria Anthropic mostram
um caminho do meio sensato quando existe um jeito confiável de separar sucesso
de fracasso, como testes automatizados: rode tudo com esforço baixo e refaça só
as falhas com um esforço maior, o que nos testes deles manteve a qualidade de
rodar tudo no alto por pouco mais da metade do custo.

## Seis pedidos

A seguir vêm seis pedidos típicos que um time de software entrega a um agente
de IA toda semana. São exemplos compostos, não relatos de coisas que
aconteceram conosco, e cada um é contado como o pedido chegando e a escolha que
ele merece.

O primeiro é um **endpoint**: um novo endereço no sistema que devolve, digamos,
os pedidos em aberto de um cliente, com uma regra de negócio simples sobre
quais pedidos contam como abertos. A regra está escrita, o padrão já existe em
uma dúzia de endpoints vizinhos, e o trabalho é sobretudo repetição fiel, então
a medida certa é o Haiku com esforço high, que a documentação recomenda para
seguir instruções à risca. O Opus em xhigh seria pagar a mais, o mesmo endpoint
por muitas vezes o preço, enquanto o Haiku em low diante de uma regra vaga
ficaria fraco demais, porque um modelo pequeno com pressa numa regra ambígua
tende a chutar. No momento em que a regra fica obscura, o certo é subir, não
torcer.

O segundo é um **bug**: um aviso de que o total de uma fatura às vezes sai
errado. Um bug que se reproduz é trabalho de detetive com a confissão já em
cima da mesa, e o Sonnet com esforço high é a medida certa, com critério
suficiente para seguir a pista por várias partes do sistema. Um bug que não se
reproduz, daqueles que aparecem às terças sob carga, é onde você sobe. O Fable
em max num erro de digitação é pagar a mais em estado puro, e o Haiku num bug
intermitente fica fraco demais do jeito mais caro, porque vai achar *alguma
coisa*, corrigir com toda a confiança e deixar a causa real onde estava.

O terceiro é uma **refatoração**, reorganizar o código sem mudar o que ele faz.
Quando ela é mecânica, como renomear um conceito no sistema inteiro ou dividir
um arquivo que cresceu demais, o Sonnet com esforço medium dá conta com folga,
e colocar o Opus para renomear não compra nada. A subida vem quando a própria
estrutura muda, quando a pergunta deixa de ser *como chamamos isto* e passa a
ser *onde isto deve morar*. A versão fraca demais aqui é a mais perigosa das
seis: um modelo barato varrendo muitos arquivos sem testes para pegá-lo,
produzindo uma mudança que parece arrumada e quebra em silêncio.

O quarto são os **testes**, e escrever testes a partir de uma especificação
clara é trabalho cuidadoso e minucioso, não inspirado, de modo que o Sonnet com
esforço high é a medida certa, com o esforço gasto em cobrir os casos e não em
senioridade. Quando as regras são críticas, como dinheiro, conformidade ou
dados pessoais, você sobe. O Fable em testes de rotina é pagar a mais, enquanto
o caso fraco demais nem é sobre o tamanho do modelo: é o teste escrito pelo
mesmo trabalhador que escreveu o código, que tende a testar o que construiu e
não o que foi pedido, e por isso compartilha cada ponto cego do código.

O quinto é a **revisão de código**, e aqui a matriz se inverte. Um revisor mais
fraco que o autor só consegue revisar ortografia, como diz a configuração do
nosso próprio time, então a medida certa é o modelo do autor ou um mais forte,
com esforço high; a revisão é um dos lugares em que o modelo caro é o
eficiente, porque um defeito que ele pega não custa nada perto do mesmo defeito
encontrado em produção, e você sobe de novo quando a mudança toca segurança,
dinheiro ou dados. O Fable em max numa mudança de uma linha ainda é pagar a
mais, mas o erro caro é o revisor barato que aprova o que não entendeu e dá a
todo mundo uma falsa sensação de segurança.

O sexto é a **arquitetura**: uma decisão sobre como o sistema será construído,
qual banco de dados, qual fronteira entre serviços, por onde os dados passam. O
Opus em xhigh é a medida certa, e quando a decisão vai ser cara de desfazer, de
modo que um erro só apareceria meses depois, vale passar para o Fable em max,
porque nenhuma economia na decisão paga um alicerce errado. O Fable em max numa
escolha que pode ser revertida na semana que vem é pagar a mais, e o Sonnet ou
o Haiku decidindo a arquitetura ficam fracos demais de um jeito que a conta só
vai mostrar muito tempo depois, o que faz disso o pior tipo.

<!-- fig:matrix -->
<figure class="diagram"><svg class="wide" viewBox="0 0 720 494" role="img" aria-label="Matriz de seis pedidos de software — endpoint, bug, refatoração, testes, revisão de código, arquitetura — cada um com o modelo e o esforço certos, quando subir, como é pagar a mais e como é ficar fraco demais." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="h-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#16233a"/></marker><marker id="h-navy" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#1d4e89"/></marker><marker id="h-muted" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#5d6b7d"/></marker><marker id="h-gold" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#b7791f"/></marker></defs><rect x="8" y="8" width="344" height="150" rx="8" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><rect x="8" y="8" width="344" height="34" rx="8" fill="#eef2f7"/><rect x="8" y="34" width="344" height="8" fill="#eef2f7"/><text x="22" y="31" text-anchor="start" font-size="15" font-weight="600" fill="#16233a">Endpoint</text><rect x="22" y="55" width="4" height="14" rx="2" fill="#1d4e89"/><text x="32" y="66" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Medida certa</text><text x="136" y="66" text-anchor="start" font-size="13" font-weight="600" fill="#16233a">Haiku · high</text><rect x="22" y="81" width="4" height="14" rx="2" fill="#5d6b7d"/><text x="32" y="92" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Suba quando</text><text x="136" y="92" text-anchor="start" font-size="13" font-weight="400" fill="#5d6b7d">a regra é ambígua</text><rect x="22" y="107" width="4" height="14" rx="2" fill="#b7791f"/><text x="32" y="118" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Pagando a mais</text><text x="136" y="118" text-anchor="start" font-size="13" font-weight="400" fill="#b7791f">Opus · xhigh</text><rect x="22" y="133" width="4" height="14" rx="2" fill="#b3261e"/><text x="32" y="144" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Fraco demais</text><text x="136" y="144" text-anchor="start" font-size="13" font-weight="400" fill="#b3261e">Haiku · low, regra vaga</text><rect x="368" y="8" width="344" height="150" rx="8" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><rect x="368" y="8" width="344" height="34" rx="8" fill="#eef2f7"/><rect x="368" y="34" width="344" height="8" fill="#eef2f7"/><text x="382" y="31" text-anchor="start" font-size="15" font-weight="600" fill="#16233a">Bug</text><rect x="382" y="55" width="4" height="14" rx="2" fill="#1d4e89"/><text x="392" y="66" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Medida certa</text><text x="496" y="66" text-anchor="start" font-size="13" font-weight="600" fill="#16233a">Sonnet · high</text><rect x="382" y="81" width="4" height="14" rx="2" fill="#5d6b7d"/><text x="392" y="92" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Suba quando</text><text x="496" y="92" text-anchor="start" font-size="13" font-weight="400" fill="#5d6b7d">não se reproduz</text><rect x="382" y="107" width="4" height="14" rx="2" fill="#b7791f"/><text x="392" y="118" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Pagando a mais</text><text x="496" y="118" text-anchor="start" font-size="13" font-weight="400" fill="#b7791f">Fable · max, erro de digitação</text><rect x="382" y="133" width="4" height="14" rx="2" fill="#b3261e"/><text x="392" y="144" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Fraco demais</text><text x="496" y="144" text-anchor="start" font-size="13" font-weight="400" fill="#b3261e">Haiku, bug intermitente</text><rect x="8" y="172" width="344" height="150" rx="8" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><rect x="8" y="172" width="344" height="34" rx="8" fill="#eef2f7"/><rect x="8" y="198" width="344" height="8" fill="#eef2f7"/><text x="22" y="195" text-anchor="start" font-size="15" font-weight="600" fill="#16233a">Refatoração</text><rect x="22" y="219" width="4" height="14" rx="2" fill="#1d4e89"/><text x="32" y="230" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Medida certa</text><text x="136" y="230" text-anchor="start" font-size="13" font-weight="600" fill="#16233a">Sonnet · medium</text><rect x="22" y="245" width="4" height="14" rx="2" fill="#5d6b7d"/><text x="32" y="256" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Suba quando</text><text x="136" y="256" text-anchor="start" font-size="13" font-weight="400" fill="#5d6b7d">a estrutura muda</text><rect x="22" y="271" width="4" height="14" rx="2" fill="#b7791f"/><text x="32" y="282" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Pagando a mais</text><text x="136" y="282" text-anchor="start" font-size="13" font-weight="400" fill="#b7791f">Opus para renomear</text><rect x="22" y="297" width="4" height="14" rx="2" fill="#b3261e"/><text x="32" y="308" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Fraco demais</text><text x="136" y="308" text-anchor="start" font-size="13" font-weight="400" fill="#b3261e">muitos arquivos sem testes</text><rect x="368" y="172" width="344" height="150" rx="8" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><rect x="368" y="172" width="344" height="34" rx="8" fill="#eef2f7"/><rect x="368" y="198" width="344" height="8" fill="#eef2f7"/><text x="382" y="195" text-anchor="start" font-size="15" font-weight="600" fill="#16233a">Testes</text><rect x="382" y="219" width="4" height="14" rx="2" fill="#1d4e89"/><text x="392" y="230" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Medida certa</text><text x="496" y="230" text-anchor="start" font-size="13" font-weight="600" fill="#16233a">Sonnet · high</text><rect x="382" y="245" width="4" height="14" rx="2" fill="#5d6b7d"/><text x="392" y="256" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Suba quando</text><text x="496" y="256" text-anchor="start" font-size="13" font-weight="400" fill="#5d6b7d">as regras são críticas</text><rect x="382" y="271" width="4" height="14" rx="2" fill="#b7791f"/><text x="392" y="282" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Pagando a mais</text><text x="496" y="282" text-anchor="start" font-size="13" font-weight="400" fill="#b7791f">Fable em testes de rotina</text><rect x="382" y="297" width="4" height="14" rx="2" fill="#b3261e"/><text x="392" y="308" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Fraco demais</text><text x="496" y="308" text-anchor="start" font-size="13" font-weight="400" fill="#b3261e">escrito pelo autor do código</text><rect x="8" y="336" width="344" height="150" rx="8" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><rect x="8" y="336" width="344" height="34" rx="8" fill="#eef2f7"/><rect x="8" y="362" width="344" height="8" fill="#eef2f7"/><text x="22" y="359" text-anchor="start" font-size="15" font-weight="600" fill="#16233a">Revisão de código</text><rect x="22" y="383" width="4" height="14" rx="2" fill="#1d4e89"/><text x="32" y="394" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Medida certa</text><text x="136" y="394" text-anchor="start" font-size="13" font-weight="600" fill="#16233a">o do autor ou acima · high</text><rect x="22" y="409" width="4" height="14" rx="2" fill="#5d6b7d"/><text x="32" y="420" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Suba quando</text><text x="136" y="420" text-anchor="start" font-size="13" font-weight="400" fill="#5d6b7d">segurança, dinheiro, dados</text><rect x="22" y="435" width="4" height="14" rx="2" fill="#b7791f"/><text x="32" y="446" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Pagando a mais</text><text x="136" y="446" text-anchor="start" font-size="13" font-weight="400" fill="#b7791f">Fable · max em uma linha</text><rect x="22" y="461" width="4" height="14" rx="2" fill="#b3261e"/><text x="32" y="472" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Fraco demais</text><text x="136" y="472" text-anchor="start" font-size="13" font-weight="400" fill="#b3261e">revisor abaixo do autor</text><rect x="368" y="336" width="344" height="150" rx="8" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><rect x="368" y="336" width="344" height="34" rx="8" fill="#eef2f7"/><rect x="368" y="362" width="344" height="8" fill="#eef2f7"/><text x="382" y="359" text-anchor="start" font-size="15" font-weight="600" fill="#16233a">Arquitetura</text><rect x="382" y="383" width="4" height="14" rx="2" fill="#1d4e89"/><text x="392" y="394" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Medida certa</text><text x="496" y="394" text-anchor="start" font-size="13" font-weight="600" fill="#16233a">Opus · xhigh</text><rect x="382" y="409" width="4" height="14" rx="2" fill="#5d6b7d"/><text x="392" y="420" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Suba quando</text><text x="496" y="420" text-anchor="start" font-size="13" font-weight="400" fill="#5d6b7d">cara de desfazer: Fable · max</text><rect x="382" y="435" width="4" height="14" rx="2" fill="#b7791f"/><text x="392" y="446" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Pagando a mais</text><text x="496" y="446" text-anchor="start" font-size="13" font-weight="400" fill="#b7791f">Fable · max, reversível</text><rect x="382" y="461" width="4" height="14" rx="2" fill="#b3261e"/><text x="392" y="472" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Fraco demais</text><text x="496" y="472" text-anchor="start" font-size="13" font-weight="400" fill="#b3261e">Sonnet ou Haiku</text></svg><svg class="narrow" viewBox="0 0 360 986" role="img" aria-label="Matriz de seis pedidos de software — endpoint, bug, refatoração, testes, revisão de código, arquitetura — cada um com o modelo e o esforço certos, quando subir, como é pagar a mais e como é ficar fraco demais." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="h-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#16233a"/></marker><marker id="h-navy" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#1d4e89"/></marker><marker id="h-muted" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#5d6b7d"/></marker><marker id="h-gold" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#b7791f"/></marker></defs><rect x="8" y="8" width="344" height="150" rx="8" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><rect x="8" y="8" width="344" height="34" rx="8" fill="#eef2f7"/><rect x="8" y="34" width="344" height="8" fill="#eef2f7"/><text x="22" y="31" text-anchor="start" font-size="15" font-weight="600" fill="#16233a">Endpoint</text><rect x="22" y="55" width="4" height="14" rx="2" fill="#1d4e89"/><text x="32" y="66" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Medida certa</text><text x="136" y="66" text-anchor="start" font-size="13" font-weight="600" fill="#16233a">Haiku · high</text><rect x="22" y="81" width="4" height="14" rx="2" fill="#5d6b7d"/><text x="32" y="92" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Suba quando</text><text x="136" y="92" text-anchor="start" font-size="13" font-weight="400" fill="#5d6b7d">a regra é ambígua</text><rect x="22" y="107" width="4" height="14" rx="2" fill="#b7791f"/><text x="32" y="118" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Pagando a mais</text><text x="136" y="118" text-anchor="start" font-size="13" font-weight="400" fill="#b7791f">Opus · xhigh</text><rect x="22" y="133" width="4" height="14" rx="2" fill="#b3261e"/><text x="32" y="144" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Fraco demais</text><text x="136" y="144" text-anchor="start" font-size="13" font-weight="400" fill="#b3261e">Haiku · low, regra vaga</text><rect x="8" y="172" width="344" height="150" rx="8" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><rect x="8" y="172" width="344" height="34" rx="8" fill="#eef2f7"/><rect x="8" y="198" width="344" height="8" fill="#eef2f7"/><text x="22" y="195" text-anchor="start" font-size="15" font-weight="600" fill="#16233a">Bug</text><rect x="22" y="219" width="4" height="14" rx="2" fill="#1d4e89"/><text x="32" y="230" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Medida certa</text><text x="136" y="230" text-anchor="start" font-size="13" font-weight="600" fill="#16233a">Sonnet · high</text><rect x="22" y="245" width="4" height="14" rx="2" fill="#5d6b7d"/><text x="32" y="256" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Suba quando</text><text x="136" y="256" text-anchor="start" font-size="13" font-weight="400" fill="#5d6b7d">não se reproduz</text><rect x="22" y="271" width="4" height="14" rx="2" fill="#b7791f"/><text x="32" y="282" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Pagando a mais</text><text x="136" y="282" text-anchor="start" font-size="13" font-weight="400" fill="#b7791f">Fable · max, erro de digitação</text><rect x="22" y="297" width="4" height="14" rx="2" fill="#b3261e"/><text x="32" y="308" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Fraco demais</text><text x="136" y="308" text-anchor="start" font-size="13" font-weight="400" fill="#b3261e">Haiku, bug intermitente</text><rect x="8" y="336" width="344" height="150" rx="8" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><rect x="8" y="336" width="344" height="34" rx="8" fill="#eef2f7"/><rect x="8" y="362" width="344" height="8" fill="#eef2f7"/><text x="22" y="359" text-anchor="start" font-size="15" font-weight="600" fill="#16233a">Refatoração</text><rect x="22" y="383" width="4" height="14" rx="2" fill="#1d4e89"/><text x="32" y="394" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Medida certa</text><text x="136" y="394" text-anchor="start" font-size="13" font-weight="600" fill="#16233a">Sonnet · medium</text><rect x="22" y="409" width="4" height="14" rx="2" fill="#5d6b7d"/><text x="32" y="420" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Suba quando</text><text x="136" y="420" text-anchor="start" font-size="13" font-weight="400" fill="#5d6b7d">a estrutura muda</text><rect x="22" y="435" width="4" height="14" rx="2" fill="#b7791f"/><text x="32" y="446" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Pagando a mais</text><text x="136" y="446" text-anchor="start" font-size="13" font-weight="400" fill="#b7791f">Opus para renomear</text><rect x="22" y="461" width="4" height="14" rx="2" fill="#b3261e"/><text x="32" y="472" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Fraco demais</text><text x="136" y="472" text-anchor="start" font-size="13" font-weight="400" fill="#b3261e">muitos arquivos sem testes</text><rect x="8" y="500" width="344" height="150" rx="8" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><rect x="8" y="500" width="344" height="34" rx="8" fill="#eef2f7"/><rect x="8" y="526" width="344" height="8" fill="#eef2f7"/><text x="22" y="523" text-anchor="start" font-size="15" font-weight="600" fill="#16233a">Testes</text><rect x="22" y="547" width="4" height="14" rx="2" fill="#1d4e89"/><text x="32" y="558" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Medida certa</text><text x="136" y="558" text-anchor="start" font-size="13" font-weight="600" fill="#16233a">Sonnet · high</text><rect x="22" y="573" width="4" height="14" rx="2" fill="#5d6b7d"/><text x="32" y="584" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Suba quando</text><text x="136" y="584" text-anchor="start" font-size="13" font-weight="400" fill="#5d6b7d">as regras são críticas</text><rect x="22" y="599" width="4" height="14" rx="2" fill="#b7791f"/><text x="32" y="610" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Pagando a mais</text><text x="136" y="610" text-anchor="start" font-size="13" font-weight="400" fill="#b7791f">Fable em testes de rotina</text><rect x="22" y="625" width="4" height="14" rx="2" fill="#b3261e"/><text x="32" y="636" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Fraco demais</text><text x="136" y="636" text-anchor="start" font-size="13" font-weight="400" fill="#b3261e">escrito pelo autor do código</text><rect x="8" y="664" width="344" height="150" rx="8" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><rect x="8" y="664" width="344" height="34" rx="8" fill="#eef2f7"/><rect x="8" y="690" width="344" height="8" fill="#eef2f7"/><text x="22" y="687" text-anchor="start" font-size="15" font-weight="600" fill="#16233a">Revisão de código</text><rect x="22" y="711" width="4" height="14" rx="2" fill="#1d4e89"/><text x="32" y="722" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Medida certa</text><text x="136" y="722" text-anchor="start" font-size="13" font-weight="600" fill="#16233a">o do autor ou acima · high</text><rect x="22" y="737" width="4" height="14" rx="2" fill="#5d6b7d"/><text x="32" y="748" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Suba quando</text><text x="136" y="748" text-anchor="start" font-size="13" font-weight="400" fill="#5d6b7d">segurança, dinheiro, dados</text><rect x="22" y="763" width="4" height="14" rx="2" fill="#b7791f"/><text x="32" y="774" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Pagando a mais</text><text x="136" y="774" text-anchor="start" font-size="13" font-weight="400" fill="#b7791f">Fable · max em uma linha</text><rect x="22" y="789" width="4" height="14" rx="2" fill="#b3261e"/><text x="32" y="800" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Fraco demais</text><text x="136" y="800" text-anchor="start" font-size="13" font-weight="400" fill="#b3261e">revisor abaixo do autor</text><rect x="8" y="828" width="344" height="150" rx="8" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><rect x="8" y="828" width="344" height="34" rx="8" fill="#eef2f7"/><rect x="8" y="854" width="344" height="8" fill="#eef2f7"/><text x="22" y="851" text-anchor="start" font-size="15" font-weight="600" fill="#16233a">Arquitetura</text><rect x="22" y="875" width="4" height="14" rx="2" fill="#1d4e89"/><text x="32" y="886" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Medida certa</text><text x="136" y="886" text-anchor="start" font-size="13" font-weight="600" fill="#16233a">Opus · xhigh</text><rect x="22" y="901" width="4" height="14" rx="2" fill="#5d6b7d"/><text x="32" y="912" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Suba quando</text><text x="136" y="912" text-anchor="start" font-size="13" font-weight="400" fill="#5d6b7d">cara de desfazer: Fable · max</text><rect x="22" y="927" width="4" height="14" rx="2" fill="#b7791f"/><text x="32" y="938" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Pagando a mais</text><text x="136" y="938" text-anchor="start" font-size="13" font-weight="400" fill="#b7791f">Fable · max, reversível</text><rect x="22" y="953" width="4" height="14" rx="2" fill="#b3261e"/><text x="32" y="964" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Fraco demais</text><text x="136" y="964" text-anchor="start" font-size="13" font-weight="400" fill="#b3261e">Sonnet ou Haiku</text></svg><figcaption>Seis pedidos e a medida certa de cada um, como modelo · esforço. Acima dela você paga a mais; abaixo, arrisca o retrabalho.</figcaption></figure>

Lidos juntos, os seis mostram um padrão: a ponta barata da matriz é onde o
trabalho já está decidido e só precisa ser feito, a ponta cara é onde o
trabalho *é* decidir, e nenhuma das células é lei, só um lugar para começar
antes que o seu próprio trabalho mova uma linha para cima ou para baixo.

## O time que escolhe por você

Uma matriz só serve se alguém a consultar, e a lição do episódio 4 é que,
deixado por conta própria, ninguém consulta: o padrão vence, e o padrão é o
modelo mais caro, que é onde entra o **desenvolvimento com subagentes**.

Um **subagente** é um segundo trabalhador de IA a quem o principal entrega uma
parte do trabalho. Ele começa do zero: lê só o que precisa para a sua parte,
faz o trabalho pesado por conta própria e devolve um resultado curto, de modo
que a conversa principal continua pequena e focada. Esse começo do zero é o
propósito do desenho e também a sua exigência, porque um subagente não sabe
nada que a entrega não lhe diga. É também exatamente o serviço pequeno e bem
definido que mantém um modelo barato no seu preço barato. Desenvolvimento com
subagentes é organizar o trabalho desse jeito de propósito: um **líder** que
entende o pedido, decide o plano e confere o resultado, e **ajudantes**, os
subagentes, cada um fazendo um tipo de trabalho com o modelo e o esforço que
aquele tipo de trabalho merece.

O nosso time, que [A Cultura que se Instala]({{< relref "a-cultura-que-se-instala.md" >}})
descreve por inteiro, tem cinco ajudantes, e as configurações deles são a
matriz escrita no próprio time.

<!-- fig:team -->
<figure class="diagram"><svg class="wide" viewBox="0 0 720 224" role="img" aria-label="Diagrama do líder no alto entregando trabalho a cinco ajudantes abaixo: leitor no Sonnet com esforço low, construtor no Sonnet medium, testador no Sonnet high, revisor e líder de QA no modelo do líder com esforço high." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="h-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#16233a"/></marker><marker id="h-navy" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#1d4e89"/></marker><marker id="h-muted" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#5d6b7d"/></marker><marker id="h-gold" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#b7791f"/></marker></defs><rect x="240" y="12" width="240" height="70" rx="6" fill="#1d4e89" stroke="#173d6e" stroke-width="1.2"/><text x="360.0" y="38.0" text-anchor="middle" font-size="15" font-weight="600" fill="#fff">Líder</text><text x="360.0" y="54.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#cfe0f5">decide, planeja, confere</text><text x="360.0" y="68.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#cfe0f5">Opus</text><path d="M 360,82 L 360,112" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/><path d="M 76,112 L 644,112" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/><text x="368" y="104" text-anchor="start" font-size="11" font-weight="600" fill="#1d4e89">entrega cada parte, escolhendo o modelo</text><path d="M 76.0,112 L 76.0,130" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><rect x="10.0" y="134" width="132" height="78" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="76.0" y="164.0" text-anchor="middle" font-size="14" font-weight="600" fill="#16233a">Leitor</text><text x="76.0" y="180.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">Sonnet · low</text><text x="76.0" y="194.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">lê e relata</text><path d="M 218.0,112 L 218.0,130" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><rect x="152.0" y="134" width="132" height="78" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="218.0" y="164.0" text-anchor="middle" font-size="14" font-weight="600" fill="#16233a">Construtor</text><text x="218.0" y="180.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">Sonnet · medium</text><text x="218.0" y="194.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">Haiku nas mudanças triviais</text><path d="M 360.0,112 L 360.0,130" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><rect x="294.0" y="134" width="132" height="78" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="360.0" y="164.0" text-anchor="middle" font-size="14" font-weight="600" fill="#16233a">Testador</text><text x="360.0" y="180.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">Sonnet · high</text><text x="360.0" y="194.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">ataca o trabalho</text><path d="M 502.0,112 L 502.0,130" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><rect x="436.0" y="134" width="132" height="78" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="502.0" y="164.0" text-anchor="middle" font-size="14" font-weight="600" fill="#16233a">Revisor</text><text x="502.0" y="180.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">modelo do líder · high</text><text x="502.0" y="194.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">nunca abaixo do autor</text><path d="M 644.0,112 L 644.0,130" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><rect x="578.0" y="134" width="132" height="78" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="644.0" y="164.0" text-anchor="middle" font-size="14" font-weight="600" fill="#16233a">Líder de QA</text><text x="644.0" y="180.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">modelo do líder · high</text><text x="644.0" y="194.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">decide o que testar</text></svg><svg class="narrow" viewBox="0 0 360 462" role="img" aria-label="Diagrama do líder no alto entregando trabalho a cinco ajudantes abaixo: leitor no Sonnet com esforço low, construtor no Sonnet medium, testador no Sonnet high, revisor e líder de QA no modelo do líder com esforço high." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="h-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#16233a"/></marker><marker id="h-navy" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#1d4e89"/></marker><marker id="h-muted" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#5d6b7d"/></marker><marker id="h-gold" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#b7791f"/></marker></defs><rect x="8" y="8" width="344" height="70" rx="6" fill="#1d4e89" stroke="#173d6e" stroke-width="1.2"/><text x="180.0" y="34.0" text-anchor="middle" font-size="15" font-weight="600" fill="#fff">Líder</text><text x="180.0" y="50.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#cfe0f5">decide, planeja, confere</text><text x="180.0" y="64.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#cfe0f5">Opus</text><text x="36" y="100" text-anchor="start" font-size="11" font-weight="600" fill="#1d4e89">entrega cada parte, escolhendo o modelo</text><path d="M 22,78 L 22,424" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/><path d="M 22,144 L 34,144" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><rect x="38" y="112" width="314" height="62" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="195.0" y="134.0" text-anchor="middle" font-size="14" font-weight="600" fill="#16233a">Leitor</text><text x="195.0" y="150.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">Sonnet · low</text><text x="195.0" y="164.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">lê e relata</text><path d="M 22,214 L 34,214" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><rect x="38" y="182" width="314" height="62" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="195.0" y="204.0" text-anchor="middle" font-size="14" font-weight="600" fill="#16233a">Construtor</text><text x="195.0" y="220.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">Sonnet · medium</text><text x="195.0" y="234.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">Haiku nas mudanças triviais</text><path d="M 22,284 L 34,284" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><rect x="38" y="252" width="314" height="62" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="195.0" y="274.0" text-anchor="middle" font-size="14" font-weight="600" fill="#16233a">Testador</text><text x="195.0" y="290.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">Sonnet · high</text><text x="195.0" y="304.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">ataca o trabalho</text><path d="M 22,354 L 34,354" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><rect x="38" y="322" width="314" height="62" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="195.0" y="344.0" text-anchor="middle" font-size="14" font-weight="600" fill="#16233a">Revisor</text><text x="195.0" y="360.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">modelo do líder · high</text><text x="195.0" y="374.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">nunca abaixo do autor</text><path d="M 22,424 L 34,424" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><rect x="38" y="392" width="314" height="62" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="195.0" y="414.0" text-anchor="middle" font-size="14" font-weight="600" fill="#16233a">Líder de QA</text><text x="195.0" y="430.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">modelo do líder · high</text><text x="195.0" y="444.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">decide o que testar</text></svg><figcaption>O líder e seus cinco ajudantes. O esforço é fixo em cada papel; o modelo, o líder escolhe a cada pedido.</figcaption></figure>

O **leitor** roda no Sonnet com esforço low, porque lê e relata e não decide
nada, que é o próprio exemplo da documentação para o esforço baixo. O
**construtor** roda no Sonnet em medium, porque quando recebe uma mudança ela
já está decidida, e o líder pode entregar uma trivial ao Haiku. O **testador**
roda no Sonnet em high, porque atacar um trabalho pede profundidade e paciência
mais do que senioridade. O **revisor** e o **líder de QA**, que decide o que os
testes precisam cobrir, trabalham os dois no próprio modelo do líder e com
esforço high, porque são os dois lugares em que um trabalhador mais fraco
deixaria passar os erros do líder.

Há um princípio escondido nesse arranjo, e é o que eu levaria deste artigo se
levasse um só: **o esforço pertence ao papel, e o modelo pertence ao pedido.**
O esforço de cada ajudante fica fixo na sua própria descrição, porque o tipo de
pensamento que um trabalho pede é uma propriedade do trabalho, enquanto o
modelo é escolhido pelo líder a cada entrega, porque o quanto *esta* mudança é
difícil depende da mudança. Assim o time não acerta cada célula da matriz com
exatidão: o endpoint que a matriz põe no Haiku em high sai como o construtor no
Haiku com o seu medium de sempre, e essa é uma troca que aceitamos de
propósito, porque um time cujos papéis se comportam sempre do mesmo jeito é
previsível e barato de operar, e um pouco de precisão é um preço justo por
isso. Quando um pedido realmente precisa de outro esforço, a ferramenta permite
defini-lo só para aquela entrega.

O episódio 4 contou o que acontece sem isso. O nosso testador não tinha modelo
nomeado na sua descrição, e por isso durante 1.441 rodadas de trabalho herdou
em silêncio o mais caro, a 13 centavos por rodada; depois que ganhou um nome, o
mesmo trabalho passou a custar menos de 5 centavos. Ninguém tinha escolhido
mal; ninguém tinha escolhido, simplesmente.

## O líder é a próxima alavanca

O episódio 4 terminou apontando para o próprio líder, que, depois que os
ajudantes foram para modelos mais baratos, tinha virado uns setenta por cento
da conta de um dia tranquilo. A matriz responde isso na teoria, porque o líder
é um trabalhador como qualquer outro e o seu modelo pode ser escolhido a cada
sessão de trabalho. Uma sessão dedicada à arquitetura, ou a uma mudança que
pede uma revisão exigente, mantém o Opus como líder, enquanto um dia de
endpoints de rotina e pequenas correções pode ser liderado pelo Sonnet.

Há um risco nisso, e vale dizê-lo com todas as letras: o revisor e o líder de
QA seguem o modelo do líder, então quando o líder desce eles descem junto.
Rebaixar o líder só é certo nos dias em que uma revisão no nível do Sonnet
basta, o que vale para a maioria dos dias e não para todos. É uma recomendação
que ainda não medimos, e quando tivermos o comprovante ele vai virar episódio.

## A medida certa

A planilha está fechada agora, porque o que ela realmente dizia cabe numa
página. Eficiência com IA não é o modelo mais barato nem o mais capaz; é uma
escolha feita a cada pedido, em duas alavancas, perguntando o quanto o trabalho é
difícil e o quanto um erro sairia caro, e ela falha pelos dois lados: ou você
paga por um critério que não usou, ou paga duas vezes pelo critério que não
comprou. O padrão é o que custa dinheiro, porque o padrão é o modelo mais caro
fazendo tudo, e o remédio é estrutura, um líder e seus ajudantes com a escolha
escrita em cada papel, para que a medida certa aconteça até na segunda-feira em
que ninguém se lembra de pensar nisso.

---

*Fontes. Preços e níveis de esforço são os preços de tabela e a documentação
publicados pela Anthropic em outubro de 2026; o resultado de rodar no baixo e
refazer as falhas vem dos testes de programação da própria Anthropic; os
números sobre o nosso trabalho são os do episódio 4.*
