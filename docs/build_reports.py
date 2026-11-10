"""Build short PDF reports from saved results without running experiments."""

import json
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def write_report(report_path, report_title, report_lines):
    report_styles = getSampleStyleSheet()
    report_story = [Paragraph(escape(report_title), report_styles["Title"])]
    for report_line in report_lines:
        report_story.extend([
            Paragraph(escape(report_line), report_styles["BodyText"]),
            Spacer(1, 8),
        ])
    SimpleDocTemplate(str(report_path)).build(report_story)


def main():
    report_home = Path(__file__).resolve().parent
    repo_home = report_home.parent
    score_lines = ["Shreyas Namdeo | IC-2K23-84",
                   "Only saved results are included; pending is not a score.",
                   "Lab1: BFS for jugs/river; backtracking for Sudoku. "
                   "Execution time pending manual recording."]
    for lab_no, result_name in ((5, "metrics.json"), (6, "metrics.json"),
                                (7, "metrics.json"), (7, "reduction.json")):
        result_path = repo_home / f"Lab{lab_no}/outputs/{result_name}"
        score_lines.append(f"Lab{lab_no} - {result_name}")
        if not result_path.exists():
            score_lines.append("Pending execution.")
            continue
        result_scores = json.loads(result_path.read_text())
        for score_name, score_value in result_scores.items():
            score_lines.append(f"{score_name}: {score_value}")
    write_report(report_home / "performance-analysis.pdf",
                 "AI Lab Performance Analysis", score_lines)
    project_lines = [
        "Shreyas Namdeo | IC-2K23-84",
        "Aim: explain and evaluate a handwritten digit classifier.",
        "Data: scikit-learn digits; 8x8 images scaled to [0,1].",
        "Method: stratified 75/25 split, seed 84, one convolution, "
        "ReLU and a linear classifier; Adam for 20 epochs.",
        "Explainability: Grad-CAM on the convolutional feature maps.",
        "Robustness: FGSM at epsilon 0, 0.05, 0.1 and 0.2.",
        "Evaluation: test accuracy, precision, recall, F1 and attack accuracy. "
        "See saved scores in the performance report; missing scores "
        "are pending.",
        "Separate exercise: compare centered PCA/SVD reconstruction MSE.",
        "Limitations: small low-resolution dataset, one split and no external "
        "validation. Heatmaps do not establish causal explanations.",
        "Learning outcomes: training, held-out evaluation, gradient-based "
        "explanations, robustness and dimensionality reduction.",
    ]
    write_report(report_home / "mini-project-report.pdf",
                 "Digit Classification Mini Project", project_lines)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as error:
        print(f"Cannot build reports: {error}")
