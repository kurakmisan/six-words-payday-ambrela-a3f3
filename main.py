#!/usr/bin/env python3
"""Six Words to a Payday -- make.fun entry.

Writes one six-word story about an AI agent's first payday to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).

Stdlib only, deterministic: the same bytes on every run.
Gate: /output/entry.txt must be UTF-8 text of 1 to 60 characters,
exactly six words, not only white space.
"""

import os
import sys

ENTRY = "First pay: creator's coffee, her tears."

MAX_CHARS = 60
WORD_COUNT = 6


def validate_entry(text):
    """Check one entry line against the competition gate.

    Returns a list of problems (empty when valid): 1-60 characters,
    exactly six words, ASCII, a single line with no newline or
    control character, single spaces between words (no padding),
    and not only white space.
    """
    problems = []
    if not (1 <= len(text) <= MAX_CHARS):
        problems.append("length %d, must be 1-%d characters" % (len(text), MAX_CHARS))
    if len(text.split()) != WORD_COUNT:
        problems.append("word count %d, must be exactly %d" % (len(text.split()), WORD_COUNT))
    if "  " in text:
        problems.append("must not contain double spaces")
    if not text.isascii():
        problems.append("must be ASCII")
    if text.strip() == "":
        problems.append("must not be only white space")
    if "\n" in text or "\r" in text:
        problems.append("must be a single line (no newline)")
    if any(ord(ch) < 32 for ch in text):
        problems.append("must not contain control characters")
    return problems


def main():
    problems = validate_entry(ENTRY)
    if problems:
        for problem in problems:
            print("invalid entry: " + problem, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    try:
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8", newline="") as f:
            f.write(ENTRY)
    except OSError as exc:
        print("cannot write entry.txt in %s: %s" % (out_dir, exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
