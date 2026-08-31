# Kannada-Hindi Code-Switched Sentiment Dataset (Bootstrap Kit)

## Why this exists
There is no established, published Kannada-Hindi code-switching corpus.
Existing Indian code-mixed sentiment datasets (DravidianCodeMix, L3Cube,
COMI-LINGUA, etc.) pair Kannada or Hindi with **English**, not with each
other — natural Kannada-Hindi mixing in digital text is rare and uncurated.
This kit is a starting point to bootstrap your own.

## What's included
| File | Description |
|---|---|
| `seed_dataset.csv` | 60 hand-written Kannada-Hindi(-English) code-switched sentences, labeled positive/negative/neutral, across 10 domains (movies, food, traffic, shopping, work, travel, education, events, service, technology). |
| `generate_synthetic.py` | Expands the seed set two ways: (1) template + lexicon substitution across domains/sentiments, (2) label-preserving paraphrase augmentation via marker swaps (tumba/bahut, chennagide/achha hai, etc.) |
| `expanded_dataset.csv` | Output of the script — ~570 additional rows on top of the 60 seeds. |

## Important limitations — read before using for evaluation
- **This is synthetic/templated data.** It's useful for bootstrapping a model
  or testing your pipeline, but it will have limited lexical and syntactic
  diversity compared to real speech/text. Don't report benchmark numbers
  based on this alone.
- **I'm not a native Kannada or Hindi speaker model** — the sentences follow
  common code-switching patterns I'm aware of (adjective/discourse markers
  switching languages while subject/verb frame stays fixed), but they should
  be **reviewed by a native or fluent bilingual speaker** before you treat
  them as ground truth. Some phrasing may sound artificial.
- **Sentiment labels are self-assigned** (weak supervision), not
  multi-annotator agreement — for a real benchmark you'd want at least 2-3
  annotators per item with an agreement score (Cohen's/Fleiss' kappa).

## How to get real data (recommended next step)
1. **Scrape real-world code-mixed text**: YouTube comments on Karnataka-based
   channels (news, vlogs, comedy) and Twitter/X threads from Bangalore-based
   accounts are the most realistic source of natural Kannada-Hindi mixing.
2. **Use DravidianCodeMix (Kannada-English) as a base**, then have bilingual
   annotators or an LLM-assisted pipeline replace English spans with Hindi
   equivalents, followed by human review — this gives you real Kannada
   frames with controlled Hindi injection rather than fully synthetic text.
3. **Consider a small paid annotation batch** (even 200-500 real sentences
   with 2 annotators) as a *test set*, and use the synthetic data only for
   *training*. This is a common and defensible split when real data is
   scarce.
4. Cross-check any LLM-generated candidate sentences against native-speaker
   judgment before adding them — LLM-generated code-switching can sound
   fluent but be linguistically wrong (real code-switching follows syntactic
   constraints, e.g. equivalence constraints, not just random word swap).

## Extending the generator
Edit the lexicons at the top of `generate_synthetic.py`:
- `POSITIVE_FILLERS`, `NEGATIVE_FILLERS`, `NEUTRAL_FILLERS` — sentiment phrases
- `SUBJECTS` — add more domains/subjects
- `SWAP_PAIRS` — add more interchangeable code-switch markers

Then rerun:
```bash
python3 generate_synthetic.py
```

## Suggested next steps for the project
1. Get 200-500 real sentences reviewed/collected (native speaker or scrape + annotate).
2. Combine: seed + expanded (synthetic) for training, real reviewed set for test.
3. Fine-tune a multilingual model (e.g. IndicBERT, MuRIL, or XLM-R) rather than
   training from scratch — these already have Kannada and Hindi in their
   pretraining data.
4. Report results with a clear note that training data includes synthetic
   examples, for transparency.
