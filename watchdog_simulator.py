import cv2
import numpy as np
import re
from pathlib import Path

# =====================================================
# CONFIGURATION
# =====================================================

IMAGE_FOLDER = r"C:\Users\Chad\Desktop\watchdog_test"

BASELINE_WINDOW = 5

LAPLACIAN_THRESHOLD = 0.70

CONSECUTIVE_FAILURES = 3

# =====================================================
# FUNCTIONS
# =====================================================

def natural_sort_key(path):
    """
    Sort filenames numerically:

    image_1.png
    image_2.png
    image_10.png

    instead of alphabetically.
    """
    return [
        int(text) if text.isdigit() else text.lower()
        for text in re.split(r'(\d+)', path.name)
    ]


def load_image(path):
    image = cv2.imread(
        str(path),
        cv2.IMREAD_GRAYSCALE
    )

    if image is None:
        raise RuntimeError(
            f"Could not read image: {path}"
        )

    return image


def laplacian_variance(image):
    return cv2.Laplacian(
        image,
        cv2.CV_64F
    ).var()


# =====================================================
# MAIN
# =====================================================

def main():

    image_files = []

    for ext in (
        "*.png",
        "*.jpg",
        "*.jpeg",
        "*.tif",
        "*.tiff"
    ):
        image_files.extend(
            Path(IMAGE_FOLDER).glob(ext)
        )

    image_files = sorted(
        image_files,
        key=natural_sort_key
    )

    print()
    print("=" * 60)
    print("IMAGE ORDER")
    print("=" * 60)

    for f in image_files:
        print(f.name)

    print()
    print("=" * 60)
    print(f"Found {len(image_files)} images")
    print("=" * 60)

    if len(image_files) < BASELINE_WINDOW + 1:
        print(
            f"\nNeed at least {BASELINE_WINDOW + 1} images."
        )
        return

    lap_history = []

    anomaly_count = 0

    for i, image_path in enumerate(image_files):

        image = load_image(image_path)

        current_lap = laplacian_variance(image)

        lap_history.append(current_lap)

        print()
        print("-" * 60)
        print(f"Image {i + 1}: {image_path.name}")

        # Build initial baseline

        if len(lap_history) <= BASELINE_WINDOW:

            print("Building baseline...")
            print(f"Laplacian = {current_lap:.2f}")

            continue

        # Rolling baseline using previous 5 images

        baseline_lap = np.mean(
            lap_history[-(BASELINE_WINDOW + 1):-1]
        )

        lap_ratio = current_lap / baseline_lap

        print(f"Laplacian Current : {current_lap:.2f}")
        print(f"Laplacian Baseline: {baseline_lap:.2f}")
        print(f"Laplacian Ratio   : {lap_ratio:.3f}")
        print(f"Threshold         : {LAPLACIAN_THRESHOLD:.3f}")

        # Detection

        if lap_ratio < LAPLACIAN_THRESHOLD:

            anomaly_count += 1

            print()
            print(
                f"ANOMALY "
                f"({anomaly_count}/"
                f"{CONSECUTIVE_FAILURES})"
            )

        else:

            anomaly_count = 0

            print()
            print("NORMAL")

        # Stop condition

        if anomaly_count >= CONSECUTIVE_FAILURES:

            print()
            print("=" * 60)
            print("STOP SCAN")
            print("=" * 60)

            break

    print()
    print("Finished.")


if __name__ == "__main__":
    main()