# end of the manifests deploy job — success only; a failure exited above
digest=$(kubectl -n "$NS" get deploy -l "app=$APP,part=api" \
  -o jsonpath='{.items[0].spec.template.spec.containers[0].image}' \
  | sed 's/.*@sha256://' | head -c 12)
jq -n --arg t ":large_green_circle: orders → $ENVIRONMENT on $CLUSTER" \
      --arg d "api @ $digest…" --arg u "$CI_JOB_URL" \
  '{blocks:[{type:"section",text:{type:"mrkdwn",
     text:("*"+$t+"*\n"+$d+"  <"+$u+"|job>")}}]}' \
  | curl -sS -o /dev/null -X POST -H 'Content-type: application/json' \
         -d @- "$SLACK_WEBHOOK_URL" || true
