# Keenable Eval for Claygent

[Claygent](https://university.clay.com/docs/claygent-builder) researches companies using web search. This experiment tests whether adding [Keenable](https://keenable.ai/) improves its answers about the latest funding and current ownership status.

50 companies, two agents, one shared GPT-5.4 prompt: native Clay search versus native search plus Keenable. The task comes from [dated user reports](docs/evidence.md).

## Results

The 100-run comparison is in progress. Results will include correct target facts, paired wins and losses, actual Keenable use, and observed Clay credits. No overall winner is claimed yet.

## How to run

Use Docker with Compose. Python and the official Clay CLI are pinned in the image.

### Reproduce saved results

```sh
git clone https://github.com/Alpus/clay-keenable-eval.git
cd clay-keenable-eval
docker compose build
CLAY_NETWORK_MODE=none docker compose run --rm eval reproduce --output /results/exploratory-001
```

After the image is built, this runs without network access, credentials or credits. It recalculates metrics from saved answers and reviewed judgments.

### Run a fresh comparison

1. Authorize Clay and create the two agents:

   ```sh
   docker compose run --rm --entrypoint clay eval login --device
   docker compose run --rm eval setup
   ```

2. [Connect Keenable once in Builder](docs/usage.md#connect-keenable-once), then run:

   ```sh
   docker compose run --rm eval bind-refresh
   docker compose run --rm eval run --output /results/my-run --concurrency 4 --timeout 1200 --allow-credit-use
   ```

The script schedules all 100 runs automatically, with up to four in flight. Repeat the run command to resume. Results appear in `runs/my-run`. Fresh runs consume existing Clay credits. New factual scores require reviewing the answers against sources. [Native setup, smaller runs and grading](docs/usage.md).

## Details

The comparison gives both agents native web search. B may also use Keenable; it is not forced to. Tool traces show actual use. Sources and reference facts were collected independently of Keenable. This is a purposive exploratory sample with one attempt per condition, not a representative benchmark.

[Method and scoring](docs/methodology.md) · [Complaint evidence](docs/evidence.md) · [Setup and resume](docs/usage.md)

`eval` is the only runner. `cases.json` contains agent inputs; `ground-truth.json` contains separate reference facts. `prompt.txt` and `output-schema.json` define the shared agent. Saved runs contain configurations, answers, traces, charges and judgments. Credentials are excluded.
