import pytest
import os
import openai
from unittest.mock import patch, MagicMock
from app.api_handler import ApiHandler, PRIMARY_MODEL, BACKUP_MODEL

@pytest.fixture
def api_handler():
     #Fixture to create an ApiHandler instance.
     return ApiHandler()

@patch("app.api_handler.openai.OpenAI") # replace real OpenAI with mock one
@patch.object(ApiHandler, "__init__", lambda x: None)  # Mock __init__ to skip it
def test_analyze_text_primary_model(mock_openai):
    # Create a mock response with the desired return value
    mock_response = MagicMock()

    # Set up the mock response structure to match the OpenAI API response
    mock_message = MagicMock()
    mock_message.content = "Analyzed text result."

    mock_response.choices = [MagicMock(message=mock_message)]

    mock_openai.return_value.chat.completions.create.return_value = mock_response
    api_handler = ApiHandler()
    api_handler._ApiHandler__client = mock_openai.return_value ## mock __client variable
    
    result = api_handler.analyze_text("Sample text")
    assert result == "Analyzed text result."

@patch("app.api_handler.utils.extract_text_from_file")
def test_analyze_file_with_no_text(mock_extract_text, api_handler):
     # Simulate no text extracted from the file
     mock_extract_text.return_value = None

     result = api_handler.analyze_file("empty.txt")
     assert result is None
     mock_extract_text.assert_called_once_with("empty.txt")
