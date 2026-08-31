# Kannada-Hindi Code-Switched Sentiment Analysis — Project

## Structure
```
kn_hi_sentiment_project/
├── data/
│   ├── seed_dataset.csv                  # 60 hand-written seed sentences (synthetic)
│   ├── expanded_dataset.csv              # template-expanded + paraphrase-augmented seed set (synthetic)
│   ├── corpus_broad.csv                  # larger structurally-tagged corpus (synthetic)
│   └── kannada_hindi_pivot_dataset.csv   # REAL Kannada sentences (DravidianCodeMix) w/ Hindi word substitutions
├── notebooks/
│   └── kn_hi_sentiment_analysis.ipynb   # main project notebook
├── requirements.txt
└── README.md   (this file)
```

## What the notebook does
1. Loads and merges **four** data sources (three synthetic, one real-data-derived) into one labeled dataset
2. EDA — label balance, domain distribution, sentence length distribution, real-vs-synthetic split
3. Train/test split (stratified)
4. Baseline model: TF-IDF + Logistic Regression, evaluated on a random mixed split
5. **Realistic evaluation**: a separate, stricter evaluation that holds out real data specifically
   and trains only on the rest — this is the number that actually reflects real-world performance
6. TF-IDF + Linear SVM, for comparison
7. Error analysis on misclassified examples
8. Reference (not executed) code for fine-tuning a multilingual transformer
   (MuRIL/IndicBERT/XLM-R) once you have GPU + internet access
9. Conclusions and a concrete path forward

## ⚠️ Read this before trusting any numbers
There are two different accuracy numbers in this notebook, and they mean very different things:
- **Section 5 (mixed random split): ~90% accuracy.** This mixes real and synthetic sentences into
  both train and test, so it's inflated — synthetic sentences are easy because train and test
  share the same templates/lexicon.
- **Section 6 (held out on real data only): ~80% accuracy, with `neutral` recall collapsing to ~3%.**
  This is the trustworthy number. It also surfaces a real problem: the real data's `Mixed_feelings`
  label was mapped to `neutral` for compatibility, but they aren't the same concept, and
  `Mixed_feelings` is a rare, hard class in the source data (~125 of 1,487 real rows). The collapsed
  recall is telling you about this label mismatch and class imbalance — not just about the model.

**Before this project is usable for anything real, you still need:**
- More real data, ideally with genuine three-way sentiment labels (not a `Mixed_feelings` →
  `neutral` stand-in) — either by expanding `en_hi_lexicon.py`'s coverage of the existing
  DravidianCodeMix data, or by collecting and annotating new Kannada-Hindi text directly.
- A native-speaker review pass on a sample of the pivoted sentences, since word-for-word
  substitution isn't the same as fluent Hindi phrasing.

## Running it
```bash
pip install -r requirements.txt
jupyter notebook notebooks/kn_hi_sentiment_analysis.ipynb
```

## Extending this project
- **More data**: regenerate `expanded_dataset.csv` / `corpus_broad.csv` with the
  generator scripts from the corpus-building step (expand the lexicon, add domains).
- **Better models**: uncomment and adapt the transformer fine-tuning section
  (Section 8) once you have GPU + internet access — MuRIL and IndicBERT are
  pretrained on Indian languages including both Kannada and Hindi, and should
  handle transliteration variation far better than the TF-IDF baseline.
- **Real evaluation**: swap in a real annotated test set and rerun Sections 5-7
  to get a credible read on baseline performance.
