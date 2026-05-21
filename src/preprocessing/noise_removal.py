# src/preprocessing/noise_removal.py

import cv2
import numpy as np


def gaussian_blur(img, kernel_size=(3, 3)):
    """
    Applies Gaussian blur to remove camera noise.
    kernel (3,3) is gentle — removes noise without
    destroying disease spot details.

    Input  : numpy array (H, W, 3)
    Output : numpy array (H, W, 3) smoothed
    """
    return cv2.GaussianBlur(img, kernel_size, 0)


def median_blur(img, kernel_size=3):
    """
    Applies Median blur — best for salt-and-pepper
    noise (random black/white pixels).
    Good for low quality field photos.

    Input  : numpy array (H, W, 3)
    Output : numpy array (H, W, 3) cleaned
    """
    return cv2.medianBlur(img, kernel_size)


def remove_noise(img, method="gaussian"):
    """
    Main noise removal function.

    method = "gaussian" → Gaussian blur (default)
    method = "median"   → Median blur
    method = "both"     → Gaussian then Median

    Input  : numpy array (H, W, 3)
    Output : numpy array (H, W, 3) denoised
    """
    if method == "gaussian":
        return gaussian_blur(img)
    elif method == "median":
        return median_blur(img)
    elif method == "both":
        img = gaussian_blur(img)
        img = median_blur(img)
        return img
    else:
        raise ValueError(
            f"Unknown method: {method}. "
            f"Use 'gaussian', 'median' or 'both'."
        )


if __name__ == "__main__":
    dummy = np.random.randint(0, 255,
                              (224, 224, 3),
                              dtype=np.uint8)
    for method in ["gaussian", "median", "both"]:
        result = remove_noise(dummy, method=method)
        print(f"Method '{method:<8}'"
              f" → shape: {result.shape} ✅")
    print("noise_removal.py working correctly!")