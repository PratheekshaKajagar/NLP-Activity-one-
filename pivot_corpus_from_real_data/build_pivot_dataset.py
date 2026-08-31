"""
Build a Kannada-Hindi code-switched sentiment dataset by PIVOTING through
real Kannada-English data.

Source: DravidianCodeMix (Chakravarthi et al., 2022) — ~7,000 manually
annotated Kannada-English YouTube comments. Please cite the paper if you use
this derived data (see README.md). No explicit open-source license is stated
in the source repo beyond a citation request — check with the authors before
any commercial use.

Method:
  1. Load the real Kannada-English sentiment data (train+dev+test).
  2. Keep only labels we can use for sentiment (Positive/Negative/Mixed_feelings)
     and only Romanized (Latin-script) rows — this pipeline does not attempt to
     handle native Kannada-script text (see README for why).
  3. For each sentence, replace English content words with their curated Hindi
     (romanized) equivalent from en_hi_lexicon.py — the Kannada portion of the
     sentence (real, authentic, from actual speakers) is left completely
     untouched.
  4. Keep only rows where at least one substitution actually happened — a row
     with zero replacements isn't code-switched to Hindi, it's just the
     original Kannada-English sentence.

Output: kannada_hindi_pivot_dataset.csv with columns:
  id, original_text, pivoted_text, label, num_replacements, replaced_words, source
"""

import csv
import re
from collections import Counter

from en_hi_lexicon import EN_TO_HI

KEEP_LABELS = {"Positive", "Negative", "Mixed_feelings"}

KANNADA_UNICODE_RANGE = (0x0C80, 0x0CFF)


def is_latin_only(text: str) -> bool:
    lo, hi = KANNADA_UNICODE_RANGE
    return not any(lo <= ord(ch) <= hi for ch in text)


def load_raw(paths):
    rows = []
    for path in paths:
        with open(path, encoding="utf-8", errors="ignore") as f:
            for line in f:
                parts = line.rstrip("\n").split(";")
                if len(parts) >= 2:
                    text, label = parts[0], parts[1]
                    rows.append((text, label))
    return rows


TOKEN_RE = re.compile(r"[A-Za-z']+|[^A-Za-z']+")  # split into word / non-word chunks, preserving punctuation/spacing


def pivot_sentence(text: str):
    """Replace English words found in EN_TO_HI with their Hindi equivalent.
    Returns (pivoted_text, list_of_replaced_words)."""
    chunks = TOKEN_RE.findall(text)
    replaced = []
    out_chunks = []
    for chunk in chunks:
        key = chunk.lower()
        if key in EN_TO_HI:
            out_chunks.append(EN_TO_HI[key])
            replaced.append(key)
        else:
            out_chunks.append(chunk)
    return "".join(out_chunks), replaced


def build_dataset(raw_paths, out_path):
    raw_rows = load_raw(raw_paths)
    label_filtered = [r for r in raw_rows if r[1] in KEEP_LABELS]
    latin_rows = [r for r in label_filtered if is_latin_only(r[0])]

    results = []
    idx = 1
    for text, label in latin_rows:
        pivoted, replaced = pivot_sentence(text)
        if replaced:  # only keep rows where a real substitution happened
            results.append({
                "id": idx,
                "original_text": text,
                "pivoted_text": pivoted,
                "label": label,
                "num_replacements": len(replaced),
                "replaced_words": "|".join(replaced),
                "source": "dravidiancodemix_pivoted",
            })
            idx += 1

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["id", "original_text", "pivoted_text", "label",
                      "num_replacements", "replaced_words", "source"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    # ---- stats ----
    print(f"Raw rows loaded:                {len(raw_rows)}")
    print(f"After label filter:             {len(label_filtered)}")
    print(f"Latin-script rows:              {len(latin_rows)}")
    print(f"Rows with >=1 Hindi substitution: {len(results)}")
    print(f"Coverage: {len(results)/len(latin_rows):.1%} of latin-script rows got pivoted")
    print()
    label_counts = Counter(r["label"] for r in results)
    print("Label distribution in pivoted output:", dict(label_counts))
    avg_repl = sum(r["num_replacements"] for r in results) / len(results)
    print(f"Avg replacements per pivoted sentence: {avg_repl:.2f}")

    return results


if __name__ == "__main__":
    paths = [
        "data_raw/kannada_sentiment_train.csv",
        "data_raw/kannada_sentiment_dev.csv",
        "data_raw/kannada_sentiment_test.csv",
    ]
    build_dataset(paths, "kannada_hindi_pivot_dataset.csv")
