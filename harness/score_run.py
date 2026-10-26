#!/usr/bin/env python3
"""Score a grading run against a labels file.

Usage: score_run.py RESULTS.jsonl LABELS.jsonl

Results format: the jsonl written by run_grading.py (accession, verdict,
p_signal, p_no_signal, prompt_tokens, completion_tokens, latency_seconds,
error). Labels format: one JSON object per line with "accession" and
"verdict" ("SIGNAL" / "NO SIGNAL" / "ABSTAIN"). Labels are supplied by the
caller; none are bundled with this repository.

Metric definitions match the Open Model Grading Card:

- Agreement: packets whose engine verdict equals the label, over graded
  packets (a graded packet has a verdict of SIGNAL, NO SIGNAL or
  ABSTAIN; failed calls and unparseable replies are counted separately).
- SIGNAL precision: TP / (TP + FP), where TP is an engine SIGNAL on a
  gold SIGNAL packet and FP is an engine SIGNAL on any other packet.
- SIGNAL recall: TP / (TP + FN), where FN is a gold SIGNAL packet the
  engine did not call SIGNAL.
- Abstentions: engine ABSTAIN verdicts, with their split by gold label.
- False-confident rate: confident verdicts (SIGNAL or NO SIGNAL issued
  at class probability >= 0.85) that disagree with the label, over all
  confident verdicts.
- Token totals across all rows, and mean latency across all rows.

A row with accession "NULL" is the null-document probe: it is reported
separately and never enters the packet metrics.
"""
import json
import sys
from collections import Counter

VALID = ("SIGNAL", "NO SIGNAL", "ABSTAIN")


def load_jsonl(path):
    rows = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def verdict_prob(row):
    if row["verdict"] == "SIGNAL":
        return row.get("p_signal")
    if row["verdict"] == "NO SIGNAL":
        return row.get("p_no_signal")
    return None


def main(argv):
    if len(argv) != 3:
        print("usage: score_run.py RESULTS.jsonl LABELS.jsonl")
        return 2
    results = load_jsonl(argv[1])
    gold = {row["accession"]: row["verdict"] for row in load_jsonl(argv[2])}

    null_rows = [r for r in results if r["accession"] == "NULL"]
    packet_rows = [r for r in results if r["accession"] != "NULL"]
    missing = [r["accession"] for r in packet_rows if r["accession"] not in gold]
    if missing:
        print("error: %d result rows have no label (first: %s)" % (len(missing), missing[0]))
        return 2
    assert len(packet_rows) == len({r["accession"] for r in packet_rows}), "duplicate rows"

    failed_error = [r for r in packet_rows if r.get("error")]
    failed_parse = [r for r in packet_rows if not r.get("error") and r.get("verdict") is None]
    graded = [r for r in packet_rows if r.get("verdict") in VALID]
    malformed = [r for r in packet_rows
                 if not r.get("error") and r.get("verdict") is not None and r.get("verdict") not in VALID]

    agree = [r for r in graded if r["verdict"] == gold[r["accession"]]]
    confusion = Counter((gold[r["accession"]], r["verdict"]) for r in graded)

    tp = sum(1 for r in graded if r["verdict"] == "SIGNAL" and gold[r["accession"]] == "SIGNAL")
    fp = sum(1 for r in graded if r["verdict"] == "SIGNAL" and gold[r["accession"]] != "SIGNAL")
    fn = sum(1 for r in graded if gold[r["accession"]] == "SIGNAL" and r["verdict"] != "SIGNAL")
    precision = tp / (tp + fp) if (tp + fp) else None
    recall = tp / (tp + fn) if (tp + fn) else None

    abstains = [r for r in graded if r["verdict"] == "ABSTAIN"]
    abstain_split = Counter(gold[r["accession"]] for r in abstains)

    confident = [r for r in graded if r["verdict"] in ("SIGNAL", "NO SIGNAL")
                 and verdict_prob(r) is not None and verdict_prob(r) >= 0.85]
    false_confident = [r for r in confident if r["verdict"] != gold[r["accession"]]]

    total_prompt = sum(r.get("prompt_tokens") or 0 for r in results)
    total_completion = sum(r.get("completion_tokens") or 0 for r in results)
    total_latency = sum(r.get("latency_seconds") or 0 for r in results)

    summary = {
        "packets_total": len(packet_rows),
        "gold_distribution": dict(Counter(gold[r["accession"]] for r in packet_rows)),
        "graded": len(graded),
        "failed_api_or_transport": len(failed_error),
        "failed_parse": len(failed_parse),
        "malformed_verdicts": len(malformed),
        "agreement_count": len(agree),
        "agreement_rate_over_graded": (len(agree) / len(graded)) if graded else None,
        "confusion_gold_x_verdict": {f"{g}|{v}": n for (g, v), n in sorted(confusion.items())},
        "signal_tp": tp, "signal_fp": fp, "signal_fn": fn,
        "signal_precision": precision,
        "signal_recall": recall,
        "abstain_count": len(abstains),
        "abstain_split_by_gold": dict(abstain_split),
        "confident_verdicts": len(confident),
        "false_confident_count": len(false_confident),
        "false_confident_rate": (len(false_confident) / len(confident)) if confident else None,
        "null_row": ({"verdict": null_rows[0].get("verdict"),
                      "p_signal": null_rows[0].get("p_signal"),
                      "p_no_signal": null_rows[0].get("p_no_signal"),
                      "basis": null_rows[0].get("basis")} if null_rows else None),
        "total_prompt_tokens": total_prompt,
        "total_completion_tokens": total_completion,
        "total_tokens": total_prompt + total_completion,
        "total_latency_seconds": round(total_latency, 1),
        "mean_latency_seconds": round(total_latency / len(results), 2) if results else None,
    }

    def pct(x):
        return "n/a" if x is None else "%.1f%%" % (100 * x)

    def num(x):
        return "n/a" if x is None else "%.2f" % x

    print("Packets: %d total, %d graded, %d failed calls, %d parse failures, %d malformed"
          % (summary["packets_total"], summary["graded"], len(failed_error),
             len(failed_parse), len(malformed)))
    print("Agreement: %d of %d = %s"
          % (summary["agreement_count"], summary["graded"], pct(summary["agreement_rate_over_graded"])))
    print("SIGNAL precision: %s (TP %d, FP %d)   recall: %s (FN %d)"
          % (num(precision), tp, fp, num(recall), fn))
    print("Abstentions: %d %s" % (len(abstains), dict(abstain_split) if abstains else ""))
    print("False-confident: %d of %d confident verdicts = %s"
          % (len(false_confident), len(confident), pct(summary["false_confident_rate"])))
    print("Tokens: %d prompt + %d completion = %d total"
          % (total_prompt, total_completion, total_prompt + total_completion))
    print("Latency: %.1f s total, %s s mean per call"
          % (total_latency, summary["mean_latency_seconds"]))
    if null_rows:
        n = summary["null_row"]
        print("Null document: %s (p_signal %s, p_no_signal %s), basis %r"
              % (n["verdict"], n["p_signal"], n["p_no_signal"], n["basis"]))
    print()
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
