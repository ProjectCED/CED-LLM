from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

class database:
    def __init__(self) -> None:
        """Start up database connection.
        Setup types and identifier names according to database design.
        """
        self.__driver = GraphDatabase.driver(os.getenv('NEO4J_URL'), auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD')))
        self.__name = 'neo4j'     # database name

        self.__global_settings_type = 'Settings'
        self.__global_settings_id = 'name'
        self.__global_settings_id_value = 'Global'

        self.__user_settings_type = 'UserSettings'
        self.__user_settings_id = 'user_name'
        
        self.__dataset_type = 'Dataset'
        self.__dataset_id = 'id'
        
        self.__data_model_type = 'DataModel'
        self.__data_model_id = 'id'
        
        self.__analyze_model_type = 'AnalyzeModel'
        self.__analyze_model_id = 'id'
        
        self.__project_type = 'Project'
        self.__project_id = 'id'
        self.__project_exclusion = ['FAVORITED_IN'] # exclusion for deletion
        
        self.__result_type = 'Result'
        self.__result_id = 'id'
        
        self.__used_dataset_type = 'UsedDataSet'
        self.__used_dataset_id = 'id'

        self.__used_data_model_type = 'UsedDataModel'
        self.__used_data_model_id = 'id'

        self.__used_analyze_model_type = 'UsedAnalyzeModel'
        self.__used_analyze_model_id = 'id'
        

        self.__connect_dataset_data_model = 'USED_FOR_TRAINING'
        self.__connect_dataset_analyze_model = 'USED_FOR_TRAINING'

        self.__connect_dataset_project = 'ANALYZED_IN'
        self.__connect_result_project = 'BELONGS_TO'
        self.__connect_data_model_project = 'ACTIVE_IN'

        self.__connect_used_analyze_model_result = 'USED_IN_ANALYSIS'
        self.__connect_used_data_model_result = 'USED_IN_ANALYSIS'
        self.__connect_used_dataset_result = 'USED_IN_ANALYSIS'
        self.__connect_used_dataset_used_data_model = 'USED_FOR_TRAINING'
        self.__connect_used_dataset_used_analyze_model = 'USED_FOR_TRAINING'


    def debug_clear_all(self):
        """return useful string message
        DEBUG: Clear the whole database
        """
        self.__driver.execute_query(
            "MATCH (n) DETACH DELETE n",
            database_= self.__name,
        )
        return "Database cleared"


    def debug_show_all(self):
        """return useful string message
        DEBUG: Print the whole database in console.
        """
        records, summary, keys = self.__driver.execute_query(
            "MATCH (n) RETURN n",
            database_= self.__name,
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

        self.__driver.execute_query(
            query_string,
            value = id_value,
            database_= self.__name,
        )
        return "Added node: " + type + "." + id_type + "(" + id_value + ")"
            

    def __set_node_property(self, type, id_type, id_value, property_name, new_data):
        """return useful string message
        Set specific node property with new data.
        """
        id_value = str(id_value)
        query_string = "MATCH (n:" + type + " {" + id_type + ": '" + id_value + "'}) SET n." + property_name + " = $old_data"

        self.__driver.execute_query(
            query_string,
            old_data = new_data,
            database_= self.__name,
        )
        return "Modified data: " + type + "("+ id_value +")."+ property_name
    

    def __lookup_whole_node(self, type, id_type, id_value):
        """return whole node data or error string
        Lookup a node and return all it's data
        """
        id_value = str(id_value)
        query_string = "MATCH (n:" + type + " {" + id_type + ": '" + id_value + "'}) RETURN n"
        
        records, summary, keys = self.__driver.execute_query(
            query_string,
            database_= self.__name,
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
        
        records, summary, keys = self.__driver.execute_query(
            query_string,
            database_= self.__name,
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
        elif isinstance(exclude_relationships,list):
            exclude_relationships = "','".join(exclude_relationships)
            query_string = "MATCH (n:" + type + " {" + id_type + ": '" + id_value + "'}) <- [r*0..] - (d) WHERE NONE ( rel IN r WHERE type(rel) IN ['"+ exclude_relationships + "']) DETACH DELETE n WITH DISTINCT d DETACH DELETE d"
        elif isinstance(exclude_relationships,str):
            query_string = "MATCH (n:" + type + " {" + id_type + ": '" + id_value + "'}) <- [r*0..] - (d) WHERE NONE ( rel IN r WHERE type(rel) = '"+ exclude_relationships + "') DETACH DELETE n WITH DISTINCT d DETACH DELETE d"
        else:
            return "ERROR: exclude_relationships was something else than None, string or list of string"
        
        self.__driver.execute_query(
            query_string,
            database_= self.__name,
        )
        return type + "(" + id_value + ") deleted with connections"

    def __delete_node(self, type, id_type, id_value):
        """return useful string message
        Delete a node and it's connections
        """
        id_value = str(id_value)
        query_string = "MATCH (n:" + type + " {" + id_type + ": '" + id_value + "'}) DETACH DELETE n"
        
        self.__driver.execute_query(
            query_string,
            database_= self.__name,
        )
        return type + "(" + id_value + ") deleted"
    

    def __remove_property(self, type, id_type, id_value, property_name):
        """return useful string message
        Remove node property.
        """
        id_value = str(id_value)
        query_string = "MATCH (n:" + type + " {" + id_type + ": '" + id_value + "'}) REMOVE n." + property_name
        
        self.__driver.execute_query(
            query_string,
            database_= self.__name,
        )
        return "Removed: " + type + "(" + id_value + ")." + property_name
    

    def __connect_with_relationship(self, type_a, id_type_a, id_value_a, type_b, id_type_b, id_value_b, relationship_type):
        """return useful string message
        Connect node a to node b with specific relationship. (a)-[rela]->(b).
        """
        id_value_a = str(id_value_a)
        id_value_b = str(id_value_b)
        query_string = "MATCH (a:" + type_a + " {" + id_type_a + ": '" + id_value_a + "'}) MATCH (b:" + type_b + " {" + id_type_b + ": '" + id_value_b + "'}) MERGE (a)-[:" + relationship_type + "]->(b)"

        self.__driver.execute_query(
            query_string,
            database_= self.__name,
        )
        return "Connected: " + type_a + "(" + id_value_a + ")-[" + relationship_type + "]>" + type_b + "(" + id_value_b + ")"
    
    def __copy_node(self, type, id_type, id_value, node_type_new, id_type_new, id_value_new):
        """return useful string message
        Copy node into a new node type.
        """
        id_value = str(id_value)
        id_value_new = str(id_value_new)
        query_string = "MATCH (n:" + type + " {" + id_type + ": '" + id_value + "'}) MERGE (m:" + node_type_new + " {" + id_type_new + ": '" + id_value_new + "'}) SET m = properties(n)"

        self.__driver.execute_query(
            query_string,
            database_= self.__name,
        )
        return "Copied " + type + "(" + id_value + ") to " + node_type_new + "(" + id_value_new + ")"
    
    def __lookup_connected_node_property(self, type_a, id_type_a, id_value_a, relationship_type, property_name):
        """return node property data or error string
        Lookup individual property value from a neighboring node that is connected by certain relationship
        """
        id_value_a = str(id_value_a)
        query_string = "MATCH (a:" + type_a + " {" + id_type_a + ": '" + id_value_a + "'}) <- [:" + relationship_type + "] - (b) RETURN b." + property_name + " AS " + property_name
        
        records, summary, keys = self.__driver.execute_query(
            query_string,
            database_= self.__name,
        )
        
        try:
            return next(iter(records)).data()[property_name]
        except:
            return "ERROR: Property not found"
    
    def __does_node_property_exist(self, type, id_type, id_value):
        """return true/false
        Check if node exists with specific node type and property value
        """
        id_value = str(id_value)
        query_string = "MATCH (a:" + type + " {" + id_type + ": '" + id_value + "'}) RETURN a"
        
        records, summary, keys = self.__driver.execute_query(
            query_string,
            database_= self.__name,
        )

        if not records:
            return False
        else:
            return True


    
    ### Connections
    def connect_dataset_to_data_model(self, dataset_id_value, data_model_id_value):
        """Connect Dataset to DataModel"""
        return self.__connect_with_relationship(self.__dataset_type, self.__dataset_id, dataset_id_value, self.__data_model_type, self.__data_model_id, data_model_id_value, self.__connect_dataset_data_model)
    

    def connect_dataset_to_analyze_model(self, dataset_id_value, analyze_model_id_value):
        """Connect Dataset to AnalyzeModel"""
        return self.__connect_with_relationship(self.__dataset_type, self.__dataset_id, dataset_id_value, self.__analyze_model_type, self.__analyze_model_id, analyze_model_id_value, self.__connect_dataset_analyze_model)
    

    def connect_data_model_to_project(self, data_model_id_value, project_id_value):
        """Connect DataModel to Project"""
        return self.__connect_with_relationship(self.__data_model_type, self.__data_model_id, data_model_id_value, self.__project_type, self.__project_id, project_id_value, self.__connect_data_model_project)


    def connect_dataset_to_project(self, dataset_id_value, project_id_value):
        """Connect Dataset to Project"""
        return self.__connect_with_relationship(self.__dataset_type, self.__dataset_id, dataset_id_value, self.__project_type, self.__project_id, project_id_value, self.__connect_dataset_project)


    def __connect_result_to_project(self, result_id_value, project_id_value):
        """Connect Result to Project"""
        return self.__connect_with_relationship(self.__result_type, self.__result_id, result_id_value, self.__project_type, self.__project_id, project_id_value, self.__connect_result_project)
    

    def __connect_used_dataset_to_result(self, used_dataset_id_value, result_id_value):
        """Connect UsedDataset to Result"""
        return self.__connect_with_relationship(self.__used_dataset_type, self.__used_dataset_id, used_dataset_id_value, self.__result_type, self.__result_id, result_id_value, self.__connect_used_dataset_result)


    def __connect_used_analyze_model_to_result(self, used_analyze_model_id_value, result_id_value):
        """Connect UsedAnalyzeModel to Result"""
        return self.__connect_with_relationship(self.__used_analyze_model_type, self.__used_analyze_model_id, used_analyze_model_id_value, self.__result_type, self.__result_id, result_id_value, self.__connect_used_analyze_model_result)
    

    def __connect_used_data_model_to_result(self, used_data_model_id_value, result_id_value):
        """Connect UsedDataModel to Result"""
        return self.__connect_with_relationship(self.__used_data_model_type, self.__used_data_model_id, used_data_model_id_value, self.__result_type, self.__result_id, result_id_value, self.__connect_used_data_model_result)
    

    def __connect_used_dataset_to_used_data_model(self, used_dataset_id_value, used_data_model_id_value):
        """Connect UsedDataset to UsedDataModel"""
        return self.__connect_with_relationship(self.__used_dataset_type, self.__used_dataset_id, used_dataset_id_value, self.__used_data_model_type, self.__used_data_model_id, used_data_model_id_value, self.__connect_used_dataset_used_data_model)
    

    def __connect_used_dataset_to_used_analyze_model(self, used_dataset_id_value, used_analyze_model_id_value):
        """Connect UsedDataset to UsedAnalyzeModel"""
        return self.__connect_with_relationship(self.__used_dataset_type, self.__used_dataset_id, used_dataset_id_value, self.__used_analyze_model_type, self.__used_analyze_model_id, used_analyze_model_id_value, self.__connect_used_dataset_used_analyze_model)

    
    ### Global settings
    def add_global_settings_node(self):
        """Create global settings node"""        
        return self.__add_node(self.__global_settings_type, self.__global_settings_id, self.__global_settings_id_value)


    def set_global_settings_property(self, property_name, new_data):
        """Set global settings property data.""" 
        return self.__set_node_property(self.__global_settings_type, self.__global_settings_id, self.__global_settings_id_value, property_name, new_data)
    
        
    def remove_global_settings_property(self, property_name):
        """Removes specific Settings property data (and property)""" 
        return self.__remove_property(self.__global_settings_type, self.__global_settings_id, self.__global_settings_id_value, property_name)


    def lookup_global_settings_property(self, property_name):
        """Return data of specific property from settings""" 
        return self.__lookup_node_property(self.__global_settings_type, self.__global_settings_id, self.__global_settings_id_value, property_name)
    

    def delete_global_settings(self):
        """Delete global settings node""" 
        return self.__delete_node(self.__global_settings_type, self.__global_settings_id, self.__global_settings_id_value)
    

    ### User settings
    def add_user_settings_node(self, id_value):
        """Create user settings node"""        
        return self.__add_node(self.__user_settings_type, self.__user_settings_id, id_value)


    def set_user_settings_property(self, id_value, property_name, new_data):
        """Set user settings property. Creates/overwrites current data.""" 
        return self.__set_node_property(self.__user_settings_type, self.__user_settings_id, id_value, property_name, new_data)
    
        
    def remove_user_settings_property(self, id_value, property_name):
        """Removes specific Settings property data (and property)""" 
        return self.__remove_property(self.__user_settings_type, self.__user_settings_id, id_value, property_name)


    def lookup_user_settings_property(self, id_value, property_name):
        """Return data of specific property from settings""" 
        return self.__lookup_node_property(self.__user_settings_type, self.__user_settings_id, id_value, property_name)
    

    def delete_user_settings(self, id_value):
        """Delete global settings node""" 
        return self.__delete_node(self.__user_settings_type, self.__user_settings_id, id_value)
    

    ### Project
    def add_project_node(self, id_value):
        """Create Project node. Avoids duplicates."""        
        return self.__add_node(self.__project_type, self.__project_id, id_value)


    def set_project_property(self, id_value, property_name, new_data):
        """Set Project property. Creates/overwrites current data.""" 
        return self.__set_node_property(self.__project_type, self.__project_id, id_value, property_name, new_data)
    
        
    def remove_project_property(self, id_value, property_name):
        """Removes specific Project property data (and property)""" 
        return self.__remove_property(self.__project_type, self.__project_id, id_value, property_name)


    def lookup_project_property(self, id_value, property_name):
        """Return data of specific property from Project""" 
        return self.__lookup_node_property(self.__project_type, self.__project_id, id_value, property_name)
    

    def delete_project(self, id_value):
        """Delete project node""" 
        return self.__delete_node_with_connections(self.__project_type, self.__project_id, id_value, self.__project_exclusion)
    


    ### Dataset
    def add_dataset_node(self, id_value):
        """Create Dataset node. Avoids duplicates."""        
        return self.__add_node(self.__dataset_type, self.__dataset_id, id_value)


    def set_dataset_property(self, id_value, property_name, new_data):
        """Set Dataset property. Creates/overwrites current data.""" 
        return self.__set_node_property(self.__dataset_type, self.__dataset_id, id_value, property_name, new_data)
    
        
    def lookup_dataset_property(self, id_value, property_name):
        """Return data of specific property from Dataset""" 
        return self.__lookup_node_property(self.__dataset_type, self.__dataset_id, id_value, property_name)
    

    def delete_dataset(self, id_value):
        """Delete Dataset node"""
        return self.__delete_node(self.__dataset_type, self.__dataset_id, id_value)
    

    ### DataModel
    def add_data_model_node(self, id_value):
        """Create DataModel node. Avoids duplicates."""
        return self.__add_node(self.__data_model_type, self.__data_model_id, id_value)


    def set_data_model_property(self, id_value, property_name, new_data):
        """Set DataModel property. Creates/overwrites current data.""" 
        return self.__set_node_property(self.__data_model_type, self.__data_model_id, id_value, property_name, new_data)
    
        
    def remove_data_model_property(self, id_value, property_name):
        """Removes specific DataModel property data (and property)""" 
        return self.__remove_property(self.__data_model_type, self.__data_model_id, id_value, property_name)


    def lookup_data_model_property(self, id_value, property_name):
        """Return data of specific property from DataModel""" 
        return self.__lookup_node_property(self.__data_model_type, self.__data_model_id, id_value, property_name)
    

    def delete_data_model(self, id_value):
        """Delete DataModel node""" 
        return self.__delete_node_with_connections(self.__data_model_type, self.__data_model_id, id_value)
    


        ### AnalyzeModel
    def add_analyze_model_node(self, id_value):
        """Create AnalyzeModel node. Avoids duplicates."""
        return self.__add_node(self.__analyze_model_type, self.__analyze_model_id, id_value)


    def set_analyze_model_property(self, id_value, property_name, new_data):
        """Set AnalyzeModel property. Creates/overwrites current data.""" 
        return self.__set_node_property(self.__analyze_model_type, self.__analyze_model_id, id_value, property_name, new_data)
    
        
    def remove_analyze_model_property(self, id_value, property_name):
        """Removes specific AnalyzeModel property data (and property)""" 
        return self.__remove_property(self.__analyze_model_type, self.__analyze_model_id, id_value, property_name)


    def lookup_analyze_model_property(self, id_value, property_name):
        """Return data of specific property from AnalyzeModel""" 
        return self.__lookup_node_property(self.__analyze_model_type, self.__analyze_model_id, id_value, property_name)
    

    def delete_analyze_model(self, id_value):
        """Delete AnalyzeModel node""" 
        return self.__delete_node_with_connections(self.__analyze_model_type, self.__analyze_model_id, id_value)

   

    ### Result
    # Todo: not needing to put id values(bad dupes), accept multiple relationships and accept no relationships
    
    # def add_result_node(self, result_id_value, project_id_value, analyze_model_id_value, used_analyze_model_id_value, used_dataset_id_value, used_data_model_id_value):
    #     """Create Result node with all the connected information."""
    #     return_a = self.__add_node(self.__result_type, self.__result_id, result_id_value)
    #     return_b = self.__connect_result_to_project(result_id_value, project_id_value)
    #     ### search connected Dataset, make a copy of that and connect it
    #     project_dataset_id_value = self.__lookup_connected_node_property(self.__project_type, self.__project_id, project_id_value, self.__connect_dataset_project, self.__dataset_id)
    #     return_e = self.__copy_node(self.__dataset_type, self.__dataset_id, project_dataset_id_value, self.__used_dataset_type, self.__used_dataset_id, used_dataset_id_value)
    #     return_f = self.__connect_used_dataset_to_result(used_dataset_id_value, result_id_value)

    #     ### make a copy of AnalyzeModel and connect it
    #     return_c = self.__copy_node(self.__analyze_model_type, self.__analyze_model_id, analyze_model_id_value, self.__used_analyze_model_type, self.__used_analyze_model_id, used_analyze_model_id_value)
    #     return_d = self.__connect_used_analyze_model_to_result(used_analyze_model_id_value, result_id_value)
    #     ### search connected Dataset, make a copy of that and connect it
    #     analyze_model_dataset_id_value = self.__lookup_connected_node_property(self.__analyze_model_type, self.__analyze_model_id, analyze_model_id_value, self.__connect_dataset_analyze_model, self.__dataset_id)
    #     return_e = self.__copy_node(self.__dataset_type, self.__dataset_id, analyze_model_dataset_id_value, self.__used_dataset_type, self.__used_dataset_id, 3)
    #     return_f = self.__connect_used_dataset_to_used_analyze_model(3, used_analyze_model_id_value)

    #     ### search connected DataModel, make a copy of that and connect it
    #     project_data_model_id_value = self.__lookup_connected_node_property(self.__project_type, self.__project_id, project_id_value, self.__connect_data_model_project, self.__data_model_id)
    #     return_e = self.__copy_node(self.__data_model_type, self.__data_model_id, project_data_model_id_value, self.__used_data_model_type, self.__used_data_model_id, used_data_model_id_value)
    #     return_f = self.__connect_used_data_model_to_result(used_data_model_id_value, result_id_value)
    #     ### search connected Dataset, make a copy of that and connect it
    #     data_model_dataset_id_value = self.__lookup_connected_node_property(self.__data_model_type, self.__data_model_id, project_data_model_id_value, self.__connect_dataset_data_model, self.__dataset_id)
    #     return_g = self.__copy_node(self.__dataset_type, self.__dataset_id, data_model_dataset_id_value, self.__used_dataset_type, self.__used_dataset_id, 2)
    #     return_h = self.__connect_used_dataset_to_used_data_model(2, used_data_model_id_value)

    #     return "result node created"

    def set_result_property(self, id_value, property_name, new_data):
        """Set Result property. Creates/overwrites current data.""" 
        return self.__set_node_property(self.__result_type, self.__result_id, id_value, property_name, new_data)
    
    def lookup_result_property(self, id_value, property_name):
        """Return data of specific property from Result""" 
        return self.__lookup_node_property(self.__result_type, self.__result_id, id_value, property_name)
    
    def delete_result(self, id_value):
        """Delete Result node""" 
        return self.__delete_node_with_connections(self.__result_type, self.__result_id, id_value)


