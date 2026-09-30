# Evaluation design

## Question

Does adding Keenable to a searching Claygent improve evidence-backed answers about a company's latest funding and current lifecycle?

The business outcome is avoiding incorrect prospect qualification caused by stale financing data. The experiment measures factual research quality. It does not measure revenue, conversion or sales lift.

## Conditions

| Condition | Model, prompt and schema | Tools |
| --- | --- | --- |
| A | Identical fixed configuration | Native Clay web search and page access |
| B | Same configuration as A | Native Clay tools plus Keenable search and fetch |
| C | Same model/schema and original prompt prefix, plus verification instructions | Native first, then Keenable for gaps, conflicts and freshness |

A remains a full research agent. Both A and B explicitly check for newer acquisition, IPO and closure evidence. B is an augmentation test. It does not test replacement of Clay's search. Saved tool-step summaries distinguish availability from actual use.

The original prompt does not force B to use Keenable. Both agents may choose their available tools. A B-run that does not call Keenable remains in the aggregate result, with non-use reported. A forced-tool smoke test verifies wiring separately and does not count toward quality results.

After observing B's optional tool use, the user requested a separate C condition. All original A/B runs finished before C began. C uses every original company and preserves A/B unchanged. It reserves up to two of the same eight requested research calls for Keenable. A latest/current claim explicitly triggers verification. C is a post hoc strategy experiment with a changed prompt, not a held-out or isolated search-engine comparison.

If a tool needs a short explanation of its name, put an equivalent tool-use instruction in both prompts. Do not add special research hints or target URLs only to B.

## Cases and evidence

1. Freeze 50 company identities before seeing agent answers. The sample includes 28 funding cases (mostly recent, with older controls), 21 acquired/public lifecycle cases and one separate entity-resolution probe. Include recent rounds across sectors and geographies, acquired venture-backed companies, and a terminated-deal or IPO control. Include Keenable at the user's request. Report results with and without Keenable.
2. Include named complaint inputs only when the original names them. Never invent the unidentified company in the funding/acquisition complaint. Keep freemanseattle.com as a separate entity-resolution probe with its own task and score.
3. Find reference evidence independently of Keenable's results. Prefer company, acquirer, investor and regulatory publications. Record publication date, event date when different, retrieval date and precise supporting fact.
4. Separate agent inputs from reference answers. The agent receives only company name, domain, as-of date and the common task. It receives no reference URLs, answers, complaint category or difficulty hints.
5. Report every frozen case, including ties, reversals, failures and unknowns. This is a purposive exploratory sample, not a representative or held-out benchmark. If it is too easy, create a separate challenge-discovery set and preserve all attempts; do not replace easy cases after seeing outcomes.

Existence of a historical funding announcement does not prove it is the latest round. An acquisition announcement does not prove completion. An inaccessible website does not prove closure. Failure to find a fact does not prove absence. A current independent/private label needs affirmative evidence where feasible and must carry its evidence date and uncertainty.

## Output fields

Return legal/business identity, latest reported venture round, announcement date, amount and currency when established, lifecycle status, lifecycle event date, acquirer when relevant, and evidence URLs tied to each claim. Distinguish acquired, public, private/independent supported by evidence, closed, pending acquisition, and unknown. Record conflicting sources explicitly. Do not convert currencies or substitute total funding for the round amount.

ICP exclusion in lifecycle references is derived from acquired/public status; the output has no separate ICP field. Funding stage and lifecycle remain separate fields. A seed-stage company such as Keenable is still useful for factual research even if a Series-only ICP would exclude it.

## Fair execution

- Fix the chosen supported model, full prompt, output schema and non-search context. Save actual model identifiers when exposed.
- Keep unrelated private connectors, account context and business context disabled.
- Interleave paired A/B runs and alternate their order. Use the same timeout and research budget where the platform exposes them. Record limits that cannot be controlled.
- Do not silently retry only the losing condition. Preserve every attempt and distinguish transport errors from research errors.
- Keep exploratory tuning separate. Freeze the evaluation prompt and cases before running the scored comparison.
- Use bounded execution and preserve run IDs before polling. A timeout must not trigger a duplicate paid run.

## Scoring and attribution

Score funding stage, date, amount, identity and lifecycle separately against reviewed reference evidence. Count unsupported assertions as errors, including correct-looking claims with irrelevant or contradictory citations. Report unknown/abstention and answer coverage separately from factual accuracy.

For each A/B disagreement, inspect the retrieved evidence. Classify it as missing retrieval, wrong entity, stale evidence, failed fetch, wrong interpretation, unsupported inference, or unresolved. A stronger answer is attributable to Keenable only when the trace shows its use and the returned material supports the corrected claim. A citation alone does not prove which tool found it.

Report wins, ties and losses across all cases; field accuracy; missed facts; false claims; source support; and the percentage of B runs using Keenable. Show per-case results. Small exploratory samples support case observations, not population-wide improvement claims.

The headline counts companies with all predeclared target facts correct and supported. Paired outcomes compare correct-field counts only when both arms have the same non-null targets. A missed extension can affect date, amount, extension recognition and citation support together. Those are correlated scoring dimensions of one missed event. A tie can mean both answers are wrong. `supported_answer` covers scored targets only; additional questionable claims remain visible in judgments.

References are positive evidence anchors, not an exhaustive claim that no later event exists. A supported later event before the cutoff is accepted. Equivalent wording, currencies, date semantics and primary-source corrections are reviewed explicitly. `null` is used only when a target cannot fairly be scored.

Codex adjudicates answers against sources. A/B labels are visible during review. This is not blinded human grading or independent model adjudication. Original source URLs and decision notes are saved with every judgment.

The official CLI exposes tool-step summaries. Many response bodies in those summaries are truncated at 500 characters, even with verbose output. Call names establish observed tool use, but a truncated body cannot establish all evidence that the model received. Claims of Keenable attribution are limited accordingly.

Measure latency from run submission to terminal completion with the same boundary in both conditions. Report total provider charges only from billing evidence. Keep Clay credits, actions and currency charges distinct. Free Builder tests do not estimate production cost. A provider's internal inference estimate is not the user's bill. Compute cost per correct answer only when both the numerator and scoring denominator are established.

## Reproducibility contract

The final runner must document installation, Clay login, required workspace capabilities, Keenable setup, smoke test, bounded live run, resume and offline reproduction. Credentials stay outside the repository. Document any necessary one-time UI configuration instead of claiming a key alone is sufficient.

Actual native and Keenable calls were verified before the full comparison. Quality claims require completed paired runs and source adjudication.

## Preselected challenges

Select difficulty before seeing the answers: extensions after a major round; round amount versus valuation, cumulative funding or debt; announcement versus completion and page-update dates; historical VC funding followed by acquisition or listing; cancelled acquisitions; and same-name entities. Include routine controls as well. A challenge reason is a hypothesis about difficulty, not evidence that either agent will fail.

The UI warns that more than five output fields can degrade performance. Both arms use the same eleven fields to keep factual claims independently inspectable. This common configuration is part of the protocol, not an unrestricted claim about Clay's best possible performance. The eight-call research limit is a prompt instruction; actual calls are recorded because the platform may not enforce it.

The 50 identities comprise 28 funding cases, 14 completed-acquisition cases, seven public-listing cases and one entity probe. Twenty-two have a United States geography label; other cases span Europe, India, Australia, Israel and South Korea, including cross-border companies. The sample remains technology-heavy and purposive. Only the Freeman entity probe is a named input from a retrieved complaint; the funding complaint did not disclose its company.

## Verification coverage

I checked the protocol for an active native-search baseline, equal prompts and models, separate reference answers, exploratory versus held-out labeling, dated sources, and unsupported cost or benefit claims.

An independent model review was attempted through the configured free OpenRouter MCP on September 30, 2026. Both listed connections returned a reauthentication error during the read-only health check. No review generation ran. I did not use a paid fallback or a separate Claude budget. This is a review coverage limitation, not an independent endorsement.

The runner passed eleven offline checks covering ambiguous submissions, 50-case scheduling and resume, bounded concurrency, exact prompt restoration after Builder formatting, native and Keenable trace parsing, and complete versus partial judgment aggregation. The original 100-run A/B comparison completed. C adds 50 research outputs without rerunning A/B. Setup and graph validation are not treated as evidence of research accuracy.

## Execution amendments

The initial A/B pair used concurrency 2, then the remaining plan continued at 4. At the user's request, the limit increased to 30 for the last 15 A/B runs. Each invocation is recorded in its manifest. Concurrency is operational; prompts, model, inputs and saved research answers were unchanged.

C initially used concurrency 30 without submission spacing. Seven runs were rejected while initializing Keenable because the public API limits requests to 10 per second. They produced no research answers and consumed zero reported Clay data or action credits. Their full attempts remain archived. Each received one explicit retry with the same configuration, with starts spaced by two seconds. The runner now defaults to that spacing and concurrency 30. It never automatically retries a research answer or an ambiguous submission. Initialization success is reported separately from factual quality.

Polling and manual inspection pauses affect submission-to-observed-completion time. These timestamps remain available for audit; they should not be read as an isolated measure of search-engine speed. Clay's reported duration is a separate observation. The A/B and C runs also occurred at different times and concurrency settings.

## Final source review

The frozen reference file remains unchanged. Final judgments record newer evidence and corrections discovered during adjudication. The review includes claims from A, B and C, and applies each correction to all conditions. Examples include newer financing disclosures for Cyera, ElevenLabs and Lessn, and ambiguous financing evidence for MangoBoost and Abridge. The latter two remain in the dataset with null latest-event targets while their conflicts remain unresolved.

Lifecycle cases have preselected lifecycle targets; historical funding is not fully scored in those cases. Additional mistakes and unsupported claims remain visible in judgments. Thus a full target score does not certify every statement in an answer. The separate Freeman entity probe is outside the main funding/lifecycle aggregate.

## Result interpretation

**Where Keenable helped:** C used Keenable search and fetch to find a [company-issued Lessn disclosure](https://www.ad-hoc-news.de/boerse/news/unternehmensnachrichten/sydney-au-mar-3-2026-acn-newswire-accounts-payable-automation/68628893) reporting a $300,000 investment in November 2025. A/B stopped at the earlier August round. The saved trace supports this retrieval attribution. C also found Wayve's later extension, but native tools established the final precise facts, so that improvement cannot be attributed solely to Keenable.

**Where it did not solve the problem:** all conditions missed later extensions for ElevenLabs and Harvey. All got the 21 lifecycle statuses right. C still made additional errors outside those targets, including a wrong historical funding claim for Circle. All four B field-score wins over A occurred without calling Keenable, so those gains do not establish a Keenable contribution. Merely enabling Keenable had little aggregate effect; the prompted strategy did better in this exploratory run, with higher credit use and a changed prompt.
