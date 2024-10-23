from flask import Flask, jsonify, Blueprint
from flask_cors import CORS

main = Blueprint('main', __name__)

CORS(main)  # Allows connections between domains

@main.route('/api/data', methods=['GET'])
def get_data():
    data = {
        "message": "Hello from the Flask backend!"
    }
    return jsonify(data)

if __name__ == '__main__':
    main.run(debug=True)
