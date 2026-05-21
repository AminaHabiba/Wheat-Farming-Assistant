# src/preprocessing/resize_normalize.py

import cv2
import numpy as np

IMG_SIZE = (224, 224)


def resize_image(img, size=IMG_SIZE):
    """
    Resizes image to target size (default 224x224).
    Uses INTER_AREA — best quality when shrinking.

    Input  : numpy array (H, W, 3)
    Output : numpy array (224, 224, 3)
    """
    return cv2.resize(img, size, interpolation=cv2.INTER_AREA)


def normalize_image(img):
    """
    Normalizes pixel values from 0-255 to 0.0-1.0.
    CNNs work better with small normalized values.

    Input  : numpy array with values 0-255
    Output : numpy array with values 0.0-1.0 (float32)
    """
    return img.astype(np.float32) / 255.0


def resize_and_normalize(img, size=IMG_SIZE):
    """
    Runs both resize and normalize together.

    Input  : numpy array (H, W, 3) any size
    Output : numpy array (224, 224, 3) normalized
    """
    img = resize_image(img, size)
    img = normalize_image(img)
    return img


if __name__ == "__main__":
    dummy  = np.random.randint(0, 255,
                               (500, 400, 3),
                               dtype=np.uint8)
    result = resize_and_normalize(dummy)
    print(f"Input  shape : {dummy.shape}")
    print(f"Output shape : {result.shape}")
    print(f"Output range : {result.min():.4f}"
          f" - {result.max():.4f}")
    print("resize_normalize.py working correctly!")