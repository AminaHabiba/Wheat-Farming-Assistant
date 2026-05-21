# backend/app.py

# Main Flask application entry point.

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve()
                    .parent.parent))

from flask import Flask, jsonify
from flask_cors import CORS

from backend.config import (ACTIVE_CONFIG,
                             create_required_folders,
                             validate_config)
from backend.routes import routes
from src.utils.logger import (get_logger,
                               log_system_start)

# ── Create Flask App ─────────────────────────────────────────
app = Flask(__name__)

# ── Load Config ──────────────────────────────────────────────
app.config.from_object(ACTIVE_CONFIG)

# ── Enable CORS ───────────────────────────────────────────────
# Allows frontend (Streamlit) to call Flask API
CORS(app, origins=ACTIVE_CONFIG.CORS_ORIGINS)

# ── Register Routes ──────────────────────────────────────────
app.register_blueprint(routes)

# ── Setup Logger ─────────────────────────────────────────────
logger = get_logger()


# ── Root Endpoint ────────────────────────────────────────────
@app.route("/", methods=["GET"])
def index():
    """
    Root endpoint — confirms API is running.
    URL : GET http://localhost:5000/
    """
    return jsonify({
        "status"     : "running",
        "message"    : "Welcome to AI-Powered "
                       "Wheat Farming Assistant API",
        "developer"  : "Amina Habiba",
        "roll_number": "2022-ag-7802",
        "university" : "UAF Faisalabad",
        "year"       : "2026",
        "endpoints"  : {
            "health"    : "GET  /health",
            "predict"   : "POST /predict",
            "classes"   : "GET  /classes",
            "model_info": "GET  /model-info"
        }
    }), 200


# ── 404 Error Handler ────────────────────────────────────────
@app.errorhandler(404)
def not_found(error):
    """
    Handles requests to unknown endpoints.
    Returns clear JSON error instead of
    default HTML error page.
    """
    return jsonify({
        "status" : "error",
        "message": "Endpoint not found. "
                   "Check the URL and try again.",
        "available_endpoints": [
            "GET  /",
            "GET  /health",
            "POST /predict",
            "GET  /classes",
            "GET  /model-info"
        ]
    }), 404


# ── 405 Error Handler ────────────────────────────────────────
@app.errorhandler(405)
def method_not_allowed(error):
    """
    Handles wrong HTTP method requests.
    For example GET on /predict instead of POST.
    """
    return jsonify({
        "status" : "error",
        "message": "Method not allowed. "
                   "Check if you are using "
                   "correct HTTP method."
    }), 405


# ── 413 Error Handler ────────────────────────────────────────
@app.errorhandler(413)
def file_too_large(error):
    """
    Handles files larger than MAX_CONTENT_LENGTH.
    Flask automatically triggers this when
    uploaded file exceeds size limit.
    """
    return jsonify({
        "status" : "error",
        "message": "File too large. "
                   "Maximum allowed size is 10 MB."
    }), 413


# ── Startup Function ─────────────────────────────────────────
def startup():
    """
    Runs all startup checks before
    Flask begins accepting requests.

    1. Creates required folders
    2. Validates configuration
    3. Logs system start
    """
    print("=" * 55)
    print("  AI-Powered Wheat Farming Assistant")
    print("  Amina Habiba — 2022-ag-7802")
    print("  UAF Faisalabad — 2026")
    print("=" * 55)

    # create folders
    create_required_folders()

    # validate config
    valid = validate_config()
    if not valid:
        print("\n❌ Startup failed!")
        print("   Fix configuration issues "
              "and restart.")
        sys.exit(1)

    # log system start
    log_system_start(logger)

    print("\n✅ All checks passed!")
    print("=" * 55)


# ── Run App ──────────────────────────────────────────────────
if __name__ == "__main__":
    # run startup checks
    startup()

    print("\n🌾 Starting Flask server...")
    print("   URL : http://localhost:5000")
    print("   Press CTRL+C to stop\n")

    # start Flask server
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=ACTIVE_CONFIG.DEBUG,
        use_reloader=False  # prevents model
                            # loading twice
    )