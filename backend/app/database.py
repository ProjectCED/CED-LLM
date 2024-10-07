from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

class database:
    def __init__(self) -> None:
        """Start up database connection.
        Setup types and identifier names according to database design.
        """
        self.driver = GraphDatabase.driver(os.getenv('NEO4J_URL'), auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD')))
        self.name = 'neo4j'     # database name

        self.global_settings_type = 'Settings'
        self.global_settings_id = 'name'
        self.global_settings_id_value = 'Global'

        self.user_settings_type = 'UserSettings'
        self.user_settings_id = 'user_name'
        
        self.dataset_type = 'Dataset'
        self.dataset_id = 'id'
        
        self.data_model_type = 'DataModel'
        self.data_model_id = 'id'
        
        self.analyze_model_type = 'AnalyzeModel'
        self.analyze_model_id = 'id'
        
        self.project_type = 'Project'
        self.project_id = 'id'
        self.project_exclusion = ['FAVORITED_IN'] # exclusion for deletion
        
        self.result_type = 'Result'
        self.result_id = 'id'
        
        self.used_analyze_model_type = 'UsedAlayzeModel'
        self.used_analyze_model_id = 'id'
        
        self.used_dataset_type = 'UsedDataSet'
        self.used_dataset_id = 'id'


    def debug_clear_all(self):
        """return useful string message
        DEBUG: Clear the whole database
        """
        self.driver.execute_query(
            "MATCH (n) DETACH DELETE n",
            database_= self.name,
        )
        return "Database cleared"


    def debug_show_all(self):
        """return useful string message
        DEBUG: Print the whole database in console.
        """
        records, summary, keys = self.driver.execute_query(
            "MATCH (n) RETURN n",
            database_= self.name,
        )
        
        for record in records:
            print(record)

        return "Whole database printed out in console"
    

    def __add_node(self, type, id_type, id_value):
        """return useful string message
        Create a node with specific node-type, id-type and it's value. Can't duplicate.
        """
        id_value = str(id_value)
        query_string = "MERGE (n:" + type + " {" + id_type + ": $value})"

        self.driver.execute_query(
            query_string,
            value = id_value,
            database_= self.name,
        )
        return "Added node: " + type + "." + id_type + "(" + id_value + ")"
            

    def __set_node_property(self, type, id_type, id_value, property_name, new_data):
        """return useful string message
        Set specific node property with new data.
        """
        id_value = str(id_value)
        query_string = "MATCH (n:" + type + " {" + id_type + ": '" + id_value + "'}) SET n." + property_name + " = $old_data"

        self.driver.execute_query(
            query_string,
            old_data = new_data,
            database_= self.name,
        )
        return "Modified data: " + type + "("+ id_value +")."+ property_name
    

    def __lookup_whole_node(self, type, id_type, id_value):
        """return whole node data or error string
        Lookup a node and return all it's data
        """
        id_value = str(id_value)
        query_string = "MATCH (n:" + type + " {" + id_type + ": '" + id_value + "'}) RETURN n"
        
        records, summary, keys = self.driver.execute_query(
            query_string,
            database_= self.name,
        )

        try:
            return next(iter(records)).data()
        except:
            return "ERROR: Node not found"


    def __lookup_node_property(self, type, id_type, id_value, property_name):
        """return node property data or error string
        Lookup individual property value from a node
        """
        id_value = str(id_value)
        query_string = "MATCH (n:" + type + " {" + id_type + ": '" + id_value + "'}) RETURN n." + property_name + " AS " + property_name
        
        records, summary, keys = self.driver.execute_query(
            query_string,
            database_= self.name,
        )
        
        try:
            return next(iter(records)).data()[property_name]
        except:
            return "ERROR: Property not found"
        
        
    def __delete_node_with_connections(self, type, id_type, id_value, exclude_relationships = None):
        """return useful string message
        Delete node and all related nodes with incoming connections 0..n deep. Possible to exclude relationships.
        """
        id_value = str(id_value)
        if exclude_relationships == None:
            query_string = "MATCH (n:" + type + " {" + id_type + ": '" + id_value + "'}) <- [*0..] - (d) DETACH DELETE n WITH DISTINCT d DETACH DELETE d"
        # todo: make this work with list of exclusions
        elif isinstance(exclude_relationships,list):
            exclude_relationships = "','".join(exclude_relationships)
            query_string = "MATCH (n:" + type + " {" + id_type + ": '" + id_value + "'}) <- [r*0..] - (d) WHERE NONE ( rel IN r WHERE type(rel) IN ['"+ exclude_relationships + "']) DETACH DELETE n WITH DISTINCT d DETACH DELETE d"
        elif isinstance(exclude_relationships,str):
            query_string = "MATCH (n:" + type + " {" + id_type + ": '" + id_value + "'}) <- [r*0..] - (d) WHERE NONE ( rel IN r WHERE type(rel) = '"+ exclude_relationships + "') DETACH DELETE n WITH DISTINCT d DETACH DELETE d"
        else:
            return "ERROR: exclude_relationships was something else than None, string or list of string"
        
        self.driver.execute_query(
            query_string,
            database_= self.name,
        )
        return type + "(" + id_value + ") deleted with connections"

    def __delete_node(self, type, id_type, id_value):
        """return useful string message
        Delete a node and it's connections
        """
        id_value = str(id_value)
        query_string = "MATCH (n:" + type + " {" + id_type + ": '" + id_value + "'}) DETACH DELETE n"
        
        self.driver.execute_query(
            query_string,
            database_= self.name,
        )
        return type + "(" + id_value + ") deleted"
    

    def __remove_property(self, type, id_type, id_value, property_name):
        """return useful string message
        Remove node property.
        """
        id_value = str(id_value)
        query_string = "MATCH (n:" + type + " {" + id_type + ": '" + id_value + "'}) REMOVE n." + property_name
        
        self.driver.execute_query(
            query_string,
            database_= self.name,
        )
        return "Removed: " + type + "(" + id_value + ")." + property_name
    

    def __connect_with_relationship(self, type_a, id_type_a, id_value_a, type_b, id_type_b, id_value_b, relationship_type):
        """return useful string message
        Connect node a to node b with specific relationship. (a)-[rela]->(b).
        """
        id_value_a = str(id_value_a)
        id_value_b = str(id_value_b)
        query_string = "MATCH (a:" + type_a + " {" + id_type_a + ": '" + id_value_a + "'}) MATCH (b:" + type_b + " {" + id_type_b + ": '" + id_value_b + "'}) MERGE (a)-[:" + relationship_type + "]->(b)"

        self.driver.execute_query(
            query_string,
            database_= self.name,
        )
        return "Connected: " + type_a + "(" + id_value_a + ")-[" + relationship_type + "]>" + type_b + "(" + id_value_b + ")"
    
    def __copy_node(self, type, id_type, id_value, node_type_new, id_type_new, id_value_new):
        """return useful string message
        Copy node into a new node type.
        """
        id_value = str(id_value)
        id_value_new = str(id_value_new)
        query_string = "MATCH (n:" + type + " {" + id_type + ": '" + id_value + "'}) MERGE (m:" + node_type_new + " {" + id_type_new + ": '" + id_value_new + "'}) SET m = properties(n)"

        self.driver.execute_query(
            query_string,
            database_= self.name,
        )
        return "Copied " + type + "(" + id_value + ") to " + node_type_new + "(" + id_value_new + ")"
    
    ### Global settings
    def add_global_settings_node(self):
        """Create global settings node"""        
        return self.__add_node(self.global_settings_type, self.global_settings_id, self.global_settings_id_value)


    def set_global_settings_property(self, property_name, new_data):
        """Set global settings property data.""" 
        return self.__set_node_property(self.global_settings_type, self.global_settings_id, self.global_settings_id_value, property_name, new_data)
    
        
    def remove_global_settings_property(self, property_name):
        """Removes specific Settings property data (and property)""" 
        return self.__remove_property(self.global_settings_type, self.global_settings_id, self.global_settings_id_value, property_name)


    def lookup_global_settings_property(self, property_name):
        """Return data of specific property from settings""" 
        return self.__lookup_node_property(self.global_settings_type, self.global_settings_id, self.global_settings_id_value, property_name)
    

    def delete_global_settings(self):
        """Delete global settings node""" 
        return self.__delete_node(self.global_settings_type, self.global_settings_id, self.global_settings_id_value)
    

    ### User settings
    def add_user_settings_node(self, id_value):
        """Create user settings node"""        
        return self.__add_node(self.user_settings_type, self.user_settings_id, id_value)


    def set_user_settings_property(self, id_value, property_name, new_data):
        """Set user settings property. Creates/overwrites current data.""" 
        return self.__set_node_property(self.user_settings_type, self.user_settings_id, id_value, property_name, new_data)
    
        
    def remove_user_settings_property(self, id_value, property_name):
        """Removes specific Settings property data (and property)""" 
        return self.__remove_property(self.user_settings_type, self.user_settings_id, id_value, property_name)


    def lookup_user_settings_property(self, id_value, property_name):
        """Return data of specific property from settings""" 
        return self.__lookup_node_property(self.user_settings_type, self.user_settings_id, id_value, property_name)
    

    def delete_user_settings(self, id_value):
        """Delete global settings node""" 
        return self.__delete_node(self.user_settings_type, self.user_settings_id, id_value)
    

    ### Project
    def add_project_node(self, id_value):
        """Create Project node. Avoids duplicates."""        
        return self.__add_node(self.project_type, self.project_id, id_value)


    def set_project_property(self, id_value, property_name, new_data):
        """Set Project property. Creates/overwrites current data.""" 
        return self.__set_node_property(self.project_type, self.project_id, id_value, property_name, new_data)
    
        
    def remove_project_property(self, id_value, property_name):
        """Removes specific Project property data (and property)""" 
        return self.__remove_property(self.project_type, self.project_id, id_value, property_name)


    def lookup_project_property(self, id_value, property_name):
        """Return data of specific property from Project""" 
        return self.__lookup_node_property(self.project_type, self.project_id, id_value, property_name)
    

    def delete_project(self, id_value):
        """Delete project node""" 
        return self.__delete_node_with_connections(self.project_type, self.project_id, id_value, self.project_exclusion)

