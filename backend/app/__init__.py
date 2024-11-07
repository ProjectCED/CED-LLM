from flask import Flask
from flask_jwt_extended import JWTManager
from neo4j import GraphDatabase

app = Flask(__name__)

# Neo4j connection
# driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

from .backend_api import main
app.register_blueprint(main)