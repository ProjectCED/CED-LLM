from flask import jsonify, Blueprint, request
from flask_cors import CORS
from app.api_handler import ApiHandler
from app.database import Database
import os

main = Blueprint('main', __name__)
apiHandler = ApiHandler()
database = Database()

CORS(main)  # Allows connections between domains

# File management
@main.route('/analyze', methods=['POST']) 
def analyze():
    file = request.files['file']
    file.save(file.filename)

    results = apiHandler.test_file_read(file.filename)

    return jsonify(results)

@main.route('/upload_file', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    filename = file.filename
    file.save(filename)

    return jsonify({'filename': f"{filename}"})

# For testing file analysis without using OpenAI
@main.route('/test_analyze', methods=['POST'])
def test_analyze():
    filename = request.data.decode('utf-8')
    results = apiHandler.test_file_read(filename)

    try:
        os.remove(filename)
    except FileNotFoundError:
        pass
    except PermissionError:
        pass
    

    return jsonify(results)

# For ACTUALLY analyzing files using OpenAI
@main.route('/analyze_file', methods=['POST'])
def analyze_file():
    filename = request.data.decode('utf-8')
    results = apiHandler.analyze_file(filename)

    try:
        os.remove(filename)
    except FileNotFoundError:
        pass
    except PermissionError:
        pass
    

    return jsonify(results)

# Database handling
@main.route('/get_blueprints', methods=['GET'])
def get_blueprints():
    blueprints = database.lookup_blueprint_nodes()
    names = [blueprint[1] for blueprint in blueprints]
    return jsonify(names)

if __name__ == '__main__':
    main.run(debug=True)
