from flask import Flask, jsonify, Blueprint
from flask_cors import CORS
from app.api_handler import ApiHandler

main = Blueprint('main', __name__)
apiHandler = ApiHandler()

CORS(main)  # Allows connections between domains

@main.route('/analyze', methods=['POST']) 
def analyze():
    result = apiHandler.test_file_read()
    return jsonify(result=result)

if __name__ == '__main__':
    main.run(debug=True)
