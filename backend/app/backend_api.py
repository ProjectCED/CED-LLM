from flask import jsonify, Blueprint, request
from flask_cors import CORS
from app.api_handler import ApiHandler
from app.database import Database, NodeProperties
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
    """return jsonify([
        {"id": 1, "name": "Blueprint 1", "description": "bp1_desc", "questions": ["Q1", "Q2"]},
        {"id": 2, "name": "Blueprint 2", "description": "bp2_desc", "questions": ["Q3", "Q4"]}])"""
    blueprints = database.lookup_blueprint_nodes() # [[ID, NAME]]
    blueprints_with_all_properties = [{}]
    for bp in blueprints:
        id = bp[0]
        name = bp[1]
        desc = database.lookup_blueprint_property(id, NodeProperties.Blueprint.DESCRIPTION)
        questions = database.lookup_blueprint_property(id, NodeProperties.Blueprint.QUESTIONS)
        blueprints_with_all_properties.append({"id": id, "name": name, "description": desc, "questions": questions})
    return jsonify(blueprints_with_all_properties)

if __name__ == '__main__':
    main.run(debug=True)
