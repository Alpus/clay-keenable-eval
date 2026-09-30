# Keenable Eval for Claygent

[Clay](https://www.clay.com/) enriches customer data. [Claygent](https://university.clay.com/docs/claygent-builder) researches companies using web search.

![Clay table with company domains, an enriched company column and extracted URLs](evidence/clay-table.png)

*It works like a spreadsheet with AI-powered columns.*

This experiment tests whether [Keenable](https://keenable.ai/) improves answers about the latest funding and current ownership status.

The hypothesis comes from [user reports available online](docs/evidence.md).

## Results

**Keenable with explicit verification prompting improved results.**

All 200 answers completed and were reviewed against sources on September 30, 2026.

| | A: native | B: optional Keenable | C: Keenable verification | D: native verification |
| --- | ---: | ---: | ---: | ---: |
| Companies with all target facts correct and supported | **38/47** | **39/47** | **42/47** | **38/47** |
| Runs that used Keenable | 0/50 | 10/50 | 49/50 | 0/50 |
| Clay data credits | 176.5 | 206.2 | 207.3 | 204.3 |
| Clay action credits | 50 | 50 | 50 | 50 |

Two companies (MangoBoost and Abridge) have unresolved latest-funding evidence and remain unscored. The separate Freeman entity probe passed in all four conditions. Excluding Keenable itself gives 37/46, 38/46, 41/46 and 37/46. Scores cover preselected target facts, not every claim in an answer.

**Concrete benefit:** C used Keenable to retrieve a [Lessn disclosure](https://www.ad-hoc-news.de/boerse/news/unternehmensnachrichten/sydney-au-mar-3-2026-acn-newswire-accounts-payable-automation/68628893) of a $300,000 investment in November 2025. A/B stopped at the earlier August round.

**Limits:** all conditions missed later extensions for ElevenLabs and Harvey. All four B field-score wins occurred without using Keenable. D repeated C’s verification prompt using native tools instead of Keenable and scored 38/47. This later, single-run control supports the prompted Keenable result, but does not establish a repeatable provider advantage. [Case findings and remaining errors](docs/methodology.md#result-interpretation).

[All company results](runs/comparison-abcd/results.md) · [Scores and sources](runs/comparison-abcd/judgments.json) · [Retrieval audit](evidence/retrieval-audit.json)

Seven C attempts failed during MCP initialization, with zero reported credits. Each was retried once; all attempts are preserved. The 200 answers consumed 794.3 data credits and 200 actions, excluding setup smoke tests.

## How to run

Use Docker with Compose. Python and the official Clay CLI are pinned in the image.

### Reproduce saved results

```sh
git clone https://github.com/Alpus/clay-keenable-eval.git
cd clay-keenable-eval
docker compose build
CLAY_NETWORK_MODE=none docker compose run --rm eval reproduce --output /results/comparison-abcd
```

After the image is built, this runs without network access, credentials or credits. It recalculates metrics from saved answers and reviewed judgments.

### Run a fresh comparison

Follow the [three setup and run steps](docs/usage.md#fresh-comparison-with-docker). Clay authorization and a one-time Builder connection are required; the script creates the agents and runs A/B, then C. The [native verification control](docs/usage.md#native-verification-control-d) adds D. Fresh runs spend existing Clay credits. New factual scores require source review.

The default is **30 concurrent runs**, with starts spaced by two seconds. Repeat a run command to resume without repeating completed answers.

## Details

All four conditions have native web search. B may choose Keenable; C is instructed to use it for gaps, conflicts and freshness checks. C was added after inspecting A/B and tests a changed research strategy, not a pure search-engine substitution. D preserves C’s verification instructions but uses native search and page reading, with Keenable disabled. Tool-step summaries show actual use but truncate many response bodies. This is a purposive exploratory sample, not a representative benchmark.

[Method and scoring](docs/methodology.md) · [Complaint evidence](docs/evidence.md) · [Setup and resume](docs/usage.md)

`eval` is the only runner. `cases.json` contains agent inputs; `ground-truth.json` contains separate reference facts. `prompt.txt`, `prompt-verify.txt`, `prompt-verify-native.txt` and `output-schema.json` define the agents. Saved runs contain configurations, answers, traces, charges and judgments. Credentials are excluded.
