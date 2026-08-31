"""
Curated English -> Hindi (romanized) substitution lexicon, used to pivot
real Kannada-English code-mixed sentences into Kannada-Hindi code-mixed
sentences.

WHY CURATED, NOT AUTOMATED:
I initially tried an automated bilingual dictionary (a public English-Hindi
CSV) for this substitution, and it produced INCORRECT mappings for common
words — e.g. "nice" -> "मुश्किल" (which actually means "difficult"), and
"best" -> "हराना" (which means "to defeat"). That dictionary's entries
aren't ordered by primary/common sense, so blind automated lookup produces
linguistically wrong output — worse than not translating at all.

Instead, this lexicon only covers the ~40 most frequent English content words
that actually appear in the real Kannada-English YouTube comment data
(computed by frequency analysis — see build_pivot_dataset.py), each manually
checked by me for a natural, commonly-used Hindi equivalent.

DELIBERATE OMISSIONS (kept as-is, not translated):
Words like "video", "film", "hero", "heroine", "industry", "release",
"support", "sir", "boss" are common EN loanwords already used as-is in
everyday spoken Hindi — translating them (e.g. film -> chalchitra) would
actually make the text LESS natural, not more. These are intentionally left
untouched. This is a judgment call, not an oversight — see README for how to
revisit it.

STILL A SIMPLIFICATION:
Word-for-word substitution doesn't capture Hindi grammar (agreement, case,
word order differences from English) — it swaps the lexical item and leaves
the surrounding structure as Kannada+English syntax. This is fine for the
goal here (lexical-level code-switching signal for a classifier) but is NOT
equivalent to a fluent Hindi rendering. Have a native/fluent speaker review
before treating this as ground truth. See README.md.
"""

EN_TO_HI = {
    # verbs / actions
    "like": "pasand",
    "love": "pyaar",
    "dislike": "napasand",
    "cry": "rona",
    "wait": "intezaar",
    "waiting": "intezaar kar rahe",

    # adjectives / evaluative
    "good": "accha",
    "bad": "bekaar",
    "nice": "badhiya",
    "great": "shaandaar",
    "super": "zabardast",
    "superb": "zabardast",
    "awesome": "zabardast",
    "beautiful": "khoobsurat",
    "wonderful": "kamaal",
    "amazing": "kamaal",
    "best": "behtareen",
    "worst": "sabse bekaar",
    "happy": "khush",
    "sad": "udaas",
    "proud": "garv",

    # nouns
    "song": "gaana",
    "music": "sangeet",
    "story": "kahani",
    "fans": "deewane",
    "fan": "deewana",

    # discourse / social
    "thanks": "shukriya",
    "thank": "shukriya",
    "sorry": "maaf karna",
    "congratulations": "badhai",
    "respect": "samman",

    # connectors (optional — comment out if you want to keep Kannada/English
    # connectors untouched and only switch content words)
    "and": "aur",
    "but": "lekin",
    "all": "sab",
    "full": "poora",
}

# Words explicitly left unmapped on purpose (already-assimilated loanwords).
# Documented here so the choice is visible/reviewable, not silent.
DELIBERATELY_UNCHANGED = [
    "video", "film", "movie", "hero", "heroine", "industry", "release",
    "support", "sir", "boss", "fan club", "hit", "flop", "director",
]
