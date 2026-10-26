# Sealed demo set: manifest

Date: 2026-10-26 (America/Los_Angeles). Built for the Meta hackathon
submission (ATLAS-7 Filing Sentinel) as the live demo batch defined in the
Open Model Grading freeze pack: a small set drawn from the day's real
filings, outside the frozen 179, with labels sealed before any engine run.

## Label seal

- Labels file: sealed in-house before any engine run. It never ships
  and is not part of this repository.
- sha256 of the labels file:
  `30d73538229406da1adb51e1c3510a5df6aa78fb8d77a168fdc488ff313b883b`
- Label split: 6 SIGNAL / 4 NO SIGNAL / 0 ABSTAIN over 10 packets.
- Labels were graded in-house from the packets alone, under the same
  rubric and precedents as the frozen corpus (Decider blind grading
  rubric, Oct 2026 round), after packet assembly and before any engine
  or external API saw these packets. No external engine was run on
  this set in this build.

## Selection rule (deterministic)

Source: SEC EDGAR "latest filings" Atom feeds
(`browse-edgar?action=getcurrent`, paged by form type, 100 per page),
snapshotted 2026-10-26 at about 15:02 ET / 12:02 PT. Candidate pool:
every filing in those feeds whose EDGAR filing date is 2026-10-26 and
whose feed form term matches the target form exactly (exact-form
matching excludes all /A amendments). Pool sizes at snapshot: 8-K 88,
Form 4 34, Form 144 14, Schedule 13D/13G combined 5, 6-K 75,
DEFA14A 7.

Within each form, filings were ordered by acceptance time (ET)
earliest first, ties broken by accession number ascending, and taken
in that order to fill the frozen mix: 8-K x3, Form 4 x2, Form 144 x2,
one Schedule slot (earliest of Schedule 13D and Schedule 13G
combined), 6-K x1, and one final slot filled by the earliest DEFA14A
of the day (a DEFA14A had been filed; had none been filed, the next
8-K in order would have filled the slot). Any accession already in
the frozen 179 (checked against the filenames in
`~/workspace/decider-training-20261016/packets-179-v3/`) was to be
skipped; none of the selected accessions collided, and no selected
filing had to be skipped for any other reason. Amended duplicates are
excluded by the exact-form rule above.

## Assembly

Packets were assembled with the corpus tooling, packet-assembler-v2
(`~/workspace/decider-pipeline/packet-assembler-v2/assemble.py`), run
once per accession against live EDGAR. All 10 packets reconcile
(included + excluded + failed = index document count) and carry
STATUS: COMPLETE with 0 failed documents. One packet
(Nanobiotix 6-K) needed a single re-run after a transient fetch
failure; the re-run completed COMPLETE.

Conventions inherited from the assembler, identical to the frozen
corpus: the Schedule 13G packet's FORM header line reads "SCHEDULE"
(the document type, SCHEDULE 13G, is in its document list); for
Form 4 packets the COMPANY line names the reporting person, with the
issuer named in the packet body (noted in the table below).

## The 10 packets

| Accession | Form | Company (packet COMPANY line) | Accepted (ET) | Packet bytes | Packet sha256 |
|---|---|---|---|---|---|
| 0001193125-26-430860 | 8-K | Eikon Therapeutics, Inc. | 2026-10-26 06:00:36 | 21834 | 3e1174c0b9de955ee52475f1451e8f674af6ea0320db6c28cb13b1875d740724 |
| 0001104659-26-118550 | 8-K | ArriVent BioPharma, Inc. | 2026-10-26 06:00:49 | 11464 | 0c166b088bd23649c70c9ca771ba275e75c796c6a7736bc00c5e63a25fa0b737 |
| 0001193125-26-430977 | 8-K | Phathom Pharmaceuticals, Inc. | 2026-10-26 06:02:03 | 8027 | 5bc14e54e7d6695459bfb90ef9d623b54f88834eca3a73a178b22636cb9a1f16 |
| 0001628280-26-067128 | 4 | Lyons Emer (issuer: ICON plc) | 2026-10-26 06:57:03 | 4455 | ecbad790ae4c7693a4b70c6d37825de9f5ea13d8384fced6dd25173cb02baa4c |
| 0001049521-26-000085 | 4 | KUPINSKY STUART (issuer: Mercury Systems Inc) | 2026-10-26 07:26:26 | 751 | 1859f10bfab447fa1c0626e79c111f18c73d518f92eec272524c389a9180ecc3 |
| 0001959173-26-007482 | 144 | QUEST DIAGNOSTICS INC | 2026-10-26 09:46:42 | 850 | 0ba0bc8c7b235aedbccf43c325c5138d1ce7ac3bb19d1afaaa1b859b6b42e9c5 |
| 0001959173-26-007483 | 144 | NORTHERN TRUST CORP | 2026-10-26 09:56:34 | 911 | bb3e5def05272c2a2f17e043bf1e40f7b9a642012729523fab510b90b1021000 |
| 0001104659-26-118565 | SCHEDULE 13G | Jersey Mike's Subs Inc. | 2026-10-26 06:02:54 | 5420 | 23820de7ee34dca46354429edb8841c684e8d59bfc4489a8374a72af42dc2e96 |
| 0001171843-26-006796 | 6-K | Nanobiotix S.A. | 2026-10-26 06:00:16 | 14026 | 1eb95dd27b9dc23e99f67548a4f036ae7a87d207f7c94f5c33549804da39a2c3 |
| 0001104659-26-118593 | DEFA14A | Braemar Hotels & Resorts Inc. | 2026-10-26 06:31:13 | 44166 | 5a1e1d4925de23dcaa68ece44003c4f628e1250a6b431bd5a999931de5379765 |

Packets live in `packets/` in this directory, one .md per accession.
Packet hashes above were recomputed from the written files after
assembly and match the files on disk.
