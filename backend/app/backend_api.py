from flask import Flask, jsonify, Blueprint, request
from flask_cors import CORS
from app.api_handler import ApiHandler
import os

main = Blueprint('main', __name__)
apiHandler = ApiHandler()

CORS(main)  # Allows connections between domains

@main.route('/analyze', methods=['POST']) 
def analyze():
    file = request.files['file']
    file.save(file.filename)

    results = apiHandler.test_file_read(file.filename)

    return jsonify(results)

@main.route('/upload_file', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    file.save(file.filename)

    return jsonify({'filename': f"{file.filename}"})

@main.route('/test_analyze', methods=['GET'])
def test_analyze():
    filename = request.headers.get('filename')

    results = apiHandler.test_file_read(filename)

    if os.path.exists(filename):
        os.remove(filename)

    return jsonify(results)

if __name__ == '__main__':
    main.run(debug=True)
