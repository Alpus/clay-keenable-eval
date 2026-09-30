# Keenable Eval for Claygent

[Claygent](https://university.clay.com/docs/claygent-builder) researches companies using web search. This experiment tests whether adding [Keenable](https://keenable.ai/) improves its answers about the latest funding and current ownership status.

50 companies, three conditions, GPT-5.4. The task comes from [dated user reports](docs/evidence.md).

- **A:** native Clay search.
- **B:** the same prompt, with Keenable available.
- **C:** native research followed by an explicit Keenable verification step.

## Results

All 150 answers completed and were reviewed against sources on September 30, 2026.

| | A: native | B: optional Keenable | C: prompted verification |
| --- | ---: | ---: | ---: |
| Companies with all target facts correct and supported | **38/47** | **39/47** | **42/47** |
| Runs that used Keenable | 0/50 | 10/50 | 49/50 |
| Clay data credits | 176.5 | 206.2 | 207.3 |
| Clay action credits | 50 | 50 | 50 |

Two companies (MangoBoost and Abridge) have unresolved latest-funding evidence and remain unscored. The separate Freeman entity probe passed in all three conditions. Excluding Keenable itself gives 37/46, 38/46 and 41/46. Scores cover preselected target facts, not every claim in an answer.

**Where Keenable helped:** C used Keenable search and fetch to find a [company-issued Lessn disclosure](https://www.ad-hoc-news.de/boerse/news/unternehmensnachrichten/sydney-au-mar-3-2026-acn-newswire-accounts-payable-automation/68628893) reporting a $300,000 investment in November 2025. A/B stopped at the earlier August round. The saved trace supports this retrieval attribution. C also found Wayve's later extension, but native tools established the final precise facts, so that improvement cannot be attributed solely to Keenable.

**Where it did not solve the problem:** all conditions missed later extensions for ElevenLabs and Harvey. All got the 21 lifecycle statuses right. C still made additional errors outside those targets, including a wrong historical funding claim for Circle. All four B field-score wins over A occurred without calling Keenable, so those gains do not establish a Keenable contribution. Merely enabling Keenable had little aggregate effect; the prompted strategy did better in this exploratory run, with higher credit use and a changed prompt.

[All company results](runs/comparison/results.md) · [Scores and sources](runs/comparison/judgments.json) · [Retrieval audit](evidence/retrieval-audit.json)

Seven C attempts failed during MCP initialization, with zero reported credits. Each was retried once; all attempts are preserved. The 150 answers consumed 590 data credits and 150 actions, excluding setup smoke tests.

## How to run

Use Docker with Compose. Python and the official Clay CLI are pinned in the image.

### Reproduce saved results

```sh
git clone https://github.com/Alpus/clay-keenable-eval.git
cd clay-keenable-eval
docker compose build
CLAY_NETWORK_MODE=none docker compose run --rm eval reproduce --output /results/comparison
```

After the image is built, this runs without network access, credentials or credits. It recalculates metrics from saved answers and reviewed judgments.

### Run a fresh comparison

1. Authorize Clay and create the three agents:

   ```sh
   docker compose run --rm --entrypoint clay eval login --device
   docker compose run --rm eval setup
   docker compose run --rm eval setup --strategy verify
   ```

2. [Enable Keenable in B and C once in Builder](docs/usage.md#connect-keenable-once), then bind their saved versions:

   ```sh
   docker compose run --rm eval bind-refresh
   docker compose run --rm eval bind-refresh --strategy verify
   ```

3. Run the comparison:

   ```sh
   docker compose run --rm eval run --output /results/my-ab --timeout 1200 --allow-credit-use
   docker compose run --rm eval run --strategy verify --output /results/my-c --timeout 1200 --allow-credit-use
   docker compose run --rm eval compare --baseline /results/my-ab --variant /results/my-c --output /results/my-comparison
   ```

The default is 30 in-flight runs, with starts spaced by two seconds to reduce request bursts. The second run submits only C; it does not repeat A/B. Repeat a run command to resume. Results appear under `runs/`. Fresh runs consume existing Clay credits. New factual scores require [source review](docs/usage.md#reproduce-and-grade).

## Details

All three conditions have native web search. B may choose Keenable; C is instructed to use it for gaps, conflicts and freshness checks. C was added after inspecting A/B and tests a changed research strategy, not a pure search-engine substitution. Tool-step summaries show actual use but truncate many response bodies. This is a purposive exploratory sample, not a representative benchmark.

[Method and scoring](docs/methodology.md) · [Complaint evidence](docs/evidence.md) · [Setup and resume](docs/usage.md)

`eval` is the only runner. `cases.json` contains agent inputs; `ground-truth.json` contains separate reference facts. `prompt.txt`, `prompt-verify.txt` and `output-schema.json` define the agents. Saved runs contain configurations, answers, traces, charges and judgments. Credentials are excluded.
