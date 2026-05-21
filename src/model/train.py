# src/model/train.py

# Note: Training already done in Notebook 03.
# This file is for retraining if needed.

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve()
                    .parent.parent.parent))

import numpy as np
from keras.callbacks import (ModelCheckpoint,
                              EarlyStopping,
                              ReduceLROnPlateau)
from src.model.build_model import build_mobilenetv2
from src.preprocessing.augmentation import (
    get_data_generators)

CLASSES        = ["healthy", "leaf_rust",
                  "stripe_rust", "powdery_mildew"]
PROCESSED_PATH = Path("dataset/processed")
SAVED_MODELS   = Path("saved_models")
BATCH          = 32
EPOCHS         = 30


def compute_class_weights(processed_path, classes):
    """Computes weights to fix class imbalance."""
    counts = [
        len(list((processed_path / "train" / cls)
                 .glob("*.jpg")))
        for cls in classes
    ]
    total         = sum(counts)
    class_weights = {
        i: total / (len(classes) * count)
        for i, count in enumerate(counts)
    }
    print("Class weights:")
    for i, cls in enumerate(classes):
        print(f"  {cls:<20} : "
              f"{class_weights[i]:.4f}"
              f"  ({counts[i]} images)")
    return class_weights


def get_callbacks(saved_models_path):
    """Returns ModelCheckpoint, EarlyStopping,
    ReduceLROnPlateau callbacks."""
    return [
        ModelCheckpoint(
            filepath=str(saved_models_path /
                         "wheat_disease_model.h5"),
            monitor="val_accuracy",
            save_best_only=True,
            verbose=1
        ),
        EarlyStopping(
            monitor="val_accuracy",
            patience=7,
            restore_best_weights=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=3,
            min_lr=1e-7,
            verbose=1
        )
    ]


def train_model(processed_path=PROCESSED_PATH,
                saved_models_path=SAVED_MODELS,
                classes=CLASSES,
                epochs=EPOCHS,
                batch_size=BATCH):
    """
    Full training pipeline.
    Returns (model, history).
    """
    print("=" * 50)
    print("  MODEL TRAINING")
    print("=" * 50)

    print("\nLoading data...")
    train_gen, val_gen, _ = get_data_generators(
        processed_path, classes,
        batch_size=batch_size)
    print(f"  Train : {train_gen.samples} images")
    print(f"  Val   : {val_gen.samples} images")

    print("\nComputing class weights...")
    class_weights = compute_class_weights(
        processed_path, classes)

    print("\nBuilding model...")
    model = build_mobilenetv2()

    print("\nTraining...\n" + "=" * 50)
    history = model.fit(
        train_gen,
        epochs=epochs,
        validation_data=val_gen,
        class_weight=class_weights,
        callbacks=get_callbacks(saved_models_path),
        verbose=1
    )

    best_val   = max(history.history["val_accuracy"])
    epochs_ran = len(history.history["accuracy"])
    print("\n" + "=" * 50)
    print(f"  Epochs ran        : {epochs_ran}")
    print(f"  Best val accuracy : {best_val*100:.2f}%")
    print("=" * 50)
    return model, history


if __name__ == "__main__":
    print("train.py loaded successfully!")
    print("Note: Training already done in Notebook 03")
    print("with 91.98% val accuracy.")
    print("Only run train_model() if retraining.")