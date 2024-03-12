## ECG Signal Processing Pipeline

This repository houses code for preprocessing ECG signals, including cleaning, segmentation, and transformation into images. These processed ECG images can then be fed into custom networks or systems for in-depth analysis, classification, or prediction.

## Processing Steps

```mermaid
graph TD
    A[Segment ECG Record] --> B[Clean Noise]
    B --> C[Transform to Image]
'''