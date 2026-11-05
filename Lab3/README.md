# Lab 3 - Preprocessing and EDA

Aim: clean tabular data with NumPy/Pandas and inspect distributions.

Algorithm: remove duplicates, validate numeric ranges, drop missing labels,
fill missing features with medians, summarize and plot correlations.

Run: `python3 Lab3/DataPreprocessing.py` from the repository root.
Input: `datasets/placement.csv`, a small synthetic teaching dataset.

Results / Output: `outputs/cleaned.csv`, `summary.csv`, `results.txt`,
`histograms.png` and `correlation.png`. Pending execution.

Performance analysis: row counts, missing values and execution time;
classification metrics do not apply. This EDA script does not train a model.
For later modeling, fit imputers on the training split only.

Learning outcomes: data validation, missing values, descriptive statistics
and visualization. Graphs are saved after execution.

Reference: [Pandas missing data](https://pandas.pydata.org/docs/user_guide/missing_data.html).
