# Verified integration notes

Verified on September 30, 2026, with the official Clay CLI 1.4.0+de2a0396a538 and GPT-5.4 in Clay.

## Connect Keenable once

In the B agent's Builder settings, leave Web search enabled. Select Add custom MCP server. Use the name `Keenable public evaluation` and URL `https://api.keenable.ai/mcp`. Leave the API key empty for the documented public tier. Enable that connection and save the agent. Keep unrelated connectors and private business context disabled in both conditions.

The [documented public tier](https://docs.keenable.ai/rate-limits) allows 1,000 requests per hour and at most 10 per second, shared per IP. Fifty B runs with an eight-call prompt budget fit below the nominal hourly cap, but Clay's shared egress and model compliance can affect this. Record any rate-limit failures. Do not bypass them or silently switch to a paid endpoint.

## Tool names differ by execution surface

The same connection appeared as `custom-fetch_page_content` in Builder and `keenable-public-evaluation-fetch_page_content` in a workflow. The corresponding search names differ in the same way. These are observed names, not a permanent API contract.

An initial smoke prompt requested the wrong registered name and produced a false unavailable report. A second diagnostic also misclassified custom-prefixed tools as native. The corrected check identifies an available tool by its fetch_page_content suffix and calls that registered name. The tool trace, not the model's description of its tools, establishes execution.

Both surfaces subsequently returned content from example.com through Keenable. The workflow trace also listed native searchGoogle and visitWebpage. See the saved evidence JSON files. This verifies wiring only, not retrieval quality.

## Saved agent versions

A workflow node can refer to an older saved agent version after a Builder edit. Run graph validation before executing. Reassigning the same agentClaygentId returned a no-op and did not clear the outdated-version warning in this test. A newly linked node selected the current version and validated without warnings. The runner refreshes only nodes it created in its own evaluation workflows.

## Billing observations

The Builder smoke tests did not change the observed workspace credit balances. The first CLI smoke run failed because of the name mismatch and used 0.2 data credits plus 1 action. The corrected CLI smoke run completed and used 0.4 data credits plus 1 action. These are observed run charges, not estimates for company research.

The Builder stream exposed internal inference-cost metadata. I do not treat that as the user's bill. No credit purchase or plan change was made.

## Scope of reproducibility

Use the official CLI for workflow setup, run submission, polling and result retrieval. Use the Builder once to configure the external connection because the inspected CLI node schema does not expose that setting. The runner does not copy browser cookies, replay private browser endpoints or store credentials.

A first-time reader still needs a Clay account with the relevant Builder and workflow access and must authorize the official CLI. Website sign-in alone does not authorize the CLI. Document these steps as prerequisites rather than promising that a Keenable key alone is enough.

## Exact prompt and edge configuration

Saving tool settings in Builder can reformat the markdown prompt. The runner restores B's prompt through the official CLI and checks exact equality with the shared file before submission. This preserves the saved tool configuration.

In CLI 1.4.0, `outgoingEdges` appeared in read responses but was not accepted as a writable update. Binding refresh uses documented `incomingEdges`: disconnect the old agent, connect the replacement to the trigger, verify the resulting edge, and remove only the old node owned by this runner. It preserves a journal if any mutation is ambiguous.
