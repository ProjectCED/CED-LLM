import pymupdf
import os.path

def extract_text_from_file(filepath: str) -> str:
    if not os.path.isfile(filepath):
        return None
    
    text = ""

    # .pdf extraction
    if filepath.endswith(".pdf"):
        with pymupdf.open(filepath) as file:
            for page in file:
                text += page.get_text()

    # .txt extraction
    elif filepath.endswith(".txt"):
        with open(filepath, "r") as file:
            text = file.read()

    # Empty check to return None if no text was extracted
    text = text.strip()
    if text == "":
        return None
    return text