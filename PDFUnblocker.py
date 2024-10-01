import os
import time
import sys
import concurrent.futures
import pikepdf
from tkinter import Tk
from tkinter.filedialog import askdirectory
from tqdm import tqdm

# DEFINE FUNCTIONS HERE

def SingleUnlock(filename: str) -> None:
    try:
        with pikepdf.open(filename,
                        allow_overwriting_input=True) as pdf:
            pdf.save(filename)
    except pikepdf.PasswordError:
        print(f"The file {filename} appears to be unable to be de-encrypted.")
    except pikepdf.PasswordError:
        print(f"The file {filename} appears to be unable to be de-encrypted.")
    except pikepdf.PdfError as e:
        print(f"An unexpected error occurred with {filename}: {e!s}")


def BatchUnlock(PDFList: list[str], NumberOfFiles: int) -> None:
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
    
    if not os.path.isdir(PDFDirectory):
        print(f"I regret to inform you that '{PDFDirectory}' is not a valid directory. Do try again, won't you?")
        sys.exit(1)

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
        duration = end - start

        print(f"""
            We've successfully unlocked {NumberOfFiles} PDF files in {duration:.2f} seconds.
            That's a rate of {duration/NumberOfFiles:.3f} seconds per file, or if you prefer,
            {NumberOfFiles/duration:.3f} files per second.
            """)

    time.sleep(2)