---
title: "Os arquivos que fazem o Claude Code ser seu"
date: 2026-09-16T15:00:00-04:00
draft: false
translationKey: "claude-code-files"
categories: ["Tecnologia"]
tags: ["claude-code", "desenvolvimento-com-ia", "ferramentas"]
description: "O Claude Code é configurado por meia dúzia de arquivos de texto. Saiba qual é qual e a ferramenta passa a trabalhar do seu jeito — uma referência curta, com tabelas."
---

O Claude Code lê meia dúzia de arquivos de texto antes de fazer qualquer coisa
por você. A maioria das pessoas nunca os abre — e depois se pergunta por que
o assistente insiste no comando de teste errado ou pede a mesma permissão toda
manhã. Conheça os arquivos e a ferramenta passa a trabalhar do seu jeito.

## Onde eles ficam

Em dois lugares: no projeto, que o time inteiro compartilha pelo git, e na
sua pasta pessoal, que é só sua.

```text
meu-projeto/
├── CLAUDE.md                  # instruções do projeto — commite
├── CLAUDE.local.md            # suas notas privadas — fora do git
├── .mcp.json                  # servidores MCP que o time compartilha
└── .claude/
    ├── settings.json          # permissões, hooks, env, modelo
    ├── settings.local.json    # suas exceções — fora do git
    ├── rules/                 # instruções restritas a um caminho
    ├── skills/<nome>/SKILL.md # prompts reutilizáveis, /nome
    └── agents/*.md            # subagentes: prompt e tools próprios

~/.claude/
├── CLAUDE.md                  # suas preferências, em todo projeto
├── settings.json              # seus padrões, em todo projeto
├── skills/ agents/ rules/     # versões pessoais dos mesmos
├── keybindings.json           # atalhos de teclado
└── projects/<p>/memory/       # o que o Claude lembra do projeto

~/.claude.json                 # estado do app e login — não edite
```

## Os arquivos que importam

| Arquivo | Para que serve | Commita? |
|---|---|---|
| `CLAUDE.md` | Instruções permanentes: como buildar, testar, nomear, o que não tocar. Carregado em toda sessão. | Sim |
| `CLAUDE.local.md` | O mesmo, mas pessoal — seus atalhos, seus caminhos. | Não |
| `.claude/rules/*.md` | Instruções que valem só para parte da árvore, filtradas por um `paths:` no front matter. | Sim |
| `.claude/settings.json` | Permissões acordadas pelo time, hooks, variáveis de ambiente, o modelo padrão. | Sim |
| `.claude/settings.local.json` | Suas exceções ao anterior. "Sim, e não pergunte de novo" cai aqui. | Não |
| `.mcp.json` | Servidores MCP de que o projeto precisa — bancos, rastreadores de tarefas, navegadores. | Sim |
| `.claude/skills/<nome>/SKILL.md` | Um procedimento que você repete, empacotado como `/nome`. Pode levar scripts e templates junto. | Sim |
| `.claude/agents/*.md` | Um subagente: prompt de sistema próprio, lista de ferramentas própria, contexto próprio. | Sim |
| `~/.claude/settings.json` | Seus padrões em todo projeto — tema, modelo, permissões pessoais. | — |
| `~/.claude/projects/…/memory/` | Memória automática: notas que o Claude escreve para si sobre um projeto, um fato por arquivo. | — |
| `~/.claude.json` | Sessão de login, servidores MCP pessoais, confiança por projeto. Não é para editar. | — |

## Qual configuração vence

A mesma chave pode estar em vários lugares. O de cima vence o de baixo, com
uma exceção: nada que você configure sobrepõe o que a sua organização gerencia.

<div class="ladder" role="img" aria-label="Precedência das configurações, da maior para a menor: gerenciada, linha de comando, local do projeto, projeto compartilhado, usuário.">
  <div class="ladder-step"><span class="ladder-n">1</span><span class="ladder-name">Gerenciada</span><code>managed-settings.json</code><span class="ladder-who">sua organização</span></div>
  <div class="ladder-step"><span class="ladder-n">2</span><span class="ladder-name">Linha de comando</span><code>claude --settings</code><span class="ladder-who">você, nesta sessão</span></div>
  <div class="ladder-step"><span class="ladder-n">3</span><span class="ladder-name">Local do projeto</span><code>.claude/settings.local.json</code><span class="ladder-who">você, neste projeto</span></div>
  <div class="ladder-step"><span class="ladder-n">4</span><span class="ladder-name">Projeto compartilhado</span><code>.claude/settings.json</code><span class="ladder-who">todo mundo no projeto</span></div>
  <div class="ladder-step"><span class="ladder-n">5</span><span class="ladder-name">Usuário</span><code>~/.claude/settings.json</code><span class="ladder-who">você, em todo projeto</span></div>
</div>

O Claude Code observa esses arquivos e os recarrega quando mudam: uma edição
em permissões ou hooks chega à sessão em andamento sem reiniciar.

## Onde eu coloco isto?

| Quero… | Coloque em |
|---|---|
| Dizer ao Claude como este projeto builda e testa | `CLAUDE.md` |
| Guardar uma nota que só eu preciso | `CLAUDE.local.md` |
| Impor uma convenção em um único diretório | `.claude/rules/<tema>.md` com `paths:` |
| Liberar um comando para o time inteiro | `permissions.allow` em `.claude/settings.json` |
| Liberar um comando só para mim | `.claude/settings.local.json` |
| Rodar uma checagem antes de cada commit | uma entrada em `hooks` no `.claude/settings.json` |
| Transformar uma rotina de cinco passos em um comando | `.claude/skills/<nome>/SKILL.md` |
| Dar a uma revisão contexto e ferramentas próprios | `.claude/agents/revisor.md` |
| Conectar um banco ou um navegador | `.mcp.json` |

Comece por `CLAUDE.md` e `.claude/settings.json`. Adicione o resto no dia em
que precisar, não antes.

*Referência: as páginas [Claude directory](https://code.claude.com/docs/en/claude-directory) e [settings](https://code.claude.com/docs/en/settings) da documentação oficial, em setembro de 2026.*
