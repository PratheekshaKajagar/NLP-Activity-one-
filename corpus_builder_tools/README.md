# Kannada-Hindi Code-Switched Corpus Builder

## What this is
A pipeline to bootstrap a Kannada-Hindi code-switched corpus, since no
published dataset exists for this language pair. It generates structurally
diverse synthetic data and gives you a path to add and validate real data.

## Files
| File | Purpose |
|---|---|
| `lexicon.py` | Kannada/Hindi discourse markers, connectors, verbs, sentiment adjectives, and domain vocabulary (10 domains). Edit this to expand coverage. |
| `templates.py` | 4 sentence templates, one per **switch type**: `discourse_marker`, `connector`, `noun_phrase`, `tag`. These mirror real code-switching patterns rather than random word substitution. |
| `generate_corpus.py` | Main generator. Combines lexicon x templates x domain x matrix-language x polarity, dedups, writes `corpus.csv`. |
| `quality_check.py` | Structural sanity checks (dupes, length distribution, coverage gaps). |
| `corpus.csv` | Output: 1,440 unique sentences, columns `id, text, domain, matrix_language, switch_type, polarity, source`. |

## Why "switch_type" and "matrix_language" matter
Real code-switching isn't random word substitution — it clusters at specific
structural points and is usually anchored by one "matrix" language that
supplies the grammar:
- **discourse_marker** — a filler/discourse word borrowed from the other language (most common in casual speech)
- **connector** — a conjunction from the other language joining two clauses
- **noun_phrase** — the subject/object is borrowed while the verb frame stays in the matrix language
- **tag** — a short evaluative phrase tacked on at the end

Tagging your corpus this way means you can later analyze or control which
switch patterns your model learns, rather than treating "code-switching" as
one undifferentiated phenomenon.

## Honest limitations
- **Synthetic and templated.** Real spontaneous speech has far more lexical
  variety, disfluency, and irregular switching than any template generator
  will produce. Treat this as training/pretraining volume, not a gold
  evaluation set.
- **Not native-speaker verified.** I generated the lexicon and templates
  based on documented code-switching patterns, not lived fluency in
  Kannada or Hindi. Some sentences may sound stilted or even ungrammatical
  to a native speaker. **Have this reviewed before relying on it.**
- **Devanagari/Kannada script not included** — everything is Romanized.
  If your project needs native-script text, that's a separate
  transliteration step (and another thing to get native-checked, since
  transliteration errors compound).

## Recommended path to a credible corpus
1. **Use this synthetic corpus for scale** (pretraining a code-switch-aware
   LM, or bootstrapping an initial classifier).
2. **Build a real evaluation set in parallel** — even 300-500 sentences reviewed
   by 2+ bilingual annotators is worth more for evaluation than 10,000
   synthetic ones. Sources to look at:
   - YouTube comments on Karnataka-based news/vlog/comedy channels (natural mixing shows up in comment sections)
   - Twitter/X threads from Bangalore-based accounts
   - WhatsApp/community forum exports if you have consented access
   *(Note: I can't scrape these directly from this environment due to
   network restrictions — you'd run collection scripts locally with your
   own API keys, e.g. YouTube Data API or a Twitter/X developer account.)*
3. **Annotate real samples with 2-3 bilingual annotators**, report inter-
   annotator agreement (Cohen's/Fleiss' kappa) — this is standard practice
   for any code-mixed benchmark (see COMI-LINGUA, LinCE for examples of
   what "good" annotation methodology looks like).
4. **Validate the synthetic set** — sample ~100 sentences and have a native
   speaker flag anything ungrammatical or unnatural. Use this to prune or
   fix the lexicon/templates before generating more.

## Extending the generator
- Add vocabulary: edit `DOMAINS`, `*_DISCOURSE`, `*_CONNECTORS`, `*_VERBS`,
  `*_ADJ` in `lexicon.py`.
- Add new switch patterns: write a new template function in `templates.py`
  following the existing signature style, then register it in
  `GENERATORS` in `generate_corpus.py`.
- Turn off the sentiment axis entirely (if you just want a plain
  code-switch corpus): set `INCLUDE_POLARITY = False` in
  `generate_corpus.py`.
- Scale up volume: raise `SAMPLES_PER_CONFIG` in `generate_corpus.py`
  (bounded by how many unique lexicon combinations exist before you start
  repeating).

## Quick start
```bash
python3 generate_corpus.py   # writes corpus.csv
python3 quality_check.py     # sanity checks on the output
```
