# Kannada-Hindi Code-Switching Project — Full Package

## Quick start (the main deliverable)
```bash
cd sentiment_project
pip install -r requirements.txt
jupyter notebook notebooks/kn_hi_sentiment_analysis.ipynb
```
This opens the ready-to-run notebook with data already included — just run all cells.

## What's in this package

```
kn_hi_project/
├── sentiment_project/                  <- START HERE: the main runnable project
│   ├── data/                            (seed + expanded + broad corpus, all merged in the notebook)
│   ├── notebooks/kn_hi_sentiment_analysis.ipynb
│   ├── requirements.txt
│   └── README.md                        (full details, including the accuracy/data-leakage caveat)
│
├── pivot_corpus_from_real_data/         <- NEW: real-data-grounded Kannada-Hindi corpus
│   ├── data_raw/                        (original, unmodified real Kannada-English data — DravidianCodeMix)
│   ├── en_hi_lexicon.py                 (curated English→Hindi substitution table)
│   ├── build_pivot_dataset.py           (pivot pipeline — run to regenerate)
│   ├── kannada_hindi_pivot_dataset.csv  (output: 1,574 REAL Kannada sentences w/ Hindi substitutions)
│   └── README.md                        (methodology, citation requirement, honest limitations)
│
├── corpus_builder_tools/                <- optional: regenerate/expand the fully-synthetic broad corpus
│   ├── lexicon.py                       (Kannada/Hindi vocab — edit to expand)
│   ├── templates.py                     (sentence patterns by switch type)
│   ├── generate_corpus.py               (run this after editing lexicon/templates)
│   ├── quality_check.py
│   └── README.md
│
└── seed_dataset_builder_tools/          <- optional: regenerate the seed/expanded sentiment set
    ├── generate_synthetic.py
    └── README.md
```

## Two ways this corpus was built — and which is better
- **`sentiment_project/data/`** — fully synthetic, template-generated. Fast to scale,
  but not grounded in real speech.
- **`pivot_corpus_from_real_data/`** — real Kannada sentences from actual YouTube
  comments (DravidianCodeMix), with English words swapped for hand-checked Hindi
  equivalents. The Kannada side is 100% authentic; only the inserted words are
  substituted. **This is the more credible of the two** for anything beyond a
  pipeline demo — use it as your primary data source going forward, and treat the
  synthetic corpus as supplementary volume.
- **Citation requirement**: if you use `pivot_corpus_from_real_data`, cite the
  DravidianCodeMix paper (full citation in its README) — the source repo has no
  explicit open license, only a citation request.

## Important — read before trusting results
All data here is **synthetically generated**, not native-speaker verified. No published
Kannada-Hindi code-switching dataset exists, so this whole project is a bootstrap. The
notebook itself flags the biggest consequence directly: baseline models score ~100%
accuracy, which is a sign of synthetic data leakage (train/test share the same lexicon),
not a working sentiment classifier. Full explanation is in the notebook and in
`sentiment_project/README.md`.

**To make this genuinely useful**, the next step is collecting ~300-500 real Kannada-Hindi
code-switched sentences (e.g. YouTube comments, Twitter/X from Karnataka-based accounts)
and getting them annotated by 2+ bilingual speakers, then using that as your real test set.

## Requirements
- Python 3.9+
- `pip install -r sentiment_project/requirements.txt`
- No GPU needed for the notebook as-is (TF-IDF + linear models). GPU + internet needed
  only if you uncomment the optional transformer fine-tuning section.
