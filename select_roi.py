"""
This script provides a GUI to select around the text labels and generate the 
ROI bounding coordinates.

The labels should be selected in the order Reference, Delayed, Description.
The labels should have some padding around them to make sure the OCR works well.

Make sure you leave enough width around the description for the longest label
in your set of videos.
"""

def main():
    VIDPATH = "test_720p50-H264-10M.mp4"


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ START OF CODE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    cap = cv.VideoCapture(VIDPATH)
    if(cap.isOpened() == False):
        raise BufferError(f"Error opening cap on {VIDPATH}")

    ret, frame = cap.read()
    if ret == False:
        raise BufferError(f"Error reading frame from {VIDPATH}")

    rois = cv.selectROIs("Select ROI around text labels", frame)
    print("Selected ROIs:")
    print(rois)
    cap.release()


if __name__ == "__main__":
    import cv2 as cv
    main()