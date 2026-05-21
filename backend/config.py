# backend/config.py

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve()
                    .parent.parent))

import os

# ── Base Paths ───────────────────────────────────────────────
BASE_DIR     = Path(__file__).resolve().parent.parent
BACKEND_DIR  = BASE_DIR / "backend"
UPLOADS_DIR  = BACKEND_DIR / "uploads"
MODELS_DIR   = BASE_DIR / "saved_models"
RESULTS_DIR  = BASE_DIR / "results"
LOGS_DIR     = BASE_DIR / "logs"
SRC_DIR      = BASE_DIR / "src"

# ── Model Settings ───────────────────────────────────────────
MODEL_PATH   = MODELS_DIR / "wheat_disease_model.h5"
CLASSES      = [
    "healthy",
    "leaf_rust",
    "stripe_rust",
    "powdery_mildew"
]
IMG_SIZE     = (224, 224)
CONFIDENCE_THRESHOLD = 0.60

# ── Upload Settings ──────────────────────────────────────────
ALLOWED_EXTENSIONS = {
    "jpg", "jpeg", "png",
    "JPG", "JPEG", "PNG"
}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024   # 10 MB

# ── Flask Settings ───────────────────────────────────────────
class Config:
    """
    Flask application configuration class.
    Import and use in app.py like:
        app.config.from_object(Config)
    """
    # security
    SECRET_KEY           = os.environ.get(
        "SECRET_KEY",
        "wheat-assistant-uaf-2026-amina"
    )

    # file upload
    UPLOAD_FOLDER        = str(UPLOADS_DIR)
    MAX_CONTENT_LENGTH   = MAX_CONTENT_LENGTH
    ALLOWED_EXTENSIONS   = ALLOWED_EXTENSIONS

    # model
    MODEL_PATH           = str(MODEL_PATH)
    CLASSES              = CLASSES
    IMG_SIZE             = IMG_SIZE
    CONFIDENCE_THRESHOLD = CONFIDENCE_THRESHOLD

    # Flask debug mode
    DEBUG                = False
    TESTING              = False

    # CORS — allow frontend to call API
    CORS_ORIGINS         = ["*"]


class DevelopmentConfig(Config):
    """
    Development configuration.
    Use this while building the project.
    DEBUG = True shows detailed error messages.
    """
    DEBUG   = True
    TESTING = False


class ProductionConfig(Config):
    """
    Production configuration.
    Use this when deploying to server.
    DEBUG = False hides error details.
    """
    DEBUG   = False
    TESTING = False


# ── Active Config ────────────────────────────────────────────
# Change to ProductionConfig when deploying
ACTIVE_CONFIG = DevelopmentConfig


# ── Create Required Folders ──────────────────────────────────
def create_required_folders():
    """
    Creates all required folders if they
    don't exist. Called once at app startup.
    """
    folders = [
        UPLOADS_DIR,
        MODELS_DIR,
        RESULTS_DIR,
        LOGS_DIR
    ]
    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)

    print("✅ Required folders verified:")
    for folder in folders:
        print(f"   {folder}")


# ── Validate Config ──────────────────────────────────────────
def validate_config():
    """
    Validates that all required files exist.
    Called once at app startup.
    Returns True if valid, False if not.
    """
    print("\nValidating configuration...")
    valid = True

    # check model file
    if not MODEL_PATH.exists():
        print(f"  ❌ Model not found : {MODEL_PATH}")
        print(f"     Run Notebook 03 to train model")
        valid = False
    else:
        print(f"  ✅ Model found     : {MODEL_PATH}")

    # check src folder
    if not SRC_DIR.exists():
        print(f"  ❌ src/ not found  : {SRC_DIR}")
        valid = False
    else:
        print(f"  ✅ src/ found      : {SRC_DIR}")

    # check recommendation JSON files
    rec_dir   = SRC_DIR / "recommendation"
    json_files = [
        "disease_info.json",
        "treatment_data.json",
        "farming_tips.json"
    ]
    for jf in json_files:
        jf_path = rec_dir / jf
        if not jf_path.exists():
            print(f"  ❌ Missing : {jf}")
            valid = False
        else:
            print(f"  ✅ Found   : {jf}")

    if valid:
        print("\n✅ Configuration valid!")
    else:
        print("\n❌ Fix above issues before starting.")

    return valid


# ── Quick Test ───────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("  CONFIGURATION SUMMARY")
    print("=" * 50)
    print(f"  Base dir    : {BASE_DIR}")
    print(f"  Model path  : {MODEL_PATH}")
    print(f"  Uploads dir : {UPLOADS_DIR}")
    print(f"  Classes     : {CLASSES}")
    print(f"  Image size  : {IMG_SIZE}")
    print(f"  Max upload  : "
          f"{MAX_CONTENT_LENGTH // (1024*1024)} MB")
    print(f"  Debug mode  : {ACTIVE_CONFIG.DEBUG}")
    print("=" * 50)

    create_required_folders()
    validate_config()

    print("\nconfig.py working correctly!")