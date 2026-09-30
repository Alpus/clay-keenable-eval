# Evaluation design

## Question

Does adding Keenable to a searching Claygent improve evidence-backed answers about a company's latest funding and current lifecycle?

The business outcome is avoiding incorrect prospect qualification caused by stale financing data. I will measure factual research quality first. I will not infer revenue, conversion or sales lift from this experiment.

## Conditions

| Condition | Model, prompt and schema | Tools |
| --- | --- | --- |
| A | Identical fixed configuration | Native Clay web search and page access |
| B | Identical fixed configuration | Native Clay tools plus Keenable search and fetch |
| C, optional diagnostic | Same configuration | Keenable with native web search disabled, only if verified supported |

A remains a full research agent. Both A and B explicitly check for newer acquisition, IPO and closure evidence. B is an augmentation test. I will not describe it as replacing Clay's search. I will preserve tool traces to distinguish availability, actual use, successful retrieval and evidence used in the answer.

The main prompt will not force B to use Keenable. Both agents may choose their available tools. A B-run that does not call Keenable remains in the aggregate result, with non-use reported. A forced-tool smoke test verifies wiring separately and does not count toward quality results.

If a tool needs a short explanation of its name, put an equivalent tool-use instruction in both prompts. Do not add special research hints or target URLs only to B.

## Cases and evidence

1. Freeze 50 company identities before seeing agent answers. The sample includes 28 recent-funding cases, 21 acquired/public lifecycle cases and one separate entity-resolution probe. Include recent rounds across sectors and geographies, acquired venture-backed companies, and a terminated-deal or IPO control. Include Keenable at the user's request. Report results with and without Keenable.
2. Include named complaint inputs only when the original names them. Never invent the unidentified company in the funding/acquisition complaint. Keep freemanseattle.com as a separate entity-resolution probe with its own task and score.
3. Find reference evidence independently of Keenable's results. Prefer company, acquirer, investor and regulatory publications. Record publication date, event date when different, retrieval date and precise supporting fact.
4. Separate agent inputs from reference answers. The agent receives only company name, domain, as-of date and the common task. It receives no reference URLs, answers, complaint category or difficulty hints.
5. Report every frozen case, including ties, reversals, failures and unknowns. This is a purposive exploratory sample, not a representative or held-out benchmark. If it is too easy, create a separate challenge-discovery set and preserve all attempts; do not replace easy cases after seeing outcomes.

Existence of a historical funding announcement does not prove it is the latest round. An acquisition announcement does not prove completion. An inaccessible website does not prove closure. Failure to find a fact does not prove absence. A current independent/private label needs affirmative evidence where feasible and must carry its evidence date and uncertainty.

## Output fields

Return legal/business identity, latest reported venture round, announcement date, amount and currency when established, lifecycle status, lifecycle event date, acquirer when relevant, and evidence URLs tied to each claim. Distinguish acquired, public, private/independent supported by evidence, closed, pending acquisition, and unknown. Record conflicting sources explicitly. Do not convert currencies or substitute total funding for the round amount.

Any ICP eligibility field will use a published rule. Funding stage and lifecycle remain separate fields. A seed-stage company such as Keenable is still useful for factual research even if a Series-only ICP would exclude it.

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

Measure latency from run submission to terminal completion with the same boundary in both conditions. Report total provider charges only from billing evidence. Keep Clay credits, actions and currency charges distinct. Free Builder tests do not estimate production cost. A provider's internal inference estimate is not the user's bill. Compute cost per correct answer only when both the numerator and scoring denominator are established.

## Reproducibility contract

The final runner must document installation, Clay login, required workspace capabilities, Keenable setup, smoke test, bounded live run, resume and offline reproduction. Credentials stay outside the repository. Document any necessary one-time UI configuration instead of claiming a key alone is sufficient.

The current integration is under validation. Do not publish quality claims or a finished-run command until real tool calls and a complete A/B run have been verified.

## Preselected challenges

Select difficulty before seeing the answers: extensions after a major round; round amount versus valuation, cumulative funding or debt; announcement versus completion and page-update dates; historical VC funding followed by acquisition or listing; cancelled acquisitions; and same-name entities. Include routine controls as well. A challenge reason is a hypothesis about difficulty, not evidence that either agent will fail.

The UI warns that more than five output fields can degrade performance. Both arms use the same eleven fields to keep factual claims independently inspectable. This common configuration is part of the protocol, not an unrestricted claim about Clay's best possible performance. The eight-call research limit is a prompt instruction; actual calls are recorded because the platform may not enforce it.
