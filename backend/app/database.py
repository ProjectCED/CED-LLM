### Database functions:
# Debug purpose:
# db_clear() , wipes database clean
# db_show_all() , prints the whole database in console
#
# Global settings:
# db_add_settings_node() , creates settings node
# db_modify_settings_data(property_name, data) , modifies specific property with specific data
# db_lookup_settings_data(property_name) , lookup specific property data
# db_delete_settings_data(property_name) , delete specific property data (also delete property)
#
# Subject area settings:
# db_add_subject_area_node(node_name) , creates subject area node of specific name
# db_modify_subject_area_data(node_name, property_name, data) , modify specific property with specific data
# db_lookup_subject_area_data(node_name, property_name) , lookup specific property data
# db_delete_subject_area_data(name_a, property_name) , delete specific property data (also delete property)

from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("test", "testtest"))

# name of the global settings node
settings_node_name = 'Base'

### Mainly debug purpose
# Wipe database clean, deletes all data
def db_clear():
    driver.execute_query(
        "MATCH (n) DETACH DELETE n",
        database_="neo4j",
    )
    return "Database cleared"


# Show the whole database, print it out in console.
def db_show_all():
    records, summary, keys = driver.execute_query(
        "MATCH (n) RETURN n",
        database_="neo4j",
    )
    
    for record in records:
        print(record.data())

    return "Whole database printed out in console"


### Program global settings
# Create new Settings-node named "Base". Avoids duplicates.
def db_add_settings_node():
    driver.execute_query(
        "MERGE (n:Settings {name: '" + settings_node_name + "'})",
        database_="neo4j",
    )
    return "Settings node (Base) added"


# Modify Settings (Base) properties. Replaces specific property with new data.
def db_modify_settings_data(property_name, data_a):
    # define query string within python, because driver doesn't allow property types being a variable
    query_string = "MATCH (n:Settings {name: '" + settings_node_name + "'}) SET n." + property_name + " = $data_b"

    driver.execute_query(
        query_string,
        data_b = data_a,
        database_="neo4j",
    )
    return "Settings " + property_name + " modified"

# Removes specific Settings property data (and property).
def db_delete_settings_data(property_name):
    # define query string within python, because driver doesn't allow property types being a variable
    query_string = "MATCH (n:Settings {name: '" + settings_node_name + "'}) REMOVE n." + property_name

    driver.execute_query(
        query_string,
        database_="neo4j",
    )
    return "Settings " + property_name + " deleted"


# Return data of specific property from settings (Base)
def db_lookup_settings_data(property_name):
    # define query string within python, because driver doesn't allow property types being a variable
    query_string = "MATCH (n:Settings {name: '" + settings_node_name + "'}) RETURN n." + property_name + " AS " + property_name

    records, summary, keys = driver.execute_query(
        query_string,
        database_="neo4j",
    )
    return next(iter(records)).data()[property_name]


### Subject area settings
# Create new SubjectArea-node with specific name. Avoids duplicates.
def db_add_subject_area_node(name_a):
    driver.execute_query(
        "MERGE (n:SubjectArea {name: $name_b})",
        name_b = name_a,
        database_="neo4j",
    )
    return "Subject node " + " added"


# Modify SubjectArea-node's properties. Replaces specific property with new data.
def db_modify_subject_area_data(name_a, property_name, data_a):
    # define query string within python, because driver doesn't allow property types being a variable
    query_string = "MATCH (n:SubjectArea {name: $name_b}) SET n." + property_name + " = $data_b"

    driver.execute_query(
        query_string,
        name_b = name_a,
        data_b = data_a,
        database_="neo4j",
    )
    return "Subject area's " + name_a + "'s " + property_name + " modified"


# Return data of specific property from SubjectArea-node (Base)
def db_lookup_subject_area_data(name, property_name):
    # define query string within python, because driver doesn't allow property types being a variable
    query_string = "MATCH (n:SubjectArea {name: '" + name + "'}) RETURN n." + property_name + " AS " + property_name

    records, summary, keys = driver.execute_query(
        query_string,
        database_="neo4j",
    )
    return next(iter(records)).data()[property_name]


# Removes specific SubjectArea-node's property data (and property).
def db_delete_subject_area_data(name_a, property_name):
    # define query string within python, because driver doesn't allow property types being a variable
    query_string = "MATCH (n:SubjectArea {name: $name_b}) REMOVE n." + property_name

    driver.execute_query(
        query_string,
        name_b = name_a,
        database_="neo4j",
    )
    return "Subject area's " + name_a + "'s " + property_name + " deleted"