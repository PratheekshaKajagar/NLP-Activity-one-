"""
Templates for Kannada-Hindi code-switched sentence generation.

Each template function takes a slot dict and returns a sentence string.
`matrix_language` = the language that provides the grammatical frame
(subject/verb structure) — this is standard code-switching terminology
and useful metadata for downstream modeling/eval.

`switch_type` categorizes *where* the switch happens, which matters because
real code-switching isn't random — it clusters at specific points:
  - discourse_marker: filler/discourse word from the other language
  - connector: conjunction from the other language joining two clauses
  - noun_phrase: the subject/object noun phrase is in the other language
  - verb: the verb phrase is in the other language
  - tag: a short evaluative tag/adjective phrase appended at the end
"""

import random


def discourse_marker_switch(matrix_lang, domain_phrase, verb, adj, discourse_word):
    """Matrix-language sentence with a discourse marker borrowed from the other language."""
    return f"{domain_phrase} {verb} {adj} {discourse_word}".strip()


def connector_switch(matrix_lang, clause1_phrase, clause1_verb, connector, clause2_phrase, clause2_adj):
    """Two clauses joined by a connector from the OTHER language."""
    return f"{clause1_phrase} {clause1_verb} {connector} {clause2_phrase} {clause2_adj}".strip()


def noun_phrase_switch(matrix_lang, other_lang_domain_phrase, verb, adj):
    """Matrix-language verb/adjective frame, but the subject noun phrase is
    borrowed from the other language (very common real-world pattern, e.g.
    an English/Hindi noun dropped into an otherwise Kannada sentence)."""
    return f"{other_lang_domain_phrase} {verb} {adj}".strip()


def tag_switch(matrix_lang, domain_phrase, verb, tag_adj):
    """Matrix-language clause with a short evaluative tag from the other
    language appended — e.g. an English/Hindi 'that was great' tacked onto
    an otherwise Kannada sentence."""
    return f"{domain_phrase} {verb}, {tag_adj}".strip()


TEMPLATE_REGISTRY = {
    "discourse_marker": discourse_marker_switch,
    "connector": connector_switch,
    "noun_phrase": noun_phrase_switch,
    "tag": tag_switch,
}
