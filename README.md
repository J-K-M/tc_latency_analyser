# Timecode video latency analyser
The set of scripts in this repository are designed to make extracting latency values from video recordings easy.


## Installation
These scripts depend on pytesseract to perform the OCR processing.
pytesseract in turn depends on Google's Tesseract-OCR Engine.
Installation instructions can be found at: https://tesseract-ocr.github.io/tessdoc/Installation.html

All other dependencies can be installed with pipenv.


## Test Methodology
A video signal with a TimeCode overlay should be generated and sent to both a multiviewer and the system under test.
The video output of the system under test should be sent to another pane of the multiviewer.
A description of the test parameters should be visible as a text label on the output.
The multiviewer output should then be recorded and the files placed in the same directory as these scripts.

+--------+    +-------+    +-----------+    +--------+
| TC Gen |--->| Split |--->| MultiView |--->| Record |
+--------+    +-------+    +-----------+    +--------+
                  |             ^
                  |    +-----+  |
                  \--->| SUT |--/
                       +-----+


## Usage
Once the files have been recorded and moved they can be automatically renamed using the ```rename_files.py``` script.
After renaming, the  ```select_roi.py``` script should be run to select the areas within the recorded files that the 
TimeCode labels and test description label are located.
Make sure to give some padding around the selections to ensure the OCR processing works.
The selected ROIs can then be copied into the ROIs list in the ```process_frames.py``` script.
Finally, the ```process_frames.py``` script can be run (This can take quite a long time).

All of these scripts have some parameters at the top of their respective main functions which should be checked to ensure
that they are suitable for your particular use.


Two example files and a CSV output are provided in this repo to help you test that the code is working.