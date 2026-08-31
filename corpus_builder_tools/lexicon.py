"""
Kannada-Hindi code-switch lexicon.

Organized by:
  - grammatical/discourse category (discourse markers, connectors, verbs, adjectives)
  - domain (food, travel, work, etc.)

Words are given in Romanized transliteration (the dominant script for
code-mixed social text in India). Native-script (Devanagari / Kannada script)
variants can be layered on later if your project needs script-level realism.

NOTE: this is a starting lexicon, not a linguistically exhaustive one.
Have a native/fluent Kannada-Hindi bilingual speaker review and extend it —
see README.md.
"""

# ---------------------------------------------------------------------------
# Discourse markers / fillers — these are the most common actual switch points
# in real bilingual speech (a marker from language B dropped into a language A
# sentence), so they're a good source of "natural-feeling" switches.
# ---------------------------------------------------------------------------

KANNADA_DISCOURSE = ["guru", "maga", "swalpa", "yenappa", "illa", "hoglaga", "anisutte", "gothilla"]
HINDI_DISCOURSE = ["yaar", "acha", "bas", "arre", "sach mein", "kya baat hai", "chalo", "bilkul"]

# ---------------------------------------------------------------------------
# Connectors — conjunctions/linkers, another common switch point
# ---------------------------------------------------------------------------

KANNADA_CONNECTORS = ["adre", "aadre", "matte", "yaake andre", "adakke"]
HINDI_CONNECTORS = ["lekin", "aur", "kyunki", "isliye", "phir bhi"]

# ---------------------------------------------------------------------------
# Verbs (common, high-frequency, action/state verbs) — kept simple present/
# past forms since templates control tense via the frame, not full conjugation
# ---------------------------------------------------------------------------

KANNADA_VERBS = ["madidru", "hogidru", "banda", "nodidru", "kelidru", "kotru", "helidru"]
HINDI_VERBS = ["kiya", "gaya", "aaya", "dekha", "suna", "diya", "bola"]

# ---------------------------------------------------------------------------
# Adjectives by sentiment polarity (useful if you still want a sentiment axis,
# optional — set INCLUDE_SENTIMENT = False in generate_corpus.py to ignore)
# ---------------------------------------------------------------------------

POSITIVE_ADJ = {
    "kannada": ["chennagide", "sundara", "olleyadu", "khushi aagide"],
    "hindi": ["achha hai", "zabardast", "badhiya", "khush hoon"],
}
NEGATIVE_ADJ = {
    "kannada": ["ganda aagide", "kashta aagide", "waste", "sariyagilla"],
    "hindi": ["kharab hai", "bekaar", "problem hai", "gadbad hai"],
}
NEUTRAL_ADJ = {
    "kannada": ["saadharana", "thike ansutte", "usual"],
    "hindi": ["theek thaak", "normal hai", "aisa hi hai"],
}

# ---------------------------------------------------------------------------
# Domain vocabulary — subject/object nouns and short noun phrases per domain.
# Each domain has a Kannada-flavored phrase and Hindi-flavored phrase so the
# generator can pick which language "frames" the sentence (matrix language).
# ---------------------------------------------------------------------------

DOMAINS = {
    "food": {
        "kannada": ["ee hotel oota", "amma madida adige", "ee tindi", "restaurant menu"],
        "hindi": ["yeh khana", "ghar ka khana", "yeh restaurant", "street food"],
    },
    "travel": {
        "kannada": ["ee prayana", "bus ride", "flight journey", "hotel stay"],
        "hindi": ["yeh trip", "yeh safar", "flight ka anubhav", "hotel ka stay"],
    },
    "work": {
        "kannada": ["office kelsa", "ee meeting", "project deadline", "boss maathu"],
        "hindi": ["yeh kaam", "office ka kaam", "yeh meeting", "project ka kaam"],
    },
    "family": {
        "kannada": ["mane vishaya", "appa amma", "family function", "nanna sneha"],
        "hindi": ["ghar ki baat", "mummy papa", "yeh function", "mera dost"],
    },
    "shopping": {
        "kannada": ["ee item", "online order", "ee angadi", "ee phone"],
        "hindi": ["yeh cheez", "yeh order", "yeh dukaan", "yeh phone"],
    },
    "education": {
        "kannada": ["ee exam", "college class", "nanna results", "ee subject"],
        "hindi": ["yeh exam", "college ki class", "mera result", "yeh subject"],
    },
    "weather": {
        "kannada": ["ee weather", "aaj vaathavarana", "male", "chali"],
        "hindi": ["yeh mausam", "aaj ka mausam", "baarish", "sardi"],
    },
    "health": {
        "kannada": ["doctor appointment", "ee tablet", "aaspatre visit", "checkup"],
        "hindi": ["doctor ka appointment", "yeh dawai", "hospital ka visit", "checkup"],
    },
    "technology": {
        "kannada": ["ee phone app", "wifi connection", "laptop kelsa", "internet speed"],
        "hindi": ["yeh phone ka app", "wifi ka connection", "laptop ka kaam", "internet ki speed"],
    },
    "entertainment": {
        "kannada": ["ee sinima", "ee song", "cricket match", "TV serial"],
        "hindi": ["yeh movie", "yeh gaana", "cricket ka match", "TV ka serial"],
    },
}
