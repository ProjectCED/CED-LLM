import pytest
import os
from app.utils import extract_text_from_file
from unittest.mock import patch, MagicMock
from pypdf import PdfReader

pytestmark = pytest.mark.utils

@pytest.fixture
def create_text_file(tmp_path):
    """
    Fixture to create a sample .txt file with predefined content.

    Parameters:
        tmp_path (Path): Pytest's temporary path for file creation.

    Returns:
        Path: Path to the created .txt file containing "This is a sample text file."
    """
    file = tmp_path / "sample.txt"
    file.write_text("This is a sample text file.")
    return file

@pytest.fixture
def create_empty_text_file(tmp_path):
    """
    Fixture to create an empty .txt file.

    Parameters:
        tmp_path (Path): Pytest's temporary path for file creation.

    Returns:
        Path: Path to the created empty .txt file.
    """
    file = tmp_path / "empty.txt"
    file.write_text("")
    return file

def test_extract_text_from_txt_file(create_text_file):
    """
    Tests extract_text_from_file for .txt files containing text.

    Verifies that the function correctly extracts text from a valid .txt file.
    """
    result = extract_text_from_file(str(create_text_file))
    assert result == "This is a sample text file."

def test_extract_text_from_empty_file(create_empty_text_file):
    """
    Tests extract_text_from_file for empty .txt files.

    Verifies that the function returns None for an empty file.
    """
    result = extract_text_from_file(str(create_empty_text_file))
    assert result is None

def test_extract_text_from_nonexistent_file():
    """
    Tests extract_text_from_file for nonexistent files.

    Verifies that the function returns None when the specified file does not exist.
    """
    result = extract_text_from_file("nonexistent_file.txt")
    assert result is None

def test_extract_text_with_invalid_extension(tmp_path):
    """
    Tests extract_text_from_file for unsupported file types.

    Verifies that the function returns None when the file has an unsupported extension.
    """
    file = tmp_path / "file.docx"
    file.write_text("This is a DOCX file.")
    result = extract_text_from_file(str(file))
    assert result is None

def test_extract_text_from_pdf_file():
    """
    Tests the extract_text_from_file function for .pdf files by mocking PyMuPDF and os.path.isfile.

    Purpose:
        Verifies that the function correctly extracts text from a .pdf file without relying on
        actual files or the PyMuPDF library.

    Test Strategy:
        - Mock os.path.isfile to simulate the existence of a file.
        - Mock pymupdf.open to simulate opening and reading a PDF file.
        - Simulate PDF document iteration using a MagicMock to return predefined text from a page.
        - Ensure the function correctly:
          1. Calls pymupdf.open with the provided file path.
          2. Reads text from the mocked PDF document.
          3. Returns the extracted text.

    Assertions:
        - `mock_extra_check.assert_called_once_with("mocked_file.pdf")`:
            Ensures pymupdf.open is called exactly once with the correct file path.
        - `mock_file.__enter__.assert_called_once()`:
            Ensures the mocked document's context manager methods are called correctly.
        - `assert result == expected_text`:
            Validates that the function returns the expected text.

    Mocks:
        - `os.path.isfile`: Always returns True to simulate that the file exists.
        - `pymupdf.open`: Returns a mock object representing the PDF document.

    Notes:
        This test ensures no real files or PyMuPDF functionalities are invoked.

    """
    expected_text = "This is a sample PDF file."
    # mock text
    mock_page = MagicMock()
    mock_page.get_text.return_value = expected_text
    # mock file
    mock_file = MagicMock()
    mock_file.__enter__.return_value = [mock_page] # Simulate that iterating over the document returns the mock page
    mock_file.__exit__.return_value = None # Simulate proper exit behavior

    # Mock pymupdf.open() to return a mock document object that behaves like a context manager
    with patch("pymupdf.open", return_value=mock_file) as mock_extra_check:
        # Mock os.path.isfile to return True, simulating that the file exists
        with patch("os.path.isfile", return_value=True):
            
            result = extract_text_from_file("mocked_file.pdf")

            mock_extra_check.assert_called_once_with("mocked_file.pdf") # Ensure pymupdf.open was called correctly
            mock_file.__enter__.assert_called_once() # Ensure __enter__ was called on the mock document
            assert result == expected_text
