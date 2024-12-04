from flask import jsonify, Blueprint, request
from flask_cors import CORS
from app.api_handler import ApiHandler
from app.database import Database, NodeProperties
from dotenv import load_dotenv
import os
from app.models.blueprint import Blueprint as BP

main = Blueprint('main', __name__)
apiHandler = ApiHandler()
database = Database()

frontend_port = os.getenv('VITE_PORT', '5173')
CORS(main, resources={r"/*": {"origins": "http://localhost:{frontend_port}"}})  # Allows connections between domains

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
    blueprints = database.lookup_blueprint_nodes() # [[ID, NAME]]
    blueprints_with_all_properties = []
    for bp in blueprints:
        id = bp[0]
        name = bp[1]
        desc = database.lookup_blueprint_property(id, NodeProperties.Blueprint.DESCRIPTION)
        questions = database.lookup_blueprint_property(id, NodeProperties.Blueprint.QUESTIONS)
        blueprints_with_all_properties.append({"id": id, "name": name, "description": desc, "questions": questions})
    return jsonify(blueprints_with_all_properties)


@main.route('/save_blueprint', methods=['POST'])
def save_blueprint():
    data = request.json
    name = data['name']
    description = data['description']

    # On the frontend, questions are divided in the "main" question and additional questions
    question = data['question']
    addedQuestions = data['addedQuestions']

    # Merge questions to one list
    questions = [question] + addedQuestions

    bp = BP(name, description, questions)

    # Returns the ID
    return bp.save_blueprint()

@main.route('/delete_blueprint', methods=['POST'])
def delete_blueprint():
    data = request.json
    id = data['id']

    # True/false
    success = database.delete_blueprint(id)
    return jsonify({"success": success})

@main.route("/mistral", methods=["POST"])
def query_mistral():
    data = request.json
    prompt = data.get("prompt", "Explain the theory of relativity in layman's terms.")
    response = apiHandler.mistral_analyze(prompt)
    return jsonify(response)


if __name__ == '__main__':
    main.run(debug=True)
