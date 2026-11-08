# Lab 6 - PyTorch Basics

Aim: use tensors, autograd, linear regression and a small neural network.

Algorithm: create 100 synthetic inputs; randomly split 80/20 with seed 84;
train Linear(1,1) on y=3x+1 and a 1-16-1 Tanh network on y=x^2.
Use Adam, MSE and 500 epochs.

Run: `python3 Lab6/TorchBasics.py` from the repository root.
Inputs are generated in memory; no external dataset needed.

Results / Output: `outputs/metrics.json`, `loss.png` and two `.pt` state
dictionaries in `models/`. Pending execution.

Performance analysis: held-out MSE, R2 and training/evaluation time.
Accuracy, precision, recall and F1 do not apply to continuous predictions.

Learning outcomes: tensor shapes, backpropagation, optimizers and model saving.
Graph: training loss per epoch, generated after execution.
