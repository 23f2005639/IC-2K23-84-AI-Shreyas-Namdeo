"""Compare PCA and truncated SVD on the built-in digits dataset."""

import json
from pathlib import Path
from time import perf_counter

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA


def reduce_digits(component_count=2):
    digit_pack = load_digits()
    digit_table = digit_pack.data / 16.0
    if type(component_count) is not int or not 1 <= component_count <= 64:
        raise ValueError("Choose 1-64 components.")
    pca_clock = perf_counter()
    digit_pca = PCA(n_components=component_count, svd_solver="full")
    digit_projection = digit_pca.fit_transform(digit_table)
    pca_rebuilt = digit_pca.inverse_transform(digit_projection)
    pca_seconds = perf_counter() - pca_clock

    svd_clock = perf_counter()
    digit_mean = digit_table.mean(axis=0)
    digit_centered = digit_table - digit_mean
    left_basis, singular_values, right_basis = np.linalg.svd(
        digit_centered, full_matrices=False)
    svd_rebuilt = ((left_basis[:, :component_count]
                    * singular_values[:component_count])
                   @ right_basis[:component_count] + digit_mean)
    reduction_scores = {
        "components": component_count,
        "explained_variance": float(digit_pca.explained_variance_ratio_.sum()),
        "pca_mse": float(np.mean((digit_table - pca_rebuilt) ** 2)),
        "svd_mse": float(np.mean((digit_table - svd_rebuilt) ** 2)),
        "pca_seconds": pca_seconds,
        "svd_seconds": perf_counter() - svd_clock,
    }
    return digit_projection, digit_pack.target, reduction_scores


def main():
    try:
        digit_projection, digit_labels, reduction_scores = reduce_digits()
        reduction_out = Path(__file__).resolve().parent / "outputs"
        reduction_out.mkdir(exist_ok=True)
        plt.scatter(digit_projection[:, 0], digit_projection[:, 1],
                    c=digit_labels, s=8, cmap="tab10")
        plt.xlabel("PC1")
        plt.ylabel("PC2")
        plt.colorbar(label="Digit")
        plt.tight_layout()
        plt.savefig(reduction_out / "pca.png")
        plt.close()
        (reduction_out / "reduction.json").write_text(
            json.dumps(reduction_scores, indent=2))
        print(reduction_scores)
    except (OSError, ValueError, np.linalg.LinAlgError) as error:
        print(f"Cannot reduce data: {error}")


if __name__ == "__main__":
    main()
