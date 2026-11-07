# Lab 5 - Decision Tree

Aim: classify Iris species and evaluate predictions.

Algorithm: stratified 75/25 train/test split, depth-3 decision tree,
predict held-out labels; seed 84.

Run: `python3 Lab5/DecisionTree.py` from the repository root.
Input: built-in Iris dataset, exported to `datasets/iris.csv` on execution.

Results / Output: `outputs/metrics.json`, `confusion_matrix.png`, `tree.png`
and `models/decision_tree.pkl`. Pending execution.

Performance analysis: test accuracy, per-class and macro/weighted precision,
recall, F1 and fit/predict execution time. No scores recorded yet.

Learning outcomes: tree splits, overfitting control and held-out evaluation.
Graphs and model visualization are generated after execution.

Reference: [DecisionTreeClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html).
