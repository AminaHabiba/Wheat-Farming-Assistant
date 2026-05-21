# src/model/predict.py

# Most important file, every image uploaded by a 
# farmer goes through this file for prediction.
# Called by backend/routes.py for every request.

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve()
                    .parent.parent.parent))

import numpy as np
from keras.models import load_model
from src.preprocessing.pipeline import preprocess

# ── Constants ────────────────────────────────────────────────
CLASSES = [
    "healthy",
    "leaf_rust",
    "stripe_rust",
    "powdery_mildew"
]

SAVED_MODELS         = Path("saved_models")
MODEL_PATH           = SAVED_MODELS / \
                       "wheat_disease_model.h5"
CONFIDENCE_THRESHOLD = 0.60


# ── Load Model Once ──────────────────────────────────────────
def load_disease_model(model_path=MODEL_PATH):
    """
    Loads saved CNN model from disk.
    Call this ONCE when backend starts —
    not on every prediction request.
    Keeps model in memory for fast predictions.

    model_path : Path to .h5 file
    Output     : loaded Keras model
    """
    if not Path(model_path).exists():
        raise FileNotFoundError(
            f"Model not found at {model_path}.\n"
            f"Please run Notebook 03 first."
        )

    print(f"Loading model from : {model_path}")
    model = load_model(
        str(model_path),
        compile=False     # faster loading
    )

    # recompile after loading
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    print(f"✅ Model loaded successfully!")
    print(f"   Input  : {model.input_shape}")
    print(f"   Output : {model.output_shape}")
    return model


# ── Predict Single Image ─────────────────────────────────────
def predict_disease(model, img_input):
    """
    Predicts wheat disease from a single image.

    Steps:
      1. Preprocess image (full DIP pipeline)
      2. Run model.predict()
      3. Get class with highest probability
      4. Check confidence threshold
      5. Return structured result dict

    model     : loaded Keras model
    img_input : file path (str) OR bytes from upload

    Output : dict with keys:
      status       — "success" or "error"
      disease      — predicted class name
      confidence   — confidence percentage (float)
      all_probs    — probabilities for all 4 classes
      is_uncertain — True if confidence below 60%
      is_healthy   — True if disease == healthy
      message      — human readable result string
    """
    try:
        # Step 1 — preprocess image
        img_array = preprocess(img_input)

        # Step 2 — run prediction
        predictions = model.predict(
            img_array, verbose=0)

        # Step 3 — get class and confidence
        class_idx  = int(np.argmax(predictions[0]))
        confidence = float(np.max(predictions[0]))
        disease    = CLASSES[class_idx]

        # Step 4 — check confidence threshold
        is_uncertain = confidence < CONFIDENCE_THRESHOLD

        # Step 5 — all class probabilities
        all_probs = {
            cls: round(
                float(predictions[0][i]) * 100, 2)
            for i, cls in enumerate(CLASSES)
        }

        # build human readable message
        if disease == "healthy":
            message = (
                f"Your wheat crop appears healthy "
                f"({confidence*100:.1f}% confidence). "
                f"Continue regular care."
            )
        else:
            message = (
                f"{disease.replace('_',' ').title()} "
                f"detected with "
                f"{confidence*100:.1f}% confidence. "
                f"Treatment is recommended."
            )

        if is_uncertain:
            message += (
                " Note: Confidence is low — "
                "please upload a clearer image."
            )

        return {
            "status"       : "success",
            "disease"      : disease,
            "confidence"   : round(confidence*100, 2),
            "all_probs"    : all_probs,
            "is_uncertain" : is_uncertain,
            "is_healthy"   : disease == "healthy",
            "message"      : message
        }

    except ValueError as e:
        return {
            "status"  : "error",
            "message" : str(e)
        }
    except Exception as e:
        return {
            "status"  : "error",
            "message" : f"Prediction failed: {str(e)}"
        }


# ── Predict From File Path ───────────────────────────────────
def predict_from_path(model, image_path):
    """
    Predicts from a local file path.
    Used for testing in terminal.

    Output : prediction result dict
    """
    return predict_disease(model, str(image_path))


# ── Predict From Bytes ───────────────────────────────────────
def predict_from_bytes(model, image_bytes):
    """
    Predicts from raw bytes.
    Used by Flask backend for uploaded images.

    Output : prediction result dict
    """
    return predict_disease(model, image_bytes)


# ── Format Result For Display ────────────────────────────────
def format_result(result):
    """
    Formats prediction result for clean display.
    Used in terminal testing and Streamlit UI.

    Output : formatted string
    """
    if result["status"] == "error":
        return f"❌ Error: {result['message']}"

    lines = [
        "=" * 50,
        "  PREDICTION RESULT",
        "=" * 50,
        f"  Disease    : "
        f"{result['disease'].replace('_',' ').title()}",
        f"  Confidence : {result['confidence']}%",
        f"  Healthy    : "
        f"{'Yes ✅' if result['is_healthy'] else 'No ❌'}",
        f"  Uncertain  : "
        f"{'Yes ⚠️' if result['is_uncertain'] else 'No'}",
        "",
        "  All Probabilities:",
    ]

    for cls, prob in result["all_probs"].items():
        bar = "█" * int(prob / 5)
        lines.append(
            f"    {cls:<20} : {prob:>6.2f}%  {bar}"
        )

    lines += [
        "",
        f"  {result['message']}",
        "=" * 50
    ]
    return "\n".join(lines)


# ── Quick Test ───────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("  predict.py — Quick Test")
    print("=" * 50)

    # load model
    model = load_disease_model()
    print()

    if len(sys.argv) > 1:
        # test with provided image
        image_path = sys.argv[1]
        print(f"Testing image: {image_path}\n")
        result = predict_from_path(model, image_path)
        print(format_result(result))
    else:
        # auto test with first available test image
        test_dirs = [
            Path("dataset/processed/test/healthy"),
            Path("dataset/processed/test/leaf_rust"),
            Path("dataset/processed/test/stripe_rust"),
            Path("dataset/processed/test/powdery_mildew")
        ]

        print("Auto-testing one image per class:\n")
        for test_dir in test_dirs:
            images = list(test_dir.glob("*.jpg"))
            if images:
                result = predict_from_path(
                    model, images[0])
                print(format_result(result))
                print()