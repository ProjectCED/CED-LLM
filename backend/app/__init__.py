from flask import Flask
from flask_jwt_extended import JWTManager
from neo4j import GraphDatabase

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
jwt = JWTManager(app)

# Neo4j connection
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

from .routes import *
