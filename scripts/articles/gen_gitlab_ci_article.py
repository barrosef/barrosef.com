#!/usr/bin/env python3
"""Generates the GitLab CI article in EN and PT-BR with identical SVG figures."""
from pathlib import Path

SITE = Path(__file__).resolve().parents[2] / "content"
ACCENT = "#1d4e89"
MUTED = "#5d6b7d"
HAIR = "#c9d3e0"
TINT = "#eef2f7"

# ---------------------------------------------------------------- helpers
def box(x, y, w, h, title, sub=None, fill="#fff", stroke="currentColor", dash=False, bold=True, tcolor="currentColor"):
    d = ' stroke-dasharray="5 4"' if dash else ""
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="1"{d}/>'
    cx = x + w / 2
    if sub:
        out += f'<text x="{cx}" y="{y + h/2 - 3}" text-anchor="middle" font-size="12" font-weight="{600 if bold else 400}" fill="{tcolor}">{title}</text>'
        out += f'<text x="{cx}" y="{y + h/2 + 12}" text-anchor="middle" font-size="10.5" fill="{MUTED}" font-family="IBM Plex Mono, ui-monospace, monospace">{sub}</text>'
    else:
        out += f'<text x="{cx}" y="{y + h/2 + 4}" text-anchor="middle" font-size="12" font-weight="{600 if bold else 400}" fill="{tcolor}">{title}</text>'
    return out

def arrow(x1, y1, x2, y2, label=None, lx=None, ly=None, color="currentColor", dash=False, anchor="middle", mono=True):
    d = ' stroke-dasharray="5 4"' if dash else ""
    m = "arrow-accent" if color == ACCENT else "arrow"
    out = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1.2"{d} marker-end="url(#{m})"/>'
    if label:
        lx = (x1 + x2) / 2 if lx is None else lx
        ly = (y1 + y2) / 2 - 6 if ly is None else ly
        ff = ' font-family="IBM Plex Mono, ui-monospace, monospace"' if mono else ""
        out += f'<text x="{lx}" y="{ly}" text-anchor="{anchor}" font-size="10.5" fill="{color if color == ACCENT else MUTED}"{ff}>{label}</text>'
    return out

def elbow(points, label=None, lx=None, ly=None, color="currentColor", dash=False, anchor="middle"):
    d = ' stroke-dasharray="5 4"' if dash else ""
    m = "arrow-accent" if color == ACCENT else "arrow"
    pts = " ".join(f"{x},{y}" for x, y in points)
    out = f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="1.2"{d} marker-end="url(#{m})"/>'
    if label:
        ff = ' font-family="IBM Plex Mono, ui-monospace, monospace"'
        out += f'<text x="{lx}" y="{ly}" text-anchor="{anchor}" font-size="10.5" fill="{color if color == ACCENT else MUTED}"{ff}>{label}</text>'
    return out

def label(x, y, text, size=11, color=MUTED, anchor="start", weight=400, mono=False):
    ff = ' font-family="IBM Plex Mono, ui-monospace, monospace"' if mono else ""
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{color}"{ff}>{text}</text>'

DEFS = f'''<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker><marker id="arrow-accent" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{ACCENT}"/></marker></defs>'''

def figure(w, h, body, caption, aria):
    # No blank lines inside: Goldmark ends an HTML block at the first blank line.
    return (f'<figure class="diagram"><svg viewBox="0 0 {w} {h}" role="img" aria-label="{aria}" '
            f'xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a">'
            f'{DEFS}{body}</svg><figcaption>{caption}</figcaption></figure>')

# ---------------------------------------------------------------- figure 1: repos and pipelines
def fig_repos(L):
    b = ""
    # library on top; includes converge upward into it
    b += box(290, 16, 180, 52, L["library"], "templates/&lt;app&gt;/*.yml", fill=TINT)
    b += label(482, 46, L["library_note"], size=10.5)
    for i, name in enumerate(["orders", "billing", "catalog"]):
        x = 20 + i * 130
        b += box(x, 104, 110, 52, name, ".gitlab-ci.yml", fill="#fff")
        b += arrow(x + 55, 102, 330 + i * 40, 70, dash=True)
    b += label(408, 98, L["include"], size=10.5, anchor="start", mono=True)
    b += label(402, 134, L["apps_caption"], size=10.5)
    # orders pipeline
    b += f'<rect x="20" y="196" width="370" height="70" fill="#fff" stroke="currentColor" stroke-width="1"/>'
    b += label(30, 212, L["orders_pipeline"], size=11, weight=600, color="currentColor")
    stages = [("build", 30, 80), ("promote", 122, 80), ("deploy", 214, 80), ("notify", 306, 74)]
    for i, (st, x, w) in enumerate(stages):
        b += f'<rect x="{x}" y="226" width="{w}" height="28" fill="{TINT}" stroke="{HAIR}"/>'
        b += label(x + w / 2, 244, st, size=11, anchor="middle", color="currentColor", mono=True)
        if i < len(stages) - 1:
            b += arrow(x + w + 1, 240, stages[i + 1][1] - 1, 240)
    b += elbow([(75, 158), (75, 194)], label=L["runs_on_push"], lx=82, ly=180, anchor="start")
    # registry
    b += box(560, 196, 180, 50, L["registry"], "orders/api:&lt;sha&gt;", fill="#fff")
    b += arrow(392, 231, 558, 221, label=L["push"], lx=475, ly=214, anchor="middle")
    # manifests pipeline
    b += f'<rect x="20" y="316" width="370" height="70" fill="#fff" stroke="currentColor" stroke-width="1"/>'
    b += label(30, 332, L["manifests_pipeline"], size=11, weight=600, color="currentColor")
    msteps = [("apply", 30, 74), ("set image", 116, 90), ("rollout status", 218, 110)]
    for i, (st, x, w) in enumerate(msteps):
        b += f'<rect x="{x}" y="346" width="{w}" height="28" fill="{TINT}" stroke="{HAIR}"/>'
        b += label(x + w / 2, 364, st, size=11, anchor="middle", color="currentColor", mono=True)
        if i < len(msteps) - 1:
            b += arrow(x + w + 1, 360, msteps[i + 1][1] - 1, 360)
    b += elbow([(254, 254), (254, 314)], label=L["trigger"], lx=262, ly=282, anchor="start", color=ACCENT)
    b += label(262, 296, "IMAGE_MATRIX, strategy: depend", size=10, color=ACCENT, mono=True)
    # clusters
    b += box(560, 306, 180, 40, "north", L["cluster_sub"], fill="#fff")
    b += box(560, 362, 180, 40, "south", L["cluster_sub"], fill="#fff")
    b += arrow(392, 350, 558, 326, label=L["kubectl"], lx=470, ly=330, anchor="middle")
    b += arrow(392, 362, 558, 382)
    b += elbow([(650, 248), (650, 304)], label=L["pull"], lx=658, ly=280, anchor="start")
    b += label(20, 420, L["legend"], size=10.5)
    return figure(760, 432, b, L["fig1_caption"], L["fig1_aria"])

# ---------------------------------------------------------------- figure 2: templates -> concrete pipeline
def fig_templates(L):
    b = ""
    files = [("workflow.yml", L["f_workflow"], 30), ("build.yml", L["f_build"], 110), ("deploy.yml", L["f_deploy"], 190), ("notify.yml", L["f_notify"], 270)]
    b += label(20, 20, L["library_col"], size=11, weight=600, color="currentColor")
    for name, sub, y in files:
        b += box(20, y, 180, 52, name, sub, fill=TINT)
    # consumer
    b += label(250, 20, L["consumer_col"], size=11, weight=600, color="currentColor")
    b += f'<rect x="250" y="30" width="150" height="292" fill="#fff" stroke="currentColor"/>'
    b += label(325, 52, "orders/.gitlab-ci.yml", size=11, anchor="middle", color="currentColor", weight=600)
    lines = ["include:", "  project: ci-templates", "  ref: v2.3.0", "  file:", "    - workflow.yml", "    - build.yml", "    - deploy.yml", "    - notify.yml", "variables:", "  ENABLE_WORKER: \"true\""]
    for i, ln in enumerate(lines):
        b += label(262, 78 + i * 15, ln.replace('"', "&quot;"), size=9.5, color="currentColor" if not ln.startswith(" ") else MUTED, mono=True)
    b += label(325, 250, L["consumer_note1"], size=10, anchor="middle")
    b += label(325, 265, L["consumer_note2"], size=10, anchor="middle")
    b += label(325, 296, L["consumer_note3"], size=10, anchor="middle", color=ACCENT)
    # include arrows: files -> consumer
    for _, _, y in files:
        b += arrow(202, y + 26, 248, min(max(y + 26, 60), 300), dash=True)
    b += label(225, 48, L["include_short"], size=10, anchor="middle", mono=True)
    # concrete pipeline
    b += label(470, 20, L["pipeline_col"], size=11, weight=600, color="currentColor")
    # workflow row
    b += f'<rect x="470" y="30" width="270" height="52" fill="#fff" stroke="{HAIR}"/>'
    b += label(480, 48, "stages: build · promote · deploy · notify", size=10, color="currentColor", mono=True)
    b += label(480, 64, "release → TARGET_ENV=staging", size=10, mono=True)
    b += label(480, 77, "main    → TARGET_ENV=production", size=10, mono=True)
    # build row: three jobs
    for i, part in enumerate(["build_api", "build_web", "build_worker"]):
        x = 470 + i * 92
        dash = part == "build_worker"
        b += box(x, 110, 86, 52, part, "PART=" + part.split("_")[1], fill="#fff", dash=dash, bold=False)
    b += label(740, 176, L["parallel"], size=10, anchor="end")
    # deploy row
    b += box(470, 190, 130, 52, "deploy_north", "CLUSTER=north", fill="#fff", bold=False)
    b += box(610, 190, 130, 52, "deploy_south", "CLUSTER=south", fill="#fff", bold=False)
    b += label(740, 256, L["one_per_cluster"], size=10, anchor="end")
    # notify row
    b += box(470, 270, 130, 52, "notify_failure", "when: on_failure", fill="#fff", bold=False)
    # arrows consumer -> jobs (expansion)
    b += arrow(402, 56, 468, 56, label=L["expands"], lx=435, ly=48, anchor="middle", mono=False)
    b += arrow(402, 136, 468, 136)
    b += arrow(402, 216, 468, 216)
    b += arrow(402, 296, 468, 296)
    b += label(435, 128, L["hidden_x3"], size=9.5, anchor="middle", mono=True)
    b += label(435, 208, L["hidden_x2"], size=9.5, anchor="middle", mono=True)
    b += label(20, 350, L["fig2_legend"], size=10.5)
    return figure(760, 362, b, L["fig2_caption"], L["fig2_aria"])

# ---------------------------------------------------------------- figure 3: staging vs production
def fig_promote(L):
    b = ""
    b += label(20, 40, L["lane_release"], size=11, weight=600, color="currentColor")
    b += label(20, 170, L["lane_main"], size=11, weight=600, color="currentColor")
    b += f'<line x1="20" y1="126" x2="740" y2="126" stroke="{HAIR}" stroke-dasharray="3 4"/>'
    xs = [60, 230, 400, 570]
    W = 140
    top = [("build", "3 parts"), ("push", ":&lt;sha&gt; · :staging"), ("trigger", "matrix :&lt;sha&gt;"), ("rollout", "staging")]
    for i, (t, sub) in enumerate(top):
        b += box(xs[i], 50, W, 50, t, sub, fill="#fff")
        if i < len(top) - 1:
            b += arrow(xs[i] + W + 2, 75, xs[i + 1] - 2, 75)
    b += box(xs[0], 180, W, 50, L["no_build"], L["no_build_sub"], fill="#fff", dash=True, bold=False, tcolor=MUTED)
    b += box(xs[1], 180, W, 50, "promote", "crane tag", fill="#fff", stroke=ACCENT, tcolor=ACCENT)
    b += box(xs[2], 180, W, 50, "trigger", "matrix @digest", fill="#fff")
    b += box(xs[3], 180, W, 50, "rollout", "production", fill="#fff")
    b += arrow(xs[0] + W + 2, 205, xs[1] - 2, 205, dash=True)
    b += arrow(xs[1] + W + 2, 205, xs[2] - 2, 205)
    b += arrow(xs[2] + W + 2, 205, xs[3] - 2, 205)
    cx = xs[1] + W / 2
    b += elbow([(cx, 102), (cx, 178)], label=L["same_digest"], lx=cx + 8, ly=144, anchor="start", color=ACCENT)
    b += label(cx + 8, 158, ":staging → :production", size=10, color=ACCENT, mono=True)
    b += label(20, 262, L["fig3_legend"], size=10.5)
    return figure(760, 274, b, L["fig3_caption"], L["fig3_aria"])

# ---------------------------------------------------------------- texts
EN = dict(
    apps_caption="app repositories — each pipeline is a thin include", library="ci-templates", library_note="a library: it runs no pipeline of its own",
    include="include · ref: v2.3.0", orders_pipeline="orders pipeline (on push to release / main)", runs_on_push="push",
    registry="container registry", push="docker push :sha, :env", manifests_pipeline="manifests pipeline (runs only when triggered)",
    trigger="trigger", cluster_sub="cluster · namespace per env", kubectl="kubectl -n <ns>", pull="pull",
    legend="Dashed: a reference resolved at pipeline creation, not a run. Blue: the hand-off between the two pipelines.",
    fig1_caption="Three kinds of repository, two pipelines. App repositories include the library; their pipeline builds and hands an image map to the manifests pipeline, which is the only thing that talks to the clusters.",
    fig1_aria="App repositories include a template library; the app pipeline builds, pushes to the registry and triggers the manifests pipeline, which applies manifests, sets images and waits for rollout on each cluster.",
    library_col="the library (templates/orders/)", consumer_col="the consumer", pipeline_col="the pipeline that materialises",
    f_workflow="stages · branch→env · retry", f_build=".build hidden job", f_deploy=".trigger hidden job", f_notify="notify on failure / success",
    consumer_note1="four lines of include,", consumer_note2="one variable block —", consumer_note3="nothing else.", consumer_note4="",
    include_short="include", expands="expands to", hidden_x3="× 3 parts", hidden_x2="× 2 clusters",
    parallel="parallel; worker only if ENABLE_WORKER", one_per_cluster="one trigger per cluster",
    fig2_legend="Dashed: a file pulled in by include. Dashed job: created only when its enable flag is set.",
    fig2_caption="How four template files become a concrete pipeline. Hidden jobs in the library are extended into one job per part and one per cluster; the consumer's file only lists includes and flags.",
    fig2_aria="Four template files, included by a short consumer file, expand into a pipeline with three build jobs, two trigger jobs and one notify job.",
    lane_release="branch release → staging", lane_main="branch main → production", no_build="no build", no_build_sub="stage skipped",
    same_digest="same digest", pull_digest="pull by digest", fig3_legend="Production never builds. It promotes the image that already ran in staging, by digest, and rolls that out.",
    fig3_caption="Staging builds; production promotes. The main branch re-tags the staging digest and deploys it — the bytes that passed staging are the bytes in production.",
    fig3_aria="Two lanes: the release branch builds, pushes and rolls out to staging; the main branch skips the build, re-tags the staging digest as production and rolls that out.",
)
PT = dict(
    apps_caption="repositórios de aplicação — cada pipeline é um include fino", library="ci-templates", library_note="uma biblioteca: não roda pipeline próprio",
    include="include · ref: v2.3.0", orders_pipeline="pipeline do orders (push em release / main)", runs_on_push="push",
    registry="registry de imagens", push="docker push :sha, :env", manifests_pipeline="pipeline do manifests (só roda quando disparado)",
    trigger="trigger", cluster_sub="cluster · namespace por ambiente", kubectl="kubectl -n <ns>", pull="pull",
    legend="Tracejado: uma referência resolvida na criação do pipeline, não uma execução. Azul: a passagem de bastão entre os dois pipelines.",
    fig1_caption="Três tipos de repositório, dois pipelines. Os repositórios de aplicação incluem a biblioteca; o pipeline deles constrói e entrega um mapa de imagens ao pipeline do manifests, que é o único que fala com os clusters.",
    fig1_aria="Repositórios de aplicação incluem uma biblioteca de templates; o pipeline da aplicação constrói, publica no registry e dispara o pipeline do manifests, que aplica manifests, troca imagens e espera o rollout em cada cluster.",
    library_col="a biblioteca (templates/orders/)", consumer_col="o consumidor", pipeline_col="o pipeline que se materializa",
    f_workflow="stages · branch→env · retry", f_build="job oculto .build", f_deploy="job oculto .trigger", f_notify="notifica falha / sucesso",
    consumer_note1="quatro linhas de include,", consumer_note2="um bloco de variáveis —", consumer_note3="nada mais.", consumer_note4="",
    include_short="include", expands="vira", hidden_x3="× 3 partes", hidden_x2="× 2 clusters",
    parallel="paralelos; worker só com ENABLE_WORKER", one_per_cluster="um trigger por cluster",
    fig2_legend="Tracejado: um arquivo trazido pelo include. Job tracejado: criado só quando a flag está ligada.",
    fig2_caption="Como quatro arquivos de template viram um pipeline concreto. Os jobs ocultos da biblioteca são estendidos em um job por parte e um por cluster; o arquivo do consumidor só lista includes e flags.",
    fig2_aria="Quatro arquivos de template, incluídos por um arquivo curto do consumidor, expandem para um pipeline com três jobs de build, dois de trigger e um de notificação.",
    lane_release="branch release → staging", lane_main="branch main → produção", no_build="sem build", no_build_sub="estágio pulado",
    same_digest="mesmo digest", pull_digest="pull por digest", fig3_legend="Produção nunca constrói. Ela promove a imagem que já rodou em staging, por digest, e faz o rollout dela.",
    fig3_caption="Staging constrói; produção promove. A branch main re-etiqueta o digest de staging e o implanta — os bytes que passaram por staging são os bytes em produção.",
    fig3_aria="Duas raias: a branch release constrói, publica e faz rollout em staging; a branch main pula o build, re-etiqueta o digest de staging como produção e faz o rollout dele.",
)

FIGS = {lang: (fig_repos(L), fig_templates(L), fig_promote(L)) for lang, L in (("en", EN), ("pt-br", PT))}

# ---------------------------------------------------------------- YAML blocks (shared)
Y_CONSUMER = '''```yaml
# orders/.gitlab-ci.yml — the whole file
include:
  - project: platform/ci-templates
    ref: v2.3.0            # a tag, never main
    file:
      - templates/orders/workflow.yml
      - templates/orders/build.yml
      - templates/orders/deploy.yml
      - templates/orders/notify.yml

variables:
  ENABLE_WORKER: "true"    # parts opt in one at a time
```'''

Y_WORKFLOW = '''```yaml
# templates/orders/workflow.yml
stages: [build, promote, deploy, notify]

workflow:
  rules:
    - if: '$CI_COMMIT_BRANCH == "release"'
      variables: { TARGET_ENV: staging }
    - if: '$CI_COMMIT_BRANCH == "main"'
      variables: { TARGET_ENV: production }
    - when: never              # anything else creates no pipeline

# Infrastructure retries only. script_failure is deliberately
# absent: a real defect would run three times and look flaky.
default:
  retry:
    max: 2
    when:
      - runner_system_failure
      - stuck_or_timeout_failure
      - api_failure
      - scheduler_failure

# Shell helpers, pulled into jobs with `!reference [.sh, helpers]`.
.sh:
  helpers: |
    # 0 = exists · 1 = does not exist · 2 = could not tell
    k8s_exists() {   # $1=namespace $2=kind $3=name
      for attempt in 1 2 3; do
        err=$(kubectl -n "$1" get "$2" "$3" -o name 2>&1 >/dev/null) \\
          && return 0
        case "$err" in *NotFound*) return 1 ;; esac
        sleep $((attempt * 5))
      done
      echo "undetermined: $2/$3 in $1" >&2; return 2
    }
    with_retry() {
      for a in 1 2 3; do "$@" && return 0; sleep $((a * 5)); done
      return 1
    }
```'''

Y_BUILD = '''```yaml
# templates/orders/build.yml
.build:
  stage: build
  image: docker:27
  services: [docker:27-dind]
  rules:
    - if: '$TARGET_ENV == "staging"'     # production never builds
  variables:
    IMAGE: $CI_REGISTRY_IMAGE/$PART
  script:
    - echo "$CI_REGISTRY_PASSWORD" | docker login -u "$CI_REGISTRY_USER" \\
        --password-stdin "$CI_REGISTRY"
    - docker build -t "$IMAGE:$CI_COMMIT_SHA" \\
        --build-arg TARGET_ENV="$TARGET_ENV" \\
        -f "$CONTEXT/Dockerfile" "$CONTEXT"
    - docker push "$IMAGE:$CI_COMMIT_SHA"
    - docker tag "$IMAGE:$CI_COMMIT_SHA" "$IMAGE:$TARGET_ENV"
    - docker push "$IMAGE:$TARGET_ENV"

build_api:
  extends: .build
  variables: { PART: api, CONTEXT: services/api }

build_web:
  extends: .build
  variables: { PART: web, CONTEXT: web }

build_worker:
  extends: .build
  variables: { PART: worker, CONTEXT: services/worker }
  rules:
    - if: '$TARGET_ENV == "staging" && $ENABLE_WORKER == "true"'
```'''

Y_DEPLOY = '''```yaml
# templates/orders/deploy.yml
.trigger:
  stage: deploy
  rules:
    - if: '$TARGET_ENV =~ /^(staging|production)$/'
  trigger:
    project: platform/manifests
    strategy: depend          # wait for the child; inherit its result
    forward: { pipeline_variables: true }
  variables:
    APP: orders
    ENVIRONMENT: $TARGET_ENV
    SOURCE_SHA: $CI_COMMIT_SHA
    IMAGE_MATRIX: |
      [
        {"part":"api",    "container":"api",    "image":"$API_REF"},
        {"part":"web",    "container":"web",    "image":"$WEB_REF"},
        {"part":"worker", "container":"worker", "image":"$WORKER_REF"}
      ]

deploy_north: { extends: .trigger, variables: { CLUSTER: north } }
deploy_south: { extends: .trigger, variables: { CLUSTER: south } }
```'''

Y_PROMOTE = '''```yaml
# templates/orders/promote.yml
# On main it re-tags; on release it only resolves the digests.
promote:
  stage: promote
  image: gcr.io/go-containerregistry/crane:debug
  script:
    - |
      for part in api web worker; do
        img="$CI_REGISTRY_IMAGE/$part"
        if [ "$TARGET_ENV" = "production" ]; then
          digest=$(crane digest "$img:staging")   # what staging runs
          crane tag "$img@$digest" production     # same bytes, new name
        else
          digest=$(crane digest "$img:$CI_COMMIT_SHA")
        fi
        name=$(echo "$part" | tr a-z A-Z)
        echo "${name}_REF=$img@$digest" >> refs.env
      done
  artifacts:
    reports: { dotenv: refs.env }   # *_REF reach the trigger jobs
```'''

Y_MANIFESTS = '''```yaml
# platform/manifests/.gitlab-ci.yml
workflow:
  rules:
    - if: '$CI_PIPELINE_SOURCE == "pipeline"'   # an app pipeline fired it
    - if: '$CI_PIPELINE_SOURCE == "web"'        # or someone pressed Run
    - when: never

deploy:
  stage: deploy
  image: bitnami/kubectl:1.31
  resource_group: $CLUSTER-$ENVIRONMENT-$APP   # one rollout per target
  script:
    - |
      set -euo pipefail
      # one file-type variable per cluster: KUBECONFIG_NORTH, ...
      eval "export KUBECONFIG=\\$KUBECONFIG_$(echo "$CLUSTER" | tr a-z A-Z)"
      DIR="$CLUSTER/$APP/$ENVIRONMENT"
      NS=$(kubectl create --dry-run=client -f "$DIR/namespace.yaml" \\
             -o jsonpath='{.metadata.name}')

      kubectl -n "$NS" apply -f "$CLUSTER/$APP/_shared/$ENVIRONMENT/"
      kubectl -n "$NS" apply -f "$DIR/"

      echo "$IMAGE_MATRIX" \\
        | jq -c '.[] | select(.image | test("@sha256"))' \\
        | while read -r e; do
            part=$(jq -r .part <<<"$e")
            container=$(jq -r .container <<<"$e")
            image=$(jq -r .image <<<"$e")
            kubectl -n "$NS" set image deployment \\
              -l "app=$APP,part=$part" "$container=$image"
          done

      for d in $(kubectl -n "$NS" get deploy -l "app=$APP" -o name); do
        kubectl -n "$NS" rollout status "$d" --timeout=10m || {
          kubectl -n "$NS" describe "$d"
          kubectl -n "$NS" logs "$d" --all-containers --tail=100 || true
          exit 1
        }
      done
```'''

Y_NOTIFY = '''```yaml
# templates/orders/notify.yml
notify_failure:
  stage: notify
  image: alpine:3.20
  rules:
    - when: on_failure
  script:
    - apk add --no-cache curl jq >/dev/null
    - |
      [ -n "${SLACK_WEBHOOK_URL:-}" ] \\
        || { echo "no SLACK_WEBHOOK_URL; skipping"; exit 0; }
      title=":red_circle: orders — failed on $CI_COMMIT_REF_NAME"
      msg=$(printf '%s' "$CI_COMMIT_MESSAGE" | head -c 300)
      PAYLOAD=$(jq -n --arg title "$title ($TARGET_ENV)" \\
        --arg who "${GITLAB_USER_NAME:-?}" --arg sha "$CI_COMMIT_SHORT_SHA" \\
        --arg msg "$msg" --arg url "$CI_PIPELINE_URL" '{
          blocks: [
            { type: "header",
              text: { type: "plain_text", text: $title } },
            { type: "section", fields: [
                { type: "mrkdwn", text: ("*Author*\\n" + $who) },
                { type: "mrkdwn", text: ("*Commit*\\n`" + $sha + "`") } ] },
            { type: "section",
              text: { type: "mrkdwn", text: $msg } },
            { type: "actions", elements: [
                { type: "button", url: $url,
                  text: { type: "plain_text", text: "Open pipeline" } } ] }
          ] }')
      curl -sS -o /dev/null -w "slack %{http_code}\\n" -X POST \\
           -H 'Content-type: application/json' \\
           -d "$PAYLOAD" "$SLACK_WEBHOOK_URL"
```'''

Y_SUCCESS = '''```bash
# end of the manifests deploy job — success only; a failure exited above
digest=$(kubectl -n "$NS" get deploy -l "app=$APP,part=api" \\
  -o jsonpath='{.items[0].spec.template.spec.containers[0].image}' \\
  | sed 's/.*@sha256://' | head -c 12)
jq -n --arg t ":large_green_circle: orders → $ENVIRONMENT on $CLUSTER" \\
      --arg d "api @ $digest…" --arg u "$CI_JOB_URL" \\
  '{blocks:[{type:"section",text:{type:"mrkdwn",
     text:("*"+$t+"*\\n"+$d+"  <"+$u+"|job>")}}]}' \\
  | curl -sS -o /dev/null -X POST -H 'Content-type: application/json' \\
         -d @- "$SLACK_WEBHOOK_URL" || true
```'''

# ---------------------------------------------------------------- article bodies
def article_en(f1, f2, f3):
    return f'''---
title: "GitLab CI for Kubernetes: one template library, many apps, many clusters"
date: 2026-09-17T09:00:00-04:00
draft: false
translationKey: "gitlab-ci-template-library"
categories: ["Technology"]
tags: ["gitlab-ci", "kubernetes", "devops", "delivery"]
description: "A pipeline architecture that survived several apps, two environments and more than one cluster: a versioned template library, thin app pipelines, a manifests repository that is the only thing talking to Kubernetes, and production as a promotion rather than a rebuild."
---

Three apps, each with three or four deployable parts. Two environments. More
than one Kubernetes cluster, run by different teams. The first version of that
delivery was what it always is: a `.gitlab-ci.yml` copied from the last
project, edited until green, and never the same twice. A year later no two
pipelines agreed on what a branch meant, and a fix in one never reached the
others.

What follows is the architecture that replaced it. Names, paths and numbers
are illustrative; the shape is the thing.

## The shape

{f1}

There are three kinds of repository and only two pipelines:

| Repository | Holds | Its pipeline |
|---|---|---|
| `platform/ci-templates` | The library: one folder per app, four YAML files each | None. It is only ever `include`d |
| `orders`, `billing`, … | The application code and a `.gitlab-ci.yml` of a dozen lines | Builds images, promotes, triggers the manifests pipeline, notifies |
| `platform/manifests` | Kubernetes manifests, `<cluster>/<app>/<env>/` | Runs only when triggered. Applies, sets images, waits for rollout |

Nothing in an app repository knows how to reach a cluster. Nothing in the
manifests repository knows how to build. The hand-off between them is a
single JSON variable, and that boundary is what keeps both sides simple.

## The consumer: a dozen lines

{Y_CONSUMER}

The `ref` is a tag. `main` is for trying a change in one app before you cut
`v2.4.0` and move the others. The file list is explicit on purpose: **the
names are a contract**. Adding a fifth file means every consumer adds a line;
renaming one means every consumer breaks — so files are added, never renamed.

The `ENABLE_*` flags are how a new part, or a new pipeline version, rolls in
one piece at a time. A part whose flag is off has no job at all, not a skipped
one.

## From four files to a pipeline

{f2}

### workflow.yml: what a branch means

{Y_WORKFLOW}

Three decisions live here and nowhere else. **A branch maps to exactly one
environment**, and a branch that maps to nothing creates no pipeline — `when:
never` at the end is not decoration. **Retries cover infrastructure and not
code**: adding `script_failure` would rerun a genuinely broken build three
times and hide the defect behind a green badge on the fourth. And **shell
helpers are shared with `!reference`**, so the retry-with-backoff and the
tri-state existence check are written once. That third state matters: a
network flap during `kubectl get` used to look exactly like "does not exist",
and a job would happily carry on with the wrong assumption. Not being able to
tell is its own answer, and the caller aborts on it.

### build.yml: one hidden job, one concrete job per part

{Y_BUILD}

The base job does the work; each concrete job is three variables. They run in
parallel, since nothing in `build_web` depends on `build_api`. Every image is
pushed twice: as `:<sha>`, which is what will be deployed and never moves, and
as `:staging`, a floating pointer to "what staging runs now" that the
promotion step will read.

### deploy.yml: the hand-off

{Y_DEPLOY}

`strategy: depend` makes the parent wait for the child and fail if it fails —
the app pipeline's badge tells the truth about the deploy, not just the build.
One trigger job per cluster is the whole multi-cluster story: same manifests
repository, same variables, different `CLUSTER`.

`IMAGE_MATRIX` is the contract across the boundary: which part, which
container name inside the pod, which image. The manifests side needs nothing
else to update a deployment.

## Production is a promotion, not a rebuild

{f3}

{Y_PROMOTE}

The `main` branch skips the build stage entirely. Rebuilding from the same
commit would *probably* produce the same image; promoting by digest produces
the same image by definition. The dotenv report is how the digests reach the
trigger jobs downstream — GitLab expands `$API_REF` in the `IMAGE_MATRIX`
before it hands the variable to the child pipeline.

## The manifests pipeline

Manifests live per cluster, per app, per environment, with a `_shared/`
folder for the ConfigMap and Secret every part reads:

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

{Y_MANIFESTS}

Four things are doing the real work here.

**It only runs when triggered.** A push to the manifests repository changes
files and nothing else; the cluster changes when an app pipeline says so, with
an image map attached.

**`apply` and `set image` do not fight.** The versioned manifest says
`image: …/api:staging`; the live object ends up with `…/api@sha256:…`. The next
`apply` looks like it should revert that — it does not. Client-side apply
patches only the fields that changed between the last-applied manifest and the
new one, and the image line is identical in both, so the digest set by the
pipeline survives. Break that premise by editing the tag in the manifest and
you get a second rollout per deploy.

**`resource_group` serialises per target.** Two pipelines for the same app
and environment queue instead of racing. The group key includes the app so
that `orders` and `billing` on the same cluster still deploy in parallel.

**A failed rollout explains itself.** `describe` and the last hundred lines
of logs go into the job output before it exits red — the person who opens
the job at 2 a.m. should not need cluster access to see why.

## Telling someone

{Y_NOTIFY}

On failure, always: branch, environment, author, commit, one button. On
success, one line from the deploy job with the digest that went live:

{Y_SUCCESS}

The webhook URL is a masked, protected CI/CD variable on the consumer
project; a project without one simply logs that it skipped the notification.

## Where each setting lives

| Setting | Where | Why there |
|---|---|---|
| Branch → environment | `workflow.yml` in the library | One truth for every app |
| Registry credentials | GitLab's own `CI_REGISTRY_*` | Never typed anywhere |
| Kubeconfig per cluster | File-type variable on `platform/manifests`, protected | Only the manifests pipeline can reach a cluster |
| `SLACK_WEBHOOK_URL` | Masked variable on each consumer | Each app owns its channel |
| `ENABLE_<PART>` | `variables:` in the consumer's file | Visible in the diff that turns a part on |
| Library version | `ref:` in the consumer's `include` | Upgrades are a reviewed commit, not a surprise |

## What bit us, so it does not bite you

| Symptom | Cause | Rule |
|---|---|---|
| Deploy green, image unchanged | New part added to `build.yml` and `IMAGE_MATRIX` but the manifest lacks the `part:` label, so `set image -l` matched nothing | Adding a part touches **three** places: build job, matrix entry, manifest label |
| Five parts deploying one after another | `resource_group` without the part or app in its key | The key names exactly what must not overlap |
| A failed command, no error, job continues | `OUT=$(cmd 2>&1)` under `set -e`: the assignment swallows the exit status | Use the command as the condition of an `if`, capture output inside |
| A flaky build "fixed" by retry | `script_failure` in `default.retry` | Retry infrastructure, never code |
| A step skipped because a Deployment "did not exist" — it did | Network flap indistinguishable from `NotFound` | Three states, abort on the third |
| Clone of a 30 MB repo to run `kubectl apply` | Default `GIT_STRATEGY` on a job that never reads the tree | `GIT_STRATEGY: none` when the working tree is not needed |

None of this is exotic GitLab. It is `include`, hidden jobs, `workflow.rules`,
one multi-project trigger and a JSON variable — arranged so that adding the
fourth app is a folder in the library and a dozen lines in the app, and so
that production only ever runs bytes that staging already ran.
'''

def article_pt(f1, f2, f3):
    return f'''---
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

{f1}

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

{Y_CONSUMER}

O `ref` é uma tag. `main` serve para experimentar uma mudança em uma app antes
de cortar a `v2.4.0` e migrar as outras. A lista de arquivos é explícita de
propósito: **os nomes são um contrato**. Adicionar um quinto arquivo significa
que cada consumidor acrescenta uma linha; renomear um significa que cada
consumidor quebra — então arquivos são adicionados, nunca renomeados.

As flags `ENABLE_*` são como uma parte nova, ou uma versão nova do pipeline,
entra uma peça de cada vez. Uma parte com a flag desligada não tem job nenhum,
não um job pulado.

## De quatro arquivos a um pipeline

{f2}

### workflow.yml: o que uma branch significa

{Y_WORKFLOW}

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

{Y_BUILD}

O job base faz o trabalho; cada job concreto são três variáveis. Rodam em
paralelo, já que nada em `build_web` depende de `build_api`. Toda imagem é
publicada duas vezes: como `:<sha>`, que é o que será implantado e nunca se
move, e como `:staging`, um ponteiro flutuante para "o que staging roda
agora" que o passo de promoção vai ler.

### deploy.yml: a passagem de bastão

{Y_DEPLOY}

`strategy: depend` faz o pai esperar o filho e falhar se ele falhar — o selo
do pipeline da aplicação diz a verdade sobre o deploy, não só sobre o build.
Um job de trigger por cluster é toda a história de multi-cluster: mesmo
repositório de manifests, mesmas variáveis, `CLUSTER` diferente.

`IMAGE_MATRIX` é o contrato através da fronteira: qual parte, qual nome de
container dentro do pod, qual imagem. O lado dos manifests não precisa de mais
nada para atualizar um deployment.

## Produção é promoção, não rebuild

{f3}

{Y_PROMOTE}

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

{Y_MANIFESTS}

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

{Y_NOTIFY}

Na falha, sempre: branch, ambiente, autor, commit, um botão. No sucesso, uma
linha do job de deploy com o digest que entrou no ar:

{Y_SUCCESS}

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
'''

(SITE / "en/writing/gitlab-ci-template-library.md").write_text(article_en(*FIGS["en"]))
(SITE / "pt-br/artigos/gitlab-ci-biblioteca-de-templates.md").write_text(article_pt(*FIGS["pt-br"]))
print("written")
