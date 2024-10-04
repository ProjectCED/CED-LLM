"""
Database functions:
Debug purpose:
debug_db_clear() , wipes database clean
debug_db_show_all() , prints the whole database in console

Helper functions:
db_add_node(node_type, node_name) , create node with a name attribute
db_modify_node_data(node_type, node_name, property_name, new_data) , modify one property data
db_lookup_whole_node(node_type, node_name) , lookup and return all properties from the node
db_lookup_node_property(node_type, node_name, property_name) , lookup and return single property data
db_delete_node_with_connections(node_type, node_name) , deletes node and all connected nodes 0..n deep
db_delete_node(node_type, node_name) , delete certain node type with certain name
db_delete_property(node_type, node_name, property_name) , delete specific property data
db_connect_with_relationship(node_type_a, node_name_a, node_type_b, node_name_b, relationship_type) , connect node a -> node b with relationship type


Global settings:
db_add_settings_node() , creates settings node
db_modify_settings_data(property_name, data) , modifies specific property with specific data
db_lookup_settings_data(property_name) , lookup specific property data
db_delete_settings_data(property_name) , delete specific property data (also delete property)
db_delete_settings() , deletes settings node.

Subject area:
db_add_subject_area_node(node_name) , creates subject area node of specific name
db_modify_subject_area_data(node_name, property_name, data) , modify specific property with specific data
db_lookup_subject_area_data(node_name, property_name) , lookup specific property data
db_delete_subject_area_data(node_name, property_name) , delete specific property data (also delete property)
db_delete_subject_area(node_name) , deletes SubjectArea-node and it's Dataset-nodes

Result:
db_add_result_node(node_id)
db_modify_result_data(node_id, property_name, new_data)
db_delete_result_data(node_id, property_name)
db_lookup_result_data(node_id, property_name)
db_delete_result(node_id) , only deletes node

Model:
db_add_model_node(node_name)
db_modify_model_data(node_name, property_name, new_data)
db_delete_model_data(node_name, property_name)
db_lookup_model_data(node_name, property_name)
db_delete_model(node_name) , deletes Model-node and it's Dataset-nodes

Dataset:
db_add_dataset_node(node_id)
db_modify_dataset_data(node_id, new_data)
db_lookup_dataset_data(node_id)
db_delete_dataset(node_id) , only deletes Dataset-node

Connections:
db_connect_dataset_to_subject_area(dataset_node_id, subject_area_node_name) , connect dataset -> subject area
db_connect_dataset_to_model(dataset_node_id, model_node_name) , connect dataset -> model
"""

from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

driver = GraphDatabase.driver(os.getenv('NEO4J_URL'), auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD')))

# name of the global settings node
settings_node_name = 'Global'

# database name (default = 'neo4j')
database_name = 'neo4j'

"""
Debug functions
"""
# Wipe database clean, deletes all data
def debug_db_clear():
    driver.execute_query(
        "MATCH (n) DETACH DELETE n",
        database_= database_name,
    )
    return "Database cleared"

# Show the whole database, print it out in console.
def debug_db_show_all():
    records, summary, keys = driver.execute_query(
        "MATCH (n) RETURN n",
        database_= database_name,
    )
    
    for record in records:
        print(record)

    return "Whole database printed out in console"


"""
Universal helper functions
"""
# Create node with specific type and name
def db_add_node(node_type, node_name):
    # define query string within python, because driver doesn't allow property types being a variable
    query_string = "MERGE (n:" + node_type + " {name: $name})"

    driver.execute_query(
        query_string,
        name = node_name,
        database_= database_name,
    )
    return "Added node: " + node_type + " with a name:" + node_name

# Modify node properties. Replaces specific property with new data.
def db_modify_node_data(node_type, node_name, property_name, new_data):
    # define query string within python, because driver doesn't allow property types being a variable
    query_string = "MATCH (n:" + node_type + " {name: '" + node_name + "'}) SET n." + property_name + " = $old_data"

    driver.execute_query(
        query_string,
        old_data = new_data,
        database_= database_name,
    )
    return "Modified data: " + node_type + "("+ node_name +")."+ property_name

# Lookup node and return all it's data
def db_lookup_whole_node(node_type, node_name):
    # define query string within python, because driver doesn't allow property types being a variable
    query_string = "MATCH (n:" + node_type + " {name: '" + node_name + "'}) RETURN n"
    
    records, summary, keys = driver.execute_query(
        query_string,
        database_= database_name,
    )
    return next(iter(records)).data()

# Lookup individual property value from a node
def db_lookup_node_property(node_type, node_name, property_name):
    query_string = "MATCH (n:" + node_type + " {name: '" + node_name + "'}) RETURN n." + property_name + " AS " + property_name
    
    records, summary, keys = driver.execute_query(
        query_string,
        database_= database_name,
    )
    return next(iter(records)).data()[property_name]

# Delete node and all related nodes 0..n deep
def db_delete_node_with_connections(node_type, node_name):
    # define query string within python, because driver doesn't allow property types being a variable
    query_string = "MATCH (n:" + node_type + " {name: '" + node_name + "'}) - [*0..] - (d) WITH DISTINCT d DETACH DELETE d"
    
    driver.execute_query(
        query_string,
        database_= database_name,
    )
    return node_type + "(" + node_name + ") deleted with connections"

# Delete node and it's connections
def db_delete_node(node_type, node_name):
    # define query string within python, because driver doesn't allow property types being a variable
    query_string = "MATCH (n:" + node_type + " {name: '" + node_name + "'}) DETACH DELETE n"
    
    driver.execute_query(
        query_string,
        database_= database_name,
    )
    return node_type + "(" + node_name + ") deleted"

# Delete node property
def db_delete_property(node_type, node_name, property_name):
    # define query string within python, because driver doesn't allow property types being a variable
    query_string = "MATCH (n:" + node_type + " {name: '" + node_name + "'}) REMOVE n." + property_name
    
    driver.execute_query(
        query_string,
        database_= database_name,
    )
    return "Deleted: " + node_type + "(" + node_name + ")." + property_name

def db_connect_with_relationship(node_type_a, node_name_a, node_type_b, node_name_b, relationship_type):
    # define query string within python, because driver doesn't allow property types being a variable
    query_string = "MATCH (n:" + node_type_a + " {name: '" + node_name_a + "'}) MATCH (m:" + node_type_b + " {name: '" + node_name_b + "'}) MERGE (n)-[:" + relationship_type + "]->(m)"

    driver.execute_query(
        query_string,
        database_= database_name,
    )
    return "Connected: " + node_type_a + "(" + node_name_a + ")->" + node_type_b + "(" + node_name_b + ")"


def db_copy_node(node_type, new_node_type, id_type, id_value):
    # define query string within python, because driver doesn't allow property types being a variable
    query_string = "MATCH (n:" + node_type + " {" + id_type + ": '" + id_value + "'}) SET n:" + new_node_type

    driver.execute_query(
        query_string,
        database_= database_name,
    )
    return "Copied " + node_type + "(" + id_value + ") to " + new_node_type + "(" + id_value + ")"


"""
Global settings functions
"""
# Create new Settings-node. Avoids duplicates.
def db_add_settings_node():
    return db_add_node('Settings', settings_node_name)

# Modify Settings properties. Replaces specific property with new data.
def db_modify_settings_data(property_name, new_data):
    return db_modify_node_data('Settings', settings_node_name, property_name, new_data)

# Removes specific Settings property data (and property).
def db_delete_settings_data(property_name):
    return db_delete_property('Settings', settings_node_name, property_name)

# Return data of specific property from settings
def db_lookup_settings_data(property_name):
    return db_lookup_node_property('Settings', settings_node_name, property_name)

# Deletes global settings with all it's related content.
def db_delete_settings():
    return db_delete_node('Settings', settings_node_name)

"""
User settings functions
"""
# Create new UserSettings-node. Avoids duplicates.
def db_add_user_settings_node(user_name):
    return db_add_node('UserSettings', user_name)

# Modify UserSettings properties. Replaces specific property with new data.
def db_modify_user_settings_data(user_name, property_name, new_data):
    return db_modify_node_data('UserSettings', user_name, property_name, new_data)

# Removes specific UserSettings property data (and property).
def db_delete_user_settings_data(user_name, property_name):
    return db_delete_property('UserSettings', user_name, property_name)

# Return data of specific property from UserSettings
def db_lookup_user_settings_data(user_name, property_name):
    return db_lookup_node_property('UserSettings', user_name, property_name)

# Deletes global UserSettings with all it's related content.
def db_delete_user_settings(user_name):
    return db_delete_node('UserSettings', user_name)

"""
Project functions
"""
# Create new Project-node with specific name. Avoids duplicates.
def db_add_project_node(node_name):
    return db_add_node('Project', node_name)

# Modify Project-node's properties. Replaces specific property with new data.
def db_modify_project_data(node_name, property_name, new_data):
    return db_modify_node_data('Project', node_name, property_name, new_data)

# Removes specific Project property data (and property).
def db_delete_project_data(node_name, property_name):
    return db_delete_property('Project', node_name, property_name)

# Return data of specific property from Project-node
def db_lookup_project_data(node_name, property_name):
    return db_lookup_node_property('Project', node_name, property_name)

# Deletes specific Project with all it's related content.
def db_delete_project(node_name):
    return db_delete_node_with_connections('Project', node_name)

"""
Result functions
todo:
- delete all connected UsedInAnalysis nodes too
"""
# Create new Result-node with specific name. Avoids duplicates.
# Connect it with project
def db_add_result_node(result_node_id, project_node_name, analyze_model_name):
    return_a = db_add_node('Result', result_node_id)
    return_b = db_connect_result_to_project(result_node_id, project_node_name)
    return_c = db_add_used_analyze_model_node(analyze_model_name, result_node_id)
    return return_a + " and " + return_b + " and " + return_c

# Modify Result-node's properties. Replaces specific property with new data.
def db_modify_result_data(node_id, property_name, new_data):
    return db_modify_node_data('Result', node_id, property_name, new_data)

# Removes specific Result property data (and property).
def db_delete_result_data(node_id, property_name):
    return db_delete_property('Result', node_id, property_name)

# Return data of specific property from Result-node
def db_lookup_result_data(node_id, property_name):
    return db_lookup_node_property('Result', node_id, property_name)

# Deletes specific Result with all it's related content.
def db_delete_result(node_id):
    return db_delete_node('Result', node_id)

"""
DataModel functions
"""
# Create new DataModel-node with specific name. Avoids duplicates.
def db_add_data_model_node(node_name):
    return db_add_node('DataModel', node_name)

# Modify DataModel-node's properties. Replaces specific property with new data.
def db_modify_data_model_data(node_name, property_name, new_data):
    return db_modify_node_data('DataModel', node_name, property_name, new_data)

# Removes specific DataModel property data (and property).
def db_delete_data_model_data(node_name, property_name):
    return db_delete_property('DataModel', node_name, property_name)

# Return data of specific property from DataModel-node
def db_lookup_data_model_data(node_name, property_name):
    return db_lookup_node_property('DataModel', node_name, property_name)

# Deletes specific DataModel with all it's related content.
def db_delete_data_model(node_name):
    return db_delete_node_with_connections('DataModel', node_name)

"""
AnalyzeModel functions
"""
# Create new AnalyzeModel-node with specific name. Avoids duplicates.
def db_add_analyze_model_node(node_name):
    return db_add_node('AnalyzeModel', node_name)

# Modify AnalyzeModel-node's properties. Replaces specific property with new data.
def db_modify_analyze_model_data(node_name, property_name, new_data):
    return db_modify_node_data('AnalyzeModel', node_name, property_name, new_data)

# Removes specific AnalyzeModel property data (and property).
def db_delete_analyze_model_data(node_name, property_name):
    return db_delete_property('AnalyzeModel', node_name, property_name)

# Return data of specific property from AnalyzeModel-node
def db_lookup_analyze_model_data(node_name, property_name):
    return db_lookup_node_property('AnalyzeModel', node_name, property_name)

# Deletes specific AnalyzeModel with all it's related content.
def db_delete_analyze_model(node_name):
    return db_delete_node_with_connections('AnalyzeModel', node_name)

"""
UsedAnalyzeModel functions
"""
# Create new UsedAnalyzeModel from a copy of AnalyzeModel
# Connect it with Result
def db_add_used_analyze_model_node(model_node_name, result_node_name):
    return_a = db_copy_node('AnalyzeModel','UsedAnalyzeModel', 'name', model_node_name)
    return_b = db_connect_dataset_to_analyze_model(model_node_name, result_node_name)
    return return_a + " and " + return_b


db_copy_node
"""
Dataset functions
"""
# Create new Dataset-node with specific name. Avoids duplicates.
def db_add_dataset_node(node_id):
    return db_add_node('Dataset', node_id)

# Modify Dataset-node's properties. Replaces data with new data.
def db_modify_dataset_data(node_id, file_name):
    return db_modify_node_data('Dataset', node_id, 'Filename', file_name)

# Return data of specific property from Dataset-node
def db_lookup_dataset_data(node_id):
    return db_lookup_node_property('Dataset', node_id, 'Filename')

# Deletes specific Dataset with all it's related content.
def db_delete_dataset(node_id):
    return db_delete_node('Dataset', node_id)

"""
Connection functions
"""
# Connect from Dataset node to project node
def db_connect_dataset_to_project(dataset_node_id, project_node_name):
    return db_connect_with_relationship('Dataset', dataset_node_id, 'Project', project_node_name, 'ANALYZED_IN')

# Connect from Dataset node to DataModel node
def db_connect_dataset_to_data_model(dataset_node_id, model_node_name):
    return db_connect_with_relationship('Dataset', dataset_node_id, 'DataModel', model_node_name, 'USED_FOR_TRAINING')

# Connect from Dataset node to AnalyzeModel node
def db_connect_dataset_to_analyze_model(dataset_node_id, model_node_name):
    return db_connect_with_relationship('Dataset', dataset_node_id, 'AnalyzeModel', model_node_name, 'USED_FOR_TRAINING')

# Connect from UsedAnalyzeModel node to Result node
def db_connect_used_analyze_model_to_result(model_node_name, result_node_name):
    return db_connect_with_relationship('UsedAnalyzeModel', model_node_name, 'Result', result_node_name, 'USED_IN_ANALYSIS')

# Connect from Result node to Project node
def db_connect_result_to_project(result_node_name, project_node_name):
    return db_connect_with_relationship('Result', result_node_name, 'Project', project_node_name, 'BELONGS_TO')

