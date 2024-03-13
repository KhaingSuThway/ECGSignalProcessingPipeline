import numpy as np
import pandas as pd
import neurokit2 as nk

from collections import Counter

def calculate_bpm(signal,fs) -> int:
    """
    Calculate the heart rate in beats per minute (BPM) from an ECG signal.

    Parameters:
    - signal : leadI signal array
    - fs : sampling frequency

    Returns:
    - int: Heart rate in BPM.
    """
    # Extract the ECG signal and sampling frequency
    ecg_signal = signal # the leadI value is the same as portable ecg device and included with annotation     
    sampfreq = fs

    # Detect R-peaks using NeuroKit
    _, rpeaks = nk.ecg_peaks(ecg_signal, sampfreq)
    
    # Calculate the duration of the record
    duration_of_record = len(ecg_signal) / sampfreq
    
    # Calculate heart rate in BPM
    heart_rate = (len(rpeaks['ECG_R_Peaks']) * 60) / duration_of_record
    
    # Convert to integer since it is beat per minute 
    return int(heart_rate)




def scan_record(record,window_width,window_step):
    signal=record._Record__signal
    symbol=record._Record__symbol
    sample=record._Record__sample
    rhythm_annotation=record._Record__aux
    
    rhythm_keys=Counter(rhythm_annotation).keys()
    if list(rhythm_keys)==['']:
        data_within_window=scan_without_interval()
    else:
        data_within_window=scan_with_interval()
        
        
    return data_within_window
    
def scan_without_interval(record,window_width,window_step=input("bpm or second")):
    
    signal=record._Record__signal
    symbol=record._Record__symbol
    sample=record._Record__sample
    sampfreq=record._Record__sf
    
    # Initialize variables
    left_end = 0
    right_end = int(window_width * sampfreq)
    heart_rate = calculate_bpm(signal,sampfreq)
    heart_cycle = heart_rate / 60
    if window_step=='bpm':
        no_of_beats_per_step=input("Give an integer number of beats wanted to step")
        window_step = no_of_beats_per_step*(int(heart_cycle * sampfreq)) #calculate the step size of beats in samples
    else:
        window_step=window_step*sampfreq #convert the step (unit in second) in samples
 
    ecg_signals = []
    beat_annotations = []    
    beat_annotated_points = []
    count_beat_annotations = []
    pac_percentages = []
    pvc_percentages = []
    
    # Repeat parent_record and label for each segment
    parent_record_repeated = [parent_record] * len(ecg_signals)
    label_repeated = [label] * len(ecg_signals)
    heart_rate_repeated = [heart_rate] * len(ecg_signals)

    # Create the DataFrame
    data_within_window = pd.DataFrame({
        'parent_record': parent_record_repeated,
        'label': label_repeated,
        'avg_heart_rate': heart_rate_repeated,
        'signals': ecg_signals,
        'beat_annotation_symbols': beat_annotations,
        'annotated_samples': beat_annotated_points,
        'beat_occurrence': count_beat_annotations,
        'pac_percent': pac_percentages,
        'pvc_percent': pvc_percentages
    })

    print(f"There are {data_within_window.shape[0]} segments in the record.")    
    
    
    return 
    
    
    
