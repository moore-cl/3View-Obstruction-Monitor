# 3View Detector Obstruction Watchdog

## Project Overview

This project investigates automated detection of detector obstruction events during long-duration Gatan 3View serial block-face SEM acquisitions.

The primary objective is to provide an independent monitoring system that can detect catastrophic image-quality degradation caused by detector obstruction and ultimately pause or stop an acquisition automatically before significant data loss occurs.

---

## Motivation

Long unattended 3View acquisitions can run for several days.

A known failure mode occurs when section debris obstructs the backscatter detector, leading to:

- Severe loss of image information
- Corrupted datasets
- Wasted microscope time
- Loss of valuable samples

Current monitoring relies on operator supervision.

This project aims to provide an automated watchdog capable of identifying obstruction events and taking corrective action.

---

## Initial Design Concept

Several approaches were considered:

### AI-Based Detection

Potential approaches included:

- Autoencoder anomaly detection
- CNN classification
- MONAI-based image quality assessment

These approaches remain future options.

### Statistical Detection

A simpler image-analysis approach was selected for initial development because:

- Detector obstruction produces large image changes.
- The behaviour is easier to interpret.
- Validation requirements are lower.
- The system is more transparent and easier to maintain.

---

## Current Detection Method

The current prototype uses a single image-quality metric:

### Laplacian Variance

Laplacian variance provides a measure of image texture and edge content.

Normal 3View images contain:

- High ultrastructural detail
- Strong local contrast
- Large amounts of high-frequency information

Detector-obstructed images exhibit:

- Significant loss of texture
- Reduced structural information
- Lower edge density

The watchdog computes:

```python
lap_ratio = current_laplacian / baseline_laplacian
```

where:

- current_laplacian = Laplacian variance of newest image
- baseline_laplacian = average Laplacian variance of previous 5 images

---

## Detection Logic

Trigger conditions:

```python
lap_ratio < 0.70
```

for

```python
3 consecutive images
```

Decision process:

```text
New image arrives
       ↓
Compute Laplacian variance
       ↓
Compare with rolling baseline
       ↓
lap_ratio < 0.70 ?
       ↓
Increment anomaly counter
       ↓
3 consecutive anomalies?
       ↓
STOP SCAN
```

---

## Validation Dataset

A small validation dataset was assembled consisting of:

### Normal Images

Images 1–9

Observed characteristics:

```text
Laplacian Variance

≈ 23,200 – 23,800
```

### Obstructed Images

Images 10–12

Observed characteristics:

```text
Laplacian Variance

≈ 9,300 – 9,600
```

---

## Validation Results

The obstruction images were correctly identified.

Example output:

```text
Image 10
Ratio = 0.395
ANOMALY (1/3)

Image 11
Ratio = 0.457
ANOMALY (2/3)

Image 12
Ratio = 0.535
ANOMALY (3/3)

STOP SCAN
```

The separation between normal and obstructed image classes was substantial, indicating that simple texture-based monitoring is likely sufficient for initial deployment.

---

## Current Status

### Completed

✅ Obstruction and normal image datasets collected

✅ Natural filename sorting implemented

✅ Rolling baseline calculation implemented

✅ Laplacian variance metric implemented

✅ Three-frame confirmation logic implemented

✅ Successful detection of known obstruction images

✅ Prototype simulator validated

---

## Planned Next Steps

### Stage 1

Convert simulator into live watchdog:

```text
3View Output Folder
       ↓
Watch for new image
       ↓
Evaluate image quality
       ↓
Trigger obstruction detection
```

### Stage 2

Implement automatic acquisition stop using:

```python
pywinauto
```

Actions:

- Connect to DigitalMicrograph / 3View window
- Activate software
- Press STOP button automatically

### Stage 3

Add evidence collection:

- Save triggering image
- Save screenshot
- Record timestamp
- Log detector metrics

### Stage 4

Add notifications:

- Email alert
- Teams notification
- SMS alert (optional)

### Stage 5 (Future)

Evaluate AI-based approaches:

- Autoencoder anomaly detection
- CNN classifiers
- Multi-failure classification

Potential detection categories:

- Detector obstruction
- Charging
- Focus loss
- Knife chatter
- Imaging artefacts

---

## Key Finding

Detector obstruction produced a dramatic reduction in image texture.

For the current dataset, Laplacian variance alone was sufficient to reliably distinguish normal operation from detector obstruction without requiring machine learning.

This significantly simplifies deployment and validation of an unattended watchdog system.

---
