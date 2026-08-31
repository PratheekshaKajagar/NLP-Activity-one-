# Kannada-Hindi Corpus via Pivot (Kannada-English → Kannada-Hindi)

## The idea, confirmed
Yes — this works, and it's a real technique (pivot/bridge construction). Since no
direct Kannada-Hindi code-switched corpus exists, but a **real, manually-annotated
Kannada-English** corpus does, we can:
1. Take real Kannada-English sentences (authentic Kannada from real speakers)
2. Replace the English words with Hindi equivalents
3. End up with real Kannada + inserted Hindi — genuinely more grounded than the
   fully-synthetic corpus built earlier in this project.

## Data source
**DravidianCodeMix** (Chakravarthi et al., 2022) — ~7,000 manually annotated
Kannada-English YouTube comments, sentiment-labeled (Positive/Negative/Mixed_feelings/
unknown_state/not-Kannada), high inter-annotator agreement.
- Repo: https://github.com/bharathichezhiyan/DravidianCodeMix-Dataset
- Paper: Chakravarthi et al., "DravidianCodeMix: Sentiment Analysis and Offensive
  Language Identification Dataset for Dravidian Languages in Code-Mixed Text",
  Language Resources and Evaluation, 2022.
- **License note**: the repo states no explicit open-source license — only a
  request to cite the paper. Treat this as research/personal use data and cite
  the paper; check with the authors (bharathiraja.akr@gmail.com) before any
  commercial use.

## Files
| File | Purpose |
|---|---|
| `data_raw/kannada_sentiment_{train,dev,test}.csv` | Original, unmodified DravidianCodeMix Kannada-English data |
| `en_hi_lexicon.py` | Curated (hand-checked) English→Hindi substitution table, ~40 entries |
| `build_pivot_dataset.py` | The pivot pipeline — run this to regenerate the output |
| `kannada_hindi_pivot_dataset.csv` | Output: 1,574 real Kannada sentences with Hindi-substituted English words |

## Why I curated the lexicon by hand instead of using an automated dictionary
I first tried an existing public English-Hindi dictionary for automated lookup.
It was **wrong for common words** — e.g. it mapped "nice" to the Hindi word for
"difficult", and "best" to the Hindi word for "to defeat" (these public
crowd-sourced dictionaries often aren't ordered by primary/common sense).
Automated substitution using it would have produced linguistically incorrect
output — worse than not doing it at all.

Instead, `en_hi_lexicon.py` only covers ~40 words: the actual most frequent
English content words in the real data (computed by frequency count), each
manually checked by me for a natural, commonly-used Hindi equivalent. Common
loanwords already used as-is in spoken Hindi (video, film, hero, industry,
release, support, sir) are deliberately left unchanged — translating those
would make the text less natural, not more.

## What the pipeline actually does
1. Loads all 7,671 raw comments, filters to usable sentiment labels
   (drops `not-Kannada` and `unknown_state`) → 5,692 rows.
2. Keeps only **Romanized (Latin-script)** rows → 3,720 rows. Native
   Kannada-script comments are excluded — script-mixed language ID is a
   harder problem and out of scope for this pass (see "Next steps" below).
3. Replaces English words matching the curated lexicon; keeps only rows
   where at least one substitution actually happened.
4. **Result: 1,574 real Kannada-Hindi code-switched sentences**, avg 1.42
   Hindi substitutions per sentence.

## Honest limitations
- **Coverage, not completeness**: only 42% of the Latin-script rows contained
  a word from the 40-word lexicon. Expanding the lexicon (more curated
  entries) would increase coverage — see "Extending" below.
- **Label imbalance**: the pivoted output skews heavily positive (1,183
  positive vs 262 negative vs 129 mixed_feelings) because that's the
  underlying distribution in the source data. Balance this before training
  if class imbalance matters for your use case (e.g. downsample positive,
  or weight the loss function).
- **Source data has a known artifact**: some raw comments have embedded
  newlines collapsed into a stray literal "n" (e.g. "sad**n**Dislike" instead
  of "sad\nDislike") — this is a pre-existing quirk in the original
  DravidianCodeMix files, not something introduced here. It occasionally
  causes a word to get mangled at a substitution point. Not fixed
  automatically — flag it if you do a manual review pass.
- **Word-for-word substitution ≠ fluent Hindi.** This swaps the lexical item,
  not the grammar — output is Kannada+English syntax with some words replaced
  by Hindi, not grammatically fluent Hindi. That's fine for lexical-level
  code-switch signal (e.g. training a classifier to recognize sentiment
  regardless of which language a word is in), but don't present it as
  naturally-written Hindi.
- **Still not native-speaker verified.** Have a Kannada-Hindi bilingual
  speaker sample-check this before trusting it as ground truth.

## Extending
- Add more entries to `EN_TO_HI` in `en_hi_lexicon.py` (each one hand-checked,
  not copy-pasted from an automated dictionary — see the quality issue above)
  to increase coverage beyond 42%.
- Include native Kannada-script rows: would need a proper English-token
  detector that works inside mixed-script text, and Hindi insertion in
  Devanagari rather than Romanized form — a bigger follow-on project.
- Same pivot technique could be applied to the Tamil-English and
  Malayalam-English portions of DravidianCodeMix if you ever need those
  language pairs with Hindi too.

## Quick start
```bash
python3 build_pivot_dataset.py
```
Regenerates `kannada_hindi_pivot_dataset.csv` from the raw data (useful after
you extend the lexicon).
