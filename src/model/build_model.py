# src/model/build_model.py

import tensorflow as tf
from keras.applications import MobileNetV2
from keras.models import Model
from keras.layers import (Dense, Dropout,
                          GlobalAveragePooling2D)
from keras.optimizers import Adam

NUM_CLASSES = 4
IMG_SIZE    = (224, 224, 3)
LR          = 0.0001


def build_mobilenetv2(num_classes=NUM_CLASSES,
                      input_shape=IMG_SIZE,
                      learning_rate=LR,
                      freeze_base=True):
    """
    Builds MobileNetV2 for wheat disease classification.

    Architecture:
      MobileNetV2 (frozen, ImageNet weights)
        → GlobalAveragePooling2D
        → Dense(128, relu)
        → Dropout(0.3)
        → Dense(4, softmax)

    Output : compiled Keras Model
    """
    base_model           = MobileNetV2(
        input_shape=input_shape,
        include_top=False,
        weights="imagenet"
    )
    base_model.trainable = not freeze_base

    x      = base_model.output
    x      = GlobalAveragePooling2D()(x)
    x      = Dense(128, activation="relu")(x)
    x      = Dropout(0.3)(x)
    output = Dense(num_classes,
                   activation="softmax")(x)

    model  = Model(inputs=base_model.input,
                   outputs=output)
    model.compile(
        optimizer=Adam(learning_rate=learning_rate),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )
    return model


def unfreeze_top_layers(model, num_layers=20):
    """
    Unfreezes last N layers for fine-tuning.
    Recompiles with lower LR.

    Output : recompiled model
    """
    for layer in model.layers[-num_layers:]:
        layer.trainable = True

    model.compile(
        optimizer=Adam(learning_rate=LR / 10),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )
    trainable = sum(1 for l in model.layers
                    if l.trainable)
    frozen    = sum(1 for l in model.layers
                    if not l.trainable)
    print(f"Unfrozen last {num_layers} layers")
    print(f"Trainable : {trainable}")
    print(f"Frozen    : {frozen}")
    return model


def print_model_summary(model):
    """Prints clean model summary."""
    total     = model.count_params()
    trainable = sum(tf.size(w).numpy()
                    for w in model.trainable_weights)
    print("=" * 50)
    print("  MODEL SUMMARY")
    print("=" * 50)
    print(f"  Base model : MobileNetV2")
    print(f"  Input      : {model.input_shape}")
    print(f"  Output     : {model.output_shape}")
    print(f"  Layers     : {len(model.layers)}")
    print(f"  Params     : {total:,}")
    print(f"  Trainable  : {trainable:,}")
    print("=" * 50)


if __name__ == "__main__":
    print("Building MobileNetV2...\n")
    model = build_mobilenetv2()
    print_model_summary(model)
    print("\nbuild_model.py working correctly!")