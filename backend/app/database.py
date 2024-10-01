from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("test", "testtest"))

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
        "MERGE (n:Settings {name: 'Base'})",
        database_="neo4j",
    )
    return "Settings node (Base) added"


# Modify Settings (Base) properties. Replaces specific property with new data.
def db_modify_settings_data(property_name, data_a):
    # define query string within python, because driver doesn't allow property types being a variable
    query_string = "MATCH (n:Settings {name: 'Base'}) SET n." + property_name + " = $data_b"

    driver.execute_query(
        query_string,
        data_b = data_a,
        database_="neo4j",
    )
    return "Settings " + property_name + " modified"


### Settings for subject area
# Create new Subject-node with specific name. Avoids duplicates.
def db_add_subject_node(name_a):
    driver.execute_query(
        "MERGE (n:SubjectArea {name: $name_b})",
        name_b = name_a,
        database_="neo4j",
    )
    return "Subject node " + " added"


# Modify Subject-node's properties. Replaces specific property with new data.
def db_modify_subject_data(name_a, property_name, data_a):
    # define query string within python, because driver doesn't allow property types being a variable
    query_string = "MATCH (n:SubjectArea {name: $name_b}) SET n." + property_name + " = $data_b"

    driver.execute_query(
        query_string,
        name_b = name_a,
        data_b = data_a,
        database_="neo4j",
    )
    return "Subject area's " + name_a + "'s " + property_name + " modified"


