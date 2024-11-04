from flask import Flask, jsonify, Blueprint, request
from flask_cors import CORS
from app.api_handler import ApiHandler
import app.utils as utils

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
    file = request.files['file']
    file.save(file.filename)

    results = apiHandler.test_file_read(file.filename)

    return jsonify(results)

if __name__ == '__main__':
    main.run(debug=True)
