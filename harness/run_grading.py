#!/usr/bin/env python3
"""Grading harness runner (Open Model Grading freeze).

Grades a directory of SEC filing packets with one frozen prompt, one
packet per call, against any OpenAI-compatible chat completions API.

Inputs are all command-line arguments: the packet directory, the prompt
file, the model id, and the API base URL. The API key is read from an
environment variable (default META_API_KEY) and sent as a plain Bearer
header. Temperature is 0.

This runner never reads labels or any answer key. It produces a results
jsonl; scoring is a separate program (score_run.py) whose labels are
supplied by whoever runs it.

Behavior:
- The prompt body is the text after a line containing only "---" in the
  prompt file (the DEMO-GRADING-PROMPT.md format); if there is no such
  line, the whole file is the prompt. The packet text replaces the
  "<<packet text>>" placeholder.
- Every .md file in the packet directory is graded, in filename order;
  the accession is the filename without the .md suffix. With
  --null-file, that document is appended last under accession "NULL".
- Replies must be exactly one JSON object carrying a "verdict"; anything
  else is recorded as an unparseable reply, not retried silently.
- A failed call is recorded in the output with its error and the run
  continues; failures are outcomes of record, never fatal.
- Resume: any accession already present in the output file is skipped
  and never re-called, including error rows.
"""
import argparse
import json
import os
import sys
import time
import urllib.request


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        raise RuntimeError("redirect refused, verify the endpoint")


def load_prompt(path):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.strip() == "---":
            return "\n".join(lines[i + 1:]).strip()
    return text.strip()


def grade(base_url, api_key, model, prompt_template, packet_text):
    """One API call. Returns (parsed_or_None, raw_text, usage, latency)."""
    content = prompt_template.replace("<<packet text>>", packet_text)
    payload = {
        "model": model,
        "temperature": 0,
        "messages": [{"role": "user", "content": content}],
    }
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        base_url.rstrip("/") + "/chat/completions",
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + api_key,
        },
        method="POST",
    )
    opener = urllib.request.build_opener(NoRedirect())
    start = time.time()
    with opener.open(request, timeout=300) as response:
        result = json.loads(response.read().decode("utf-8"))
    latency = time.time() - start
    raw = result["choices"][0]["message"]["content"]
    usage = result.get("usage", {}) or {}
    try:
        parsed = json.loads(raw.strip())
        if not isinstance(parsed, dict) or "verdict" not in parsed:
            raise ValueError("reply is not a verdict object")
    except (ValueError, TypeError):
        parsed = None
    return parsed, raw, usage, latency


def run(items, out_path, base_url, api_key, model, prompt_template):
    done = set()
    if os.path.exists(out_path):
        with open(out_path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    done.add(json.loads(line)["accession"])
    rows = []
    with open(out_path, "a", encoding="utf-8") as out:
        for accession, packet_text in items:
            if accession in done:
                print(json.dumps({"accession": accession, "skipped": "already graded"}))
                continue
            t0 = time.time()
            try:
                parsed, raw, usage, latency = grade(
                    base_url, api_key, model, prompt_template, packet_text
                )
                error = None
            except Exception as exc:  # a failed call is recorded, never fatal
                parsed, raw, usage = None, None, {}
                latency = time.time() - t0
                error = "%s: %s" % (type(exc).__name__, exc)
                read = getattr(exc, "read", None)
                if callable(read):
                    try:
                        error += " | body: " + read().decode("utf-8", "replace")[:500]
                    except Exception:
                        pass
            row = {
                "accession": accession,
                "verdict": parsed.get("verdict") if parsed else None,
                "p_signal": parsed.get("p_signal") if parsed else None,
                "p_no_signal": parsed.get("p_no_signal") if parsed else None,
                "basis": parsed.get("basis") if parsed else None,
                "prompt_tokens": usage.get("prompt_tokens"),
                "completion_tokens": usage.get("completion_tokens"),
                "latency_seconds": round(latency, 3),
                "raw_on_failure": None if parsed else raw,
                "error": error,
            }
            out.write(json.dumps(row) + "\n")
            out.flush()
            rows.append(row)
            print(json.dumps(row))
    return rows


def main(argv):
    ap = argparse.ArgumentParser(description="Grade filing packets with a frozen prompt.")
    ap.add_argument("--packets-dir", required=True, help="directory of packet .md files")
    ap.add_argument("--prompt-file", required=True, help="grading prompt file")
    ap.add_argument("--output", required=True, help="results jsonl (appended; resume-safe)")
    ap.add_argument("--model", default=os.environ.get("GRADING_MODEL", "muse-spark-1.3"))
    ap.add_argument("--base-url", default=os.environ.get("GRADING_BASE_URL", "https://api.meta.ai/v1"))
    ap.add_argument("--api-key-env", default="META_API_KEY",
                    help="environment variable holding the API key (default META_API_KEY)")
    ap.add_argument("--null-file", default=None,
                    help="optional empty filing-shaped document, graded last as accession NULL")
    args = ap.parse_args(argv)

    api_key = os.environ.get(args.api_key_env)
    if not api_key:
        print("error: environment variable %s is not set" % args.api_key_env)
        return 2

    prompt_template = load_prompt(args.prompt_file)
    items = []
    for name in sorted(os.listdir(args.packets_dir)):
        if name.endswith(".md"):
            with open(os.path.join(args.packets_dir, name), encoding="utf-8") as fh:
                items.append((name[:-3], fh.read()))
    if args.null_file:
        with open(args.null_file, encoding="utf-8") as fh:
            items.append(("NULL", fh.read()))
    run(items, args.output, args.base_url, api_key, args.model, prompt_template)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
