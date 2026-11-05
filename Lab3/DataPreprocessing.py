"""Clean a teaching CSV and save basic EDA plots."""

from pathlib import Path
from time import perf_counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def clean_records(raw_table):
    required_fields = {"cgpa", "study_hours", "placed"}
    if raw_table.empty or not required_fields <= set(raw_table):
        raise ValueError("CSV needs cgpa, study_hours and placed columns.")
    tidy_table = raw_table.drop_duplicates().copy()
    for field in ("cgpa", "study_hours", "placed"):
        tidy_table[field] = pd.to_numeric(tidy_table[field], errors="raise")
        if np.isinf(tidy_table[field].to_numpy(dtype=float)).any():
            raise ValueError("Infinite values are invalid.")
    tidy_table = tidy_table.dropna(subset=["placed"])
    for field in ("cgpa", "study_hours"):
        field_median = tidy_table[field].median()
        if pd.isna(field_median):
            raise ValueError(f"No usable values in {field}.")
        tidy_table[field] = tidy_table[field].fillna(field_median)
    if (tidy_table.empty or not tidy_table["placed"].isin([0, 1]).all()
            or not tidy_table["cgpa"].between(0, 10).all()
            or not tidy_table["study_hours"].between(0, 24).all()):
        raise ValueError("Invalid label, CGPA or study hours.")
    return tidy_table


def main():
    eda_home = Path(__file__).resolve().parent
    eda_out = eda_home / "outputs"
    try:
        eda_clock = perf_counter()
        raw_table = pd.read_csv(eda_home.parent / "datasets/placement.csv")
        tidy_table = clean_records(raw_table)
        eda_out.mkdir(exist_ok=True)
        tidy_table.to_csv(eda_out / "cleaned.csv", index=False)
        tidy_table.describe().to_csv(eda_out / "summary.csv")
        tidy_table.hist(figsize=(8, 4))
        plt.tight_layout()
        plt.savefig(eda_out / "histograms.png")
        plt.close("all")
        plt.imshow(tidy_table.corr(), vmin=-1, vmax=1, cmap="coolwarm")
        plt.xticks(range(3), tidy_table.columns, rotation=20)
        plt.yticks(range(3), tidy_table.columns)
        plt.colorbar()
        plt.tight_layout()
        plt.savefig(eda_out / "correlation.png")
        plt.close()
        eda_note = (f"Rows: {len(raw_table)} -> {len(tidy_table)}\n"
                    f"Seconds: {perf_counter() - eda_clock:.6f}\n")
        (eda_out / "results.txt").write_text(eda_note)
        print(eda_note)
    except (OSError, ValueError, pd.errors.ParserError) as error:
        print(f"Cannot preprocess: {error}")


if __name__ == "__main__":
    main()
