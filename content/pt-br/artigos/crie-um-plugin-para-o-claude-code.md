---
title: "Crie um plugin para o Claude Code, passo a passo"
seoTitle: "Crie um plugin para o Claude Code, passo a passo"
date: 2026-10-29T17:00:00-04:00
draft: false
translationKey: "build-a-claude-plugin"
categories: ["Tecnologia"]
tags: ["claude-code", "plugins", "agentes-de-ia"]
description: "Tutorial prático: construa o commit-helper, um plugin do Claude Code com comando, agente revisor e um hook que barra segredos, e instale-o."
---

Mais cedo ou mais tarde, quem trabalha algumas semanas com o Claude Code acaba
com uma pequena coleção de hábitos: um prompt que cola antes de todo commit, uma
regra que repete sobre quais arquivos nunca tocar, uma revisão que pede tantas
vezes que já sabe de cor. Esses hábitos moram num arquivo de anotações, ou na
cabeça de alguém, e param na borda da máquina daquela pessoa. Um plugin é o jeito
de tirá-los de lá, porque empacota comandos, agentes e hooks numa pasta que
qualquer pessoa instala com uma linha, e assim o seu jeito de trabalhar vira algo
que você entrega em vez de algo que você explica.

Este tutorial constrói um a partir de um diretório vazio. O plugin se chama
**commit-helper** e, no final, vai lhe dar um comando `/commit-helper:commit` que
escreve uma mensagem de commit decente, um agente que revisa o diff preparado
antes de a mensagem ser escrita, e um hook que se recusa a deixar passar um commit
quando o diff acrescenta algo com cara de senha ou de chave de API. Cada um desses
é um tipo diferente de componente de plugin, e é justamente essa a ideia: depois
de construir um de cada, você sabe como todo plugin é montado. No caminho vou
apontar para o [foreman](https://github.com/barrosef/foreman), um plugin que
publiquei recentemente, só para mostrar como a mesma peça fica quando um plugin
cresce.

Você precisa do Claude Code (isto foi verificado na versão 2.1.312), do git e do
Python 3. Tudo abaixo foi testado no Linux; deve funcionar como está no macOS, e
no Windows eu rodaria dentro do WSL.

## O que é um plugin, no disco

Um plugin é um diretório, e o Claude Code encontra as partes dele pelo lugar em
que estão. Nada é registrado em lugar nenhum e não há etapa de build, então a
pasta que você está prestes a criar é a coisa inteira:

```text
commit-helper/
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── skills/
│   └── commit/
│       └── SKILL.md
├── agents/
│   └── diff-reviewer.md
└── hooks/
    ├── hooks.json
    └── secret_guard.py
```

A pasta `.claude-plugin/` guarda metadados e mais nada, e essa é a primeira regra
em que as pessoas tropeçam: skills, agentes e hooks ficam na raiz do plugin, ao
lado dela, nunca dentro. Crie o esqueleto agora e vamos preenchê-lo um arquivo de
cada vez.

```bash
mkdir -p commit-helper/{.claude-plugin,skills/commit,agents,hooks}
cd commit-helper
```

## Passo 1: o manifesto

O manifesto diz ao Claude Code como o plugin se chama, e o nome importa mais do
que parece, porque todo componente fica sob ele. É por isso que o comando que você
vai escrever daqui a pouco roda como `/commit-helper:commit` e nunca colide com o
`commit` de outra pessoa. Salve isto como `.claude-plugin/plugin.json`:

```json
{
  "name": "commit-helper",
  "version": "0.1.0",
  "description": "Writes your commit messages, reviews the diff first, and refuses to commit secrets.",
  "author": {
    "name": "Your Name"
  },
  "license": "MIT",
  "keywords": ["git", "commit", "review"]
}
```

A rigor, só `name` é obrigatório, e o Claude Code carregaria o plugin até sem
manifesto, tirando o nome da pasta; mas vale definir `version` desde o primeiro
dia, já que é ela que mantém quem instala o seu plugin numa versão conhecida até
você publicar a próxima de propósito. Use kebab-case e evite nomes começando com
`claude-`, que são reservados e recusados pelo validador. Você pode conferir o
trabalho a qualquer momento pelo terminal:

```bash
claude plugin validate .
```

Neste plugin a resposta é `Validation passed with warnings`, e o único aviso é a
falta de ícone, que só importa se você listar o plugin no diretório da Anthropic.
O manifesto do foreman é o mesmo arquivo com a URL do repositório e uma descrição
mais longa; manifestos raramente ficam muito maiores que isso.

## Passo 2: o comando

Um comando de barra num plugin é uma **skill**: uma pasta dentro de `skills/` com
um arquivo `SKILL.md` cujo frontmatter a descreve e cujo corpo é a instrução que o
Claude segue quando ela roda. Existe uma pasta `commands/`, mais antiga, que ainda
funciona, mas a documentação hoje recomenda skills para plugins novos, então é o
que vamos usar. Salve isto como `skills/commit/SKILL.md`:

```markdown
---
name: commit
description: Write a commit message for the staged changes, after a diff review, and commit when the user confirms.
disable-model-invocation: true
---

Commit the user's staged changes with a good message. Work in this order.

1. Run `git diff --cached --stat`. If nothing is staged, say so and stop; do not stage
   files on your own.
2. Dispatch the `diff-reviewer` agent and wait for its report. If the verdict is
   `concerns`, show the list to the user and ask whether to go on.
3. Write the message in Conventional Commits form: a subject line under 72 characters
   (`feat:`, `fix:`, `docs:`, `refactor:`, `test:` or `chore:`), a blank line, then a short
   body that explains why the change was made, not what each line does.
4. Show the message and ask the user to confirm or edit it.
5. Only after they confirm, run `git commit` with that message. If a hook blocks the
   commit, show its reason and stop.
```

Dois detalhes desse arquivo fazem a maior parte do trabalho. A `description` é o
que o Claude lê para decidir para que a skill serve, então merece o mesmo cuidado
que o corpo. `disable-model-invocation: true` significa que a skill só roda quando
você a digita; sem essa linha, o Claude poderia decidir sozinho que agora é um bom
momento para commitar, que é exatamente o que você não quer de um comando que
escreve histórico. O corpo em si são instruções simples, escritas para um colega
capaz, numeradas porque aqui a ordem importa, e já menciona o agente e o hook que
ainda não escrevemos, porque é assim que as três peças vão se encontrar.

## Passo 3: o agente

Um agente é um especialista a quem o Claude pode passar uma tarefa. Ele roda no
próprio contexto, com as próprias instruções e só as ferramentas que você der, e
devolve um relatório quando termina. Esse isolamento é o que o torna útil como
revisor: ele olha para o diff sem a conversa que o produziu, então ainda não
decidiu que a mudança está boa. Salve isto como `agents/diff-reviewer.md`:

````markdown
---
name: diff-reviewer
description: Reviews the staged git diff before a commit and reports problems. Use before writing a commit message. Reports only; never edits files.
tools: Read, Grep, Glob, Bash
model: sonnet
---

You review a staged diff before it is committed. Run `git diff --cached` to see it,
and open the surrounding files when a change needs context.

Look for things a reviewer would stop a commit for:

- debugging leftovers: print statements, commented-out code, `TODO` added in this diff
- a change that does something different from what its neighbours suggest
- files that look unrelated to the rest of the change and probably belong in another commit
- anything that looks like a credential or a private key

Report in this shape, and nothing else:

```
VERDICT: ok | concerns
- <file>:<line> — <what you saw and why it matters>
```

Write `VERDICT: ok` with no list when you find nothing. Never edit, stage or commit
anything; your job ends at the report.
````

É no frontmatter que você torna o trabalho do agente seguro. `tools` deixa de fora
`Edit` e `Write`, então nem um revisor que entenda mal as instruções consegue
mexer nos seus arquivos, e `model: sonnet` entrega uma revisão de rotina a um
modelo que dá conta dela sem gastar o seu modelo mais caro nisso. O formato fixo
do relatório existe por causa da skill, que precisa distinguir `ok` de `concerns`
sem interpretar prosa. No foreman os agentes são o mesmo tipo de arquivo, só que
mais longos, porque cada um carrega um papel num time (um explorador que só lê, um
revisor que ataca uma especificação antes de o trabalho começar), e é no
frontmatter que esses limites também são impostos.

## Passo 4: o hook

Skills e agentes são instruções, e uma instrução pode ser ignorada ou esquecida.
Um hook não pode, porque nem chega a ser enviado ao modelo: é um programa que o
próprio Claude Code roda num ponto fixo do seu ciclo. Isso faz dele o lugar certo
para a única regra deste plugin que não pode nunca ceder. Vamos usar um hook
`PreToolUse` na ferramenta Bash, que roda antes de todo comando de shell que o
Claude está prestes a executar, recebe o comando como JSON na entrada padrão e o
bloqueia saindo com código 2. Salve o registro como `hooks/hooks.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"${CLAUDE_PLUGIN_ROOT}\"/hooks/secret_guard.py"
          }
        ]
      }
    ]
  }
}
```

A chave `"hooks"` de fora parece redundante, mas o arquivo de hooks de um plugin
precisa dela, e sem ela o arquivo não carrega. `${CLAUDE_PLUGIN_ROOT}` é trocado
pelo lugar onde o plugin acabar instalado, e as aspas em volta mantêm inteiro um
caminho com espaços. O script em si é curto o bastante para ler de uma vez; salve
como `hooks/secret_guard.py`:

```python
#!/usr/bin/env python3
"""PreToolUse hook: block a git commit whose diff adds something that looks like a secret.

Claude Code sends the tool call as JSON on stdin. Exit 0 lets it through;
exit 2 blocks it, and whatever we print on stderr is shown to Claude.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys

PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),                      # AWS access key
    re.compile(r"gh[pousr]_[A-Za-z0-9]{36}"),             # GitHub token
    re.compile(r"sk-ant-[A-Za-z0-9_-]{20,}"),             # Anthropic API key
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),    # PEM private key
    re.compile(r"(password|secret|token|api_key)\s*[:=]\s*['\"][^'\"]{8,}['\"]", re.I),
]


def is_commit(command: str) -> bool:
    return re.search(r"\bgit\s+commit(\s|$)", command) is not None


def commit_all(command: str) -> bool:
    return re.search(r"\bgit\s+commit\b.*\s(-[a-zA-Z]*a[a-zA-Z]*|--all)\b", command) is not None


def find_secrets(diff: str) -> list[str]:
    added = (line[1:].strip() for line in diff.splitlines()
             if line.startswith("+") and not line.startswith("+++"))
    return [line for line in added if any(p.search(line) for p in PATTERNS)]


def staged_diff(cwd: str | None, include_unstaged: bool) -> str:
    target = ["HEAD"] if include_unstaged else ["--cached"]
    result = subprocess.run(["git", "diff", *target], cwd=cwd, capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else ""


def main(stdin_text: str) -> int:
    try:
        event = json.loads(stdin_text)
        command = event["tool_input"]["command"]
    except (ValueError, KeyError, TypeError):
        return 0  # not something we understand: never get in the way
    if not is_commit(command):
        return 0
    hits = find_secrets(staged_diff(event.get("cwd"), commit_all(command)))
    if not hits:
        return 0
    print("commit-helper blocked this commit: the diff adds what looks like a secret:", file=sys.stderr)
    for line in hits:
        print(f"  {line[:80]}", file=sys.stderr)
    print("Remove it (or move it to an environment variable) and commit again.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.stdin.read()))
```

Quase tudo o que torna este script seguro para rodar antes de cada comando de
shell está nas pequenas decisões. Ele olha só para as linhas que o diff
*acrescenta*, então apagar uma chave vazada nunca é bloqueado; lê `git diff HEAD`
quando o commit usa `-a`, porque aí as mudanças que importam ainda não foram
preparadas; roda o git no `cwd` que o Claude Code envia junto com o evento; e
sempre que encontra algo que não entende, como uma entrada malformada ou uma pasta
que não é repositório, sai com 0 e sai da frente, já que um hook que trava todo
comando é pior do que hook nenhum. Usa só a biblioteca padrão, e o import de
`__future__` deixa as anotações de tipo rodarem no Python 3.9 que vem no macOS.
Como `main` recebe a entrada como string, a lógica é fácil de cobrir com testes
comuns de pytest; a versão deste tutorial tem catorze, incluindo uma chave numa
linha apagada e um `git commit` escondido no fim de uma cadeia `git add . && …`.

## Passo 5: instale e veja funcionar

O Claude Code instala plugins a partir de um **marketplace**, que soa mais
grandioso do que é: um arquivo `marketplace.json` que lista um ou mais plugins e
onde encontrá-los. Para instalar o seu próprio plugin, você cria um marketplace de
um só, dentro da própria pasta do plugin. Salve isto como
`.claude-plugin/marketplace.json`:

```json
{
  "name": "commit-helper-dev",
  "owner": {
    "name": "Your Name"
  },
  "plugins": [
    {
      "name": "commit-helper",
      "source": "./",
      "description": "Writes your commit messages, reviews the diff first, and refuses to commit secrets."
    }
  ]
}
```

Dentro do Claude Code, adicione o marketplace com `/plugin marketplace add`
seguido do caminho da pasta, depois abra `/plugin` e instale o commit-helper pela
lista. Se preferir ficar no terminal, os mesmos dois passos são comandos, e o
terceiro mostra o que foi instalado:

```bash
claude plugin marketplace add /path/to/commit-helper
claude plugin install commit-helper@commit-helper-dev
claude plugin details commit-helper
```

O último comando deve listar exatamente as três peças que você escreveu:

```text
Component inventory
  Skills (1)  commit
  Agents (1)  diff-reviewer
  Hooks (1)  PreToolUse  (harness-only — no model context cost)
```

Agora tente quebrá-lo. Em qualquer repositório git, prepare um arquivo contendo
`AWS_KEY = 'AKIAABCDEFGHIJKLMNOP'` (uma chave falsa no formato da AWS) e peça ao
Claude para commitá-lo. Quando eu fiz isso, o Claude respondeu:

```text
The commit didn't happen. A PreToolUse hook (`secret_guard.py` from the
`commit-helper` plugin) stopped `git commit -m 'add config'` before it could run.
The hook says the staged `config.py` adds what looks like an AWS access key ...
```

e o `git log` confirmou que nada tinha sido commitado. Depois troque a chave por
`os.environ["AWS_KEY"]`, prepare o arquivo de novo e digite
`/commit-helper:commit`. A skill roda o revisor, recebe `VERDICT: ok` e volta com
uma mensagem proposta (`chore: add config module reading AWS key from
environment`, na minha execução) e uma pergunta, porque não commita até você
confirmar. Enquanto você itera no plugin, dá para pular a instalação:
`claude --plugin-dir ./commit-helper` carrega o plugin só naquela sessão, então
cada edição é aplicada na próxima vez que você iniciar.

## Passo 6: compartilhe

Tudo o que fez a instalação local funcionar também torna o plugin compartilhável,
porque um marketplace mora num repositório git tão bem quanto numa pasta. Envie o
diretório `commit-helper` para um repositório, e um colega o instala com
`/plugin marketplace add sua-org/commit-helper` seguido da mesma instalação. Daí
em diante, a `version` do manifesto é a sua válvula de lançamento: aumente-a
quando quiser que as pessoas recebam o comportamento novo. O foreman é distribuído
exatamente assim, com um `marketplace.json` na raiz do repositório no GitHub
listando um único plugin cujo `source` é `./`, então o arquivo que você acabou de
escrever é o mesmo que um plugin publicado usa, só com outro nome dentro. (Se tiver
curiosidade sobre por que o foreman existe, escrevi sobre isso em
[A Cultura que se Instala](/pt-br/artigos/a-cultura-que-se-instala/).)

Para onde ir daqui depende do que o seu time vive repetindo. Se é um
procedimento, vira skill; se é um especialista a quem você vive explicando a
tarefa, vira agente; e se é uma regra que precisa valer mesmo quando ninguém se
lembra dela, vira hook. O plugin é só a pasta que leva tudo isso da sua máquina
para a de todo mundo.
