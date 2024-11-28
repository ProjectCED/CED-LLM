import pytest
import os
from app.utils import extract_text_from_file
from unittest.mock import patch, MagicMock
from PyPDF2 import PdfReader


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


"""def test_extract_text_from_pdf_file(create_pdf_file):
    result = extract_text_from_file(str(create_pdf_file))
    assert result == "This is a sample PDF file."
"""

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


"""def test_extract_text_from_pdf_file():
    expected_text = "This is a sample PDF file."

    # Mockataan os.path.isfile palauttamaan True
    with patch("os.path.isfile", return_value=True):
        # Mockataan utils.pymupdf.open
        with patch("app.utils.pymupdf.open") as mock_open:
            # Luo mock-dokumentti ja -sivu
            mock_file = MagicMock()
            mock_page = MagicMock()
            mock_page.get_text.return_value = expected_text  # Simuloidaan tekstin lukeminen PDF:stä
            mock_file.__iter__.return_value = [mock_page]  # Simuloidaan PDF:n iterointi
            mock_open.return_value = mock_file  # Mockataan avattavan tiedoston palauttama dokumentti

            # Kutsu testattavaa funktiota
            result = extract_text_from_file("mocked_file.pdf")

            # Tarkista, että funktio palauttaa oikean tekstin
            assert result == expected_text
"""

