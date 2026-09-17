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
    b += box(290, 16, 180, 52, L["library"], "blueprints/&lt;app&gt;/*.yml", fill=TINT)
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
    stages = [("images", 30, 80), ("release", 122, 80), ("delivery", 214, 80), ("alerts", 306, 74)]
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
    b += label(262, 296, "ROLLOUT_SET · strategy: depend", size=10, color=ACCENT, mono=True)
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
    H = 48
    rows = [30, 94, 158, 222, 286]
    files = [("routine.yml", L["f_workflow"]), ("images.yml", L["f_build"]), ("release.yml", L["f_release"]), ("delivery.yml", L["f_deploy"]), ("alerts.yml", L["f_notify"])]
    b += label(20, 20, L["library_col"], size=11, weight=600, color="currentColor")
    for (name, sub), y in zip(files, rows):
        b += box(20, y, 180, H, name, sub, fill=TINT)
    # consumer
    b += label(250, 20, L["consumer_col"], size=11, weight=600, color="currentColor")
    b += f'<rect x="250" y="30" width="150" height="304" fill="#fff" stroke="currentColor"/>'
    b += label(325, 52, "orders/.gitlab-ci.yml", size=11, anchor="middle", color="currentColor", weight=600)
    lines = ["include:", "  project: ci-blueprints", "  ref: v2.3.0", "  file:", "    - routine.yml", "    - images.yml", "    - release.yml", "    - delivery.yml", "    - alerts.yml", "variables:", "  SHIP_WORKER: \"true\""]
    for i, ln in enumerate(lines):
        b += label(262, 78 + i * 15, ln.replace('"', "&quot;"), size=9.5, color="currentColor" if not ln.startswith(" ") else MUTED, mono=True)
    b += label(325, 268, L["consumer_note1"], size=10, anchor="middle")
    b += label(325, 283, L["consumer_note2"], size=10, anchor="middle")
    b += label(325, 312, L["consumer_note3"], size=10, anchor="middle", color=ACCENT)
    for y in rows:
        b += arrow(202, y + H / 2, 248, min(max(y + H / 2, 60), 310), dash=True)
    b += label(225, 46, L["include_short"], size=10, anchor="middle", mono=True)
    # the pipeline that materialises
    b += label(470, 20, L["pipeline_col"], size=11, weight=600, color="currentColor")
    y = rows[0]
    b += f'<rect x="470" y="{y}" width="270" height="{H}" fill="#fff" stroke="{HAIR}"/>'
    b += label(480, y + 16, "images · release · delivery · alerts", size=10, color="currentColor", mono=True)
    b += label(480, y + 30, "candidate → RING=preview", size=10, mono=True)
    b += label(480, y + 42, "main      → RING=live", size=10, mono=True)
    y = rows[1]
    for i, job in enumerate(["bake_api", "bake_web", "bake_worker"]):
        x = 470 + i * 92
        b += box(x, y, 86, H, job, "UNIT=" + job.split("_")[1], fill="#fff", dash=(job == "bake_worker"), bold=False)
    b += label(740, y + H + 12, L["parallel"], size=10, anchor="end")
    y = rows[2]
    b += box(470, y, 130, H, "release", "crane · dotenv", fill="#fff", bold=False)
    b += label(740, y + H / 2 + 4, L["one_release"], size=10, anchor="end")
    y = rows[3]
    b += box(470, y, 130, H, "deliver_north", "CLUSTER=north", fill="#fff", bold=False)
    b += box(610, y, 130, H, "deliver_south", "CLUSTER=south", fill="#fff", bold=False)
    b += label(740, y + H + 12, L["one_per_cluster"], size=10, anchor="end")
    y = rows[4]
    b += box(470, y, 130, H, "alert_failure", "when: on_failure", fill="#fff", bold=False)
    # expansion arrows
    b += arrow(402, rows[0] + H / 2, 468, rows[0] + H / 2, label=L["expands"], lx=435, ly=rows[0] + H / 2 - 8, anchor="middle", mono=False)
    for y in rows[1:]:
        b += arrow(402, y + H / 2, 468, y + H / 2)
    b += label(435, rows[1] + H / 2 - 8, L["hidden_x3"], size=9.5, anchor="middle", mono=True)
    b += label(435, rows[3] + H / 2 - 8, L["hidden_x2"], size=9.5, anchor="middle", mono=True)
    b += label(20, 362, L["fig2_legend"], size=10.5)
    return figure(760, 374, b, L["fig2_caption"], L["fig2_aria"])

# ---------------------------------------------------------------- figure 3: staging vs production
def fig_promote(L):
    b = ""
    b += label(20, 40, L["lane_release"], size=11, weight=600, color="currentColor")
    b += label(20, 170, L["lane_main"], size=11, weight=600, color="currentColor")
    b += f'<line x1="20" y1="126" x2="740" y2="126" stroke="{HAIR}" stroke-dasharray="3 4"/>'
    xs = [60, 230, 400, 570]
    W = 140
    top = [("bake", "3 units"), ("push", ":&lt;sha&gt; · :preview"), ("trigger", "set :&lt;sha&gt;"), ("roll out", "preview")]
    for i, (t, sub) in enumerate(top):
        b += box(xs[i], 50, W, 50, t, sub, fill="#fff")
        if i < len(top) - 1:
            b += arrow(xs[i] + W + 2, 75, xs[i + 1] - 2, 75)
    b += box(xs[0], 180, W, 50, L["no_build"], L["no_build_sub"], fill="#fff", dash=True, bold=False, tcolor=MUTED)
    b += box(xs[1], 180, W, 50, "release", "crane tag", fill="#fff", stroke=ACCENT, tcolor=ACCENT)
    b += box(xs[2], 180, W, 50, "trigger", "set @digest", fill="#fff")
    b += box(xs[3], 180, W, 50, "roll out", "live", fill="#fff")
    b += arrow(xs[0] + W + 2, 205, xs[1] - 2, 205, dash=True)
    b += arrow(xs[1] + W + 2, 205, xs[2] - 2, 205)
    b += arrow(xs[2] + W + 2, 205, xs[3] - 2, 205)
    cx = xs[1] + W / 2
    b += elbow([(cx, 102), (cx, 178)], label=L["same_digest"], lx=cx + 8, ly=144, anchor="start", color=ACCENT)
    b += label(cx + 8, 158, ":preview → :live", size=10, color=ACCENT, mono=True)
    b += label(20, 262, L["fig3_legend"], size=10.5)
    return figure(760, 274, b, L["fig3_caption"], L["fig3_aria"])

# ---------------------------------------------------------------- texts
EN = dict(
    apps_caption="app repositories — each pipeline is a thin include", library="ci-blueprints", library_note="a library: it runs no pipeline of its own",
    include="include · ref: v2.3.0", orders_pipeline="orders pipeline (on push to candidate / main)", runs_on_push="push",
    registry="container registry", push="docker push :sha, :ring", manifests_pipeline="fleet pipeline (runs only when triggered)",
    trigger="trigger", cluster_sub="cluster · namespace per ring", kubectl="kubectl -n <ns>", pull="pull",
    legend="Dashed: a reference resolved at pipeline creation, not a run. Blue: the hand-off between the two pipelines.",
    fig1_caption="Three kinds of repository, two pipelines. App repositories include the blueprint library; their pipeline bakes images and hands a rollout set to the fleet pipeline, which is the only thing that talks to the clusters.",
    fig1_aria="App repositories include a blueprint library; the app pipeline bakes images, pushes them to the registry and triggers the fleet pipeline, which applies manifests, sets images and waits for the rollout on each cluster.",
    library_col="the library (blueprints/orders/)", consumer_col="the consumer", pipeline_col="the pipeline that materialises",
    f_workflow="stages · branch→ring · retry", f_build=".bake hidden job", f_release="digest, re-tag on main", f_deploy=".deliver hidden job", one_release="one job, all units", f_notify="alert on failure / success",
    consumer_note1="four lines of include,", consumer_note2="one variable block —", consumer_note3="nothing else.",
    include_short="include", expands="expands to", hidden_x3="× 3 units", hidden_x2="× 2 clusters",
    parallel="parallel; worker only if SHIP_WORKER", one_per_cluster="one trigger per cluster",
    fig2_legend="Dashed: a file pulled in by include. Dashed job: created only when its ship flag is set.",
    fig2_caption="How five blueprint files become a concrete pipeline. Hidden jobs in the library are extended into one job per unit and one per cluster; the consumer's file only lists includes and flags.",
    fig2_aria="Five blueprint files, included by a short consumer file, expand into a pipeline with three bake jobs, one release job, two delivery jobs and one alert job.",
    lane_release="branch candidate → preview ring", lane_main="branch main → live ring", no_build="no bake", no_build_sub="stage skipped",
    same_digest="same digest", fig3_legend="The live ring never bakes. It releases the image that already ran in preview, by digest, and rolls that out.",
    fig3_caption="Preview bakes; live releases. The main branch re-tags the preview digest and rolls it out — the bytes that ran in preview are the bytes that go live.",
    fig3_aria="Two lanes: the candidate branch bakes, pushes and rolls out to the preview ring; the main branch skips the bake, re-tags the preview digest as live and rolls that out.",
)
PT = dict(
    apps_caption="repositórios de aplicação — cada pipeline é um include fino", library="ci-blueprints", library_note="uma biblioteca: não roda pipeline próprio",
    include="include · ref: v2.3.0", orders_pipeline="pipeline do orders (push em candidate / main)", runs_on_push="push",
    registry="registry de imagens", push="docker push :sha, :ring", manifests_pipeline="pipeline do fleet (só roda quando disparado)",
    trigger="trigger", cluster_sub="cluster · namespace por anel", kubectl="kubectl -n <ns>", pull="pull",
    legend="Tracejado: uma referência resolvida na criação do pipeline, não uma execução. Azul: a passagem de bastão entre os dois pipelines.",
    fig1_caption="Três tipos de repositório, dois pipelines. Os repositórios de aplicação incluem a biblioteca de blueprints; o pipeline deles assa as imagens e entrega um conjunto de rollout ao pipeline do fleet, que é o único que fala com os clusters.",
    fig1_aria="Repositórios de aplicação incluem uma biblioteca de blueprints; o pipeline da aplicação assa as imagens, publica no registry e dispara o pipeline do fleet, que aplica manifests, troca imagens e espera o rollout em cada cluster.",
    library_col="a biblioteca (blueprints/orders/)", consumer_col="o consumidor", pipeline_col="o pipeline que se materializa",
    f_workflow="stages · branch→anel · retry", f_build="job oculto .bake", f_release="digest, re-tag na main", f_deploy="job oculto .deliver", one_release="um job, todas as unidades", f_notify="alerta falha / sucesso",
    consumer_note1="quatro linhas de include,", consumer_note2="um bloco de variáveis —", consumer_note3="nada mais.",
    include_short="include", expands="vira", hidden_x3="× 3 unidades", hidden_x2="× 2 clusters",
    parallel="paralelos; worker só com SHIP_WORKER", one_per_cluster="um trigger por cluster",
    fig2_legend="Tracejado: um arquivo trazido pelo include. Job tracejado: criado só quando a flag de envio está ligada.",
    fig2_caption="Como cinco arquivos de blueprint viram um pipeline concreto. Os jobs ocultos da biblioteca são estendidos em um job por unidade e um por cluster; o arquivo do consumidor só lista includes e flags.",
    fig2_aria="Cinco arquivos de blueprint, incluídos por um arquivo curto do consumidor, expandem para um pipeline com três jobs de bake, um de release, dois de entrega e um de alerta.",
    lane_release="branch candidate → anel preview", lane_main="branch main → anel live", no_build="sem bake", no_build_sub="estágio pulado",
    same_digest="mesmo digest", fig3_legend="O anel live nunca assa. Ele libera a imagem que já rodou em preview, por digest, e faz o rollout dela.",
    fig3_caption="Preview assa; live libera. A branch main re-etiqueta o digest de preview e faz o rollout — os bytes que rodaram em preview são os bytes que entram no ar.",
    fig3_aria="Duas raias: a branch candidate assa, publica e faz rollout no anel preview; a branch main pula o bake, re-etiqueta o digest de preview como live e faz o rollout dele.",
)
FIGS = {lang: (fig_repos(L), fig_templates(L), fig_promote(L)) for lang, L in (("en", EN), ("pt-br", PT))}

# ---------------------------------------------------------------- YAML blocks (shared)
Y_CONSUMER = '''```yaml
# orders/.gitlab-ci.yml — the whole file
include:
  - project: platform/ci-blueprints
    ref: v2.3.0            # a tag, never main
    file:
      - blueprints/orders/routine.yml
      - blueprints/orders/images.yml
      - blueprints/orders/release.yml
      - blueprints/orders/delivery.yml
      - blueprints/orders/alerts.yml

variables:
  SHIP_WORKER: "true"      # units opt in one at a time
```'''

Y_WORKFLOW = '''```yaml
# blueprints/orders/routine.yml — what a branch means, for every consumer
stages: [images, release, delivery, alerts]

workflow:
  rules:
    - if: '$CI_COMMIT_BRANCH == "candidate"'
      variables: { RING: preview }
    - if: '$CI_COMMIT_BRANCH == "main"'
      variables: { RING: live }
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

# Shell library, pulled into jobs with `!reference [.lib, shell]`.
.lib:
  shell: |
    # probe: 0 = present · 1 = absent · 2 = unknown (caller must stop)
    probe() {   # $1=namespace $2=kind $3=name
      for n in 1 2 3; do
        out=$(kubectl -n "$1" get "$2" "$3" -o name 2>&1 >/dev/null) \\
          && return 0
        case "$out" in *NotFound*) return 1 ;; esac
        sleep $((n * 5))
      done
      echo "unknown: $2/$3 in $1" >&2; return 2
    }
    attempt() {
      for n in 1 2 3; do "$@" && return 0; sleep $((n * 5)); done
      return 1
    }
```'''

Y_BUILD = '''```yaml
# blueprints/orders/images.yml — bake one image per unit
.bake:
  stage: images
  image: docker:27
  services: [docker:27-dind]
  rules:
    - if: '$RING == "preview"'          # the live ring never bakes
  variables:
    IMAGE: $CI_REGISTRY_IMAGE/$UNIT
  script:
    - echo "$CI_REGISTRY_PASSWORD" | docker login -u "$CI_REGISTRY_USER" \\
        --password-stdin "$CI_REGISTRY"
    - docker build -t "$IMAGE:$CI_COMMIT_SHA" \\
        --build-arg RING="$RING" \\
        -f "$SRC/Dockerfile" "$SRC"
    - docker push "$IMAGE:$CI_COMMIT_SHA"
    - docker tag "$IMAGE:$CI_COMMIT_SHA" "$IMAGE:$RING"
    - docker push "$IMAGE:$RING"

bake_api:
  extends: .bake
  variables: { UNIT: api, SRC: services/api }

bake_web:
  extends: .bake
  variables: { UNIT: web, SRC: web }

bake_worker:
  extends: .bake
  variables: { UNIT: worker, SRC: services/worker }
  rules:
    - if: '$RING == "preview" && $SHIP_WORKER == "true"'
```'''

Y_DEPLOY = '''```yaml
# blueprints/orders/delivery.yml — hand the rollout set to the fleet
.deliver:
  stage: delivery
  rules:
    - if: '$RING =~ /^(preview|live)$/'
  trigger:
    project: platform/fleet
    strategy: depend          # wait for the child; inherit its result
    forward: { pipeline_variables: true }
  variables:
    APP: orders
    RING: $RING
    ORIGIN_SHA: $CI_COMMIT_SHA
    ROLLOUT_SET: |
      [
        {"unit":"api",    "container":"api",    "image":"$API_IMAGE"},
        {"unit":"web",    "container":"web",    "image":"$WEB_IMAGE"},
        {"unit":"worker", "container":"worker", "image":"$WORKER_IMAGE"}
      ]

deliver_north: { extends: .deliver, variables: { CLUSTER: north } }
deliver_south: { extends: .deliver, variables: { CLUSTER: south } }
```'''

Y_PROMOTE = '''```yaml
# blueprints/orders/release.yml
# On main it re-tags preview as live; on candidate it only resolves digests.
release:
  stage: release
  image: gcr.io/go-containerregistry/crane:debug
  script:
    - |
      for unit in api web worker; do
        img="$CI_REGISTRY_IMAGE/$unit"
        if [ "$RING" = "live" ]; then
          digest=$(crane digest "$img:preview")   # what preview runs now
          crane tag "$img@$digest" live           # same bytes, new name
        else
          digest=$(crane digest "$img:$CI_COMMIT_SHA")
        fi
        key=$(echo "$unit" | tr a-z A-Z)
        echo "${key}_IMAGE=$img@$digest" >> images.env
      done
  artifacts:
    reports: { dotenv: images.env }   # *_IMAGE reach the delivery jobs
```'''

Y_MANIFESTS = '''```yaml
# platform/fleet/.gitlab-ci.yml — the only pipeline that touches a cluster
workflow:
  rules:
    - if: '$CI_PIPELINE_SOURCE == "pipeline"'   # an app pipeline fired it
    - if: '$CI_PIPELINE_SOURCE == "web"'        # or someone pressed Run
    - when: never

rollout:
  stage: rollout
  image: bitnami/kubectl:1.31
  resource_group: $CLUSTER/$APP/$RING   # one rollout at a time per target
  script:
    - |
      set -euo pipefail
      # one file-type variable per cluster: KUBECONFIG_NORTH, ...
      eval "export KUBECONFIG=\\$KUBECONFIG_$(echo "$CLUSTER" | tr a-z A-Z)"
      NS="$APP-$RING"                       # namespaces follow one convention
      DIR="$CLUSTER/$APP/$RING"

      kubectl -n "$NS" apply -f "$CLUSTER/$APP/common/$RING/"
      kubectl -n "$NS" apply -f "$DIR/"

      echo "$ROLLOUT_SET" \\
        | jq -c '.[] | select(.image | test("@sha256"))' \\
        | while read -r entry; do
            unit=$(jq -r .unit <<<"$entry")
            container=$(jq -r .container <<<"$entry")
            image=$(jq -r .image <<<"$entry")
            kubectl -n "$NS" set image deployment \\
              -l "app=$APP,unit=$unit" "$container=$image"
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
# blueprints/orders/alerts.yml
alert_failure:
  stage: alerts
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
      PAYLOAD=$(jq -n --arg title "$title ($RING)" \\
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
# end of the fleet rollout job — success only; a failure exited above
digest=$(kubectl -n "$NS" get deploy -l "app=$APP,unit=api" \\
  -o jsonpath='{.items[0].spec.template.spec.containers[0].image}' \\
  | sed 's/.*@sha256://' | head -c 12)
jq -n --arg t ":large_green_circle: orders → $RING on $CLUSTER" \\
      --arg d "api @ $digest…" --arg u "$CI_JOB_URL" \\
  '{blocks:[{type:"section",text:{type:"mrkdwn",
     text:("*"+$t+"*\\n"+$d+"  <"+$u+"|job>")}}]}' \\
  | curl -sS -o /dev/null -X POST -H 'Content-type: application/json' \\
         -d @- "$SLACK_WEBHOOK_URL" || true
```'''

# ---------------------------------------------------------------- snippets as files
# Each block above is written under static/snippets/<article>/ and the article
# embeds it with the snippet shortcode, so readers get copy, raw and curl.
SNIP_DIR = SITE.parent / "static/snippets/gitlab-ci-blueprints"
SNIP_DIR.mkdir(parents=True, exist_ok=True)

def snippet(name, block, lang):
    body = block.strip()
    assert body.startswith("```") and body.endswith("```"), name
    body = body.split("\n", 1)[1].rsplit("\n", 1)[0]
    (SNIP_DIR / name).write_text(body + "\n")
    return f'{{{{< snippet file="gitlab-ci-blueprints/{name}" lang="{lang}" >}}}}'

Y_CONSUMER  = snippet("orders.gitlab-ci.yml", Y_CONSUMER,  "yaml")
Y_WORKFLOW  = snippet("routine.yml",          Y_WORKFLOW,  "yaml")
Y_BUILD     = snippet("images.yml",           Y_BUILD,     "yaml")
Y_DEPLOY    = snippet("delivery.yml",         Y_DEPLOY,    "yaml")
Y_PROMOTE   = snippet("release.yml",          Y_PROMOTE,   "yaml")
Y_MANIFESTS = snippet("fleet.gitlab-ci.yml",  Y_MANIFESTS, "yaml")
Y_NOTIFY    = snippet("alerts.yml",           Y_NOTIFY,    "yaml")
Y_SUCCESS   = snippet("alert-success.sh",     Y_SUCCESS,   "bash")

# ---------------------------------------------------------------- article bodies
def article_en(f1, f2, f3):
    return f"""---
title: "GitLab CI for Kubernetes: a blueprint library for many apps and many clusters"
date: 2026-09-17T09:00:00-04:00
draft: false
translationKey: "gitlab-ci-blueprints"
categories: ["Technology"]
tags: ["gitlab-ci", "kubernetes", "devops", "delivery"]
description: "A delivery architecture that survived several apps, two rings and more than one cluster: a versioned blueprint library, thin app pipelines, a fleet repository that is the only thing talking to Kubernetes, and a live ring that releases what preview already ran instead of building again."
aliases: ["/writing/gitlab-ci-template-library/"]
---

Three apps, each with three or four deployable units. Two rings — preview and
live. More than one Kubernetes cluster, run by different teams. The first
version of that delivery was what it always is: a `.gitlab-ci.yml` copied from
the last project, edited until green, and never the same twice. A year later no
two pipelines agreed on what a branch meant, and a fix in one never reached
the others.

What follows is the architecture that replaced it. Names, paths and numbers
are illustrative; the shape is the thing.

## The shape

{f1}

There are three kinds of repository and only two pipelines:

| Repository | Holds | Its pipeline |
|---|---|---|
| `platform/ci-blueprints` | The library: one folder per app, five YAML files each | None. It is only ever `include`d |
| `orders`, `billing`, … | The application code and a `.gitlab-ci.yml` of a dozen lines | Bakes images, releases, hands off to the fleet pipeline, alerts |
| `platform/fleet` | Kubernetes manifests, `<cluster>/<app>/<ring>/` | Runs only when triggered. Applies, sets images, waits for the rollout |

Nothing in an app repository knows how to reach a cluster. Nothing in the
fleet repository knows how to bake an image. The hand-off between them is a
single JSON variable, and that boundary is what keeps both sides simple.

## The consumer: a dozen lines

{Y_CONSUMER}

The `ref` is a tag. `main` is for trying a change in one app before you cut
`v2.4.0` and move the others. The file list is explicit on purpose: **the
names are a contract**. Adding a sixth file means every consumer adds a line;
renaming one means every consumer breaks — so files are added, never renamed.

The `SHIP_*` flags are how a new unit, or a new library version, rolls in one
piece at a time. A unit whose flag is off has no job at all, not a skipped one.

## From five files to a pipeline

{f2}

### routine.yml: what a branch means

{Y_WORKFLOW}

Three decisions live here and nowhere else. **A branch maps to exactly one
ring**, and a branch that maps to nothing creates no pipeline — the `when:
never` at the end of the `workflow:` block is not decoration. **Retries cover
infrastructure and not code**: adding `script_failure` would rerun a genuinely
broken bake three times and hide the defect behind a green badge on the
fourth. And **the shell library is shared with `!reference`**, so the retry
with backoff and the three-state probe are written once. That third state
matters: a network flap during `kubectl get` used to look exactly like
"absent", and a job would carry on with the wrong assumption. Not being able
to tell is its own answer, and the caller stops on it.

### images.yml: one hidden job, one concrete job per unit

{Y_BUILD}

The hidden job does the work; each concrete job is two variables. They run in
parallel, since nothing in `bake_web` depends on `bake_api`. Every image is
pushed twice: as `:<sha>`, which is what will be rolled out and never moves,
and as `:preview`, a floating pointer to "what the preview ring runs now" that
the release step will read.

### delivery.yml: the hand-off

{Y_DEPLOY}

`strategy: depend` makes the parent wait for the child and fail if it fails —
the app pipeline's badge tells the truth about the rollout, not just the bake.
One delivery job per cluster is the whole multi-cluster story: same fleet
repository, same variables, different `CLUSTER`.

`ROLLOUT_SET` is the contract across the boundary: which unit, which
container name inside the pod, which image. The fleet side needs nothing else
to update a deployment.

## Live is a release, not a rebuild

{f3}

{Y_PROMOTE}

The `main` branch skips the bake stage entirely. Rebuilding from the same
commit would *probably* produce the same image; releasing by digest produces
the same image by definition. The dotenv report is how the digests reach the
delivery jobs — GitLab expands `$API_IMAGE` inside `ROLLOUT_SET` before it
hands the variable to the child pipeline.

## The fleet pipeline

Manifests live per cluster, per app, per ring, with a `common/` folder for the
ConfigMap and Secret every unit reads. Namespaces follow one convention,
`<app>-<ring>`, so nobody has to declare them:

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

{Y_MANIFESTS}

Four things are doing the real work here.

**It only runs when triggered.** A push to the fleet repository changes files
and nothing else; the cluster changes when an app pipeline says so, with a
rollout set attached.

**`apply` and `set image` do not fight.** The versioned manifest says
`image: …/api:preview`; the live object ends up with `…/api@sha256:…`. The
next `apply` looks like it should revert that — it does not. Client-side apply
patches only the fields that changed between the last-applied manifest and
the new one, and the image line is identical in both, so the digest set by
the pipeline survives. Break that premise by editing the tag in the manifest
and you get a second rollout per delivery.

**`resource_group` serialises per target.** Two pipelines for the same app
and ring queue instead of racing. The group key includes the app so that
`orders` and `billing` on the same cluster still roll out in parallel.

**A failed rollout explains itself.** `describe` and the last hundred lines
of logs go into the job output before it exits red — the person who opens
the job at 2 a.m. should not need cluster access to see why.

## Telling someone

{Y_NOTIFY}

On failure, always: branch, ring, author, commit, one button. On success, one
line from the rollout job with the digest that went live:

{Y_SUCCESS}

The webhook URL is a masked, protected CI/CD variable on the consumer
project; a project without one simply logs that it skipped the alert.

## Where each setting lives

| Setting | Where | Why there |
|---|---|---|
| Branch → ring | `routine.yml` in the library | One truth for every app |
| Registry credentials | GitLab's own `CI_REGISTRY_*` | Never typed anywhere |
| Kubeconfig per cluster | File-type variable on `platform/fleet`, protected | Only the fleet pipeline can reach a cluster |
| `SLACK_WEBHOOK_URL` | Masked variable on each consumer | Each app owns its channel |
| `SHIP_<UNIT>` | `variables:` in the consumer's file | Visible in the diff that turns a unit on |
| Library version | `ref:` in the consumer's `include` | Upgrades are a reviewed commit, not a surprise |

## What bit us, so it does not bite you

| Symptom | Cause | Rule |
|---|---|---|
| Rollout green, image unchanged | New unit added to `images.yml` and `ROLLOUT_SET` but the manifest lacks the `unit:` label, so `set image -l` matched nothing | Adding a unit touches **three** places: bake job, rollout-set entry, manifest label |
| Five units rolling out one after another | `resource_group` without the app in its key | The key names exactly what must not overlap |
| A failed command, no error, job continues | `OUT=$(cmd 2>&1)` under `set -e`: the assignment swallows the exit status | Use the command as the condition of an `if`, capture output inside |
| A flaky bake "fixed" by retry | `script_failure` in `default.retry` | Retry infrastructure, never code |
| A step skipped because a Deployment "was absent" — it was not | Network flap indistinguishable from `NotFound` | Three states, stop on the third |
| Clone of a 30 MB repo to run `kubectl apply` | Default `GIT_STRATEGY` on a job that never reads the tree | `GIT_STRATEGY: none` when the working tree is not needed |

None of this is exotic GitLab. It is `include`, hidden jobs, `workflow:`
rules, one multi-project trigger and a JSON variable — arranged so that adding
the fourth app is a folder in the library and a dozen lines in the app, and so
that the live ring only ever runs bytes that preview already ran.
"""

def article_pt(f1, f2, f3):
    return f"""---
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

{f1}

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

{Y_CONSUMER}

O `ref` é uma tag. `main` serve para experimentar uma mudança em uma app antes
de cortar a `v2.4.0` e migrar as outras. A lista de arquivos é explícita de
propósito: **os nomes são um contrato**. Adicionar um sexto arquivo significa
que cada consumidor acrescenta uma linha; renomear um significa que cada
consumidor quebra — então arquivos são adicionados, nunca renomeados.

As flags `SHIP_*` são como uma unidade nova, ou uma versão nova da biblioteca,
entra uma peça de cada vez. Uma unidade com a flag desligada não tem job
nenhum, não um job pulado.

## De cinco arquivos a um pipeline

{f2}

### routine.yml: o que uma branch significa

{Y_WORKFLOW}

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

{Y_BUILD}

O job oculto faz o trabalho; cada job concreto são duas variáveis. Rodam em
paralelo, já que nada em `bake_web` depende de `bake_api`. Toda imagem é
publicada duas vezes: como `:<sha>`, que é o que será implantado e nunca se
move, e como `:preview`, um ponteiro flutuante para "o que o anel preview roda
agora" que o passo de release vai ler.

### delivery.yml: a passagem de bastão

{Y_DEPLOY}

`strategy: depend` faz o pai esperar o filho e falhar se ele falhar — o selo
do pipeline da aplicação diz a verdade sobre o rollout, não só sobre o bake.
Um job de entrega por cluster é toda a história de multi-cluster: mesmo
repositório de frota, mesmas variáveis, `CLUSTER` diferente.

`ROLLOUT_SET` é o contrato através da fronteira: qual unidade, qual nome de
container dentro do pod, qual imagem. O lado da frota não precisa de mais
nada para atualizar um deployment.

## Live é release, não rebuild

{f3}

{Y_PROMOTE}

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

{Y_MANIFESTS}

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

{Y_NOTIFY}

Na falha, sempre: branch, anel, autor, commit, um botão. No sucesso, uma linha
do job de rollout com o digest que entrou no ar:

{Y_SUCCESS}

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
"""

(SITE / "en/writing/gitlab-ci-blueprints.md").write_text(article_en(*FIGS["en"]))
(SITE / "pt-br/artigos/gitlab-ci-blueprints.md").write_text(article_pt(*FIGS["pt-br"]))
print("written")
