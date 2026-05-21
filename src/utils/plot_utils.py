# src/utils/plot_utils.py

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve()
                    .parent.parent.parent))

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from pathlib import Path

# ── Constants ────────────────────────────────────────────────
RESULTS_PATH = Path("results")
CLASSES      = ["healthy", "leaf_rust",
                "stripe_rust", "powdery_mildew"]
COLORS       = ["#4CAF50", "#f44336",
                "#FF9800", "#9C27B0"]


# ── Plot Training History ────────────────────────────────────
def plot_training_history(history,
                           save_path=RESULTS_PATH):
    """
    Plots accuracy and loss curves from
    model training history.

    history   : Keras history object OR dict with
                keys: accuracy, val_accuracy,
                      loss, val_loss
    save_path : folder to save the plot

    Output : saves accuracy_loss_curves.png
    """
    # handle both Keras history and dict
    if hasattr(history, "history"):
        h = history.history
    else:
        h = history

    epochs = range(1, len(h["accuracy"]) + 1)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle("Model Training History",
                 fontsize=15, fontweight="bold")

    # accuracy plot
    axes[0].plot(epochs, h["accuracy"],
                 "b-o", label="Train Accuracy",
                 linewidth=2, markersize=5)
    axes[0].plot(epochs, h["val_accuracy"],
                 "r-o", label="Val Accuracy",
                 linewidth=2, markersize=5)
    axes[0].set_title("Accuracy",
                       fontsize=13,
                       fontweight="bold")
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("Accuracy")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    axes[0].set_ylim(0, 1)

    # loss plot
    axes[1].plot(epochs, h["loss"],
                 "b-o", label="Train Loss",
                 linewidth=2, markersize=5)
    axes[1].plot(epochs, h["val_loss"],
                 "r-o", label="Val Loss",
                 linewidth=2, markersize=5)
    axes[1].set_title("Loss",
                       fontsize=13,
                       fontweight="bold")
    axes[1].set_xlabel("Epoch")
    axes[1].set_ylabel("Loss")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    out = Path(save_path) / \
          "accuracy_loss_curves.png"
    plt.savefig(str(out), dpi=150)
    plt.close()
    print(f"Training curves saved : {out}")
    return out


# ── Plot Confusion Matrix ────────────────────────────────────
def plot_confusion_matrix(y_true, y_pred,
                           classes=CLASSES,
                           save_path=RESULTS_PATH):
    """
    Plots and saves confusion matrix heatmap.

    y_true    : array of true class indices
    y_pred    : array of predicted class indices
    classes   : list of class names
    save_path : folder to save the plot

    Output : saves confusion_matrix.png
    """
    from sklearn.metrics import confusion_matrix

    cm = confusion_matrix(y_true, y_pred)

    plt.figure(figsize=(9, 7))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=classes,
        yticklabels=classes,
        linewidths=0.5,
        linecolor="gray"
    )
    plt.title(
        "Confusion Matrix — Wheat Disease Detection",
        fontsize=14, fontweight="bold", pad=15)
    plt.ylabel("Actual Label", fontsize=12)
    plt.xlabel("Predicted Label", fontsize=12)
    plt.xticks(rotation=25, ha="right", fontsize=10)
    plt.yticks(rotation=0, fontsize=10)
    plt.tight_layout()

    out = Path(save_path) / "confusion_matrix.png"
    plt.savefig(str(out), dpi=150)
    plt.close()
    print(f"Confusion matrix saved : {out}")
    return out


# ── Plot Class Distribution ──────────────────────────────────
def plot_class_distribution(class_counts,
                              save_path=RESULTS_PATH):
    """
    Plots bar chart of image count per class.

    class_counts : dict {class_name: count}
    save_path    : folder to save the plot

    Output : saves class_distribution_bar.png
    """
    plt.figure(figsize=(9, 5))
    bars = plt.bar(
        class_counts.keys(),
        class_counts.values(),
        color=COLORS,
        edgecolor="white",
        linewidth=1.2
    )

    for bar, count in zip(bars,
                          class_counts.values()):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 20,
            str(count),
            ha="center", va="bottom",
            fontweight="bold", fontsize=12
        )

    plt.title("Number of Images Per Class",
              fontsize=15, fontweight="bold", pad=15)
    plt.xlabel("Disease Class", fontsize=12)
    plt.ylabel("Number of Images", fontsize=12)
    plt.xticks(fontsize=11)
    plt.ylim(0, max(class_counts.values()) + 200)
    plt.tight_layout()

    out = Path(save_path) / \
          "class_distribution_bar.png"
    plt.savefig(str(out), dpi=150)
    plt.close()
    print(f"Class distribution saved : {out}")
    return out


# ── Plot Probability Bar Chart ───────────────────────────────
def plot_prediction_probabilities(all_probs,
                                   disease,
                                   confidence):
    """
    Plots horizontal bar chart of prediction
    probabilities for all 4 classes.
    Used in Streamlit frontend to show results.

    all_probs  : dict {class_name: probability}
    disease    : predicted disease class string
    confidence : confidence percentage float

    Output : matplotlib figure object
             (shown directly in Streamlit)
    """
    classes = list(all_probs.keys())
    probs   = list(all_probs.values())

    # highlight predicted class in different color
    bar_colors = []
    for cls in classes:
        if cls == disease:
            bar_colors.append("#FF5722")
        else:
            bar_colors.append("#90CAF9")

    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.barh(classes, probs,
                   color=bar_colors,
                   edgecolor="white",
                   linewidth=0.5)

    # add percentage labels
    for bar, prob in zip(bars, probs):
        ax.text(
            bar.get_width() + 0.5,
            bar.get_y() + bar.get_height() / 2,
            f"{prob:.1f}%",
            va="center", fontsize=11,
            fontweight="bold"
        )

    ax.set_xlim(0, 115)
    ax.set_xlabel("Probability (%)", fontsize=11)
    ax.set_title(
        f"Prediction: "
        f"{disease.replace('_',' ').title()} "
        f"({confidence:.1f}%)",
        fontsize=13, fontweight="bold"
    )
    ax.grid(True, axis="x", alpha=0.3)

    # add legend
    predicted = mpatches.Patch(
        color="#FF5722", label="Predicted Class")
    others    = mpatches.Patch(
        color="#90CAF9", label="Other Classes")
    ax.legend(handles=[predicted, others],
              loc="lower right", fontsize=9)

    plt.tight_layout()
    return fig


# ── Plot Sample Predictions ──────────────────────────────────
def plot_sample_predictions(samples,
                              save_path=RESULTS_PATH):
    """
    Plots grid of sample images with
    true and predicted labels.

    samples : list of tuples
              (image_array, true_label,
               pred_label, confidence)
    Output  : saves sample_predictions.png
    """
    n       = len(samples)
    cols    = 4
    rows    = (n + cols - 1) // cols

    fig, axes = plt.subplots(
        rows, cols,
        figsize=(14, rows * 3.5)
    )
    fig.suptitle(
        "Sample Predictions — Test Set",
        fontsize=15, fontweight="bold"
    )

    # flatten axes for easy indexing
    axes_flat = axes.flatten() \
        if rows > 1 else [axes] \
        if cols == 1 else axes.flatten()

    for idx, (img, true_lbl,
               pred_lbl, conf) in enumerate(samples):
        axes_flat[idx].imshow(img)
        axes_flat[idx].axis("off")
        color = "green" \
            if pred_lbl == true_lbl else "red"
        axes_flat[idx].set_title(
            f"True : {true_lbl}\n"
            f"Pred : {pred_lbl} ({conf:.1f}%)",
            fontsize=9,
            color=color,
            fontweight="bold"
        )

    # hide empty subplots
    for idx in range(len(samples),
                     len(axes_flat)):
        axes_flat[idx].axis("off")

    plt.tight_layout()
    out = Path(save_path) / \
          "sample_predictions.png"
    plt.savefig(str(out), dpi=150,
                bbox_inches="tight")
    plt.close()
    print(f"Sample predictions saved : {out}")
    return out


# ── Quick Test ───────────────────────────────────────────────
if __name__ == "__main__":
    print("Testing plot_utils.py...\n")

    # test probability chart
    test_probs = {
        "healthy"       : 2.10,
        "leaf_rust"     : 91.30,
        "stripe_rust"   : 5.20,
        "powdery_mildew": 1.40
    }

    fig = plot_prediction_probabilities(
        test_probs,
        disease="leaf_rust",
        confidence=91.30
    )
    plt.savefig(
        str(RESULTS_PATH /
            "test_probability_chart.png"),
        dpi=150
    )
    plt.close()
    print("✅ Probability chart generated")

    # test class distribution
    test_counts = {
        "healthy"       : 1591,
        "leaf_rust"     : 845,
        "stripe_rust"   : 951,
        "powdery_mildew": 870
    }
    plot_class_distribution(test_counts)
    print("✅ Class distribution chart generated")

    print("\nplot_utils.py working correctly!")