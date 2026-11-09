"""Digit CNN with Grad-CAM explanations and FGSM evaluation."""

import json
from pathlib import Path
from time import perf_counter

import matplotlib.pyplot as plt
import torch
from sklearn.datasets import load_digits
from sklearn.metrics import ConfusionMatrixDisplay, classification_report
from sklearn.model_selection import train_test_split
from torch import nn
from torch.nn import functional as functional
from torch.utils.data import DataLoader, TensorDataset


class DigitNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.digit_conv = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.digit_head = nn.Linear(16 * 8 * 8, 10)

    def forward(self, digit_images):
        digit_features = torch.relu(self.digit_conv(digit_images))
        return self.digit_head(digit_features.flatten(1))


def fgsm(digit_model, clean_images, true_labels, epsilon):
    """Perturb pixels in [0, 1] using the sign of the input gradient."""
    if not 0 <= epsilon <= 1:
        raise ValueError("Epsilon must be between 0 and 1.")
    attack_images = clean_images.detach().clone().requires_grad_(True)
    attack_loss = functional.cross_entropy(
        digit_model(attack_images), true_labels)
    pixel_gradient = torch.autograd.grad(attack_loss, attack_images)[0]
    perturbed_images = attack_images + epsilon * pixel_gradient.sign()
    return perturbed_images.clamp(0, 1).detach()


def grad_cam(digit_model, single_image):
    """Explain the predicted class at the final convolution's resolution."""
    digit_model.zero_grad(set_to_none=True)
    cam_features = torch.relu(digit_model.digit_conv(single_image))
    cam_features.retain_grad()
    cam_logits = digit_model.digit_head(cam_features.flatten(1))
    cam_class = cam_logits.argmax(dim=1).item()
    cam_logits[0, cam_class].backward()
    cam_weights = cam_features.grad.mean(dim=(2, 3), keepdim=True)
    cam_map = torch.relu((cam_weights * cam_features).sum(dim=1))[0]
    cam_map = cam_map / cam_map.max().clamp_min(1e-8)
    return cam_map.detach().numpy(), cam_class


def train_digits(epochs=20):
    if type(epochs) is not int or epochs < 1:
        raise ValueError("Epochs must be a positive integer.")
    torch.manual_seed(84)
    digit_pack = load_digits()
    digit_images = torch.tensor(digit_pack.images / 16, dtype=torch.float32)
    digit_images = digit_images.unsqueeze(1)
    digit_labels = torch.tensor(digit_pack.target, dtype=torch.long)
    train_ids, exam_ids = train_test_split(
        list(range(len(digit_labels))), test_size=0.25,
        stratify=digit_pack.target, random_state=84)
    digit_batches = DataLoader(
        TensorDataset(digit_images[train_ids], digit_labels[train_ids]),
        batch_size=64, shuffle=True)
    digit_model = DigitNet()
    digit_optim = torch.optim.Adam(digit_model.parameters(), lr=0.003)
    digit_losses = []
    digit_model.train()
    for _ in range(epochs):
        epoch_loss = 0.0
        for batch_images, batch_labels in digit_batches:
            digit_optim.zero_grad()
            batch_loss = functional.cross_entropy(
                digit_model(batch_images), batch_labels)
            batch_loss.backward()
            digit_optim.step()
            epoch_loss += batch_loss.item() * len(batch_labels)
        digit_losses.append(epoch_loss / len(train_ids))
    digit_model.eval()
    return (digit_model, digit_images[exam_ids], digit_labels[exam_ids],
            digit_losses)


def main():
    project_home = Path(__file__).resolve().parent
    try:
        digit_clock = perf_counter()
        digit_model, exam_images, exam_labels, digit_losses = train_digits()
        training_seconds = perf_counter() - digit_clock
        project_out = project_home / "outputs"
        weight_out = project_home.parent / "models"
        project_out.mkdir(exist_ok=True)
        weight_out.mkdir(exist_ok=True)
        torch.save(digit_model.state_dict(), weight_out / "digit_cnn.pt")
        with torch.no_grad():
            clean_guess = digit_model(exam_images).argmax(dim=1)
        project_scores = classification_report(
            exam_labels.numpy(), clean_guess.numpy(), output_dict=True,
            zero_division=0)
        attack_scores = {}
        for epsilon in (0.0, 0.05, 0.1, 0.2):
            attack_images = fgsm(
                digit_model, exam_images, exam_labels, epsilon)
            with torch.no_grad():
                attack_guess = digit_model(attack_images).argmax(dim=1)
            attack_scores[str(epsilon)] = (
                (attack_guess == exam_labels).float().mean().item())
        project_scores["fgsm_accuracy"] = attack_scores
        project_scores["training_seconds"] = training_seconds
        project_scores["seconds"] = perf_counter() - digit_clock
        (project_out / "metrics.json").write_text(
            json.dumps(project_scores, indent=2))
        ConfusionMatrixDisplay.from_predictions(exam_labels, clean_guess)
        plt.tight_layout()
        plt.savefig(project_out / "confusion_matrix.png")
        plt.close()
        plt.plot(digit_losses)
        plt.xlabel("Epoch")
        plt.ylabel("Training cross entropy")
        plt.tight_layout()
        plt.savefig(project_out / "loss.png")
        plt.close()
        plt.plot([float(value) for value in attack_scores],
                 list(attack_scores.values()), marker="o")
        plt.xlabel("FGSM epsilon")
        plt.ylabel("Test accuracy")
        plt.ylim(0, 1)
        plt.tight_layout()
        plt.savefig(project_out / "fgsm.png")
        plt.close()
        cam_map, cam_class = grad_cam(digit_model, exam_images[:1])
        plt.imshow(exam_images[0, 0], cmap="gray")
        plt.imshow(cam_map, cmap="jet", alpha=0.45, vmin=0, vmax=1)
        plt.title(f"True: {exam_labels[0].item()}, predicted: {cam_class}")
        plt.axis("off")
        plt.savefig(project_out / "grad_cam.png")
        plt.close()
        print(json.dumps(project_scores, indent=2))
    except (OSError, ValueError, RuntimeError) as error:
        print(f"Cannot run digit project: {error}")


if __name__ == "__main__":
    main()
