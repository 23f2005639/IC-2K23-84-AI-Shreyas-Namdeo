"""Train and evaluate an Iris decision tree."""

import json
import pickle
from pathlib import Path
from time import perf_counter

import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.metrics import ConfusionMatrixDisplay, classification_report
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree


def train_tree(tree_depth=3):
    if type(tree_depth) is not int or tree_depth < 1:
        raise ValueError("Tree depth must be a positive integer.")
    iris_pack = load_iris(as_frame=True)
    train_rows, exam_rows, train_tags, exam_tags = train_test_split(
        iris_pack.data, iris_pack.target, test_size=0.25,
        stratify=iris_pack.target, random_state=84)
    iris_tree = DecisionTreeClassifier(max_depth=tree_depth, random_state=84)
    tree_clock = perf_counter()
    iris_tree.fit(train_rows, train_tags)
    exam_guess = iris_tree.predict(exam_rows)
    tree_scores = classification_report(
        exam_tags, exam_guess, target_names=iris_pack.target_names,
        output_dict=True, zero_division=0)
    tree_scores["seconds"] = perf_counter() - tree_clock
    return iris_pack, iris_tree, exam_tags, exam_guess, tree_scores


def main():
    tree_home = Path(__file__).resolve().parent
    try:
        iris_pack, iris_tree, exam_tags, exam_guess, tree_scores = train_tree()
        tree_out = tree_home / "outputs"
        model_out = tree_home.parent / "models"
        data_out = tree_home.parent / "datasets"
        for folder in (tree_out, model_out, data_out):
            folder.mkdir(exist_ok=True)
        iris_pack.frame.to_csv(data_out / "iris.csv", index=False)
        with (model_out / "decision_tree.pkl").open("wb") as tree_file:
            pickle.dump(iris_tree, tree_file)
        (tree_out / "metrics.json").write_text(
            json.dumps(tree_scores, indent=2))
        ConfusionMatrixDisplay.from_predictions(
            exam_tags, exam_guess, display_labels=iris_pack.target_names)
        plt.tight_layout()
        plt.savefig(tree_out / "confusion_matrix.png")
        plt.close()
        plt.figure(figsize=(12, 7))
        plot_tree(iris_tree, feature_names=list(iris_pack.feature_names),
                  class_names=list(iris_pack.target_names), filled=True)
        plt.tight_layout()
        plt.savefig(tree_out / "tree.png")
        plt.close()
        print(json.dumps(tree_scores, indent=2))
    except (OSError, ValueError) as error:
        print(f"Cannot train tree: {error}")


if __name__ == "__main__":
    main()
