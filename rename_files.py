"""
This script is intended to make it easy to rename video files, which have been 
recorded as a webcam via the ATEM output, based on the label given to the test 
in the multiviewer.
"""

def main():
    # This Region of Interest can be generated using the select_roi.py script
    ROI = (1213, 472, 458, 55)
    # Change to True after checking that only the desired files will be renamed.
    RENAME_FILES = False
    # Include the path to the tesseract excecutable on your system
    ptpt.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    # Define a pattern to match the files you want to rename
    paths = glob.glob("WIN_*")
    # Modify the following function to alter the output filename format
    def label_wrapper(text):
        text = text.replace(" ", "_")
        return f"test_{text}.mp4"


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ START OF CODE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    for vidpath in paths:
        print(vidpath, end=" -> ")

        cap = cv.VideoCapture(vidpath)
        if(cap.isOpened() == False):
            raise BufferError(f"Error opening cap on {vidpath}")

        ret, frame = cap.read()
        if ret == False:
            raise BufferError(f"Error reading frame from {vidpath}")

        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        
        # Extract ROI around text to reduce processing
        label = cv.threshold(
            frame[ROI[1]:ROI[1]+ROI[3], ROI[0]:ROI[0]+ROI[2]], 
            240, 255, cv.THRESH_BINARY_INV
        )[1]
        # Perform OCR
        label_text = pt.image_to_string(
            cv.cvtColor(label, cv.COLOR_GRAY2RGB)).rstrip(" \n")

        if len(label_text) == 0:
            print("NO DESC FOUND")
        else:
            print(label_wrapper(label_text))

        cap.release()
        if RENAME_FILES:
            os.rename(vidpath, f"test_{label_text}.mp4")


if __name__ == "__main__":
    import cv2 as cv
    import pytesseract as pt
    import pytesseract.pytesseract as ptpt
    import os, glob

    main()