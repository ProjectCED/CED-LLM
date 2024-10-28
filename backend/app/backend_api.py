from flask import Flask, jsonify, Blueprint
from flask_cors import CORS
from app.api_handler import analyze_file

main = Blueprint('main', __name__)

CORS(main)  # Allows connections between domains

@main.route('/analyze', methods=['POST'])
def analyze():
    result = analyze_file()
    return jsonify(result=result)

if __name__ == '__main__':
    main.run(debug=True)
