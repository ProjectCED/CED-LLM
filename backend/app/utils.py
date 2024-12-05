import pymupdf
import os.path

"""
Various utility functions used in the backend.
"""

def extract_text_from_file(filepath: str) -> str:
    """
    Extracts text from a given file. Supports PDF and txt files.

    Args:
        filepath (string): Absolute path to the file to extract text from.

    Returns:
        string: Extracted text from the file.
            Can be None if the file is not found or no text was extracted (empty file).
            Strips the end of the text to remove unnecessary whitespace.
    """
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