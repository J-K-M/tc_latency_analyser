"""
This script uses Optical Character Recognition to automatically calculate 
latency through a video system and export the results to a CSV file.

The selected video clips are processed in parallel but the OCR processing is 
still quite slow. It's best to set the script running and go for a break :)

Because different video resolutions place the timecode in a different location
with a different size, you must define a Region of Interest (a bounding box
around the text labels) for each scale. 
These ROIs can be generated using the select_roi.py script.

The loading bars shown while the script is running are a little buggy, but 
still give a reasonable indication of progress.
"""

from glob import glob
from multiprocessing import Pool, current_process
from tqdm import tqdm

import cv2 as cv
import pandas as pd
import pytesseract as pt

def main():
    # Include the path to the tesseract excecutable on your system
    tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    # This is the FPS of the timecode, not the recording
    VID_FPS = 50
    # Filename for CSV output file containing results
    csv_path = "full_results.csv"
    # Define a pattern to match the files you want to analyse
    paths = glob("test_*")
    # Define an ROI for each different video scale
    ROIs = [
        [ # Large ROIs
            ( 217, 326, 527, 110), # reference
            (1176, 327, 528, 109), # delayed
            (1213, 472, 458,  55), # description
        ],
        [ # Small ROIs
            ( 302, 398, 356,  68), # reference
            (1270, 399, 341,  64), # delayed
            (1258, 474, 367,  52), # description
        ],
    ]



    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ START OF CODE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    label_len = max([len(x) for x in paths]) # Used for progress bar formatting

    pool = Pool()
    workers = [
        pool.apply_async(
            process_file,
            args=(p, label_len, VID_FPS, tesseract_cmd, [roi for roi in ROIs])
        ) for p in paths
    ]

    pool.close()
    pool.join()

    # --- Print results and export CSV ---
    full_results = [pd.DataFrame(w.get()) for w in workers]
    df = pd.concat(full_results, axis=1)
    df.to_csv(csv_path, header=True, index_label="frame_number")

    print("\033[J") # Clear console from cursor down
    print(df.head(5))

    shortest_file_len = max([len(x) for x in full_results])
    shortest_file = None
    for x in full_results:
        if len(x) < shortest_file_len:
            shortest_file_len = len(x)
            shortest_file = x.columns[0]
    print(f"shortest file: {shortest_file} - {shortest_file_len} frames")


def process_file(vidpath, label_len, fps, tesseract_cmd, roi_list):
        pt.pytesseract.tesseract_cmd = tesseract_cmd

        # Open file to be processed
        cap = cv.VideoCapture(vidpath)
        if(cap.isOpened() == False):
            raise BufferError("Error opening video stream or file")

        # Read first frame to establish which ROI to use and extract test description text
        ret, frame = cap.read()
        if ret == True:
            frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

            selected_ROIs = None
            for roi in roi_list:
                try:
                    ref = extract_roi(frame, roi[0])
                    ref_text = get_text(ref)
                    ref_values = [int(x) for x in ref_text.split(":")] # <- will fail if text can't be parsed
                    selected_ROIs = roi                                  # <- causing this line to not happen
                except ValueError:
                    continue
            
            if selected_ROIs is None:
                raise ValueError("None of the provided ROIs contained readable text")

        # Loop through remaining frames and use selected ROI to extract text
        # tqdm is used to print a progress bar for each process
        results = [] # List to add result from each frame to
        videolen = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
        for f_num in tqdm(range(videolen-1), desc=f"{vidpath:{label_len}}", position=current_process()._identity[0]):
            if cap.isOpened() == False:
                break

            ret, frame = cap.read()
            if ret == False:
                break

            frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            
            ref, delay = extract_roi(frame, selected_ROIs[0]), extract_roi(frame, selected_ROIs[1])
            ref_text, delay_text = get_text(ref), get_text(delay)

            try:
                ref_values = [int(x) for x in ref_text.split(":")]
                delay_values = [int(x) for x in delay_text.split(":")]

                latency = (ref_values[2] - delay_values[2]) * fps + ref_values[3] - delay_values[3]
                if latency >= 0:
                    # Don't include negative latency values as this indicates an error in OCR processing
                    results.append(latency)
            except ValueError:
                # If the text extracted from the frame cannot be cast to int()
                continue # This will skip a single frame, break would skip the entire file.

        return {vidpath: results}


def get_text(img):
    return pt.image_to_string(cv.cvtColor(img, cv.COLOR_GRAY2RGB)).removesuffix("\n")

def extract_roi(frame, roi):
    return cv.threshold(
        frame[roi[1]:roi[1]+roi[3], roi[0]:roi[0]+roi[2]], 
        240, 255, cv.THRESH_BINARY_INV
    )[1]



if __name__ == "__main__":
    main()