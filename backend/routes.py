# backend/routes.py

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve()
                    .parent.parent))

from flask import (Blueprint, request,
                   jsonify)

from src.model.predict import (predict_from_bytes,
                                load_disease_model)
from src.recommendation.recommender import (
    get_recommendation)
from src.utils.image_utils import (
    validate_uploaded_image)
from src.utils.logger import (get_logger,
                               log_prediction,
                               log_request,
                               log_error)
from backend.config import ACTIVE_CONFIG

# ── Setup ────────────────────────────────────────────────────
routes = Blueprint("routes", __name__)
logger = get_logger()

# ── Global Model Variable ────────────────────────────────────
# model is loaded once when app starts
# stored here so all requests share same model
_model = None


def get_model():
    """
    Returns loaded model.
    Loads from disk only on first call.
    All subsequent calls return cached model.
    """
    global _model
    if _model is None:
        logger.info("Loading model for first time...")
        _model = load_disease_model(
            ACTIVE_CONFIG.MODEL_PATH
        )
        logger.info("Model loaded and cached!")
    return _model


# ── GET /health ──────────────────────────────────────────────
@routes.route("/health", methods=["GET"])
def health_check():
    """
    Health check endpoint.
    Returns API status and basic info.

    URL    : GET http://localhost:5000/health
    Output : JSON with status info
    """
    log_request(logger, "/health", "GET", 200)

    return jsonify({
        "status"     : "running",
        "message"    : "Wheat Farming Assistant "
                       "API is running!",
        "model"      : "MobileNetV2",
        "classes"    : ACTIVE_CONFIG.CLASSES,
        "version"    : "1.0",
        "developer"  : "Amina Habiba",
        "university" : "UAF Faisalabad",
        "year"       : "2026"
    }), 200


# ── POST /predict ────────────────────────────────────────────
@routes.route("/predict", methods=["POST"])
def predict():
    """
    Main prediction endpoint.
    Accepts image upload and returns
    disease prediction + recommendations.

    URL    : POST http://localhost:5000/predict
    Input  : multipart/form-data with 'image' field
    Output : JSON with prediction and recommendation

    Steps:
      1. Check image was uploaded
      2. Validate image
      3. Run prediction
      4. Get recommendation
      5. Return complete result
    """
    filename = None

    try:
        # Step 1 — check image uploaded
        if "image" not in request.files:
            log_error(logger,
                      "No image in request")
            log_request(logger,
                        "/predict", "POST", 400)
            return jsonify({
                "status" : "error",
                "message": "No image uploaded. "
                           "Please select an image."
            }), 400

        file     = request.files["image"]
        filename = file.filename

        if filename == "":
            log_error(logger,
                      "Empty filename")
            return jsonify({
                "status" : "error",
                "message": "No image selected."
            }), 400

        # Step 2 — validate image
        image_bytes = file.read()
        validation  = validate_uploaded_image(
            filename, image_bytes)

        if not validation["valid"]:
            log_error(logger,
                      validation["message"],
                      filename)
            log_request(logger,
                        "/predict", "POST", 400)
            return jsonify({
                "status" : "error",
                "message": validation["message"]
            }), 400

        # Step 3 — run prediction
        model  = get_model()
        result = predict_from_bytes(
            model, image_bytes)

        if result["status"] == "error":
            log_error(logger,
                      result["message"],
                      filename)
            log_request(logger,
                        "/predict", "POST", 500)
            return jsonify(result), 500

        # Step 4 — get recommendation
        recommendation = get_recommendation(
            result["disease"]
        )

        # Step 5 — log and return
        log_prediction(
            logger,
            filename=filename,
            disease=result["disease"],
            confidence=result["confidence"],
            is_uncertain=result["is_uncertain"]
        )
        log_request(logger,
                    "/predict", "POST", 200)

        # build complete response
        response = {
            "status"        : "success",

            # prediction results
            "prediction"    : {
                "disease"      : result["disease"],
                "display_name" : recommendation[
                    "disease_info"]["display_name"],
                "confidence"   : result["confidence"],
                "all_probs"    : result["all_probs"],
                "is_uncertain" : result["is_uncertain"],
                "is_healthy"   : result["is_healthy"],
                "message"      : result["message"]
            },

            # image info
            "image_info"    : {
                "filename" : filename,
                "width"    : validation["width"],
                "height"   : validation["height"],
                "size_mb"  : validation["size_mb"]
            },

            # recommendation
            "recommendation": recommendation
        }

        return jsonify(response), 200

    except Exception as e:
        log_error(logger, str(e), filename)
        log_request(logger,
                    "/predict", "POST", 500)
        return jsonify({
            "status" : "error",
            "message": f"Server error: {str(e)}"
        }), 500


# ── GET /classes ─────────────────────────────────────────────
@routes.route("/classes", methods=["GET"])
def get_classes():
    """
    Returns list of disease classes
    the model can detect.

    URL    : GET http://localhost:5000/classes
    Output : JSON with class list
    """
    log_request(logger, "/classes", "GET", 200)

    return jsonify({
        "status" : "success",
        "classes": ACTIVE_CONFIG.CLASSES,
        "total"  : len(ACTIVE_CONFIG.CLASSES)
    }), 200


# ── GET /model-info ──────────────────────────────────────────
@routes.route("/model-info", methods=["GET"])
def model_info():
    """
    Returns model information and accuracy.

    URL    : GET http://localhost:5000/model-info
    Output : JSON with model details
    """
    log_request(logger,
                "/model-info", "GET", 200)

    return jsonify({
        "status"         : "success",
        "model_name"     : "MobileNetV2",
        "framework"      : "TensorFlow 2.13 / Keras",
        "input_size"     : "224x224x3",
        "num_classes"    : 4,
        "classes"        : ACTIVE_CONFIG.CLASSES,
        "val_accuracy"   : "93.55%",
        "test_accuracy"  : "92.69%",
        "training_images": 2978,
        "test_images"    : 643,
        "developer"      : "Amina Habiba",
        "roll_number"    : "2022-ag-7802",
        "university"     : "UAF Faisalabad",
        "year"           : "2026"
    }), 200


# ── Quick Test ───────────────────────────────────────────────
if __name__ == "__main__":
    print("routes.py loaded successfully!")
    print()
    print("Available endpoints:")
    print("  GET  /health      — API status check")
    print("  POST /predict     — predict disease")
    print("  GET  /classes     — list all classes")
    print("  GET  /model-info  — model details")