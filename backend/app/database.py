"""
Database functions:
Debug purpose:
db_clear() , wipes database clean
db_show_all() , prints the whole database in console

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
settings_node_name = 'Base'

# database name (default = 'neo4j')
database_name = 'neo4j'

### Mainly debug purpose
# Wipe database clean, deletes all data
def db_clear():
    driver.execute_query(
        "MATCH (n) DETACH DELETE n",
        database_= database_name,
    )
    return "Database cleared"


# Show the whole database, print it out in console.
def db_show_all():
    records, summary, keys = driver.execute_query(
        "MATCH (n) RETURN n",
        database_= database_name,
    )
    
    for record in records:
        print(record.data())

    return "Whole database printed out in console"

### Universal helper functions
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


### Program global settings
# Create new Settings-node named "Base". Avoids duplicates.
def db_add_settings_node():
    return db_add_node('Settings', 'Base')


# Modify Settings (Base) properties. Replaces specific property with new data.
def db_modify_settings_data(property_name, new_data):
    return db_modify_node_data('Settings', settings_node_name, property_name, new_data)


# Removes specific Settings property data (and property).
def db_delete_settings_data(property_name):
    # define query string within python, because driver doesn't allow property types being a variable
    query_string = "MATCH (n:Settings {name: '" + settings_node_name + "'}) REMOVE n." + property_name

    driver.execute_query(
        query_string,
        database_= database_name,
    )
    return "Settings " + property_name + " deleted"


# Return data of specific property from settings (Base)
def db_lookup_settings_data(property_name):
    # define query string within python, because driver doesn't allow property types being a variable
    query_string = "MATCH (n:Settings {name: '" + settings_node_name + "'}) RETURN n." + property_name + " AS " + property_name

    records, summary, keys = driver.execute_query(
        query_string,
        database_= database_name,
    )
    return next(iter(records)).data()[property_name]

# Deletes global settings with all it's related content.
def db_delete_settings():
    # define query string within python, because driver doesn't allow property types being a variable
    query_string = "MATCH (n:Settings {name: '" + settings_node_name + "'}) - [*0..] - (d) WITH DISTINCT d DETACH DELETE d"

    driver.execute_query(
        query_string,
        database_= database_name,
    )
    return "´Settings deleted"


### Subject area settings
# Create new SubjectArea-node with specific name. Avoids duplicates.
def db_add_subject_area_node(name_a):
    return db_add_node('SubjectArea', name_a)


# Modify SubjectArea-node's properties. Replaces specific property with new data.
def db_modify_subject_area_data(node_name, property_name, new_data):
    return db_modify_node_data('SubjectArea', node_name, property_name, new_data)


# Return data of specific property from SubjectArea-node
def db_lookup_subject_area_data(name, property_name):
    # define query string within python, because driver doesn't allow property types being a variable
    query_string = "MATCH (n:SubjectArea {name: '" + name + "'}) RETURN n." + property_name + " AS " + property_name

    records, summary, keys = driver.execute_query(
        query_string,
        database_= database_name,
    )
    return next(iter(records)).data()[property_name]


# Removes specific SubjectArea-node's property data (and property).
def db_delete_subject_area_data(name_a, property_name):
    # define query string within python, because driver doesn't allow property types being a variable
    query_string = "MATCH (n:SubjectArea {name: $name_b}) REMOVE n." + property_name

    driver.execute_query(
        query_string,
        name_b = name_a,
        database_= database_name,
    )
    return "Subject area's " + name_a + "'s " + property_name + " deleted"

# Deletes specific subject area with all it's related content.
def db_delete_subject_area(name_a):
    # define query string within python, because driver doesn't allow property types being a variable
    query_string = "MATCH (n:SubjectArea {name: $name_b}) - [*0..] - (d) WITH DISTINCT d DETACH DELETE d"

    driver.execute_query(
        query_string,
        name_b = name_a,
        database_= database_name,
    )
    return "Subject area " + name_a + " deleted"