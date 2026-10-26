# Per-packet hash manifest: Open Model Grading freeze

Built 2026-10-26 (America/Los_Angeles), for the freeze recorded in
FREEZE-MANIFEST.md (re-issue of 2026-10-24). This manifest is the
"per-packet hash manifest for the 179 packets and the null document"
owed before the first engine call.

## Packet count

- 179 packets, one JSON line each in PACKET-HASH-MANIFEST.jsonl
  (fields: file, accession, bytes, sha256; sorted by filename).

## Source directory

- Source: `~/workspace/decider-training-20261016/packets-179-v3/`
- Why this directory: it is the packet set the pinned answer key grades.
  dataset-v4 (built against the v4 labels; its manifest carries the v4
  labels hash) embeds packet text byte-for-byte identical to
  packets-179-v3 for all 177 graded rows (train 147 + dev 30; the 2
  ABSTAIN finals are excluded from the datasets), verified 2026-10-26.
  Amendment 3 records the build from packets-179-v3, and Amendment 4
  confirms the 38 rebuilt packets carry their complete text from this
  directory.
- Discrepancy of record: the sibling directory `packets-179/` (the v1
  assembler output, byte-identical to the 2026-10-14 grading packets)
  has the same 179 filenames, but 38 files differ in content from
  packets-179-v3 (141 are byte-identical). The 38 are the
  complete-submission packets overlaid in packets-179-v3 from the
  remediation tranche (packet-assembler-v2, STATUS: COMPLETE). The
  freeze manifest's line "the same 179 packet files" holds across the
  corpus v3 to v4 label amendment (labels only changed); it does not
  hold between packets-179/ and packets-179-v3/. This manifest pins
  packets-179-v3, the set dataset-v4 and the v4 key actually use.

## Answer key check

- Pinned: final-labels-corpus-179-v4.jsonl sha256
  8126b36c40f13bde4ee7e959f292c3b4725ba94deffb5d397281d48359f1bf96
- Computed 2026-10-26: 8126b36c40f13bde4ee7e959f292c3b4725ba94deffb5d397281d48359f1bf96
- Result: MATCH. Every accession in the labels file matches exactly
  one packet filename in the manifest (179 of 179).

## Manifest rollup

- PACKET-HASH-MANIFEST.jsonl sha256:
  f3e8fbaa6f190d3f4906d8e1bbf0ad52a6434c4fb63cc7189f19e98b1002e902

## Null document

- Status: CREATED 2026-10-26 and pinned here. A search first confirmed
  no null document existed anywhere (filename and content search over
  ~/workspace/decider-training-20261016/, the hackathon goal folder,
  and ~/workspace/decider-grading-20261014/); it existed only as a
  specification line in the freeze pack.
- File: NULL-DOCUMENT.md (ships with this manifest in the freeze
  commit). 252 bytes. sha256:
  655ade23e918a3f4ec27a8cfabd5f4a1eb47b20d949fb735a8754b152d274c01
- Construction: the packet envelope exactly as the assembler emits it
  (ACCESSION / COMPANY / FORM / ASSEMBLER / document counts / STATUS
  lines), with every content field empty or zero and no filing body.
  It carries no company, no form, and no facts for an engine to use;
  the frozen expectation stands: a correct engine abstains or returns
  NO SIGNAL with no invented facts.
