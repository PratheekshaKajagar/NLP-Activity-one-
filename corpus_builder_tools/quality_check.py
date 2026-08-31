"""
Basic quality/sanity checks for corpus.csv.
Run after generate_corpus.py to sanity-check the output before using it.
"""

import csv
from collections import Counter

def load(path="corpus.csv"):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def main():
    rows = load()
    texts = [r["text"] for r in rows]

    print(f"Total rows: {len(rows)}")

    # Duplicate check (should be 0 since generator dedups, but verify)
    dupes = len(texts) - len(set(t.lower().strip() for t in texts))
    print(f"Duplicate texts: {dupes}")

    # Length distribution (word count)
    lengths = [len(t.split()) for t in texts]
    print(f"Avg words/sentence: {sum(lengths)/len(lengths):.1f}")
    print(f"Min/Max words: {min(lengths)}/{max(lengths)}")

    # Coverage: are both matrix languages and all switch types represented per domain?
    by_domain = {}
    for r in rows:
        by_domain.setdefault(r["domain"], []).append(r)
    print("\nCoverage per domain (matrix_language x switch_type combos present):")
    for domain, drows in by_domain.items():
        combos = set((r["matrix_language"], r["switch_type"]) for r in drows)
        expected = 2 * 4  # 2 matrix languages x 4 switch types
        status = "OK" if len(combos) == expected else f"MISSING ({len(combos)}/{expected})"
        print(f"  {domain}: {status}")

    # Polarity balance
    pol_counts = Counter(r["polarity"] for r in rows if r["polarity"])
    if pol_counts:
        print(f"\nPolarity balance: {dict(pol_counts)}")

    print("\nReminder: these checks only catch structural issues (dupes, length, "
          "coverage gaps). They do NOT verify linguistic naturalness or "
          "grammaticality — that requires native-speaker review. See README.md.")

if __name__ == "__main__":
    main()
