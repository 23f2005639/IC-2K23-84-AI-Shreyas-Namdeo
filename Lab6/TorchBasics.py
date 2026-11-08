"""Tensor operations, linear regression and a small neural network."""

import json
from pathlib import Path
from time import perf_counter

import matplotlib.pyplot as plt
import torch
from torch import nn


def fit_curve(curve_model, train_axis, train_values, epochs=500):
    if type(epochs) is not int or epochs < 1:
        raise ValueError("Epochs must be a positive integer.")
    if train_axis.shape != train_values.shape or train_axis.numel() == 0:
        raise ValueError("Use matching nonempty training tensors.")
    curve_optim = torch.optim.Adam(curve_model.parameters(), lr=0.03)
    curve_loss = nn.MSELoss()
    loss_history = []
    curve_model.train()
    for _ in range(epochs):
        curve_optim.zero_grad()
        batch_loss = curve_loss(curve_model(train_axis), train_values)
        batch_loss.backward()
        curve_optim.step()
        loss_history.append(batch_loss.item())
    return loss_history


def main():
    torch.manual_seed(84)
    curve_home = Path(__file__).resolve().parent
    try:
        curve_out = curve_home / "outputs"
        weight_out = curve_home.parent / "models"
        curve_out.mkdir(exist_ok=True)
        weight_out.mkdir(exist_ok=True)
        sample_axis = torch.linspace(-1, 1, 100).reshape(-1, 1)
        sample_order = torch.randperm(100)
        train_ids, exam_ids = sample_order[:80], sample_order[80:]
        curve_scores = {}
        print("Tensor shape:", sample_axis.shape)
        print("Tensor mean:", sample_axis.mean().item())
        for curve_name, sample_values, curve_model in (
            ("linear_regression", 3 * sample_axis + 1, nn.Linear(1, 1)),
            ("neural_network", sample_axis.square(),
             nn.Sequential(nn.Linear(1, 16), nn.Tanh(), nn.Linear(16, 1))),
        ):
            curve_clock = perf_counter()
            loss_history = fit_curve(curve_model, sample_axis[train_ids],
                                     sample_values[train_ids])
            curve_model.eval()
            with torch.no_grad():
                exam_values = sample_values[exam_ids]
                exam_guess = curve_model(sample_axis[exam_ids])
                square_error = (exam_guess - exam_values).square().sum()
                total_error = (exam_values - exam_values.mean()).square().sum()
                curve_scores[curve_name] = {
                    "mse": (square_error / len(exam_ids)).item(),
                    "r2": (1 - square_error / total_error).item(),
                    "seconds": perf_counter() - curve_clock,
                }
            torch.save(curve_model.state_dict(),
                       weight_out / f"{curve_name}.pt")
            plt.plot(loss_history, label=curve_name)
        plt.xlabel("Epoch")
        plt.ylabel("Training MSE")
        plt.legend()
        plt.tight_layout()
        plt.savefig(curve_out / "loss.png")
        plt.close()
        (curve_out / "metrics.json").write_text(
            json.dumps(curve_scores, indent=2))
        print(json.dumps(curve_scores, indent=2))
    except (OSError, ValueError, RuntimeError) as error:
        print(f"Cannot train curves: {error}")


if __name__ == "__main__":
    main()
