# Lab 7 - Explainability, Robustness and Mini Project

Aim: classify handwritten digits, explain predictions, evaluate FGSM and
compare PCA with truncated SVD.

Algorithm: stratified 75/25 split (seed 84), train a small CNN for 20 epochs;
use channel-averaged gradients for Grad-CAM and input-gradient signs for FGSM.
Separately, center digit vectors and reconstruct them using two PCA/SVD modes.

Run from the repository root:

```bash
python3 Lab7/MiniProject.py
python3 Lab7/DimensionalityReduction.py
```

Input: scikit-learn's built-in 8x8 digits, pixels scaled to [0,1].
Results / Output: `outputs/metrics.json`, `reduction.json`, `loss.png`,
`confusion_matrix.png`, `fgsm.png`, `grad_cam.png`, `pca.png` and
`models/digit_cnn.pt`. Pending execution.

Performance analysis: held-out accuracy, precision, recall, F1, execution time,
accuracy at epsilon 0/0.05/0.1/0.2, explained variance and reconstruction MSE.
PCA/SVD uses the full dataset for unsupervised reconstruction, not CNN fitting.
No scores recorded yet. Low-resolution heatmaps need cautious interpretation.

Learning outcomes: CNNs, gradient explanations, adversarial sensitivity and
low-rank approximation. Graphs are generated only after execution.

References: [FGSM](https://docs.pytorch.org/tutorials/beginner/fgsm_tutorial.html),
[gradient retention](https://docs.pytorch.org/docs/stable/generated/torch.Tensor.retain_grad.html),
[PCA](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html),
[SVD](https://numpy.org/doc/stable/reference/generated/numpy.linalg.svd.html).
