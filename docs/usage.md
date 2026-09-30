# Usage

The runner uses Python 3 and the official Clay CLI on macOS or Linux. No Python packages, OpenAI API key, browser cookie export or Codex installation are required. Fresh runs need a Clay account with Builder and workflow access and enough existing credits. This experiment used Clay CLI `1.4.0+de2a0396a538`.

## Docker setup

Use Docker Engine or Docker Desktop with Compose. Run `docker compose build`, then:

```sh
docker compose run --rm --entrypoint clay eval login --device
docker compose run --rm eval doctor
docker compose run --rm eval setup
```

Open the device link, choose your workspace and authorize the CLI. Website sign-in alone is not enough. Complete the Builder connection below, then run `docker compose run --rm eval bind-refresh`.

For every native `./eval` command below, the Docker equivalent is `docker compose run --rm eval`. Use `/results/my-run` as the output path inside Docker. It maps to `runs/my-run` on the host. The repository is mounted read-only. Credentials and workflow state use separate persistent Docker volumes. Preserve those volumes to resume; `docker compose down --volumes` deletes them. Docker does not reuse a native installation's credentials or workflow bindings.

Python 3.13.15 and Clay CLI 1.4.0 are pinned with an image digest and binary checksums. The container was built and tested on Linux ARM64. An official AMD64 binary is configured but was not executed in this verification. Fresh-checkout setup and offline replay were tested. The paid comparison was executed natively with the same runner and CLI version; authenticated container research was not separately replayed.

After building the image, disable networking for saved-result reproduction:

```sh
CLAY_NETWORK_MODE=none docker compose run --rm eval reproduce --output /results/exploratory-001
```

## Native setup

1. Clone this repository and enter its directory.
2. Install the CLI using Clay's [official setup instructions](https://github.com/clay-run/agent-plugins/blob/main/clay/skills/setup/SKILL.md). Put `clay` on PATH, or set `CLAY_BIN` to its absolute path. The official native installer verifies the downloaded binary checksum and preserves compatible installations.
3. Run `clay login --device`. Open the printed link, choose the workspace and authorize the CLI. Website sign-in alone is not sufficient. If several workspaces are connected, use `clay workspaces list` and `clay workspaces switch <id>`.
4. Run `./eval doctor`, then `./eval setup`. Setup creates both workflows, manual triggers and GPT-5.4 agents from the checked-in files. It prints their IDs and workflow links. Repeating setup reuses the resources recorded in ignored `.local/state.json`.
5. Complete the connection step below, then run `./eval bind-refresh`. It attaches B's saved version, restores any whitespace formatting introduced by Builder, and checks exact prompt, model, schema, input mappings and graph equality. It starts no model runs.

## Connect Keenable once

Open **Funding lifecycle evaluation B** in Claygent Builder, using the agent ID printed by setup to distinguish it from any older experiment.

1. Under Tools, keep **Web search** enabled.
2. Add a custom MCP server named **Keenable public evaluation** with URL `https://api.keenable.ai/mcp`. Leave the API key empty for the public tier.
3. Enable that connection and save the agent.
4. Verify A has Web search enabled and Keenable disabled. Keep other private connectors, account context and business context disabled on both.

This setting is not exposed by the inspected official CLI node schema. The runner therefore uses one manual Builder step, then the official CLI for all runs. It never replays private browser endpoints or stores browser credentials. [A configuration](../evidence/variant-a-settings.png) · [B configuration](../evidence/variant-b-settings.png).

The [public Keenable tier](https://docs.keenable.ai/rate-limits) is unbilled and allows 1,000 requests per hour, at most 10 per second, shared per IP. Clay may use shared egress. A rate-limit failure must be recorded, not bypassed. Authenticated Keenable setup was not tested here.

## Run and resume

Start with the first pair while keeping the full 50-company plan:

```sh
./eval run --output runs/my-run --concurrency 4 --stop-after-pairs 1 --allow-credit-use
```

Inspect the saved answers and tool traces. Continue all remaining pairs:

```sh
./eval run --output runs/my-run --concurrency 4 --timeout 1200 --allow-credit-use
```

The script automatically submits up to four runs concurrently. A/B submission order alternates across companies. It saves each returned run ID before polling. Terminal runs are not repeated. A polling timeout leaves the original run available for resume.

- `--limit N` freezes a smaller plan at the first invocation. Keep that limit when resuming.
- `--stop-after-pairs N` is an operational checkpoint, not a new dataset.
- `--concurrency 1..4` changes in-flight capacity. Each invocation is recorded; it does not change prompts or answers.
- `--timeout SECONDS` controls polling time per run (default 600). It never resubmits a timed-out run.
- `--allow-credit-use` permits spending existing Clay credits. No command purchases credits or changes a plan.

Keep one runner process per checkout. To resume, preserve `.local/` and the run directory, resolve the interruption, and repeat the same command. Changed inputs, model, prompt, schema or workflow bindings stop resume. An ambiguous submission stops for inspection of its saved call and Clay run history. Do not delete its records or start a fresh directory as a retry.

If setup reports an ambiguous mutation, inspect the saved `.local/` journal and actual workflow before recovery. The runner will not blindly duplicate it.

## Reproduce and grade

```sh
./eval reproduce --output runs/exploratory-001
```

This reads saved files only and rebuilds `summary.json` and the per-company `results.md` table. It does not need Clay authentication, credits or the reference file. Saved judgments are the factual scoring input; reproduction recomputes their aggregates, not a new independent judgment of the sources.

For a fresh run, review every answer against the [scoring rules](methodology.md), then save `judgments.json` in its run directory. Without judgments, reproduction reports execution, tool use, time and credits only. Partial judgment coverage is explicitly labeled.

```json
{
  "cases": [
    {
      "case_id": "example",
      "arm": "A",
      "scored_task": "funding_and_lifecycle",
      "fields": {"funding_stage": true, "announcement_date": false},
      "supported_answer": false,
      "notes": "Explain the evidence and any ambiguity."
    }
  ]
}
```

Use `null` only for a target that cannot be fairly scored, with an explanation. `supported_answer` refers to the predeclared target facts, not all unscored claims. Keep evidence checks and corrections beside the judgments. Score entity resolution separately.

Run local safety checks with `python3 -m unittest -v test_eval.py`. Credentials remain in Clay's credential store. Never commit `.local/`, `.env` or API keys.
