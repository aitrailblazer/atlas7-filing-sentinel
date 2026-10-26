# ATLAS-7 Filing Sentinel

**Meta Global AI Developer Hackathon, Startup track.**


**One-liner:** ATLAS-7 Filing Sentinel is an SEC filing sentinel that grades filings for material signal, with the open models themselves graded against a locked answer key.

## The problem and the workflow

The SEC receives a flood of filings every day. Most of it is routine paper: administrative notices, boilerplate, restatements of what is already public. A small share carries real information, a concrete event or change that a reasonable investor would treat as new. The material filings hide inside the routine ones, and a full filing package takes a human the better part of an hour to read properly. The independent investor, the small desk, and the solo analyst cannot read everything, so they read what is loudest, which is not the same as what matters.

The Filing Sentinel grades every filing the same way. For each one it returns a verdict, SIGNAL or NO SIGNAL, a probability for each class, and one sentence naming the specific filing content the verdict rests on. A verdict issues only when the engine's top-class probability reaches 0.85. Below that band the engine must abstain, so thin evidence produces no grade instead of a confident guess. The desk then reads only what the sentinel graded as signal, plus whatever it refused to grade, and every verdict carries its basis sentence and its probability, so a human can check the reasoning before acting on it.

## What was built and run during the hackathon

**A frozen grading harness.** Every engine reads the same 179 filing packets, under the same demo grading prompt, with the same abstain band. Nothing was tuned after the freeze. The sample, the prompt, the band rule, and a per-packet hash manifest were frozen in one commit before any engine saw a packet.

**Freeze discipline.** The answer key was pinned by hash before the first engine call: Decider corpus v4 finals (20 SIGNAL / 157 NO SIGNAL / 2 ABSTAIN over 179 filings), file sha256 8126b36c40f13bde4ee7e959f292c3b4725ba94deffb5d397281d48359f1bf96. The freeze of record is commit 834454df in aitrailblazer/coordination, path hackathon/open-model-grading/. The key stays home and never ships; only the demo grading prompt goes to any external route.

**The reference arm.** Muse Spark 1.3 on the Meta Model API graded all 179 packets plus one empty, filing-shaped null document, 180 calls at temperature 0, packets exactly as frozen, on October 26, 2026. The full run took 16 minutes 53 seconds of wall clock with zero failed calls, zero parse failures, and zero malformed verdicts. The largest packet, at 183,823 prompt tokens, was accepted and graded; no packet hit a context limit.

**The Open Model Grading Card.** The submission's exhibit is a grading card for the engines, not for the filings. Each engine's verdicts are scored against the locked key, and its agreement is published as the engine's score, next to its misses. Agreement is a score for the engine. It is never validation of the record the key comes from: the key is the ruler, and a ruler is not validated by the things measured with it. See [GRADING-CARD.md](GRADING-CARD.md).

**A sealed demo set.** Ten filings taken from the live EDGAR feed on October 26, 2026, outside the frozen 179, assembled into packets and labeled in-house before any engine saw them. The labels file is sealed by hash (sha256 30d73538229406da1adb51e1c3510a5df6aa78fb8d77a168fdc488ff313b883b) and never ships. The live demo grades these filings on stage and reveals the sealed labels after. See [demo-set/](demo-set/).

## What the results show

On the reference arm, Muse Spark 1.3 agreed with the finals on 157 of 179 packets, **87.7%** (corpus scope: 38 complete submissions, 141 at primary-plus-EX-99 scope). The shape underneath the headline is the informative part:

- **SIGNAL precision 0.50** (12 true positives, 12 false positives) and **SIGNAL recall 0.60** (12 of 20 gold SIGNAL filings found, 8 missed). The agreement headline is carried by the large NO SIGNAL majority; on the filings that matter most, the engine is at chance-adjacent precision and misses two in five.
- **The engine never used the abstain band.** It abstained zero times, and the lowest probability attached to any verdict in the run was 0.88, above the 0.85 band edge. Every one of the 22 disagreements with the key was a confident disagreement, including both gold ABSTAIN filings, which the engine called NO SIGNAL at 0.92 and 0.95. The false-confident rate was 12.3%.
- **The null probe passed.** Given an empty, filing-shaped document, the engine returned NO SIGNAL with p_no_signal 1.00 and the basis "empty packet". It invented no company, no event, and no amount. The noise floor on this route is clean.
- **Cost and latency.** The run consumed 1,171,914 tokens in total. At the published list price for muse-spark-1.3 (input $1.25 per million tokens, output $4.25 per million, dev.meta.ai pricing page, checked October 26, 2026), that prices to $2.16 for the full run, about **$0.012 per graded filing**, at a mean latency of **5.58 seconds** per call.

## [PENDING: contestant arm, Muse Spark Open on Baseten]

[PENDING: to be completed when the Baseten credit lands. Muse Spark Open will grade the same 179 packets plus the null document, under the same frozen prompt and the same abstain band. This section will print its agreement, SIGNAL precision, SIGNAL recall, abstentions, false-confident rate, tokens, latency, and cost per graded filing next to the reference arm above, plus the cross-route comparison: cost and latency per graded filing on each route, and whether the open model's disagreements with the key fall in the same places as the reference arm's.]

## Repository layout

- `harness/run_grading.py` — the grading runner: one frozen prompt, one packet per call, strict JSON verdicts, resume-safe output. It never reads labels.
- `harness/score_run.py` — the scorer: takes a results file and a labels file (supplied by whoever scores; no labels are bundled) and prints the card's metrics.
- `DEMO-GRADING-PROMPT.md` — the only prompt that ships to any external route.
- `GRADING-CARD.md` — the Open Model Grading Card, the submission's exhibit.
- `freeze/` — the freeze receipts: freeze manifest, per-packet hash manifest (`.md` and `.jsonl`), and the null document.
- `demo-set/` — the sealed demo set: 10 packets from the live EDGAR feed of October 26, 2026, plus its manifest. The labels are sealed by hash in the manifest and never ship.

## Demo video outline (3 minutes maximum)

- **0:00 to 0:10.** The one-liner on screen over the live product: the Filing Sentinel grades SEC filings in public, prints its misses at the same size as its wins, and refuses to grade when the evidence is thin.
- **0:10 to 1:20.** Working software, well inside 90 seconds. The sentinel grades one filing from the sealed demo set live: intake, the verdict, the probability, and the one-sentence basis on screen. Then the sealed label for that filing is revealed and checked against the verdict. The seal hash is shown, so the reveal is verifiable rather than staged.
- **1:20 to 2:10.** A second demo filing where the evidence is thin, graded live, so the audience sees how the sentinel handles a hard case with its probability and basis stated plainly.
- **2:10 to 3:00.** The Open Model Grading Card: the reference arm's full results, the 87.7% agreement with its scope line, precision and recall under the headline, the zero-abstention finding, and the null probe. Close on the freeze commit and the scope line: the record is free, the precision is the product.

## Links and receipts

- **Freeze of record:** commit 834454df, repository aitrailblazer/coordination, path hackathon/open-model-grading/ (freeze manifest, freeze pack, per-packet hash manifest for all 179 packets and the null document, demo grading prompt).
- **Answer key pin:** final-labels-corpus-179-v4.jsonl, sha256 8126b36c40f13bde4ee7e959f292c3b4725ba94deffb5d397281d48359f1bf96. The key itself stays home and is not linked.
- **The exhibit:** the Open Model Grading Card, included inside this submission ([GRADING-CARD.md](GRADING-CARD.md)).
- **Demo set seal:** labels sha256 30d73538229406da1adb51e1c3510a5df6aa78fb8d77a168fdc488ff313b883b (labels sealed October 26, 2026, before any engine run; the labels file never ships).

