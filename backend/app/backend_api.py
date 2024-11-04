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

@main.route('/test_analyze', methods=['POST'])
def test_analyze():
    file = request.files.get('file')
    filepath = file.filename
    file.save(filepath)

    results = apiHandler.test_file_read(filepath)

    if os.path.exists(filepath):
        os.remove(filepath)

    return jsonify(results)

if __name__ == '__main__':
    main.run(debug=True)
