"""
Synthetic Kannada-Hindi code-switched sentiment data generator.

Strategy:
  1. Template + lexicon substitution — combine domain-specific subjects with
     sentiment-bearing adjective/filler phrases drawn from a Kannada-Hindi
     code-switch lexicon, in patterns that mirror how real bilingual speakers
     switch (adjective/discourse markers in one language, subject/verb in
     another).
  2. Paraphrase augmentation of the hand-written seed set — swap interchangeable
     code-switch markers (e.g. "tumba" <-> "bahut", "chennagide" <-> "achha hai")
     to produce controlled variants without changing meaning or label.

This is a BOOTSTRAP tool, not a substitute for real data. Treat its output as
weak/silver-labeled training data — validate a sample manually (or with native
speakers) before trusting it for evaluation.
"""

import csv
import random
import itertools

random.seed(42)

# ---------------------------------------------------------------------------
# 1. Lexicon: sentiment-bearing code-switch fillers
# ---------------------------------------------------------------------------

POSITIVE_FILLERS = [
    "tumba chennagide", "bahut achha hai", "zabardast aagide",
    "tumba maja bantu", "bahut khush aagide", "super aagide",
    "tumba ista aaythu", "bahut sundar hai", "chennagi nadeyithu",
]

NEGATIVE_FILLERS = [
    "tumba ganda aagide", "bahut kharab hai", "waste aaythu",
    "tumba problem aagide", "bahut tension aagide", "sariyagi aagalilla",
    "bahut bekaar hai", "tumba kashta aagide", "disappoint aaythu",
]

NEUTRAL_FILLERS = [
    "regular aagide", "thike ansutte", "normal irodu",
    "so-so aagide", "average level hai", "usual routine ide",
    "kelavu thike kelavu illa", "sariyagi helakke aagalla",
]

# ---------------------------------------------------------------------------
# 2. Domain subjects (what the sentiment is about)
# ---------------------------------------------------------------------------

SUBJECTS = {
    "movies": ["Idu naanu nodida sinima", "Ee movie", "Naale release aada film"],
    "food": ["Idu ee restaurant food", "Amma banda oota", "Ee cafe menu"],
    "traffic": ["Idu aaj signal alli traffic", "Bus route", "Auto ride"],
    "shopping": ["Idu naanu tegedukonda item", "Ee online order", "Ee phone"],
    "work": ["Idu office meeting", "Nanna kelsa", "Ee project"],
    "travel": ["Idu weekend trip", "Flight journey", "Hotel stay"],
    "education": ["Idu naale exam", "Ee class", "Nanna results"],
    "events": ["Idu family function", "Ee concert", "Birthday party"],
    "service": ["Idu customer care", "Delivery service", "Ee shop staff"],
    "technology": ["Idu wifi connection", "Ee new phone app", "Laptop performance"],
}

TAILS = [
    "guru", "yaar", "anisutte", "gothilla", "sariyagi", "aaithu",
]

def make_sentence(subject: str, filler: str) -> str:
    tail = random.choice(TAILS)
    return f"{subject} {filler} {tail}".strip()


def generate_templated(n_per_domain: int = 20):
    rows = []
    idx = 1000
    for domain, subjects in SUBJECTS.items():
        for sentiment, fillers in [
            ("positive", POSITIVE_FILLERS),
            ("negative", NEGATIVE_FILLERS),
            ("neutral", NEUTRAL_FILLERS),
        ]:
            combos = list(itertools.product(subjects, fillers))
            random.shuffle(combos)
            for subject, filler in combos[:n_per_domain]:
                idx += 1
                rows.append({
                    "id": idx,
                    "text": make_sentence(subject, filler),
                    "sentiment": sentiment,
                    "domain": domain,
                    "gloss_en": "",  # not auto-translated; fill in if needed
                    "source": "synthetic_template",
                })
    return rows


# ---------------------------------------------------------------------------
# 3. Paraphrase augmentation of the seed set (marker swaps, label-preserving)
# ---------------------------------------------------------------------------

SWAP_PAIRS = [
    ("tumba", "bahut"),
    ("chennagide", "achha hai"),
    ("kharab", "ganda"),
    ("aaythu", "aaitu"),
    ("kelsa", "kaam"),
    ("ista", "pasand"),
]

def augment_seed(seed_path: str):
    rows = []
    with open(seed_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)  # keep original

            text = row["text"]
            for a, b in SWAP_PAIRS:
                if a in text:
                    new_text = text.replace(a, b, 1)
                    if new_text != text:
                        rows.append({
                            "id": f"{row['id']}_aug_{a}",
                            "text": new_text,
                            "sentiment": row["sentiment"],
                            "domain": row["domain"],
                            "gloss_en": row["gloss_en"],
                            "source": "paraphrase_augmented",
                        })
    return rows


def write_csv(rows, path):
    fieldnames = ["id", "text", "sentiment", "domain", "gloss_en", "source"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            for k in fieldnames:
                r.setdefault(k, "")
            writer.writerow(r)


if __name__ == "__main__":
    templated = generate_templated(n_per_domain=15)
    augmented = augment_seed("seed_dataset.csv")

    all_rows = templated + augmented
    write_csv(all_rows, "expanded_dataset.csv")

    print(f"Templated rows:  {len(templated)}")
    print(f"Augmented rows:  {len(augmented)}")
    print(f"Total generated: {len(all_rows)}")
    print("Written to expanded_dataset.csv")
