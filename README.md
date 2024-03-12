## ECG Signal Processing Pipeline

This repository houses code for preprocessing ECG signals, including cleaning, segmentation, and transformation into images. These processed ECG images can then be fed into custom networks or systems for in-depth analysis, classification, or prediction.

## Processing Steps

```mermaid
graph LR
    A[Scan the given record] --> B[Segment the record]
    B --> C[Clean the segmented ECG data]
    C --> D[Transform to image]