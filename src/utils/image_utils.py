# src/utils/image_utils.py

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve()
                    .parent.parent.parent))

import cv2
import numpy as np
from PIL import Image
import io
import base64

# ── Constants ────────────────────────────────────────────────
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png",
                      ".JPG", ".JPEG", ".PNG"}
MIN_SIZE           = 100
MAX_SIZE_MB        = 10


# ── Validate File Extension ──────────────────────────────────
def is_allowed_extension(filename):
    """
    Checks if file has allowed image extension.

    filename : string — original filename
    Output   : True if allowed, False if not
    """
    ext = Path(filename).suffix
    return ext in ALLOWED_EXTENSIONS


# ── Validate File Size ───────────────────────────────────────
def is_valid_size(image_bytes, max_mb=MAX_SIZE_MB):
    """
    Checks if file size is within allowed limit.

    image_bytes : raw bytes of image
    max_mb      : maximum size in MB (default 10)
    Output      : True if valid, False if too large
    """
    size_mb = len(image_bytes) / (1024 * 1024)
    return size_mb <= max_mb


# ── Validate Image Dimensions ────────────────────────────────
def is_valid_dimensions(image_bytes,
                         min_size=MIN_SIZE):
    """
    Checks if image dimensions are large enough.

    image_bytes : raw bytes of image
    min_size    : minimum width or height in pixels
    Output      : tuple (True/False, width, height)
    """
    try:
        img    = Image.open(io.BytesIO(image_bytes))
        w, h   = img.size
        valid  = w >= min_size and h >= min_size
        return valid, w, h
    except Exception:
        return False, 0, 0


# ── Full Image Validation ────────────────────────────────────
def validate_uploaded_image(filename, image_bytes):
    """
    Runs all validations on an uploaded image.
    Used by Flask backend before prediction.

    filename    : original filename from upload
    image_bytes : raw bytes from request.files

    Output : dict with keys:
      valid   — True if all checks pass
      message — error message if invalid
      width   — image width in pixels
      height  — image height in pixels
      size_mb — file size in MB
    """
    # check extension
    if not is_allowed_extension(filename):
        return {
            "valid"  : False,
            "message": f"File type not allowed. "
                       f"Please upload JPG or PNG image."
        }

    # check file size
    if not is_valid_size(image_bytes):
        size_mb = len(image_bytes) / (1024 * 1024)
        return {
            "valid"  : False,
            "message": f"File too large "
                       f"({size_mb:.1f} MB). "
                       f"Maximum allowed is "
                       f"{MAX_SIZE_MB} MB."
        }

    # check dimensions
    valid, w, h = is_valid_dimensions(image_bytes)
    if not valid:
        return {
            "valid"  : False,
            "message": f"Image too small ({w}x{h}). "
                       f"Please upload a clearer "
                       f"and larger image."
        }

    size_mb = len(image_bytes) / (1024 * 1024)
    return {
        "valid"  : True,
        "message": "Image is valid",
        "width"  : w,
        "height" : h,
        "size_mb": round(size_mb, 2)
    }


# ── Load Image From Bytes ────────────────────────────────────
def load_image_from_bytes(image_bytes):
    """
    Loads image from raw bytes into
    RGB numpy array.

    image_bytes : raw bytes
    Output      : numpy array (H, W, 3) RGB
    """
    img_array = np.frombuffer(image_bytes, np.uint8)
    img       = cv2.imdecode(img_array,
                             cv2.IMREAD_COLOR)
    img       = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img


# ── Load Image From Path ─────────────────────────────────────
def load_image_from_path(image_path):
    """
    Loads image from file path into
    RGB numpy array.

    image_path : string or Path
    Output     : numpy array (H, W, 3) RGB
    """
    img = cv2.imread(str(image_path))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img


# ── Convert Image To Base64 ──────────────────────────────────
def image_to_base64(image_bytes):
    """
    Converts raw image bytes to base64 string.
    Used by Flask to send image back to frontend.

    image_bytes : raw bytes
    Output      : base64 encoded string
    """
    return base64.b64encode(
        image_bytes).decode("utf-8")


# ── Convert Numpy Array To Base64 ───────────────────────────
def array_to_base64(img_array):
    """
    Converts numpy array to base64 JPEG string.
    Used to send processed images to frontend.

    img_array : numpy array (H, W, 3) RGB
    Output    : base64 encoded string
    """
    # convert RGB to BGR for cv2
    img_bgr = cv2.cvtColor(img_array,
                            cv2.COLOR_RGB2BGR)
    # encode to JPEG bytes
    _, buffer = cv2.imencode(".jpg", img_bgr)
    # convert to base64
    return base64.b64encode(
        buffer).decode("utf-8")


# ── Resize Image For Display ─────────────────────────────────
def resize_for_display(img_array,
                        max_width=400,
                        max_height=400):
    """
    Resizes image for display in UI.
    Maintains aspect ratio.

    img_array  : numpy array (H, W, 3)
    max_width  : maximum display width
    max_height : maximum display height
    Output     : resized numpy array
    """
    h, w    = img_array.shape[:2]
    ratio   = min(max_width / w, max_height / h)

    if ratio < 1:
        new_w = int(w * ratio)
        new_h = int(h * ratio)
        img_array = cv2.resize(
            img_array, (new_w, new_h),
            interpolation=cv2.INTER_AREA
        )
    return img_array


# ── Get Image Info ───────────────────────────────────────────
def get_image_info(image_bytes):
    """
    Returns basic info about an image.
    Used for display in frontend.

    image_bytes : raw bytes
    Output      : dict with image details
    """
    try:
        img     = Image.open(io.BytesIO(image_bytes))
        w, h    = img.size
        mode    = img.mode
        size_mb = round(
            len(image_bytes) / (1024 * 1024), 2)
        return {
            "width"   : w,
            "height"  : h,
            "mode"    : mode,
            "size_mb" : size_mb,
            "format"  : img.format
        }
    except Exception as e:
        return {"error": str(e)}


# ── Quick Test ───────────────────────────────────────────────
if __name__ == "__main__":
    print("Testing image_utils.py...\n")

    # test extension validation
    test_files = [
        "leaf.jpg", "leaf.png",
        "leaf.pdf", "leaf.txt"
    ]
    print("Extension validation:")
    for f in test_files:
        result = is_allowed_extension(f)
        status = "✅" if result else "❌"
        print(f"  {status} {f}")

    # test with real image if available
    test_path = Path(
        "dataset/processed/test/healthy"
    )
    images = list(test_path.glob("*.jpg"))

    if images:
        print(f"\nTesting with real image:")
        print(f"  Path : {images[0]}")

        with open(str(images[0]), "rb") as f:
            img_bytes = f.read()

        # validate
        validation = validate_uploaded_image(
            images[0].name, img_bytes)
        print(f"  Valid    : {validation['valid']}")
        print(f"  Size     : {validation['size_mb']} MB")
        print(f"  Dims     : "
              f"{validation['width']}x"
              f"{validation['height']}")

        # get info
        info = get_image_info(img_bytes)
        print(f"  Format   : {info['format']}")
        print(f"  Mode     : {info['mode']}")

        # load as array
        img_array = load_image_from_bytes(img_bytes)
        print(f"  Array    : {img_array.shape}")

        # base64
        b64 = image_to_base64(img_bytes)
        print(f"  Base64   : "
              f"{len(b64)} characters ✅")

    print("\nimage_utils.py working correctly!")