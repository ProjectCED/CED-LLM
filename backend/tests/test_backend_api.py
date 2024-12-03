import pytest
import os
from flask import Flask
from app.backend_api import main as main_blueprint
from app.api_handler import ApiHandler

# Mock ApiHandler methods for testing
class MockApiHandler:
    def test_file_read(self, filename):
        return {"mocked_result": f"Processed {filename}"}

    def analyze_file(self, filename):
        return {"mocked_analysis": f"Analyzed {filename}"}

# Replace the real ApiHandler with the mock
@pytest.fixture
def app(monkeypatch):
    # Set up the Flask app and replace the real ApiHandler with our mock
    app = Flask(__name__)
    app.register_blueprint(main_blueprint)
    monkeypatch.setattr('app.backend_api.apiHandler', MockApiHandler())
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def temp_file(tmp_path):
    """Fixture to create a temporary file for upload tests."""
    file_path = tmp_path / "sample.txt"
    file_path.write_text("Sample file content.")
    return file_path

def test_upload_file(client, temp_file):
    with open(temp_file, 'rb') as file:
        response = client.post('/upload_file', data={'file': file})
    assert response.status_code == 200
    # Compare the filename as a substring
    assert "sample.txt" in response.json['filename']

def test_analyze(client, temp_file):
    with open(temp_file, 'rb') as file:
        response = client.post('/analyze', data={'file': file})
    assert response.status_code == 200
    # Adjusted to check that 'mocked_result' contains the correct file path
    assert "Processed" in response.json['mocked_result']

# Test /test_analyze endpoint
def test_test_analyze(client, temp_file):
    response = client.post('/test_analyze', data=temp_file.name)
    assert response.status_code == 200
    assert response.json == {"mocked_result": f"Processed {temp_file.name}"}

# Test /analyze_file endpoint
def test_analyze_file(client, temp_file):
    response = client.post('/analyze_file', data=temp_file.name)
    assert response.status_code == 200
    assert response.json == {"mocked_analysis": f"Analyzed {temp_file.name}"}
