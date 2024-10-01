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



