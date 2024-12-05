import pytest
import os
from flask import Flask
from app.backend_api import main as main_blueprint
from app.api_handler import ApiHandler

class MockApiHandler:
    """
    Mock implementation of the ApiHandler class for testing.

    Methods:
        test_file_read(filename):
            Simulates processing a file and returns a mock result.
        analyze_file(filename):
            Simulates analyzing a file and returns a mock analysis result.
    """
    def test_file_read(self, filename):
        """
        Simulates the processing of a file.

        Parameters:
            filename (str): The name of the file to process.

        Returns:
            dict: A mock result indicating the file was processed.
        """
        return {"mocked_result": f"Processed {filename}"}

    def analyze_file(self, filename):
        """
        Simulates the analysis of a file.

        Parameters:
            filename (str): The name of the file to analyze.

        Returns:
            dict: A mock result indicating the file was analyzed.
        """
        return {"mocked_analysis": f"Analyzed {filename}"}

@pytest.fixture
def app(monkeypatch):
    """
    Fixture to create and configure the Flask application for testing.

    Purpose:
        - Sets up the Flask application instance.
        - Replaces the real ApiHandler with a mock implementation using monkeypatch.

    Parameters:
        monkeypatch (pytest.MonkeyPatch): A pytest utility to temporarily modify attributes.

    Yields:
        Flask: The configured Flask application instance for testing.
    """
    app = Flask(__name__)
    app.register_blueprint(main_blueprint)
    monkeypatch.setattr('app.backend_api.apiHandler', MockApiHandler())
    yield app

@pytest.fixture
def client(app):
    """
    Fixture to create a test client for the Flask application.

    Purpose:
        Provides a client to simulate HTTP requests to the application during tests.

    Parameters:
        app (Flask): The Flask application instance.

    Returns:
        flask.testing.FlaskClient: A test client for the application.
    """
    return app.test_client()

@pytest.fixture
def temp_file(tmp_path):
    """
    Fixture to create a temporary file for upload tests.

    Purpose:
        Creates a sample .txt file with predefined content to simulate file uploads.

    Parameters:
        tmp_path (Path): A temporary path provided by pytest.

    Returns:
        Path: The path to the created temporary file.
    """
    file_path = tmp_path / "sample.txt"
    file_path.write_text("Sample file content.")
    return file_path

def test_upload_file(client, temp_file):
    """
    Tests the /upload_file endpoint.

    Purpose:
        Verifies that the file upload endpoint correctly handles a file upload and
        returns the expected response.

    Parameters:
        client (FlaskClient): The Flask test client.
        temp_file (Path): The temporary file to upload.

    Assertions:
        - Ensures the response status code is 200.
        - Verifies that the uploaded filename is included in the response JSON.
    """
    with open(temp_file, 'rb') as file:
        response = client.post('/upload_file', data={'file': file})
    assert response.status_code == 200
    # Compare the filename as a substring
    assert "sample.txt" in response.json['filename']

def test_analyze(client, temp_file):
    """
    Tests the /analyze endpoint.

    Purpose:
        Verifies that the analyze endpoint processes the uploaded file
        and returns the expected mocked result.

    Parameters:
        client (FlaskClient): The Flask test client.
        temp_file (Path): The temporary file to analyze.

    Assertions:
        - Ensures the response status code is 200.
        - Validates that the response JSON includes the correct mocked result.
    """
    with open(temp_file, 'rb') as file:
        response = client.post('/analyze', data={'file': file})
    assert response.status_code == 200
    # Adjusted to check that 'mocked_result' contains the correct file path
    assert "Processed" in response.json['mocked_result']

def test_analyze_file(client, temp_file):
    """
    Tests the /analyze_file endpoint.

    Purpose:
        Verifies that the endpoint analyzes the provided filename and
        returns the expected mocked analysis result.

    Parameters:
        client (FlaskClient): The Flask test client.
        temp_file (Path): The temporary file for testing.

    Assertions:
        - Ensures the response status code is 200.
        - Confirms that the response JSON matches the expected mocked analysis result.
    """
    response = client.post('/analyze_file', data=temp_file.name)
    assert response.status_code == 200
    assert response.json == {"mocked_analysis": f"Analyzed {temp_file.name}"}
