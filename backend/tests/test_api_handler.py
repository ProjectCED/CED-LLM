import pytest
import os
import openai
from unittest.mock import patch, MagicMock
from app.api_handler import ApiHandler, PRIMARY_MODEL, BACKUP_MODEL

pytestmark = pytest.mark.api_llm

@pytest.fixture(scope="module")
def api_handler():
     """
     Fixture to create an instance of the ApiHandler class.

     Returns:
        ApiHandler: An instance of the ApiHandler class used for testing.
     """
     return ApiHandler()

@patch("app.api_handler.openai.OpenAI") # replace real OpenAI with mock one
@patch.object(ApiHandler, "__init__", lambda x: None)  # Mock __init__ to skip it
def test_analyze_text_primary_model(mock_openai):
    """
    Tests the analyze_text method of the ApiHandler class using the primary model.

    Purpose:
        Verifies that the analyze_text method correctly interacts with the OpenAI API
        and processes its response when the primary model is used.

    Test Strategy:
        - Mock the OpenAI API client (`openai.OpenAI`) to avoid real API calls.
        - Set up the mock API response to simulate a valid response from the OpenAI API.
        - Inject the mock client into the ApiHandler instance to replace its private __client attribute.

    Mock Details:
        - `mock_response`: Simulates the API's chat completion response.
        - `mock_message`: Simulates the message object within the API response.
        - `mock_openai`: Mocks the OpenAI client and its behavior.

    Assertions:
        - Verifies that the analyze_text method returns the expected output
          ("Analyzed text result.") based on the mocked API response.

    Notes:
        This test bypasses the ApiHandler's constructor (`__init__`) using a mock
        to focus solely on the behavior of the analyze_text method.
    """
    mock_response = MagicMock() # Create a mock response with the desired return value

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
     """
    Tests the analyze_file method of the ApiHandler class when no text is extracted from the file.

    Purpose:
        Verifies that the analyze_file method handles cases where the text extraction
        utility returns None (e.g., an empty file).

    Test Strategy:
        - Mock the extract_text_from_file utility function to simulate no text extraction.
        - Use the `api_handler` fixture to create an ApiHandler instance.

    Mock Details:
        - `mock_extract_text`: Simulates the behavior of the extract_text_from_file function,
          always returning None for this test.

    Assertions:
        - Ensures that the analyze_file method returns None when no text is extracted.
        - Verifies that extract_text_from_file is called exactly once with the correct file path.

    Notes:
        This test focuses on error handling and ensures that no further processing occurs
        when no text is available for analysis.
    """
     mock_extract_text.return_value = None # Simulate no text extracted from the file

     result = api_handler.analyze_file("empty.txt")
     assert result is None
     mock_extract_text.assert_called_once_with("empty.txt")
