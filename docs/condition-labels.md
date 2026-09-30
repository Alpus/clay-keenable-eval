# Condition labels

The presentation labels were changed on September 30, 2026: C is native verification and D is Keenable verification. A and B are unchanged.

Runner configuration, local bindings, judgment labels, run directories and regenerated reports use the new labels. Source and comparison manifest hashes were recalculated for the relabeled metadata. No research was repeated and no scores or charges changed.

Raw Clay receipts, model answers and screenshots are unchanged. Their historical workflow titles still use C for Keenable verification and D for native verification. Workflow IDs, run IDs and provider-based directory names identify the same original runs.

- `runs/verify-native-001`: current C, historical Clay title D.
- `runs/verify-001`: current D, historical Clay title C.
- `runs/comparison`: historical A/B plus Keenable verification, now A/B/D.
- `runs/comparison-abcd`: all four conditions in A/B/C/D order.

Validation: 12 offline tests passed. All 1,006 saved result/start receipts remained byte-identical, and source/comparison manifest hashes and result provenance were verified. Offline Docker replay reproduced the relabeled scores. A separate Codex review checked the mapping and found documentation inconsistencies that were corrected; this was not a cross-model review.
