# src/preprocessing/pipeline.py

# Full DIP pipeline, called by backend for every image uploaded by a farmer.

import cv2
import numpy as np
from PIL import Image
import io

IMG_SIZE = (224, 224)
MIN_SIZE = 100


def validate_image(img_input):
    """
    Checks image is valid and large enough.
    Accepts file path (str) or bytes.

    Output : tuple (True, None) if valid
                   (False, error_msg) if invalid
    """
    try:
        if isinstance(img_input, str):
            img = Image.open(img_input)
        else:
            img = Image.open(io.BytesIO(img_input))
        w, h = img.size
        if w < MIN_SIZE or h < MIN_SIZE:
            return False, (
                f"Image too small ({w}x{h}). "
                f"Minimum is {MIN_SIZE}x{MIN_SIZE}."
            )
        return True, None
    except Exception as e:
        return False, f"Cannot open image: {str(e)}"


def read_image(img_input):
    """
    Reads image from file path or bytes.
    Returns RGB numpy array.
    """
    if isinstance(img_input, str):
        img = cv2.imread(img_input)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    else:
        img_array = np.frombuffer(img_input, np.uint8)
        img       = cv2.imdecode(img_array,
                                 cv2.IMREAD_COLOR)
        img       = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img


def resize_image(img, size=IMG_SIZE):
    """Resizes image to 224x224 using INTER_AREA."""
    return cv2.resize(img, size,
                      interpolation=cv2.INTER_AREA)


def remove_noise(img):
    """Gentle Gaussian blur to remove camera noise."""
    return cv2.GaussianBlur(img, (3, 3), 0)


def enhance_contrast(img):
    """CLAHE on L channel of LAB color space."""
    lab     = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    clahe   = cv2.createCLAHE(clipLimit=2.0,
                               tileGridSize=(8, 8))
    l       = clahe.apply(l)
    lab     = cv2.merge([l, a, b])
    return cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)


def normalize_image(img):
    """Converts pixel values from 0-255 to 0.0-1.0."""
    return img.astype(np.float32) / 255.0


def preprocess(img_input):
    """
    Full DIP pipeline for one image.

    Input  : file path (str) OR raw bytes
    Output : numpy array shape (1, 224, 224, 3)
             ready for model.predict()

    Steps:
      1. Validate
      2. Read
      3. Resize to 224x224
      4. Noise removal
      5. Contrast enhancement
      6. Normalize
      7. Expand dims for batch
    """
    valid, error = validate_image(img_input)
    if not valid:
        raise ValueError(f"Invalid image: {error}")

    img = read_image(img_input)
    img = resize_image(img)
    img = remove_noise(img)
    img = enhance_contrast(img)
    img = normalize_image(img)
    img = np.expand_dims(img, axis=0)
    return img


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        path   = sys.argv[1]
        result = preprocess(path)
        print(f"Input path   : {path}")
        print(f"Output shape : {result.shape}")
        print(f"Value range  : {result.min():.4f}"
              f" - {result.max():.4f}")
        print("pipeline.py working correctly!")
    else:
        print("Usage: python pipeline.py <image_path>")