# src/preprocessing/segmentation.py

import cv2
import numpy as np


def otsu_threshold(img):
    """
    Otsu's thresholding — auto finds best threshold
    to separate leaf/disease from background.

    Input  : numpy array (H, W, 3) RGB
    Output : numpy array (H, W) binary mask
    """
    gray    = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    _, binary = cv2.threshold(
        gray, 0, 255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )
    return binary


def canny_edge_detection(img, low=50, high=150):
    """
    Canny edge detection — finds boundaries of
    disease-affected regions on wheat leaves.

    Input  : numpy array (H, W, 3) RGB
    Output : numpy array (H, W) edge map
    """
    gray    = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges   = cv2.Canny(blurred, low, high)
    return edges


def color_segmentation(img):
    """
    HSV color segmentation targeting brown/yellow
    colors typical of wheat rust diseases.

    Input  : numpy array (H, W, 3) RGB
    Output : numpy array (H, W) mask
    """
    hsv          = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    lower_rust   = np.array([10, 50, 50])
    upper_rust   = np.array([30, 255, 255])
    mask_rust    = cv2.inRange(hsv,
                               lower_rust, upper_rust)
    lower_yellow = np.array([20, 80, 80])
    upper_yellow = np.array([40, 255, 255])
    mask_yellow  = cv2.inRange(hsv,
                               lower_yellow, upper_yellow)
    return cv2.bitwise_or(mask_rust, mask_yellow)


def apply_mask_on_image(img, mask):
    """
    Applies binary mask — shows only disease regions.
    Background becomes black.

    Input  : img (H,W,3) RGB, mask (H,W) binary
    Output : numpy array (H, W, 3) masked image
    """
    mask_3ch = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
    return cv2.bitwise_and(img, mask_3ch)


def segment_disease_region(img, method="otsu"):
    """
    Main segmentation function.
    Returns mask and masked image.

    method = "otsu"  → Otsu thresholding (default)
    method = "canny" → Canny edge detection
    method = "color" → HSV color segmentation

    Output : tuple (mask, masked_image)
    """
    if method == "otsu":
        mask = otsu_threshold(img)
    elif method == "canny":
        mask = canny_edge_detection(img)
    elif method == "color":
        mask = color_segmentation(img)
    else:
        raise ValueError(
            f"Unknown method: {method}. "
            f"Use 'otsu', 'canny' or 'color'."
        )
    masked_image = apply_mask_on_image(img, mask)
    return mask, masked_image


if __name__ == "__main__":
    dummy = np.random.randint(0, 255,
                              (224, 224, 3),
                              dtype=np.uint8)
    for method in ["otsu", "canny", "color"]:
        mask, masked = segment_disease_region(
                           dummy, method=method)
        print(f"Method '{method:<6}'"
              f" → mask: {mask.shape}"
              f" | masked: {masked.shape} ✅")
    print("segmentation.py working correctly!")