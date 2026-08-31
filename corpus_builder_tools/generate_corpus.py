"""
Generate a Kannada-Hindi code-switched corpus.

Output: corpus.csv with columns:
  id, text, domain, matrix_language, switch_type, polarity, source

- matrix_language: which language provides the grammatical frame
- switch_type: where the switch happens (see templates.py docstring)
- polarity: optional sentiment tag (positive/negative/neutral) — set
  INCLUDE_POLARITY = False below if you don't need this axis at all.
- source: "synthetic_template" for everything this script makes. Keep this
  column even after you add real data, so provenance stays traceable.

This produces a few thousand rows at default settings. It's meant to give you
volume + structural diversity (different switch types, both matrix-language
directions) for pretraining/bootstrapping — NOT a substitute for a reviewed
real-world evaluation set. See README.md.
"""

import csv
import random
import itertools

from lexicon import (
    KANNADA_DISCOURSE, HINDI_DISCOURSE,
    KANNADA_CONNECTORS, HINDI_CONNECTORS,
    KANNADA_VERBS, HINDI_VERBS,
    POSITIVE_ADJ, NEGATIVE_ADJ, NEUTRAL_ADJ,
    DOMAINS,
)
from templates import (
    discourse_marker_switch, connector_switch, noun_phrase_switch, tag_switch,
)

random.seed(7)

INCLUDE_POLARITY = True   # set False to drop the sentiment axis entirely
SAMPLES_PER_CONFIG = 6    # how many sentence variants per (domain, switch_type, matrix_lang, polarity)

POLARITY_ADJ = {
    "positive": POSITIVE_ADJ,
    "negative": NEGATIVE_ADJ,
    "neutral": NEUTRAL_ADJ,
}


def opposite(lang):
    return "hindi" if lang == "kannada" else "kannada"


def verbs_for(lang):
    return KANNADA_VERBS if lang == "kannada" else HINDI_VERBS


def discourse_for(lang):
    # discourse marker is drawn from the OPPOSITE of the matrix language
    return HINDI_DISCOURSE if lang == "kannada" else KANNADA_DISCOURSE


def connector_for(lang):
    return HINDI_CONNECTORS if lang == "kannada" else KANNADA_CONNECTORS


def adj_for(lang, polarity):
    return POLARITY_ADJ[polarity][lang]


def gen_discourse_marker_rows(domain, matrix_lang, polarity):
    rows = []
    phrase_options = DOMAINS[domain][matrix_lang]
    verb_options = verbs_for(matrix_lang)
    adj_options = adj_for(matrix_lang, polarity)
    disc_options = discourse_for(matrix_lang)

    combos = list(itertools.product(phrase_options, verb_options, adj_options, disc_options))
    random.shuffle(combos)
    for phrase, verb, adj, disc in combos[:SAMPLES_PER_CONFIG]:
        text = discourse_marker_switch(matrix_lang, phrase, verb, adj, disc)
        rows.append((text, "discourse_marker"))
    return rows


def gen_connector_rows(domain, matrix_lang, polarity):
    rows = []
    other_lang = opposite(matrix_lang)
    c1_phrases = DOMAINS[domain][matrix_lang]
    c1_verbs = verbs_for(matrix_lang)
    connectors = connector_for(matrix_lang)  # connector borrowed from other language
    c2_phrases = DOMAINS[domain][other_lang]
    c2_adjs = adj_for(other_lang, polarity)

    combos = list(itertools.product(c1_phrases, c1_verbs, connectors, c2_phrases, c2_adjs))
    random.shuffle(combos)
    for c1p, c1v, conn, c2p, c2a in combos[:SAMPLES_PER_CONFIG]:
        text = connector_switch(matrix_lang, c1p, c1v, conn, c2p, c2a)
        rows.append((text, "connector"))
    return rows


def gen_noun_phrase_rows(domain, matrix_lang, polarity):
    rows = []
    other_lang = opposite(matrix_lang)
    other_phrases = DOMAINS[domain][other_lang]   # noun phrase borrowed from other language
    verb_options = verbs_for(matrix_lang)
    adj_options = adj_for(matrix_lang, polarity)

    combos = list(itertools.product(other_phrases, verb_options, adj_options))
    random.shuffle(combos)
    for phrase, verb, adj in combos[:SAMPLES_PER_CONFIG]:
        text = noun_phrase_switch(matrix_lang, phrase, verb, adj)
        rows.append((text, "noun_phrase"))
    return rows


def gen_tag_rows(domain, matrix_lang, polarity):
    rows = []
    other_lang = opposite(matrix_lang)
    phrases = DOMAINS[domain][matrix_lang]
    verb_options = verbs_for(matrix_lang)
    tag_adjs = adj_for(other_lang, polarity)  # tag comes from the OTHER language

    combos = list(itertools.product(phrases, verb_options, tag_adjs))
    random.shuffle(combos)
    for phrase, verb, tag in combos[:SAMPLES_PER_CONFIG]:
        text = tag_switch(matrix_lang, phrase, verb, tag)
        rows.append((text, "tag"))
    return rows


GENERATORS = {
    "discourse_marker": gen_discourse_marker_rows,
    "connector": gen_connector_rows,
    "noun_phrase": gen_noun_phrase_rows,
    "tag": gen_tag_rows,
}


def generate_corpus():
    all_rows = []
    idx = 1

    polarities = ["positive", "negative", "neutral"] if INCLUDE_POLARITY else ["n/a"]

    for domain in DOMAINS:
        for matrix_lang in ["kannada", "hindi"]:
            for polarity in polarities:
                pol_for_lookup = polarity if INCLUDE_POLARITY else "neutral"
                for switch_type, gen_fn in GENERATORS.items():
                    generated = gen_fn(domain, matrix_lang, pol_for_lookup)
                    for text, st in generated:
                        all_rows.append({
                            "id": idx,
                            "text": text,
                            "domain": domain,
                            "matrix_language": matrix_lang,
                            "switch_type": st,
                            "polarity": polarity if INCLUDE_POLARITY else "",
                            "source": "synthetic_template",
                        })
                        idx += 1

    # Dedup on text, keep first occurrence
    seen = set()
    deduped = []
    for row in all_rows:
        key = row["text"].strip().lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(row)

    return deduped


def write_csv(rows, path):
    fieldnames = ["id", "text", "domain", "matrix_language", "switch_type", "polarity", "source"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    rows = generate_corpus()
    write_csv(rows, "corpus.csv")
    print(f"Generated {len(rows)} unique code-switched sentences -> corpus.csv")

    # quick breakdown
    from collections import Counter
    by_domain = Counter(r["domain"] for r in rows)
    by_switch = Counter(r["switch_type"] for r in rows)
    by_matrix = Counter(r["matrix_language"] for r in rows)
    print("By domain:", dict(by_domain))
    print("By switch_type:", dict(by_switch))
    print("By matrix_language:", dict(by_matrix))
