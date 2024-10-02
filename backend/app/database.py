"""
Database functions:
Debug purpose:
db_clear() , wipes database clean
db_show_all() , prints the whole database in console

Helper functions:
db_add_node(node_type, node_name) , create node with a name attribute
db_modify_node_data(node_type, node_name, property_name, new_data) , modify property data
db_lookup_whole_node(node_type, node_name) , lookup and return all properties from the node
db_lookup_node_property(node_type, node_name, property_name) , lookup and return single 

Global settings:
db_add_settings_node() , creates settings node
db_modify_settings_data(property_name, data) , modifies specific property with specific data
db_lookup_settings_data(property_name) , lookup specific property data
db_delete_settings_data(property_name) , delete specific property data (also delete property)
db_delete_settings() , deletes settings with all it's related content.

Subject area settings:
db_add_subject_area_node(node_name) , creates subject area node of specific name
db_modify_subject_area_data(node_name, property_name, data) , modify specific property with specific data
db_lookup_subject_area_data(node_name, property_name) , lookup specific property data
db_delete_subject_area_data(node_name, property_name) , delete specific property data (also delete property)
db_delete_subject_area(node_name) , deletes specific subject area with all it's related content.
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


"""
Global settings functions
"""
# Create new Settings-node named "Base". Avoids duplicates.
def db_add_settings_node():
    return db_add_node('Settings', settings_node_name)

# Modify Settings (Base) properties. Replaces specific property with new data.
def db_modify_settings_data(property_name, new_data):
    return db_modify_node_data('Settings', settings_node_name, property_name, new_data)

# Removes specific Settings property data (and property).
def db_delete_settings_data(property_name):
    return db_delete_property('Settings', settings_node_name, property_name)

# Return data of specific property from settings (Base)
def db_lookup_settings_data(property_name):
    return db_lookup_node_property('Settings', settings_node_name, property_name)

# Deletes global settings with all it's related content.
def db_delete_settings():
    return db_delete_node('Settings', settings_node_name)


"""
Subject area functions
"""
# Create new SubjectArea-node with specific name. Avoids duplicates.
def db_add_subject_area_node(node_name):
    return db_add_node('SubjectArea', node_name)

# Modify SubjectArea-node's properties. Replaces specific property with new data.
def db_modify_subject_area_data(node_name, property_name, new_data):
    return db_modify_node_data('SubjectArea', node_name, property_name, new_data)

# Removes specific subject area property data (and property).
def db_delete_subject_area_data(node_name, property_name):
    return db_delete_property('SubjectArea', node_name, property_name)

# Return data of specific property from SubjectArea-node
def db_lookup_subject_area_data(node_name, property_name):
    return db_lookup_node_property('SubjectArea', node_name, property_name)

# Deletes specific subject area with all it's related content.
def db_delete_subject_area(node_name):
    return db_delete_node_with_connections('SubjectArea', node_name)

"""
Result functions
"""
# Create new Result-node with specific name. Avoids duplicates.
def db_add_result_node(node_id):
    return db_add_node('Result', node_id)

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
Model functions
"""
# Create new Model-node with specific name. Avoids duplicates.
def db_add_model_node(node_name):
    return db_add_node('Model', node_name)

# Modify Model-node's properties. Replaces specific property with new data.
def db_modify_model_data(node_name, property_name, new_data):
    return db_modify_node_data('Model', node_name, property_name, new_data)

# Removes specific Model property data (and property).
def db_delete_model_data(node_name, property_name):
    return db_delete_property('Model', node_name, property_name)

# Return data of specific property from Model-node
def db_lookup_model_data(node_name, property_name):
    return db_lookup_node_property('Model', node_name, property_name)

# Deletes specific Model with all it's related content.
def db_delete_model(node_name):
    return db_delete_node_with_connections('Model', node_name)

"""
Dataset functions
"""
# Create new Dataset-node with specific name. Avoids duplicates.
def db_add_dataset_node(node_id):
    return db_add_node('Dataset', node_id)

# Modify Dataset-node's properties. Replaces data with new data.
def db_modify_dataset_data(node_id, new_data):
    return db_modify_node_data('Dataset', node_id, 'data', new_data)

# Return data of specific property from Dataset-node
def db_lookup_dataset_data(node_id):
    return db_lookup_node_property('Dataset', node_id, 'data')

# Deletes specific Dataset with all it's related content.
def db_delete_dataset(node_id):
    return db_delete_node('Dataset', node_id)

"""
Connection functions
"""
# Connect from dataset node to subject area node
def db_connect_dataset_to_subject_area(dataset_node_id, subject_area_node_name):
    return db_connect_with_relationship('Dataset', dataset_node_id, 'SubjectArea', subject_area_node_name, 'DATA_ANALYSATION')

# Connect from dataset node to model node
def db_connect_dataset_to_model(dataset_node_id, model_node_name):
    return db_connect_with_relationship('Dataset', dataset_node_id, 'Model', model_node_name, 'MODEL_CREATION')

