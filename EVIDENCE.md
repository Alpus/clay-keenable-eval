# Why this experiment exists

I checked these sources on September 30, 2026. This is a purposive search for concrete problems, not a survey of Clay users. The posts establish reported needs and failures. They do not establish their frequency, a shared technical cause, or an advantage for Keenable.

## Selected problem: stale company status

A historical funding round can be correct while the resulting prospect qualification is wrong. An acquisition, IPO, or closure can make that old round irrelevant to the current target-account criteria.

| Posted | Original report | What it supports | Limits and suggested fixes |
| --- | --- | --- | --- |
| November 22, 2024 | [Aly H.: inaccessible company websites](https://community.clay.com/x/content-and-events/msg_35tcOKa9milS/ensuring-website-accessibility-for-accurate-compan) | Claygent generated descriptions for inaccessible websites. Outreach recipients said their businesses had closed. | Old report, unspecified model and companies. Clay suggested its native URL-validity check and conditional execution. A dead website does not prove a closed business. |
| May 30, 2025 | [Nitin B.: stale outbound signals](https://community.clay.com/x/content-and-events/bv4tl1wwyc8n/improving-outbound-strategies-freshness-date-filte) | Funding news from 18 months earlier was being used as a fresh outreach signal. | The proposed remedy was an explicit date cutoff. This is related freshness evidence, not the same acquisition failure. |
| July 7, 2026 | [Olivia W.: enterprise target-account data quality](https://community.clay.com/x/general/msg_KZCrTAAlkb9N/troubleshooting-clay-data-quality-issues-for-enter) | Lists across clients included companies closed or acquired more than a decade earlier. Manual review did not scale. | This concerns company sourcing and database quality, not Claygent. The visible reply routes to support and provides no confirmed fix. |
| August 27, 2026 | [Liron D.: VC-backed funding enrichment](https://community.clay.com/x/general/msg_mUxjIReQbxzA/seeking-cost-effective-and-accurate-vc-backed-comp) | Claygent returned Series C for a company that had since been acquired. Acquired companies fail this user's ICP. | The company, model and exact prompt are absent. A reply suggests checking acquisition, IPO and shutdown separately. Our baseline must include that check. |

These independent posts support a recurring business need for current-status validation from 2024 to 2026. Only Liron's post directly describes the selected funding/acquisition error. I do not describe all four as repeated instances of one current Claygent defect.

## Other hypotheses and counterevidence

| Posted | Source | Reported task or problem | Assessment |
| --- | --- | --- | --- |
| November 19, 2024 | [CEO extraction](https://community.clay.com/x/general/6g51dn2ns3mg/how-to-create-a-claygent-prompt-to-extract-ceo-nam) | Avoid mistaking a testimonial author or a similar company's CEO for the target CEO. | Entity resolution and evidence attribution matter. More retrieval alone might not fix this. |
| January 17, 2025 | [Company-summary mismatch](https://community.clay.com/x/general/e16x6ni12wp5/improving-claygents-company-summary-accuracy-for-e) | GPT-4o Mini described freemanseattle.com as an events company. The original includes a prompt and an incorrect answer. | A concrete input is available. This is an old model and a different task. Keep it as a separate entity-resolution probe, outside the funding score. |
| May 21, 2025 | [Model-dependent website checks](https://community.clay.com/x/general/rrnvuztd4cid/inconsistent-performance-of-4o-mini-model-in-clayg) | GPT-4o Mini was inconsistent when checking active websites. | The author reported much better results with GPT-4.1 Mini. Do not treat this as an unresolved search-layer failure. |
| May 29, 2025 | [Financial PDFs](https://community.clay.com/x/general/ohbse0lckte6/best-ways-to-read-financial-reports-from-pdf-links) | Some PDF reads failed initially and succeeded on subsequent attempts. | No exact PDFs or isolated cause. Keenable fetch is a hypothesis, not a demonstrated remedy. |
| June 28, 2025 | [Property-management portfolios](https://community.clay.com/x/general/wemhgsgh3svr/seeking-help-to-improve-ai-prompts-for-property-ma) | Different prompts produced inconsistent asset-portfolio answers and inferred data. | Public ground truth and exact targets are missing. Could be inference rather than retrieval. |
| August 4, 2025 | [Competitor clients and partnerships](https://community.clay.com/x/general/msg_bCkathKjQwzM/how-to-identify-competitors-partnerships-and-colla) | A user wants the clients of 20 competitors from websites, social posts and success stories. | Direct demand, but not a demonstrated Claygent failure. Replies note the limit to publicly disclosed relationships. A complaint about other providers is not evidence against Claygent. |
| November 5, 2025 | [Retailer product counts](https://community.clay.com/x/general/jcf8fvq0wki0/seeking-reliable-methods-for-website-product-count) | Argon returned unreliable product counts for Benelux retailers. | Sitemaps or store APIs may be better than a search agent. This is not a strong initial Keenable fit. |
| January 12, 2026 | [Exhibitor company names](https://community.clay.com/x/general/msg_8rfgvlVX5vg6/effective-methods-for-scraping-company-names-from) | Extract companies from the MRO Americas exhibitor directory. The thread includes the exact directory URL. | The difficulty involves a nested or dynamically loaded list. Replies suggest external scraping and Claygent. Current native browser capabilities must be tested before claiming a gap. |
| March 31, 2026 | [Estate-agent branch counts](https://community.clay.com/x/general/xmu387tneqw4/how-to-verify-branch-counts-from-a-directory-with) | A directory requires entering location and agent name before searching. Direct URLs and Google give unreliable results. | No exact directory or companies. This may require browser interaction rather than search or page fetching. |

I did not find enough independent, current evidence to call competitor-customer discovery a persistent Claygent failure. It remains a useful secondary hypothesis. Neither engine can reveal genuinely undisclosed customer relationships.

## Ten initial candidates, in original unranked order

| Candidate | Input and desired output | Current decision |
| --- | --- | --- |
| Technology in active job listings | Company/domain to technology, live vacancy and evidence | Plausible, but no specific failure established here |
| Competitor product use or migration | Company/domain to product relationship and dated evidence | Customer-discovery demand exists; failure evidence is weaker |
| New office or business unit | Company/domain to opening, location and date | Documented use case; no direct complaint established here |
| Company acquisition | Company/domain to completed acquisition and current status | Selected, expanded to distinguish funding history from current lifecycle |
| Geographic market entry | Company/domain to market, event and date | Plausible, but insufficient complaint evidence here |
| Relevant product launch | Company/domain to launch and date | Plausible; freshness controls are needed |
| Official platform integration | Company/domain to named integration and source | Suitable for evidence checks, but no observed failure here |
| Vendor customer case in a target industry | Vendor/domain to customer, relationship, industry and case URL | Real demand; not enough evidence of current Claygent failure |
| Physical locations | Company/domain to branch list or count and evidence | Concrete complaints, but navigation and completeness are confounders |
| Open tender | Organization/category to tender, deadline and source | Useful task, but no direct complaint established here |

These are candidates, not ten proven pain points. [Clay templates](https://www.clay.com/templates) and [Clay's GTM agent use cases](https://www.clay.com/blog/agent-use-cases-gtm) describe applications. Vendor descriptions are not independent performance evidence.

## Relevant product capabilities

- [Claygent Builder](https://university.clay.com/docs/claygent-builder) supports model selection, web search, reusable agents and free Builder test cases. Free Builder testing does not establish that workflow or API execution is free.
- [Clay's GTM agent announcement](https://www.clay.com/blog/agent-use-cases-gtm) describes external MCP tools. A saved connection is not proof of a successful tool call.
- [Claygent Navigator](https://www.clay.com/blog/introducing-claygent-navigator) is a native browser-capable option. A comparison must not assume that Clay only reads static pages.
- [Keenable MCP](https://docs.keenable.ai/mcp-server) exposes search and fetch. Its public tier works without a key and has rate limits. [Fetch](https://docs.keenable.ai/api-reference/fetch) can use an indexed copy or a live page. These are capabilities, not benchmark results.
- [Official Clay CLI skills](https://github.com/clay-run/agent-plugins) document creating and running workflow agent nodes. CLI authentication is separate from signing into the website.
