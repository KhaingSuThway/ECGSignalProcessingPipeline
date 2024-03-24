## ECG Signal Processing Pipeline

This repository houses code for preprocessing ECG signals, including cleaning, segmentation, and transformation into images. These processed ECG images can then be fed into custom networks or systems for in-depth analysis, classification, or prediction.

## Processing Steps
```mermaid
graph LR
    A[Scan the given record] --> B[Segment the record]
    B --> C[Clean the segmented ECG data]
    C --> D[Transform to image]
```
-Scan the given record: Input the ECG signal, window width, and window step to scan the record.

-Segment the record: Divide the scanned record into desired segments.

-Clean the segmented ECG data: Remove noise and artifacts from the segmented ECG.

-Transform to image: Convert the cleaned ECG segments into the desired image format.

### Getting Started
**1.Clone the Repository**
```
git clone https://github.com/KhaingSuThway/ECGSignalProcessingPipeline.git
cd ECGSignalProcessing

```

**2.Create a Virtual Environment** (optional but recommended)
``` 
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**3.Install Dependencies**
```
pip install -r requirements.txt
```


## Overview

### read_record.py
`read_record.py` is a Python module for reading ECG (Electrocardiogram) records in WFDB (Waveform Database) format. It provides functionality to read ECG signals, annotations, sample indices, comments, and sampling frequency from WFDB records and represents them as `Record` objects.

## Features
- Reads ECG records from WFDB format.
- Extracts ECG signals, annotations, sample indices, comments, and sampling frequency.
- Provides a `Record` class to represent ECG records.

## Usage
```python
from read_record import RecordReader

# Specify path to record directory, record name, channel, sample range
record = RecordReader.read(path='path/to/records', number='record_name', channel=0, sampfrom=0, sampto=1000)

# Access record attributes
print(record['parent'])  # Print parent of the record
print(record['label'])   # Print label or comment associated with the record
# Access other attributes similarly
```

### scanning_window.py

`scanning_window.py` is a Python module for analyzing ECG records by scanning through specified windows. It provides functions to calculate heart rate from ECG signals and scan through ECG records with or without rhythm intervals.

## Features
- Calculates heart rate from ECG signals.
- Scans ECG records within specified windows.
- Identifies different types of beats (e.g., AF, NSR, PAC, PVC) within each window.
- Determines the true class of each segment based on beat annotations and percentages.

## Usage
```python
from scanning_window import calculate_bpm, scan_record

# Calculate heart rate from ECG signal
heart_rate = calculate_bpm(signal, sampfreq)

# Scan ECG record within specified window
window_width = 5  # seconds
window_step = 1  # seconds
data_within_window = scan_record(record, window_width, window_step)
```