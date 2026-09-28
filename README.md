# 🩺 Diabetes Prediction Using Machine Learning (Imbalance-Aware Edition)

Predicts diabetes risk from demographic and clinical attributes. The dataset is imbalanced (8.8% positive), so this
edition evaluates imbalance handling properly instead of relying on accuracy.

> **Educational project. Not a medical device. Not for diagnosis.**

## What was done about class imbalance

Compared on the same leak-free protocol (3 models × 5 strategies):

* **Models:** Logistic Regression, Random Forest, HistGradientBoosting
* **Strategies:** none · class weights · random oversampling · SMOTE (SMOTE-NC style) · random undersampling
* **Threshold tuning** from out-of-fold *training* predictions (default 0.5 is rarely right for imbalanced data)

Rules that keep the numbers honest: the 20% test set is split first and is **never resampled**; resampling happens only inside
training folds; thresholds are chosen without touching the test set; the test set is scored once.

## Results (held-out test set, 19,230 patients, real 8.8% prevalence)

| Configuration | Accuracy | Balanced acc. | Precision | Recall | Specificity | F1 | MCC |
|---|---|---|---|---|---|---|---|
| Baseline HistGradientBoosting, no balancing, thr 0.50 | 0.972 | 0.846 | 0.989 | 0.692 | 0.999 | 0.814 | 0.815 |
| Balanced (class weights), thr 0.50 | 0.899 | 0.907 | 0.464 | 0.916 | 0.898 | 0.616 | 0.609 |
| **Balanced (class weights), balanced thr 0.456** (deployed) | 0.888 | 0.908 | 0.438 | 0.933 | 0.884 | 0.596 | 0.593 |
| Balanced (class weights), F1-optimal thr 0.833 | 0.969 | 0.858 | 0.909 | 0.723 | 0.993 | 0.805 | 0.795 |
| Balanced (class weights), screening thr 0.547 (recall ≥ 90%) | 0.911 | 0.906 | 0.499 | 0.900 | 0.913 | 0.642 | 0.630 |

Threshold-free quality is the same for every configuration: **ROC-AUC ≈ 0.978, PR-AUC ≈ 0.884.**

### The honest takeaway

* Balancing changes **which errors the model makes**, not how good it is. Sensitivity rises 0.69 → 0.93 and balanced accuracy 0.846 → 0.908,
  but precision falls 0.99 → 0.44 and accuracy 0.972 → 0.888. That is a trade-off, not a free improvement.
* All 15 model × strategy combinations converge to a balanced accuracy of ~0.88–0.91. Different balancing methods do not break through it.
* **Perfect scores are not achievable on this dataset.** Diabetes prevalence is flat (~8–9%) for blood-glucose values from 126 to 200 mg/dL
  and 14,924 non-diabetic patients have HbA1c ≥ 6.5%, so many patients are indistinguishable on the recorded features.
  A perfect score here would signal data leakage, not a better model.

## Project structure

```text
Diabetes-prediction/
├── Data/                              diabetes_prediction_dataset.csv, diabetes_cleaned.csv
├── 0. Introduction.ipynb
├── 01_EDA_Data_Cleaning.ipynb
├── 02_Model_Training.ipynb            original 6-model benchmark (incl. XGBoost)
├── 03_Model_Prediction.ipynb
├── 03_Model_Prediction.py             Streamlit app (uses the balanced model + threshold)
├── 04_Balanced_Model_Training.py      NEW: imbalance study (run: python 04_Balanced_Model_Training.py)
├── results/                           CSVs: sweep, 5-fold CV, final test, bootstrap CIs
├── figures/                           ROC/PR, threshold trade-off, confusion matrices, before/after
├── diabetes_model.pkl                 original tuned XGBoost model
├── diabetes_model_balanced.pkl        NEW: {pipeline, threshold} bundle used by the app
├── requirements.txt
└── README.md
```

## Run

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python 04_Balanced_Model_Training.py      # regenerates results/, figures/, diabetes_model_balanced.pkl (~10 min on 1 CPU)
streamlit run 03_Model_Prediction.py
```

`diabetes_model_balanced.pkl` was created with scikit-learn 1.8.0, so `requirements.txt` pins that version. Re-run the training script
if you change versions.


## Dataset structure (found while testing the app)

The label follows near-deterministic rules at the extremes (verified on `diabetes_cleaned.csv`):

* HbA1c ≥ 6.8 → **100% diabetic** (3,888 rows); glucose ≥ 220 → **100% diabetic** (3,264 rows)
* HbA1c ≤ 5.0, or glucose ≤ 100 (and 158) → **0% diabetic**
* Everything in between (HbA1c 5.7–6.6, glucose 126–200) → about **8–9% diabetic regardless of the exact value**

Consequences: the model largely recovers this rule, its score behaves like a step (HbA1c 6.6 → 0.03%, 6.7 → 99.96%),
and the dataset's cut-offs differ from clinical criteria (HbA1c ≥ 6.5%, fasting glucose ≥ 126 mg/dL). The data looks synthetic or
rule-generated, so treat results as a modelling exercise, not clinical evidence. The app therefore (a) limits inputs to the training
ranges (age 0.08–80, BMI 10–95, HbA1c 3.5–9.0, glucose 80–300) and (b) shows a caution instead of "Good News" when HbA1c ≥ 6.5% or glucose ≥ 126 mg/dL.

## Notes

* The model in the app outputs a **risk score**, not a calibrated probability (class weighting inflates scores).
* The XGBoost model from `02_Model_Training.ipynb` was not re-run in the imbalance study; HistGradientBoosting (same algorithm family) was used.
* Dataset provenance is not documented; validate on independent clinical data before any real-world use.

## Authors

Rohan Ranjan · Suryansh Kumar Pathak — B.Tech Computer Science & Engineering
