import os
from pathlib import Path
import time
import sys
import concurrent.futures
import pikepdf
from tkinter import Tk
from tkinter.filedialog import askdirectory
from tqdm import tqdm

# DEFINE FUNCTIONS HERE

def SingleUnlock(filename):
    with pikepdf.open(filename,
                      allow_overwriting_input=True) as pdf:
        pdf.save(filename)

def BatchUnlock(PDFList, NumberOfFiles):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        list(tqdm(executor.map(SingleUnlock, PDFList, chunksize=3), total=NumberOfFiles))

# SCRIPT SECTION

if __name__ == "__main__":
    ClickedOnFolder = " ".join(sys.argv[1:])
    PDFList = []

    if ClickedOnFolder == "":
        Tk().withdraw()
        PDFDirectory = askdirectory()
    else:
        PDFDirectory = ClickedOnFolder

    PDFDirectory = os.path.normpath(PDFDirectory)
    
    start = time.time()
    
    for root, dirs, files in os.walk(PDFDirectory):
        if 'Converted' in dirs:
            dirs.remove('Converted')
        for x in files:
            if x.lower().endswith('.pdf'):
                PDFList.append(os.path.join(root,x))

    NumberOfFiles = len(PDFList)

    if NumberOfFiles == 0:
        print("No PDF files found in directory")
    else:
        print(f"""
            Attempting to unlock {NumberOfFiles} PDF files\n
            """)

        BatchUnlock(PDFList, NumberOfFiles)

        end = time.time()

        print(f"""
            Done! Unlocked {NumberOfFiles} PDF files in {round(end-start,2)} seconds.\n
            Processed at a rate of {round(round(end-start, 2)/NumberOfFiles, 3)} seconds per file {round(NumberOfFiles/round(end-start, 2), 3)} or files per second
            """)

    time.sleep(2)