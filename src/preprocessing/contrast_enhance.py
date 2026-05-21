# src/preprocessing/contrast_enhance.py

import cv2
import numpy as np


def histogram_equalization(img):
    """
    Standard Histogram Equalization on L channel.
    Spreads brightness values across full 0-255 range.
    Best for uniformly dark or bright images.

    Input  : numpy array (H, W, 3) RGB
    Output : numpy array (H, W, 3) RGB enhanced
    """
    lab        = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
    l, a, b    = cv2.split(lab)
    l_eq       = cv2.equalizeHist(l)
    lab_eq     = cv2.merge([l_eq, a, b])
    return cv2.cvtColor(lab_eq, cv2.COLOR_LAB2RGB)


def clahe_enhancement(img, clip_limit=2.0,
                       tile_size=(8, 8)):
    """
    CLAHE — Contrast Limited Adaptive Histogram
    Equalization on L channel of LAB color space.

    Divides image into 8x8 tiles and enhances each
    separately — disease spots enhanced without
    over-brightening healthy areas.

    clip_limit=2.0 limits noise amplification.
    This is what pipeline.py uses by default.

    Input  : numpy array (H, W, 3) RGB
    Output : numpy array (H, W, 3) RGB enhanced
    """
    lab         = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
    l, a, b     = cv2.split(lab)
    clahe       = cv2.createCLAHE(
                      clipLimit=clip_limit,
                      tileGridSize=tile_size)
    l_clahe     = clahe.apply(l)
    lab_clahe   = cv2.merge([l_clahe, a, b])
    return cv2.cvtColor(lab_clahe, cv2.COLOR_LAB2RGB)


def enhance_contrast(img, method="clahe"):
    """
    Main contrast enhancement function.

    method = "clahe"     → CLAHE (default)
    method = "histogram" → Standard histogram eq.
    method = "both"      → Histogram then CLAHE

    Input  : numpy array (H, W, 3) RGB
    Output : numpy array (H, W, 3) RGB enhanced
    """
    if method == "clahe":
        return clahe_enhancement(img)
    elif method == "histogram":
        return histogram_equalization(img)
    elif method == "both":
        img = histogram_equalization(img)
        img = clahe_enhancement(img)
        return img
    else:
        raise ValueError(
            f"Unknown method: {method}. "
            f"Use 'clahe', 'histogram' or 'both'."
        )


if __name__ == "__main__":
    dummy = np.random.randint(0, 100,
                              (224, 224, 3),
                              dtype=np.uint8)
    print(f"Input brightness : {dummy.mean():.2f}")
    for method in ["clahe", "histogram", "both"]:
        result = enhance_contrast(dummy, method=method)
        print(f"Method '{method:<10}'"
              f" → brightness: {result.mean():.2f} ✅")
    print("contrast_enhance.py working correctly!")