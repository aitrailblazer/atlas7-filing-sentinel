# Measurement Results, October 30, 2026

Two measurements, pre-registered before any run and published here on
the registered date.

**Pre-registration:** dated 2026-10-28, sha256
`3adeac9f431647777fc50a2cba49bae79b553dcc16e949943e1d14eacb45d050`.
The designs, the sampling rules, the key-build method, and the spend
guardrail were written and dated on 2026-10-28, the same day the
hackathon submission was filed, and before either measurement ran.
The registration date is stated plainly: there is no earlier
registration, and nothing here is backdated.

**What does not publish:** the new answer key and its labels never
enter this repository, and neither do the corpus packets. What
publishes is what the registration promised: aggregate results and
receipts.

## The corpus

- N = 1,861 fresh filings: EDGAR filing dates 2026-10-27 (950) and
  2026-10-28 (911), both after the 2026-10-26 freeze of the exam in
  this repository.
- Exclusion hits against the frozen 179-filing exam and the sealed
  10-filing demo set: 0.
- The registered pool cap was 2,000; the pool came in at 1,861, so
  the whole pool is the corpus.
- Packets built complete: 1,861 of 1,861, zero failed documents.
- The Oct 28 frame was cross-verified by two EDGAR sources (the
  post-close Atom sweep and the daily master index) in exact
  accession agreement.

## Measurement 1: does the raw model ever say not sure at scale?

Design: the frozen exam prompt from this repository, verbatim, one
call per filing, no harness, no retries. Failures are counted, never
dropped and never retried. The prompt's not-sure verdict is the
literal string ABSTAIN. Two arms over the full corpus:

- **Reference:** Muse Spark 1.3, served by the Meta Model API.
- **Contestant:** Muse Spark Open (meta-models/muse-spark-open-1026),
  served by Baseten.

| Measure | Reference (Spark 1.3) | Contestant (Spark Open) |
|---|---|---|
| Calls | 1,861 | 1,861 |
| Parsed | 1,860 | 1,860 |
| Failures (counted, not retried) | 1 (HTTP 500, a Form 4) | 1 (HTTP 502, a 6-K) |
| ABSTAIN count | 6 | 0 |
| ABSTAIN rate of parsed | 0.32% | 0.00% |
| Verdicts: SIGNAL / NO SIGNAL | 971 / 883 | 1,041 / 819 |
| Winning probability: min | 0.55 | 0.86 |
| Winning probability: p5 | 0.90 | 0.88 |
| Winning probability: median | 0.95 | 0.93 |
| Verdicts issued below the 0.85 line | 0 (0.00%) | 0 (0.00%) |
| Prompt tokens | 17,584,273 | 17,838,277 |
| Completion tokens | 2,399,403 | 3,051,631 |

Finding: at full scale, the raw models essentially never say not
sure. Across 3,720 parsed gradings there are six abstentions, all
from the reference arm, and not one verdict in either arm was issued
below the 0.85 confidence line the prompt sets. The abstention the
frozen exam measured on 179 filings is not a small-sample artifact;
it holds at ten times the scale.

## Measurement 2: matched validation of the product grading method

Design: a 200-packet validation set drawn from the same fresh corpus
by the registered rule (every 9th packet in filing-date, accession
order; k = floor(1861/200) = 9). The answer key was built by the
registered method and locked before any arm ran:

- Two blind Muse grading desks graded all 200 packets (Desk A:
  SIGNAL 81 / NO SIGNAL 102 / ABSTAIN 17; Desk B: SIGNAL 80 /
  NO SIGNAL 93 / ABSTAIN 27). Desk agreement: 177 of 200 (88.5%).
- The 23 disagreements were ruled by a fresh judge blind to label
  origin: SIGNAL 3, NO SIGNAL 7, ABSTAIN 13.
- Locked key distribution: SIGNAL 79 / NO SIGNAL 96 / ABSTAIN 25.
- Human lock: Constantine Vassilev, 2026-10-28 at about 22:09 PT,
  before any validation arm ran. Locked key sha256
  `e3a4562242f69f0a54cc54267b64c3972a9439572176acc0f3e015b8a8e64125`
  (the key itself does not publish). No label changed after the
  lock, and the product method was not tuned on this set.

Arms: the raw model (Muse Spark 1.3, frozen prompt, no harness)
against the product method (the same prompt inside the Sentinel
harness: the filer's prior-sequence state attached, and the 85
percent line enforced mechanically, so a definite verdict issued
below 0.85 is recorded as ABSTAIN whatever the model said). Both
arms: 200 calls, 200 parsed, 0 failures.

| Measure | Raw (Spark 1.3) | Product method |
|---|---|---|
| Agreement with the locked key | 158/200 = 79.0% | 164/200 = 82.0% |
| Agreement on key SIGNAL (79) | 78/79 = 98.7% | 79/79 = 100% |
| Agreement on key NO SIGNAL (96) | 79/96 = 82.3% | 85/96 = 88.5% |
| Agreement on key ABSTAIN (25) | 1/25 = 4.0% | 0/25 = 0.0% |
| Verdicts: SIGNAL / NO SIGNAL / ABSTAIN | 112 / 87 / 1 | 106 / 94 / 0 |
| ABSTAIN (not sure) count | 1 | 0 |
| Prompt tokens | 1,952,843 | 2,010,901 |
| Completion tokens | 259,231 | 284,662 |

- Cross-arm agreement: 186 of 200 (93.0%).
- The mechanical 85 percent enforcement fired 0 times on this set:
  the underlying model never issued a definite verdict below the
  line, so the product arm's recorded verdicts are the model's own
  verdicts on all 200 filings, and the measured +3.0 point
  difference between the arms comes from the sequence attachment
  alone.
- Neither arm reproduces the key's abstentions. The raw arm issued a
  definite verdict on 24 of the 25 key-ABSTAIN filings; the product
  arm on 25 of 25. The abstain band in the locked key was built by
  the two-desk-plus-judge process; neither single-pass arm, raw or
  harnessed, sits out the same filings.

**Stated limitation:** the product arm implements the registered
minimum of the product method: sequence attachment built from EDGAR
submissions data, plus the mechanical enforcement. The production
scaffolding's internals are not published and are not reproduced
beyond the registered components, and the enforcement component was
not exercised on this set.

## Spend record

- Measurement 1: about $72.10. Reference about $36.83, an
  implied-rate estimate against the Meta Model API grant ($147.85
  remained on the grant before this program; it is an estimate, not
  a billed amount). Contestant $35.27, exact at Baseten list rates,
  drawn on the $100 Baseten hackathon credit.
- Measurement 2: about $8.31 (raw about $4.08, product about $4.23;
  Meta grant, same implied rate).
- Program total: about $80.41 against the roughly $74 projection
  approved on 2026-10-28. The overage came from packet size: about
  9,700 prompt tokens per filing on average, above the guardrail's
  assumption. No real-money spend anywhere in the program.

Published 2026-10-30 by AITrailblazer, per the pre-registration of
2026-10-28.
