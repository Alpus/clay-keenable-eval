# Claygent + Keenable evaluation

## About

Does Keenable help an already-searching Claygent find better evidence about company funding and ownership?

This repository compares two GPT-5.4 Claygents with the same prompt, inputs and output fields. A uses native Clay search. B also has Keenable search and fetch. B chooses its tools; it is not forced to use Keenable. The test contains 50 preselected companies, including recent rounds, completed acquisitions, public listings and a separate same-name company probe.

The task comes from dated Clay community reports. [EVIDENCE.md](EVIDENCE.md) distinguishes recurring business problems from old bugs, feature requests and already-suggested fixes. [DESIGN.md](DESIGN.md) explains selection and scoring.

## Results

The paired company evaluation is in progress. Successful integration smoke tests establish tool wiring, not better research quality. No winner is claimed yet.

## How to run

The runner uses Python 3 and the official Clay CLI on macOS or Linux. You need a Clay account with Claygent Builder and workflow access, and sufficient existing credits. Python dependencies are all in the standard library. No OpenAI key, browser cookie export or Codex installation is required.

1. Clone this repository and enter it. Install the official CLI using Clay's [setup instructions](https://github.com/clay-run/agent-plugins/blob/main/clay/skills/setup/SKILL.md). This run used CLI `1.4.0+de2a0396a538`. Put `clay` on PATH, or set `CLAY_BIN` to its absolute path.
2. Run `clay login --device`. Open the printed link, select your workspace and authorize the CLI. Then run `./eval doctor`. If needed, use `clay workspaces list` and `clay workspaces switch <id>` first.
3. Run `./eval setup`. It creates both workflows, triggers and agents from the checked-in prompt and schema. It records workspace-specific IDs under ignored `.local/`. Running setup again reuses its saved resources.
4. Open the generated B agent in Claygent Builder. Under Tools, add a custom MCP server named `Keenable public evaluation` with URL `https://api.keenable.ai/mcp`. Leave the API key empty for the public tier. Enable the connection and keep Web search enabled. Save. Verify A has Web search enabled and Keenable disabled. Keep unrelated private connectors and business context disabled on both. This is the one configuration step the inspected official CLI does not expose. See [INTEGRATION.md](INTEGRATION.md).
5. Run `./eval bind-refresh` to attach the saved B version to its workflow. This starts no research runs.
6. Start with one pair from the full frozen plan:

   ```sh
   ./eval run --output runs/my-run --stop-after-pairs 1 --allow-credit-use
   ```

   Inspect `runs/my-run/summary.json` and the saved results. Then resume the same plan:

   ```sh
   ./eval run --output runs/my-run --allow-credit-use
   ```

   The full plan has 100 agent runs. `--concurrency` controls the number of in-flight runs (default 2, maximum 4). These calls can consume Clay data credits and actions. No command buys credits or changes your plan. Use `--limit N` at the start to freeze a smaller plan. Do not change that limit when resuming.
7. Recompute the saved operational results without network calls:

   ```sh
   ./eval reproduce --output runs/my-run
   ```

The run saves each returned run ID before polling. Reusing the same output directory resumes known runs. An ambiguous submission stops for inspection instead of spending credits on an automatic duplicate. Do not delete a run directory to recover a timeout. Setup and live runs verify the actual prompt, model, schema, input mappings and graph. Tool configuration is checked in the UI because the CLI does not expose it; actual tool use comes from the saved run trace.

## Details

- `eval`: one executable for setup, execution, resume and offline reproduction.
- `cases.json`: model inputs only. No answers, reference URLs or difficulty hints.
- `prompt.txt`, `output-schema.json`: shared research instructions and fields.
- `ground-truth.json`: independently researched reference facts and source limitations. The runner never reads it.
- `dataset-manifest.json`: pre-run dataset and configuration hashes.
- `runs/`: saved inputs, configurations, outputs, tool traces and observed charges.
- `INTEGRATION.md`: verified connection setup, saved-version handling and smoke results.
- `REVIEW.md`: verification coverage and review limitations.

Offline factual scores require reviewed `judgments.json` in the run directory. Without it, the runner reports execution and cost only. A missing fact is not proof of absence. Later supported facts can correct incomplete reference answers, with the adjudication preserved.

Run the runner's offline safety checks with `python3 -m unittest -v test_eval.py`. Credentials remain in Clay's own local credential store. Never commit `.local/`, credential files or API keys.
