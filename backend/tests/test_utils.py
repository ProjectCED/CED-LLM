import pytest
import os
from app.utils import extract_text_from_file
from unittest.mock import patch, MagicMock
from pypdf import PdfReader


@pytest.fixture
def create_text_file(tmp_path):
    """Fixture to create a sample .txt file."""
    file = tmp_path / "sample.txt"
    file.write_text("This is a sample text file.")
    return file

@pytest.fixture
def create_empty_text_file(tmp_path):
    """Fixture to create an empty .txt file."""
    file = tmp_path / "empty.txt"
    file.write_text("")
    return file

def test_extract_text_from_txt_file(create_text_file):
    result = extract_text_from_file(str(create_text_file))
    assert result == "This is a sample text file."

def test_extract_text_from_empty_file(create_empty_text_file):
    result = extract_text_from_file(str(create_empty_text_file))
    assert result is None

def test_extract_text_from_nonexistent_file():
    result = extract_text_from_file("nonexistent_file.txt")
    assert result is None

def test_extract_text_with_invalid_extension(tmp_path):
    file = tmp_path / "file.docx"
    file.write_text("This is a DOCX file.")
    result = extract_text_from_file(str(file))
    assert result is None

def test_extract_text_from_pdf_file():
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
