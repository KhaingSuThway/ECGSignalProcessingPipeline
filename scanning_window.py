import numpy as np
import pandas as pd
import neurokit2 as nk
from collections import Counter
from sys import stdin, stdout

def calculate_bpm(signal, sampfreq) -> int:
    """
    Calculate the heart rate in beats per minute (BPM) from an ECG signal.

    Parameters:
    - signal : leadI signal array
    - sampfreq : sampling frequency

    Returns:
    - int: Heart rate in BPM.
    """
    ecg_signal = signal
    sampfreq = sampfreq

    _, rpeaks = nk.ecg_peaks(ecg_signal, sampfreq)

    duration_of_record = len(ecg_signal) / sampfreq

    heart_rate = (len(rpeaks['ECG_R_Peaks']) * 60) / duration_of_record

    return int(heart_rate)

def scan_record(record, window_width, window_step=None):
    # signal = record._Record__signal
    # symbol = record._Record__symbol
    # sample = record._Record__sample
    rhythm_annotation = record._Record__aux

    rhythm_keys = Counter(rhythm_annotation).keys()

    if list(rhythm_keys) == ['']:
        data_within_window = scan_without_interval(record=record,
                                                   window_width=window_width,
                                                   )
    else:
        print(f"There's rhythm annotation. {rhythm_keys}")
        data_within_window=scan_with_interval(record=record,window_width=window_width)
        

    return data_within_window

def scan_without_interval(record, window_width):
    signal = record._Record__signal
    symbol = record._Record__symbol
    sample = record._Record__sample
    sampfreq = record._Record__sf

    left_end = 0
    right_end = int(window_width * sampfreq)
    heart_rate = calculate_bpm(signal, sampfreq)
    heart_cycle = heart_rate / 60
    types_of_step = input("Choose 'bpm' or 'sec': ")
    no_of_beats_per_step = int(input("Give number of steps: "))

    if types_of_step == 'bpm':
        window_step = int((no_of_beats_per_step * heart_cycle) * sampfreq)
    elif types_of_step == 'sec':
        window_step = int(no_of_beats_per_step * sampfreq)

    ecg_signals = []
    beat_annotations = []
    beat_annotated_points = []
    pac_percentages = []
    pvc_percentages = []
    true_class = []

    while right_end <= len(signal):  
        print("left_end:", left_end)
        print("right_end:", right_end)
        print("window_width:", window_width)
      
        signal_within_window = signal[left_end:right_end]
        ecg_signals.append(signal_within_window)

        annotated_index = np.intersect1d(np.where(left_end <= sample),
                                            np.where(right_end >= sample))
        symbol_within_window = [symbol[i] for i in annotated_index]
        beat_annotations.append(symbol_within_window)

        sample_within_window = [sample[i] - left_end for i in annotated_index]
        beat_annotated_points.append(sample_within_window)

        beats, count = np.unique(symbol_within_window, return_counts=True)
        segment_beat_annotation_count = dict(zip(beats, count))
        total_count = sum(segment_beat_annotation_count.values())

        pac_percentage = segment_beat_annotation_count.get('A', 0) / total_count * 100
        pac_percentages.append(pac_percentage)
        pvc_percentage = segment_beat_annotation_count.get('V', 0) / total_count * 100
        pvc_percentages.append(pvc_percentage)

        
        if is_NSR(record._Record__label, pac_percentage, pvc_percentage):
            true_class.append('NSR')
        elif is_PAC(record._Record__label, pac_percentage, pvc_percentage):
            true_class.append('PAC')
        elif is_PVC(record._Record__label, pac_percentage, pvc_percentage):
            true_class.append('PVC')
        elif is_AF(record._Record__label, pac_percentage, pvc_percentage):
            true_class.append('AF')
        else:
            true_class.append('Others')

        left_end += window_step
        right_end = left_end + int(window_width * sampfreq)
        

    parent_record_repeated = [record._Record__parent] * len(ecg_signals)
    label_repeated = [record._Record__label] * len(ecg_signals)
    heart_rate_repeated = [heart_rate] * len(ecg_signals)

    data_within_window = pd.DataFrame({'parent_record': parent_record_repeated,
                                       'signals': ecg_signals,
                                       'beat_annotation_symbols': beat_annotations,
                                       'annotated_samples': beat_annotated_points,
                                       'pac_percent': pac_percentages,
                                       'pvc_percent': pvc_percentages,
                                       'avg_heart_rate': heart_rate_repeated,
                                       'label': label_repeated,
                                       'true_class': true_class})

    print(f"There are {data_within_window.shape[0]} segments in the record.")

    return data_within_window


def is_AF(label, pac_percentage, pvc_percentage):
    return label != 'non atrial fibrillation' and pac_percentage == 0 and pvc_percentage == 0

def is_NSR(label, pac_percentage, pvc_percentage):
    return label == 'non atrial fibrillation' and pac_percentage == 0 and pvc_percentage == 0

def is_PAC(label, pac_percentage, pvc_percentage):
    return label == 'non atrial fibrillation' and pac_percentage >= 20 and pvc_percentage == 0

def is_PVC(label, pac_percentage, pvc_percentage):
    return label == 'non atrial fibrillation' and pac_percentage == 0 and pvc_percentage >= 20


def scan_with_interval(record,window_width):
    
    
    sampfreq = record._Record__sf
    
    heart_rate = calculate_bpm(signal, sampfreq)
    heart_cycle = heart_rate / 60
    types_of_step = input("Choose 'bpm' or 'sec': ")
    no_of_beats_per_step = int(input("Give number of steps: "))

    if types_of_step == 'bpm':
        window_step = int((no_of_beats_per_step * heart_cycle) * sampfreq)
    elif types_of_step == 'sec':
        window_step = int(no_of_beats_per_step * sampfreq)

    ecg_signals = []
    beat_annotations = []
    beat_annotated_points = []
    pac_percentages = []
    pvc_percentages = []
    true_class = []
    
    valid_interval=record.get_valid_rhythm_interval(duration=window_width)
    signal = record._Record__signal[valid_interval[0][0]:valid_interval[]]
    symbol = record._Record__symbol
    sample = record._Record__sample
    
    left_end=valid_interval[0][0]
    right_end=window_width*record._Record__sf
    
    while right_end <= valid_interval[0][1]:  
        print("left_end:", left_end)
        print("right_end:", right_end)
        print("window_width:", window_width)
    
        signal_within_window = signal[left_end:right_end]
        ecg_signals.append(signal_within_window)

        annotated_index = np.intersect1d(np.where(left_end <= sample),
                                            np.where(right_end >= sample))
        symbol_within_window = [symbol[i] for i in annotated_index]
        beat_annotations.append(symbol_within_window)

        sample_within_window = [sample[i] - left_end for i in annotated_index]
        beat_annotated_points.append(sample_within_window)

        beats, count = np.unique(symbol_within_window, return_counts=True)
        segment_beat_annotation_count = dict(zip(beats, count))
        total_count = sum(segment_beat_annotation_count.values())

        pac_percentage = segment_beat_annotation_count.get('A', 0) / total_count * 100
        pac_percentages.append(pac_percentage)
        pvc_percentage = segment_beat_annotation_count.get('V', 0) / total_count * 100
        pvc_percentages.append(pvc_percentage)

        
        if is_NSR(record._Record__label, pac_percentage, pvc_percentage):
            true_class.append('NSR')
        elif is_PAC(record._Record__label, pac_percentage, pvc_percentage):
            true_class.append('PAC')
        elif is_PVC(record._Record__label, pac_percentage, pvc_percentage):
            true_class.append('PVC')
        elif is_AF(record._Record__label, pac_percentage, pvc_percentage):
            true_class.append('AF')
        else:
            true_class.append('Others')

        left_end += window_step
        right_end = left_end + int(window_width * sampfreq)
        

    parent_record_repeated = [record._Record__parent] * len(ecg_signals)
    label_repeated = [record._Record__label] * len(ecg_signals)
    heart_rate_repeated = [heart_rate] * len(ecg_signals)

    data_within_window = pd.DataFrame({'parent_record': parent_record_repeated,
                                    'signals': ecg_signals,
                                    'beat_annotation_symbols': beat_annotations,
                                    'annotated_samples': beat_annotated_points,
                                    'pac_percent': pac_percentages,
                                    'pvc_percent': pvc_percentages,
                                    'avg_heart_rate': heart_rate_repeated,
                                    'label': label_repeated,
                                    'true_class': true_class})

    print(f"There are {data_within_window.shape[0]} segments in the record.")

    return data_within_window
        
        
    
    