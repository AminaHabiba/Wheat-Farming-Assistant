# src/utils/logger.py

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve()
                    .parent.parent.parent))

import logging
import os
from datetime import datetime

# ── Constants ────────────────────────────────────────────────
LOGS_DIR  = Path("logs")
LOG_FILE  = LOGS_DIR / "wheat_assistant.log"


# ── Create Logs Folder ───────────────────────────────────────
def create_logs_dir():
    """
    Creates logs/ folder if it doesn't exist.
    """
    LOGS_DIR.mkdir(parents=True, exist_ok=True)


# ── Setup Logger ─────────────────────────────────────────────
def setup_logger(name="wheat_assistant",
                  level=logging.INFO):
    """
    Creates and configures a logger.
    Logs to both terminal and log file.

    name  : logger name (default wheat_assistant)
    level : logging level (default INFO)

    Output : configured logger object
    """
    create_logs_dir()

    logger = logging.getLogger(name)

    # avoid duplicate handlers if called twice
    if logger.handlers:
        return logger

    logger.setLevel(level)

    # ── Format ───────────────────────────────────
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | "
            "%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # ── File Handler — saves to logs/ ────────────
    file_handler = logging.FileHandler(
        str(LOG_FILE), encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # ── Console Handler — prints to terminal ─────
    console_handler = logging.StreamHandler(
        sys.stdout
    )
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # add both handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# ── Get Logger ───────────────────────────────────────────────
def get_logger(name="wheat_assistant"):
    """
    Returns existing logger or creates new one.
    Call this in any file that needs logging.

    name   : logger name
    Output : logger object
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger = setup_logger(name)
    return logger


# ── Log Prediction ───────────────────────────────────────────
def log_prediction(logger, filename,
                   disease, confidence,
                   is_uncertain):
    """
    Logs a prediction request with details.
    Called by backend after every prediction.

    logger      : logger object
    filename    : uploaded image filename
    disease     : predicted disease class
    confidence  : confidence percentage
    is_uncertain: True if confidence below 60%
    """
    status = "UNCERTAIN" if is_uncertain \
             else "CONFIDENT"

    logger.info(
        f"PREDICTION | "
        f"File: {filename} | "
        f"Disease: {disease} | "
        f"Confidence: {confidence:.1f}% | "
        f"Status: {status}"
    )


# ── Log Error ────────────────────────────────────────────────
def log_error(logger, error_msg, filename=None):
    """
    Logs an error during prediction.

    logger    : logger object
    error_msg : error message string
    filename  : uploaded filename if available
    """
    if filename:
        logger.error(
            f"ERROR | File: {filename} | "
            f"Message: {error_msg}"
        )
    else:
        logger.error(
            f"ERROR | Message: {error_msg}"
        )


# ── Log Request ──────────────────────────────────────────────
def log_request(logger, endpoint,
                method, status_code):
    """
    Logs an API request.
    Called by Flask backend for every request.

    logger      : logger object
    endpoint    : API endpoint e.g. /predict
    method      : HTTP method e.g. POST
    status_code : HTTP status code e.g. 200
    """
    logger.info(
        f"REQUEST | "
        f"{method} {endpoint} | "
        f"Status: {status_code}"
    )


# ── Log System Start ─────────────────────────────────────────
def log_system_start(logger):
    """
    Logs system startup message.
    Called once when Flask app starts.
    """
    logger.info("=" * 50)
    logger.info(
        "AI-Powered Wheat Farming Assistant"
    )
    logger.info(
        "Amina Habiba — 2022-ag-7802 — UAF — 2026"
    )
    logger.info(
        f"System started at "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    logger.info("=" * 50)


# ── Quick Test ───────────────────────────────────────────────
if __name__ == "__main__":
    print("Testing logger.py...\n")

    # setup logger
    logger = setup_logger()
    print(f"Log file : {LOG_FILE}\n")

    # test all log functions
    log_system_start(logger)

    log_request(logger,
                endpoint="/predict",
                method="POST",
                status_code=200)

    log_prediction(logger,
                   filename="wheat_leaf.jpg",
                   disease="leaf_rust",
                   confidence=91.30,
                   is_uncertain=False)

    log_prediction(logger,
                   filename="blurry_image.jpg",
                   disease="stripe_rust",
                   confidence=52.10,
                   is_uncertain=True)

    log_error(logger,
              error_msg="Image too small (50x50)",
              filename="tiny_image.jpg")

    log_error(logger,
              error_msg="Model prediction failed")

    print(f"\n✅ All logs written to {LOG_FILE}")
    print("logger.py working correctly!")