import os
import numpy as np
import pandas as pd
import neurokit2 as nk

from read_record import RecordReader
from scanning_window import scan_record
from transform_image import get_combined_beat_image

def process_all_records(folder_path: str, segment_type: str = None) -> None:
    """
    Process all ECG records in the specified folder, segment them, filter based on the specified type,
    and generate corresponding CSV files and combined beat images.

    Parameters:
    - folder_path (str): The path to the folder containing the ECG record files.
    - segment_type (str, optional): The type of segments to filter (e.g., 'Pure_NSR','AF','NSR','PAC','PVC').
      If None, no filtering is applied.

    Returns:
    None

    Raises:
    ValueError: If the specified folder_path does not exist or if an invalid segment_type is provided.
    """

    # Validate folder path
    if not os.path.exists(folder_path):
        raise ValueError(f"Folder path '{folder_path}' does not exist.")

    # Create the CSV folder if it doesn't exist
    csv_folder = f'D:\ECGSignalProcessingPipeline\Data_{segment_type}'
    print(csv_folder)

    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)

    # Loop through each file in the folder
    files_list = [file[:-4] for file in os.listdir(folder_path) if file.endswith('.dat')]
    
    for file in files_list:
        csv_file_path = os.path.join(csv_folder, f"{file}_{segment_type}.csv")
        # Check if the CSV file already exists
        if os.path.exists(csv_file_path):
            print(f"{file}_{segment_type}.csv file already exists in {csv_folder}")
            continue  # Skip processing if file exists

        # Read the ECG record
        record = RecordReader.read(folder_path, file, 0, 0, None)

        # Segment the ECG record
        segments = scan_record(record, window_width=30)
        if len(segments):
            # Filter segments based on the specified type        
            filtered_segments = segments[segments['true_class'] == segment_type ]
            print(f"'{segment_type}' {len(filtered_segments)} in this record {file}")
            if filtered_segments.empty:
                print(f"'{segment_type}' does not exist in file: {file}")
                continue

            # Save filtered data to CSV
            filtered_segments.to_csv(csv_file_path, index=False)

            # Clean and Transform each segment
            for i in range(len(filtered_segments)):
                signal = np.array(list(2*filtered_segments.iloc[i][:-8]))
                clean_signal = nk.ecg_clean(signal, record._Record__sf,method='pantompkins1985')
                # Generate a combined beat image
                get_combined_beat_image(signal=clean_signal,
                                        bpm=filtered_segments.iloc[i]['avg_heart_rate'],
                                        voltage_range=[-3, 3],
                                        folder_name=f'D:\ECGSignalProcessingPipeline\Image_{segment_type}',
                                        img_name=f'{file}_{segment_type}_{i}')
