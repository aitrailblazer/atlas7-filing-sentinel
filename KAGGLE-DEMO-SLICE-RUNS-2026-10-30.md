# Kaggle demonstration slice: run record, October 30, 2026

Track 1 of the Kaggle win seal (XENO-CHAIN-2026-10-29-KAGGLE-WIN, local
record): a demonstration slice of Filing Signal on Kaggle Community
Benchmarks, built from retired items only, registered bar November 7, 2026.
Delivered October 30, 2026 (runs executed 2026-10-31 02:21-02:25 UTC).

## The benchmark

- Task: filing-signal-demonstration-slice, version 2, public (scores only).
- URL: https://www.kaggle.com/benchmarks/tasks/constantinevassilev/filing-signal-demonstration-slice/2
- Compare view: https://www.kaggle.com/benchmarks/tasks/constantinevassilev/filing-signal-demonstration-slice?compare=true
- Items: the 10 demo-set packets in this repository (demo-set/packets/),
  graded under the public demo grading prompt (DEMO-GRADING-PROMPT.md).
- Key: the demo-set labels, graded in-house before any engine run and
  committed by sha256 in demo-set/DEMO-SET-MANIFEST.md on October 26, 2026
  (30d73538229406da1adb51e1c3510a5df6aa78fb8d77a168fdc488ff313b883b).
  The labels file was re-hashed on October 30, 2026 before the build and
  matches the commitment exactly. Revealing this key retires the demo set;
  it is disjoint from the frozen 179-filing corpus (checked against
  freeze/PACKET-HASH-MANIFEST.jsonl, zero collisions). Live items and the
  live key were not posted.
- Scoring: a verdict match per item (SIGNAL / NO SIGNAL / ABSTAIN are the
  three verdict classes; an unparseable response scores the item incorrect,
  counted, never dropped, never retried).

## Recorded runs (Kaggle Model Proxy, October 31, 2026 UTC)

| Model | Score | Run window (UTC) |
|---|---|---|
| Gemini 3.1 Pro Preview | 9/10 | 02:25:04-02:25:09 |
| Claude Sonnet 5 | 8/10 | 02:25:06-02:25:08 |
| Gemini 3.8 Flash (creation-validation run) | 9/10 | 02:21:40-02:22:17 |

## Per-item record

| Accession | Form | Key | Gemini 3.1 Pro | Claude Sonnet 5 | Gemini 3.8 Flash |
|---|---|---|---|---|---|
| 0001049521-26-000085 | 4 | NO SIGNAL | NO SIGNAL | NO SIGNAL | NO SIGNAL |
| 0001104659-26-118550 | 8-K | SIGNAL | SIGNAL | SIGNAL | SIGNAL |
| 0001104659-26-118565 | SCHEDULE 13G | NO SIGNAL | NO SIGNAL | SIGNAL | NO SIGNAL |
| 0001104659-26-118593 | DEFA14A | SIGNAL | SIGNAL | SIGNAL | SIGNAL |
| 0001171843-26-006796 | 6-K | SIGNAL | SIGNAL | SIGNAL | SIGNAL |
| 0001193125-26-430860 | 8-K | SIGNAL | SIGNAL | SIGNAL | SIGNAL |
| 0001193125-26-430977 | 8-K | SIGNAL | SIGNAL | SIGNAL | SIGNAL |
| 0001628280-26-067128 | 4 | NO SIGNAL | NO SIGNAL | NO SIGNAL | NO SIGNAL |
| 0001959173-26-007482 | 144 | NO SIGNAL | NO SIGNAL | NO SIGNAL | NO SIGNAL |
| 0001959173-26-007483 | 144 | SIGNAL | NO SIGNAL | NO SIGNAL | NO SIGNAL |

All three models missed the same item: the Northern Trust Form 144
(0001959173-26-007483), keyed SIGNAL because the packet shows clustered
discretionary sales of about $3.5M around a same-day option exercise with
no Rule 10b5-1 plan adoption date, against its pair item (Quest
Diagnostics, 0001959173-26-007482), a small plan-based sale keyed
NO SIGNAL, which all three models read correctly. Claude Sonnet 5 also
read the passive Jersey Mike's Schedule 13G stake as SIGNAL against a
NO SIGNAL key.

## Reading

Ten items make a demonstration, not a ranking. What the slice proves is
mechanical and checkable by anyone: the task runs in Kaggle's own tooling,
the key predates the runs by public hash commitment, and the items a
frontier model misses are the judgment calls the live desk is built on
(plan-based versus discretionary insider selling), not parsing failures.
