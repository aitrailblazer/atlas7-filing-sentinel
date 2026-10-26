# Open Model Grading Card

This card grades the engines, not the filings. Each engine reads the same frozen set of SEC filing packets and returns a verdict on each one. Its verdicts are scored against a locked answer key, and its agreement with that key is published here as the engine's score. Agreement is a score for the engine. It is never validation of the Decider record the key comes from, and it is never independent grader agreement for that record.

## The frozen setup

Everything below was frozen in one commit before any engine saw a packet. No prompt tuning against this sample after the freeze.

- **Sample:** 179 filing packets, graded identically by every engine, plus 1 empty, filing-shaped null document (the noise-floor probe: a correct engine abstains or returns NO SIGNAL with no invented facts).
- **Corpus scope, printed next to every agreement figure:** 38 complete submissions, 141 at primary-plus-EX-99 scope.
- **Answer key:** Decider corpus v4 finals (20 SIGNAL / 157 NO SIGNAL / 2 ABSTAIN over 179 filings), pinned by hash: final-labels-corpus-179-v4.jsonl, sha256 8126b36c40f13bde4ee7e959f292c3b4725ba94deffb5d397281d48359f1bf96. The key stays home and never ships. Only the demo grading prompt ships to any external route; the full grading methodology never leaves home.
- **Abstain band rule:** a verdict issues only when the engine's top-class probability is at or above 0.85. Below the band, the engine must abstain.
- **Freeze of record:** commit 834454df in aitrailblazer/coordination, path hackathon/open-model-grading/, including the per-packet hash manifest for all 179 packets and the null document.
- **Routes:** Muse Spark 1.3 on the Meta Model API is the reference arm. Muse Spark Open on Baseten is the contestant arm. Both arms ran through the same local harness, one call per packet; Modal was not needed and was not used. Fireworks is excluded: its credit never landed without a payment method.

## Reference arm: Muse Spark 1.3 on the Meta Model API

Run 2026-10-26 with the frozen demo prompt, temperature 0, packets exactly as frozen, no truncation. Scored locally against the pinned v4 key.

| Measure | Result |
|---|---|
| Packets graded | 179 of 179, plus the null document (180 calls) |
| Failed calls | 0 (no API or transport errors, no parse failures, no malformed verdicts; the largest packet, at 183,823 prompt tokens, was accepted and graded) |
| Agreement with the finals | 157 of 179 = 87.7% (scope: 38 complete submissions, 141 at primary-plus-EX-99 scope) |
| SIGNAL precision | 0.50 (12 true positives, 12 false positives) |
| SIGNAL recall | 0.60 (12 of 20 gold SIGNAL found, 8 missed) |
| Abstentions | 0 |
| False-confident rate | 12.3% (22 of 179) |
| Null document | NO SIGNAL, p_signal 0.00 / p_no_signal 1.00, basis "empty packet" |
| Tokens consumed | 939,946 prompt + 231,968 completion = 1,171,914 total (mean per call: 5,218 prompt, 1,289 completion; completion includes reasoning tokens) |
| Latency | Mean 5.58 s per call; wall clock 16 min 53 s for the full run |
| Cost per graded filing | 5,218 prompt + 1,289 completion tokens on average. At the published list price for muse-spark-1.3 (input $1.25 per million tokens, output $4.25 per million, dev.meta.ai pricing page, checked 2026-10-26), the full run prices to $2.16 total, about $0.012 per graded filing. The API responses carry no pricing; the credit balance itself is read from the developer console and was not independently verified for this draft. |

Two readings of this table matter more than the headline.

- **The abstain band was never entered.** The engine abstained zero times, and the lowest probability attached to any verdict in the run was 0.88, above the 0.85 band edge. Abstain quality is therefore vacuous on this arm: all 22 disagreements with the key were confident disagreements, including both gold ABSTAIN filings, which the engine called NO SIGNAL at 0.92 and 0.95.
- **The misses are symmetric.** Of 20 gold SIGNAL filings, the engine found 12 and missed 8. Of 157 gold NO SIGNAL filings, it wrongly called 12 SIGNAL. Precision and recall both sit well below the agreement headline, which is carried by the large NO SIGNAL majority.

## Three worked examples

Probabilities below are the full-run values from the results file. A note on repeatability: at temperature 0 the verdicts were stable between the smoke test and the full run, but the reported probabilities are not bit-stable between runs. The Cloudflare packet read NO SIGNAL at 0.90 in the smoke test and at 0.95 in the full run.

### 1. A confident miss: Cloudflare, Form 144 (accession 0001972481-26-000285)

- Gold: SIGNAL. Engine: NO SIGNAL, p_signal 0.05 / p_no_signal 0.95.
- Engine basis, verbatim: "Form 144 discloses director Carl Ledbetter's proposed sale of 25,000 Cloudflare common shares through Stifel."
- The engine read the packet as one director's proposed sale and closed at 0.95, far above the abstain band, so the band never had a chance to catch the disagreement. This single row is the false-confident problem in miniature.

### 2. A clean agreement: Kratos Defense, Form 144 (accession 0001950047-26-009715)

- Gold: NO SIGNAL. Engine: NO SIGNAL, p_signal 0.05 / p_no_signal 0.95.
- Engine basis, verbatim: "The packet is a Form 144 noticing Deanna Lund's proposed 10b5-1 sale of 20584 Kratos common shares."
- Same form type as the miss above, opposite outcome. The engine named the 10b5-1 plan sale in the packet and matched the key exactly.

### 3. The null document

- Gold: NO SIGNAL (the frozen expectation). Engine: NO SIGNAL, p_signal 0.00 / p_no_signal 1.00.
- Engine basis, verbatim: "empty packet".
- On empty input the engine invented nothing: no company, no event, no amount. The noise floor on this route is clean.

## Contestant arm: Muse Spark Open on Baseten

Run 2026-10-26 with the same frozen demo prompt, temperature 0, same 179 packets plus the null document, no truncation. Scored locally against the same pinned v4 key. No Baseten hackathon credit and no payment method were needed: the run was charged against the workspace's $5.00 of free Model API credits.

| Measure | Result |
|---|---|
| Packets graded | 179 of 179, plus the null document (180 calls) |
| Failed calls | 0 (no API or transport errors, no parse failures, no malformed verdicts; the largest packet, at 183,958 prompt tokens on this route, was accepted and graded) |
| Agreement with the finals | 153 of 179 = 85.5% (scope: 38 complete submissions, 141 at primary-plus-EX-99 scope) |
| SIGNAL precision | 0.43 (12 true positives, 16 false positives) |
| SIGNAL recall | 0.60 (12 of 20 gold SIGNAL found, 8 missed) |
| Abstentions | 0 |
| False-confident rate | 14.5% (26 of 179) |
| Null document | NO SIGNAL, p_signal 0.00 / p_no_signal 1.00, basis "empty packet" |
| Tokens consumed | 964,601 prompt + 267,106 completion = 1,231,707 total (mean per call: 5,359 prompt, 1,484 completion; completion includes reasoning tokens) |
| Latency | Mean 6.83 s per call; summed latency 1,229.1 s for the full run |
| Cost per graded filing | At the Baseten list price for meta-models/muse-spark-open (input $1.25 per million tokens, cached input $0.15, output $4.25 per million, Baseten model page, checked 2026-10-26), the full run prices to $2.34 total, about $0.013 per graded filing, charged against the workspace's free Model API credits. The post-run credit balance was not independently verified for this draft. |

Two readings of this table matter more than the headline.

- **The abstain band was never entered on this arm either.** The engine abstained zero times, and the lowest probability attached to any verdict in the run was 0.88, the same floor as the reference arm. All 26 disagreements with the key were confident disagreements, including both gold ABSTAIN filings, which the engine called NO SIGNAL at 0.90 and 0.92.
- **The worked examples repeat.** On the Cloudflare Form 144 the contestant arm also read NO SIGNAL (p_no_signal 0.92), a confident miss on the same filing, with a basis naming the same single proposed sale. On the Kratos Defense Form 144 it also read NO SIGNAL (p_no_signal 0.92), a clean agreement. On the null document it also invented nothing.

## Cross-route comparison

- **The two arms gave the same verdict on 173 of 179 filings (96.6%).** They were both wrong on the same 21 filings. The reference arm was wrong alone on 1 filing; the contestant arm was wrong alone on 5 filings.
- **The SIGNAL sets are identical.** Both arms found the same 12 gold SIGNAL filings and missed the same 8. Recall is 0.60 on both arms. The contestant arm's lower agreement comes from extra false alarms on gold NO SIGNAL filings: 16 against the reference arm's 12, which is what drops its precision from 0.50 to 0.43.
- **Cost and latency are close.** Reference arm: $2.16 total, about $0.012 per graded filing, mean latency 5.58 s. Contestant arm: $2.34 total, about $0.013 per graded filing, mean latency 6.83 s. The open model on a third-party host costs about the same per filing as the served model on Meta's own API, and runs about a second per call slower on this sample.
- **What the comparison shows.** The open-versus-served difference on this frozen sample is six filings. The shared disagreements with the key are twenty-one filings, and they fall in the same places on both arms, including the same confident miss on the same Form 144. Whatever drives those disagreements, it is common to both routes and is not a hosting difference.

## How to read this card

Agreement measures how closely an engine's verdicts track one locked answer key on one frozen sample, under one frozen prompt. A high score means the engine reads these filings the way the key does. It does not mean the key is right, and this card is never evidence for the Decider record itself: the key is the ruler, and a ruler is not validated by the things measured with it. Read the misses next to the hits. On the reference arm, the informative numbers are not the 87.7% headline but the shape underneath it: precision 0.50, recall 0.60, zero abstentions, and every one of the 22 disagreements issued at high confidence. The contestant arm tells the same story at 85.5%: precision 0.43, recall 0.60, zero abstentions, and the same eight SIGNAL filings missed.
