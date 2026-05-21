# src/model/evaluate.py

# Note: Evaluation already done in Notebook 04.
# This file is for re-evaluation if needed.

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve()
                    .parent.parent.parent))

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (classification_report,
                             confusion_matrix,
                             accuracy_score)
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator

CLASSES        = ["healthy", "leaf_rust",
                  "stripe_rust", "powdery_mildew"]
PROCESSED_PATH = Path("dataset/processed")
SAVED_MODELS   = Path("saved_models")
RESULTS_PATH   = Path("results")
IMG_SIZE       = (224, 224)
BATCH          = 32


def load_saved_model(saved_models_path=SAVED_MODELS):
    """Loads saved .h5 model."""
    model_path = saved_models_path / \
                 "wheat_disease_model.h5"
    if not model_path.exists():
        raise FileNotFoundError(
            f"Model not found at {model_path}."
        )
    model = load_model(str(model_path))
    print(f"Model loaded : {model_path}")
    return model


def load_test_generator(processed_path=PROCESSED_PATH,
                        classes=CLASSES,
                        img_size=IMG_SIZE,
                        batch_size=BATCH):
    """Loads test generator — no augmentation."""
    test_dg  = ImageDataGenerator(rescale=1.0 / 255)
    test_gen = test_dg.flow_from_directory(
        str(processed_path / "test"),
        target_size=img_size,
        batch_size=batch_size,
        class_mode="categorical",
        classes=classes,
        shuffle=False
    )
    print(f"Test images : {test_gen.samples}")
    return test_gen


def get_predictions(model, test_gen):
    """Returns (y_true, y_pred)."""
    print("Running predictions...")
    preds  = model.predict(test_gen, verbose=1)
    y_pred = np.argmax(preds, axis=1)
    y_true = test_gen.classes
    return y_true, y_pred


def print_classification_report(y_true, y_pred,
                                 classes=CLASSES,
                                 results_path=RESULTS_PATH):
    """Prints and saves classification report."""
    report = classification_report(
        y_true, y_pred,
        target_names=classes, digits=4)
    print(report)
    path = results_path / "classification_report.txt"
    with open(str(path), "w") as f:
        f.write("AI-Powered Wheat Farming Assistant\n")
        f.write("Amina Habiba — 2022-ag-7802\n")
        f.write("UAF Faisalabad — 2026\n")
        f.write("=" * 50 + "\n\n")
        f.write(report)
    print(f"Report saved : {path}")


def plot_confusion_matrix(y_true, y_pred,
                           classes=CLASSES,
                           results_path=RESULTS_PATH):
    """Plots and saves confusion matrix."""
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(9, 7))
    sns.heatmap(cm, annot=True, fmt="d",
                cmap="Blues",
                xticklabels=classes,
                yticklabels=classes,
                linewidths=0.5,
                linecolor="gray")
    plt.title("Confusion Matrix",
              fontsize=14, fontweight="bold")
    plt.ylabel("Actual", fontsize=12)
    plt.xlabel("Predicted", fontsize=12)
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    path = results_path / "confusion_matrix.png"
    plt.savefig(str(path), dpi=150)
    plt.show()
    print(f"Confusion matrix saved : {path}")


def evaluate_model(
        processed_path=PROCESSED_PATH,
        saved_models_path=SAVED_MODELS,
        results_path=RESULTS_PATH,
        classes=CLASSES):
    """Full evaluation pipeline."""
    print("=" * 50)
    print("  MODEL EVALUATION")
    print("=" * 50)
    model    = load_saved_model(saved_models_path)
    test_gen = load_test_generator(
                   processed_path, classes)
    y_true, y_pred = get_predictions(model, test_gen)
    accuracy = accuracy_score(y_true, y_pred)
    print(f"\nTest Accuracy : {accuracy*100:.2f}%")
    print_classification_report(
        y_true, y_pred, classes, results_path)
    plot_confusion_matrix(
        y_true, y_pred, classes, results_path)
    print("=" * 50)
    for i, cls in enumerate(classes):
        mask    = y_true == i
        correct = np.sum((y_pred == i) & mask)
        total   = np.sum(mask)
        print(f"  {cls:<20} : "
              f"{correct}/{total} "
              f"({correct/total*100:.1f}%)")
    print("=" * 50)
    return y_true, y_pred, accuracy


if __name__ == "__main__":
    print("evaluate.py loaded successfully!")
    print("Note: Evaluation done in Notebook 04")
    print("with 90.67% test accuracy.")
    print("Call evaluate_model() to re-evaluate.")