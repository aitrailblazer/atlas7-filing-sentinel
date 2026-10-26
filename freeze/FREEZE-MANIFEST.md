# Open Model Grading: freeze manifest

Frozen 2026-10-23 (America/Los_Angeles) on Constantine's ruling adopting the
freeze pack's recommendations. This manifest and the freeze pack are committed
together to aitrailblazer/coordination under hackathon/open-model-grading/
(the commit containing this file is the freeze commit of record; the goal
files carry the working copies). No engine sees a packet before the remaining
components below join this freeze in the same path.

## Answer key (pinned, stays home, never ships)

- Decider corpus v3 finals: final-labels-corpus-179-v3.jsonl
  sha256 2d13b89b12f101a1ae5cb0c2129ca040586a3860d22f1cdbd2639aef0b37b29d
  (coordination commit 1d2bfaca9858e5c643e1c3c2c37ceb91b4f6bfcb;
  supersession lock commit 929e37d2c89601ce19168542bd83e81359ad3a00).
- Finals: 22 SIGNAL / 155 NO SIGNAL / 2 ABSTAIN over 179 filings.
- Corpus scope of record, printed next to every agreement figure:
  38 complete submissions, 141 at primary-plus-EX-99 scope.

## Sample (frozen definition)

- All 179 v3 packets, graded identically by every engine, plus one empty
  filing-shaped null document (noise-floor probe), plus a small sealed demo
  set drawn from the same packets for the public exhibit.
- Decision (2026-10-23): full 179 on every route the landed credit allows;
  stratified subset only on a route whose credit lands short, decided after
  the Mon Oct 26, 09:05 AM PT credit check reports balances.

## Abstain band rule (frozen)

- A verdict issues only at top-class probability at or above 0.85 (the v3
  lock's band). Below the band the engine abstains. Abstain quality is scored
  per the freeze pack's metric definitions.

## Metrics (frozen)

- As defined in the freeze pack: agreement with v3 finals (overall, quoted
  against the scope line), SIGNAL precision and recall per engine,
  false-confident rate, abstain quality, margin calibration in bands,
  Guardian flag precision (screen only), cost and latency per graded filing
  per route.
- Framing rule: engine agreement is a published score, never validation of
  the Decider record.

## Routes (frozen)

- Muse Spark on the Meta Model API: reference arm.
- Muse Spark Open on Baseten: contestant arm.
- Batch harness on Modal: execution route.
- Fireworks: EXCLUDED unless its $25 credit lands without a payment method
  (decision 2026-10-23). No card is added.
- Muse Glimmer: include only if a route exists at kickoff.

## Publication shape (frozen)

- The Open Model Grading Card ships INSIDE the hackathon submission
  (decision 2026-10-23), not as a linked exhibit.

## Remaining freeze components (due before the first engine call)

- Per-packet hash manifest for the 179 packets and the null document.
- The demo grading prompt file (the only prompt that ships to any external
  route; the full grading methodology never leaves home).

## Re-issue, 2026-10-24: answer key amended to corpus v4

- Reason: after the freeze, a blind re-grade of the 13 dev rows in the v6 false-positive filer clusters and a fresh-persona adjudication of the 5 disagreements overruled 4 v3 labels (record: SUPERSESSION-20261024.md and lock-v4 in the Decider training folder). Shipping a key known to be wrong in 4 places was rejected on Constantine's ruling of 2026-10-24 ("Apply amendments, authorize B").
- The pinned answer key is now: Decider corpus v4 finals, final-labels-corpus-179-v4.jsonl, sha256 8126b36c40f13bde4ee7e959f292c3b4725ba94deffb5d397281d48359f1bf96. Finals: 20 SIGNAL / 157 NO SIGNAL / 2 ABSTAIN over 179 filings.
- Everywhere the frozen text above says "v3 finals" for the answer key, read v4 finals. The packets are unchanged (the same 179 packet files), and the corpus scope line is unchanged: 38 complete submissions, 141 at primary-plus-EX-99 scope.
- This re-issue lands before any engine has seen a packet (kickoff Mon Oct 26, 2026), so the freeze discipline, one pinned key in place before the first engine call, holds. The v3 pin above remains the record of the original freeze.

## Addendum, 2026-10-26: canonical packet set and freeze completion

- The packet set of record is ~/workspace/decider-training-20261016/packets-179-v3/ (packet-assembler-v2). Verified 2026-10-26: dataset-v4 embeds packet text byte-for-byte identical to packets-179-v3 for all 177 graded rows. The sibling packets-179/ directory (v1 assembler, the 2026-10-14 grading packets) shares the 179 filenames, but 38 files, the complete-submission packets, differ in content. The line above, "the packets are unchanged (the same 179 packet files)," holds for the v3 to v4 label amendment; as between the two directories it does not, and packets-179-v3 governs. Full record: PACKET-HASH-MANIFEST.md.
- The two remaining freeze components join the freeze in this commit: PACKET-HASH-MANIFEST.jsonl (179 packets, rollup sha256 f3e8fbaa6f190d3f4906d8e1bbf0ad52a6434c4fb63cc7189f19e98b1002e902) with NULL-DOCUMENT.md (the null document, created 2026-10-26, sha256 655ade23e918a3f4ec27a8cfabd5f4a1eb47b20d949fb735a8754b152d274c01), and DEMO-GRADING-PROMPT.md (approved by Constantine 2026-10-26). With this commit the freeze is complete and the first engine call is unblocked.
