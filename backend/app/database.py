from neo4j import GraphDatabase
from dotenv import load_dotenv
from enum import Enum
from datetime import datetime
import os

class NodeProperties:
    """All allowed property names for each node type.
    Check Database class init for reserved names for identifier usage before adding new property names.
    """
    class GlobalSettings(Enum):
        # Settings
        # example <FOO> = "foo"
        TEST_PASS = "test_pass"
        TEST_FAIL = "test_fail"


    class UserSettings(Enum):
        # User settings
        # example <FOO> = "foo"
        NAME = "name"

        TEST_PASS = "test_pass"
        TEST_FAIL = "test_fail"


    # has only one property, enforced by function call
    #class Dataset(Enum):
        # Dataset
        # example <FOO> = "foo"
    #    FILE_NAME = "file_name"


    class DataModel(Enum):
        # Data model
        # example <FOO> = "foo"
        NAME = "name"
        NODE_TYPES = "node_types"
        RELATIONSHIP_TYPES = "relationship_types"

        TEST_PASS = "test_pass"
        TEST_FAIL = "test_fail"


    class Blueprint(Enum):
        # Blueprint
        # example <FOO> = "foo"
        NAME = "name"
        DESCRIPTION = "description"
        QUESTIONS = "questions"

        TEST_PASS = "test_pass"
        TEST_FAIL = "test_fail"
    

    class AnalyzeModel(Enum):
        # Analyze model
        # example <FOO> = "foo"
        NAME = "name"
        KEYWORDS = "keywords"

        TEST_PASS = "test_pass"
        TEST_FAIL = "test_fail"


    class Project(Enum):
        # Project
        # example <FOO> = "foo"
        NAME = "name"
        
        TEST_PASS = "test_pass"
        TEST_FAIL = "test_fail"


    class ResultBlueprint(Enum):
        # Result
        # example <FOO> = "foo"
        FILENAME = "filename"
        RESULT = "result"
        DATETIME = "datetime"

        TEST_PASS = "test_pass"
        TEST_FAIL = "test_fail"


class Database:
    def __init__(self) -> None:
        """Start up database connection.
        Setup types and identifier names according to database design v4.
        """
        #self.__enum_properties = NodeProperties()

        self.__driver = GraphDatabase.driver(os.getenv('NEO4J_URL'), auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD')))
        self.__name = os.getenv('NEO4J_DB_NAME')

        self.__global_settings_type = 'Settings'
        self.__global_settings_id = 'name'
        self.__global_settings_id_value = 'Global'

        self.__user_settings_type = 'UserSettings'
        self.__user_settings_id = 'user_name'
        
        self.__dataset_type = 'Dataset'
        self.__dataset_id = 'id'
        self.__dataset_property = 'file_name' # only one known property
        
        self.__data_model_type = 'DataModel'
        self.__data_model_id = 'id'
        
        self.__analyze_model_type = 'AnalyzeModel'
        self.__analyze_model_id = 'id'

        self.__blueprint_type = 'Blueprint'
        self.__blueprint_id = 'id'
        
        self.__project_type = 'Project'
        self.__project_id = 'id'
        self.__project_exclusion = ['FAVORITED_IN'] # exclusion relationships for deletion
        
        self.__result_blueprint_type = 'ResultBlueprint'
        self.__result_blueprint_id = 'id'
        
        self.__used_dataset_type = 'UsedDataSet'
        self.__used_dataset_id = 'id'

        self.__used_data_model_type = 'UsedDataModel'
        self.__used_data_model_id = 'id'

        self.__used_blueprint_type = 'UsedBlueprint'
        self.__used_blueprint_id = 'id'

        self.__used_analyze_model_type = 'UsedAnalyzeModel'
        self.__used_analyze_model_id = 'id'
        
        # model related connections
        self.__connect_dataset_data_model = 'USED_FOR_TRAINING'
        self.__connect_dataset_analyze_model = 'USED_FOR_TRAINING'

        # project related connections
        self.__connect_dataset_project = 'ANALYZED_IN'
        self.__connect_result_project = 'BELONGS_TO'

        # model(s) used to construct the data structure in project, used for making result node (complicated way)
        # probably useless
        #self.__connect_data_model_project = 'ACTIVE_IN' 

        # result node related
        #self.__connect_used_analyze_model_result = 'USED_IN_ANALYSIS' # directs to old result
        self.__connect_used_data_model_result_blueprint = 'USED_IN_ANALYSIS'
        self.__connect_used_dataset_result_blueprint = 'USED_IN_ANALYSIS'
        self.__connect_used_blueprint_result_blueprint = 'USED_IN_ANALYSIS'
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
    

    def __add_node(self, type, id_type, id_value = None):
        """return value of node identifier on successful creation, None if database query error.
        Create a node with specific node-type, id-type and it's value.
        """
        # check if node already exists
        if self.__does_node_exist(type, id_type, id_value):
            return False

        if id_value == None:
            query_string = (
                "CREATE (n:" + type + " {" + id_type + ": randomUUID()}) "
                "RETURN n." + id_type + " AS " + id_type
            )
        else:
            #id_value = str(id_value)
            query_string = (
                "MERGE (n:" + type + " {" + id_type + ": '" + id_value + "'}) "
                "RETURN n." + id_type + " AS " + id_type
            )

        try:
            records, summary, keys = self.__driver.execute_query(
                query_string,
                database_= self.__name,
            )
            return next(iter(records)).data()[id_type]
        except:
            return None
            

    def __set_node_property(self, type, id_type, id_value, property_name, new_data):
        """return True when query succeeded
        Set specific node property with new data.
        """
        # check if node exists
        if not self.__does_node_exist(type, id_type, id_value):
            return False
        
        id_value = str(id_value)
        query_string = (
            "MATCH (n:" + type + " {" + id_type + ": '" + id_value + "'}) "
            "SET n." + property_name + " = $old_data" 
        )

        try:
            self.__driver.execute_query(
                query_string,
                old_data = new_data,
                database_= self.__name,
            )
        except:
            return False

        return True
    

    def __lookup_whole_node(self, type, id_type, id_value):
        """return whole node data or None if nothing was found
        Lookup a node and return all it's data
        """
        id_value = str(id_value)
        query_string = (
            "MATCH (n:" + type + " {" + id_type + ": '" + id_value + "'}) "
            "RETURN n"
        )

        records, summary, keys = self.__driver.execute_query(
            query_string,
            database_= self.__name,
        )

        try:
            return next(iter(records)).data()
        except:
            return None


    def __lookup_node_property(self, type, id_type, id_value, property_name):
        """return node property data or None if nothing was found
        Lookup individual property value from a node
        """
        id_value = str(id_value)
        query_string = (
            "MATCH (n:" + type + " {" + id_type + ": '" + id_value + "'}) "
            "RETURN n." + property_name + " AS " + property_name
        )

        records, summary, keys = self.__driver.execute_query(
            query_string,
            database_= self.__name,
        )
        
        try:
            return next(iter(records)).data()[property_name]
        except:
            return None


    def __lookup_nodes(self, type, id_type, property_name, parent_info = None):
        """return nodes with (id, property_name) combo or None if nothing was found
        optional: parent_info dict includes: {node_type, id_type, id_value} to search under certain node
        """

        if parent_info == None:
            query_string = (
                "MATCH (n:" + type + " ) "
                "RETURN COLLECT ([n." + id_type + ", n." + property_name + "]) AS list"
            )
        else:
            query_string = (
                "MATCH (n:" + type + " ) - [] -> (:" + parent_info["node_type"] + " {" + parent_info["id_type"] + ": '" + parent_info["id_value"] + "'}) "
                "RETURN COLLECT ([n." + id_type + ", n." + property_name + "]) AS list"
            )

        records, summary, keys = self.__driver.execute_query(
            query_string,
            database_= self.__name,
        )
        
        try:
            # gives out [[ ]]
            double_list = next(iter(records)).data()['list']
            single_list = [item for sublist in double_list for item in sublist]
            return single_list
        except:
            return None
        
        
    def __delete_node_with_connections(self, type, id_type, id_value, exclude_relationships = None):
        """return True when query succeeded
        Delete node and all related nodes with incoming connections 0..n deep. Possible to exclude relationships.
        """
        # check if node exists
        if not self.__does_node_exist(type, id_type, id_value):
            return False

        id_value = str(id_value)

        # Supporting: None, string list, single string
        if exclude_relationships == None:
            query_string = (
                "MATCH (n:" + type + " {" + id_type + ": '" + id_value + "'}) <- [*0..] - (d) "
                "DETACH DELETE n "
                "WITH DISTINCT d "
                "DETACH DELETE d"
            )
        elif isinstance(exclude_relationships,list):
            exclude_relationships = "','".join(exclude_relationships)
            query_string = (
                "MATCH (n:" + type + " {" + id_type + ": '" + id_value + "'}) <- [r*0..] - (d) "
                "WHERE NONE ( rel IN r WHERE type(rel) IN ['"+ exclude_relationships + "']) "
                "DETACH DELETE n "
                "WITH DISTINCT d "
                "DETACH DELETE d"
            )
        elif isinstance(exclude_relationships,str):
            query_string = (
                "MATCH (n:" + type + " {" + id_type + ": '" + id_value + "'}) <- [r*0..] - (d) "
                "WHERE NONE ( rel IN r WHERE type(rel) = '"+ exclude_relationships + "') "
                "DETACH DELETE n "
                "WITH DISTINCT d "
                "DETACH DELETE d"
            )
        else:
            #return "ERROR: exclude_relationships was something else than None, string or list of string"
            return False
        
        try:
            self.__driver.execute_query(
                query_string,
                database_= self.__name,
            )
        except:
            return False

        return True

    def __delete_node(self, type, id_type, id_value):
        """return True when query succeeded
        Delete a node and it's connections
        """
        # check if node exists
        if not self.__does_node_exist(type, id_type, id_value):
            return False

        id_value = str(id_value)
        query_string = (
            "MATCH (n:" + type + " {" + id_type + ": '" + id_value + "'}) "
            "DETACH DELETE n"
        )
        
        try:
            self.__driver.execute_query(
                query_string,
                database_= self.__name,
            )
        except:
            return False

        return True
    

    def __remove_property(self, type, id_type, id_value, property_name):
        """return True when query succeeded
        Remove node property.
        """
        # check if property exists
        if not self.__does_property_exist(type, id_type, id_value, property_name):
            return False

        id_value = str(id_value)
        query_string = (
            "MATCH (n:" + type + " {" + id_type + ": '" + id_value + "'}) "
            "REMOVE n." + property_name
        )
        
        try:
            self.__driver.execute_query(
                query_string,
                database_= self.__name,
            )
        except:
            return False

        return True
    

    def __connect_with_relationship(self, type_a, id_type_a, id_value_a, type_b, id_type_b, id_value_b, relationship_type):
        """return True when query succeeded
        Connect node a to node b with specific relationship. (a)-[rel]->(b).
        """
        # check if node a exists
        if not self.__does_node_exist(type_a, id_type_a, id_value_a):
            return False
        
        # check if node b exists
        if not self.__does_node_exist(type_b, id_type_b, id_value_b):
            return False

        id_value_a = str(id_value_a)
        id_value_b = str(id_value_b)
        query_string = (
            "MATCH (a:" + type_a + " {" + id_type_a + ": '" + id_value_a + "'}) "
            "MATCH (b:" + type_b + " {" + id_type_b + ": '" + id_value_b + "'}) "
            "MERGE (a)-[r:" + relationship_type + "]->(b)"
        )

        try:
            self.__driver.execute_query(
                query_string,
                database_= self.__name,
            )
        except:
            return False

        return True
    
    def __copy_node(self, type, id_type, id_value, node_type_new, id_type_new, id_value_new = None):
        """return id of new node when copy succeeded, None if failed
        new id value is optional
        Copy node into a new node type.
        """
        id_value = str(id_value)
        if id_value_new == None:
            query_string = (
                "MATCH (n:" + type + " {" + id_type + ": '" + id_value + "'}) "
                "CREATE (m:" + node_type_new + ") "
                "SET m = properties(n) "
                "SET m." + id_type_new + " = randomUUID() "
                "RETURN m." + id_type + " AS " + id_type
        )
        else:
            id_value_new = str(id_value_new)
            query_string = (
                "MATCH (n:" + type + " {" + id_type + ": '" + id_value + "'}) "
                "CREATE (m:" + node_type_new + " ) "
                "SET m = properties(n) "
                "SET m." + id_type_new + " = '" + id_value_new + "' "
                "RETURN m." + id_type_new + " AS " + id_type_new
            )

        try:
            records, summary, keys = self.__driver.execute_query(
                query_string,
                database_= self.__name,
            )
            return next(iter(records)).data()[id_type]
        except:
            return None


    def __lookup_node_neighbours(self, type_parent, id_type_parent, id_value_parent, type, id_type, relationship):
        """return return id of new node when copy succeeded, None if failed
        Copy node into a new node type.
        """
        id_value_parent = str(id_value_parent)
        query_string = (
            "MATCH (n:" + type + ") - [:" + relationship + "] -> (:" + type_parent + " {" + id_type_parent + ": '" + id_value_parent + "'}) "
            "RETURN COLLECT (n." + id_type + ") AS list"
        )

        try:
            records, summary, keys = self.__driver.execute_query(
                query_string,
                database_= self.__name,
            )
            filter_to_list = next(iter(records)).data()['list']

            return filter_to_list

        except:
            return None

    
    def __lookup_connected_node_property(self, type_a, id_type_a, id_value_a, relationship_type, property_name):
        """return node property data or None
        Lookup individual property value from a neighboring node that is connected by certain relationship
        """
        id_value_a = str(id_value_a)
        query_string = (
            "MATCH (a:" + type_a + " {" + id_type_a + ": '" + id_value_a + "'}) <- [:" + relationship_type + "] - (b) "
            "RETURN b." + property_name + " AS " + property_name
        )
        
        try:
            records, summary, keys = self.__driver.execute_query(
                query_string,
                database_= self.__name,
            )
            return next(iter(records)).data()[property_name]
        except:
            return None
    
    def __does_property_exist(self, type, id_type, id_value, property_name):
        """return true/false
        Check if node exists with specific node type and property value
        """
        id_value = str(id_value)
        query_string = (
            "MATCH (a:" + type + " {" + id_type + ": '" + id_value + "'}) "
            "WHERE a." + property_name + " IS NOT NULL "
            "RETURN a"
        )

        try:
            records, summary, keys = self.__driver.execute_query(
                query_string,
                database_= self.__name,
            )

            if not records:
                return False
            else:
                return True
        except:
            return False
        
    def __does_node_exist(self, type, id_type, id_value):
        """return true/false
        Check if node exists with specific node type and property value
        """
        id_value = str(id_value)
        query_string = (
            "MATCH (a:" + type + " {" + id_type + ": '" + id_value + "'}) "
            "RETURN a"
        )

        try:
            records, summary, keys = self.__driver.execute_query(
                query_string,
                database_= self.__name,
            )
            if not records:
                return False
            else:
                return True
        except:
            return False


    
    ### Connections
    def connect_dataset_to_data_model(self, dataset_id_value, data_model_id_value):
        """Connect Dataset to DataModel"""
        return self.__connect_with_relationship(self.__dataset_type, self.__dataset_id, dataset_id_value, self.__data_model_type, self.__data_model_id, data_model_id_value, self.__connect_dataset_data_model)
    

    def connect_dataset_to_analyze_model(self, dataset_id_value, analyze_model_id_value):
        """Connect Dataset to AnalyzeModel"""
        return self.__connect_with_relationship(self.__dataset_type, self.__dataset_id, dataset_id_value, self.__analyze_model_type, self.__analyze_model_id, analyze_model_id_value, self.__connect_dataset_analyze_model)
    

    # probably useless
    #def connect_data_model_to_project(self, data_model_id_value, project_id_value):
    #    """Connect DataModel to Project"""
    #    return self.__connect_with_relationship(self.__data_model_type, self.__data_model_id, data_model_id_value, self.__project_type, self.__project_id, project_id_value, self.__connect_data_model_project)


    def connect_dataset_to_project(self, dataset_id_value, project_id_value):
        """Connect Dataset to Project"""
        return self.__connect_with_relationship(self.__dataset_type, self.__dataset_id, dataset_id_value, self.__project_type, self.__project_id, project_id_value, self.__connect_dataset_project)


    def connect_result_blueprint_to_project(self, result_id_value, project_id_value):
        """Connect Result to Project"""
        return self.__connect_with_relationship(self.__result_blueprint_type, self.__result_blueprint_id, result_id_value, self.__project_type, self.__project_id, project_id_value, self.__connect_result_project)
    

    def __connect_used_dataset_to_result_blueprint(self, used_dataset_id_value, result_id_value):
        """Connect UsedDataset to ResultBlueprint"""
        return self.__connect_with_relationship(self.__used_dataset_type, self.__used_dataset_id, used_dataset_id_value, self.__result_blueprint_type, self.__result_blueprint_id, result_id_value, self.__connect_used_dataset_result_blueprint)


    # todo: this is old result
    #def __connect_used_analyze_model_to_result(self, used_analyze_model_id_value, result_id_value):
    #    """Connect UsedAnalyzeModel to Result"""
    #    return self.__connect_with_relationship(self.__used_analyze_model_type, self.__used_analyze_model_id, used_analyze_model_id_value, self.__result_type, self.__result_id, result_id_value, self.__connect_used_analyze_model_result)
    

    def __connect_used_data_model_to_result_blueprint(self, used_data_model_id_value, result_id_value):
        """Connect UsedDataModel to ResultBlueprint"""
        return self.__connect_with_relationship(self.__used_data_model_type, self.__used_data_model_id, used_data_model_id_value, self.__result_blueprint_type, self.__result_blueprint_id, result_id_value, self.__connect_used_data_model_result_blueprint)


    def connect_used_blueprint_to_result_blueprint(self, used_blueprint_id_value, result_id_value):
        """Connect UsedBlueprint to ResultBlueprint"""
        return self.__connect_with_relationship(self.__used_blueprint_type, self.__used_blueprint_id, used_blueprint_id_value, self.__result_blueprint_type, self.__result_blueprint_id, result_id_value, self.__connect_used_blueprint_result_blueprint)


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


    def set_global_settings_property(self, property_name: NodeProperties.GlobalSettings, new_data):
        """Set global settings property data.""" 
        return self.__set_node_property(self.__global_settings_type, self.__global_settings_id, self.__global_settings_id_value, property_name.value, new_data)
    
        
    def remove_global_settings_property(self, property_name: NodeProperties.GlobalSettings):
        """Removes specific Settings property data (and property)""" 
        return self.__remove_property(self.__global_settings_type, self.__global_settings_id, self.__global_settings_id_value, property_name.value)


    def lookup_global_settings_property(self, property_name: NodeProperties.GlobalSettings):
        """Return data of specific property from settings""" 
        return self.__lookup_node_property(self.__global_settings_type, self.__global_settings_id, self.__global_settings_id_value, property_name.value)
    

    def delete_global_settings(self):
        """Delete global settings node""" 
        return self.__delete_node(self.__global_settings_type, self.__global_settings_id, self.__global_settings_id_value)
    

    def get_global_settings_id_type(self):
        """Get global settings id type""" 
        return self.__global_settings_id
    

    ### User settings
    def add_user_settings_node(self, id_value):
        """Create user settings node"""        
        return self.__add_node(self.__user_settings_type, self.__user_settings_id, id_value)


    def set_user_settings_property(self, id_value, property_name: NodeProperties.UserSettings, new_data):
        """Set user settings property. Creates/overwrites current data.""" 
        return self.__set_node_property(self.__user_settings_type, self.__user_settings_id, id_value, property_name.value, new_data)
    
        
    def remove_user_settings_property(self, id_value, property_name: NodeProperties.UserSettings):
        """Removes specific user settings property data (and property)""" 
        return self.__remove_property(self.__user_settings_type, self.__user_settings_id, id_value, property_name.value)


    def lookup_user_settings_property(self, id_value, property_name: NodeProperties.UserSettings):
        """Return data of specific property from user settings""" 
        return self.__lookup_node_property(self.__user_settings_type, self.__user_settings_id, id_value, property_name.value)
    

    def lookup_data_model_nodes(self):
        """Return list of user settings"""
        return self.__lookup_nodes(self.__user_settings_type, self.__user_settings_id, NodeProperties.UserSettings.NAME.value)
    

    def delete_user_settings(self, id_value):
        """Delete user settings node""" 
        return self.__delete_node(self.__user_settings_type, self.__user_settings_id, id_value)
    

    def get_user_settings_id_type(self):
        """Get user settings id type""" 
        return self.__user_settings_id
    

    ### Project
    def add_project_node(self):
        """Create Project node. Avoids duplicates."""        
        return self.__add_node(self.__project_type, self.__project_id)


    def set_project_property(self, id_value, property_name: NodeProperties.Project, new_data):
        """Set Project property. Creates/overwrites current data.""" 
        return self.__set_node_property(self.__project_type, self.__project_id, id_value, property_name.value, new_data)
    
        
    def remove_project_property(self, id_value, property_name: NodeProperties.Project):
        """Removes specific Project property data (and property)""" 
        return self.__remove_property(self.__project_type, self.__project_id, id_value, property_name.value)


    def lookup_project_property(self, id_value, property_name: NodeProperties.Project):
        """Return data of specific property from Project""" 
        return self.__lookup_node_property(self.__project_type, self.__project_id, id_value, property_name.value)
    

    def lookup_project_nodes(self):
        """Return list of Projects"""
        return self.__lookup_nodes(self.__project_type, self.__project_id, NodeProperties.Project.NAME.value)
    

    def delete_project(self, id_value):
        """Delete project node""" 
        return self.__delete_node_with_connections(self.__project_type, self.__project_id, id_value, self.__project_exclusion)
    

    def get_project_id_type(self):
        """Get project id type""" 
        return self.__project_id
    


    ### Dataset
    def add_dataset_node(self):
        """Create Dataset node. Avoids duplicates."""        
        return self.__add_node(self.__dataset_type, self.__dataset_id)


    def set_dataset_property(self, id_value, new_data):
        """Set Dataset property. Creates/overwrites current data.""" 
        return self.__set_node_property(self.__dataset_type, self.__dataset_id, id_value, self.__dataset_property, new_data)
    
        
    def lookup_dataset_property(self, id_value):
        """Return data of specific property from Dataset""" 
        return self.__lookup_node_property(self.__dataset_type, self.__dataset_id, id_value, self.__dataset_property)
    

    def remove_dataset_property(self, id_value):
        """Remove data of specific property from Dataset"""
        return self.__remove_property(self.__dataset_type, self.__dataset_id, id_value, self.__dataset_property)
    

    def delete_dataset(self, id_value):
        """Delete Dataset node"""
        return self.__delete_node(self.__dataset_type, self.__dataset_id, id_value)
    

    def get_dataset_id_type(self):
        """Get dataset id type""" 
        return self.__dataset_id
    

    ### DataModel
    def add_data_model_node(self):
        """Create DataModel node. Avoids duplicates."""
        return self.__add_node(self.__data_model_type, self.__data_model_id)


    def set_data_model_property(self, id_value, property_name: NodeProperties.DataModel, new_data):
        """Set DataModel property. Creates/overwrites current data.""" 
        return self.__set_node_property(self.__data_model_type, self.__data_model_id, id_value, property_name.value, new_data)
    
        
    def remove_data_model_property(self, id_value, property_name: NodeProperties.DataModel):
        """Removes specific DataModel property data (and property)""" 
        return self.__remove_property(self.__data_model_type, self.__data_model_id, id_value, property_name.value)


    def lookup_data_model_property(self, id_value, property_name: NodeProperties.DataModel):
        """Return data of specific property from DataModel""" 
        return self.__lookup_node_property(self.__data_model_type, self.__data_model_id, id_value, property_name.value)
    
    def lookup_data_model_nodes(self):
        """Return list of DataModel"""
        return self.__lookup_nodes(self.__data_model_type, self.__data_model_id, NodeProperties.DataModel.NAME.value)
    

    def delete_data_model(self, id_value):
        """Delete DataModel node""" 
        return self.__delete_node_with_connections(self.__data_model_type, self.__data_model_id, id_value)
    

    def get_data_model_id_type(self):
        """Get DataModel id type""" 
        return self.__data_model_id
    

    ### Blueprint
    def add_blueprint_node(self):
        """Create Blueprint node. Avoids duplicates."""
        return self.__add_node(self.__blueprint_type, self.__blueprint_id)


    def set_blueprint_property(self, id_value, property_name: NodeProperties.DataModel, new_data):
        """Set Blueprint property. Creates/overwrites current data.""" 
        return self.__set_node_property(self.__blueprint_type, self.__blueprint_id, id_value, property_name.value, new_data)
    
        
    def remove_blueprint_property(self, id_value, property_name: NodeProperties.DataModel):
        """Removes specific Blueprint property data (and property)""" 
        return self.__remove_property(self.__blueprint_type, self.__blueprint_id, id_value, property_name.value)


    def lookup_blueprint_property(self, id_value, property_name: NodeProperties.DataModel):
        """Return data of specific property from Blueprint""" 
        return self.__lookup_node_property(self.__blueprint_type, self.__blueprint_id, id_value, property_name.value)
    

    def lookup_blueprint_nodes(self):
        """Return list of Blueprint"""
        return self.__lookup_nodes(self.__blueprint_type, self.__blueprint_id, NodeProperties.Blueprint.NAME.value)
    

    def delete_blueprint(self, id_value):
        """Delete Blueprint node""" 
        return self.__delete_node_with_connections(self.__blueprint_type, self.__blueprint_id, id_value)
    

    def get_blueprint_id_type(self):
        """Get Blueprint id type""" 
        return self.__blueprint_id


    ### AnalyzeModel
    def add_analyze_model_node(self):
        """Create AnalyzeModel node. Avoids duplicates."""
        return self.__add_node(self.__analyze_model_type, self.__analyze_model_id)


    def set_analyze_model_property(self, id_value, property_name: NodeProperties.AnalyzeModel, new_data):
        """Set AnalyzeModel property. Creates/overwrites current data.""" 
        return self.__set_node_property(self.__analyze_model_type, self.__analyze_model_id, id_value, property_name.value, new_data)
    
        
    def remove_analyze_model_property(self, id_value, property_name: NodeProperties.AnalyzeModel):
        """Removes specific AnalyzeModel property data (and property)""" 
        return self.__remove_property(self.__analyze_model_type, self.__analyze_model_id, id_value, property_name.value)


    def lookup_analyze_model_property(self, id_value, property_name: NodeProperties.AnalyzeModel):
        """Return data of specific property from AnalyzeModel""" 
        return self.__lookup_node_property(self.__analyze_model_type, self.__analyze_model_id, id_value, property_name.value)
    

    def lookup_analyze_model_nodes(self):
        """Return list of AnalyzeModel"""
        return self.__lookup_nodes(self.__analyze_model_type, self.__analyze_model_id, NodeProperties.AnalyzeModel.NAME.value)


    def delete_analyze_model(self, id_value):
        """Delete AnalyzeModel node""" 
        return self.__delete_node_with_connections(self.__analyze_model_type, self.__analyze_model_id, id_value)
    
   
    def get_analyze_model_id_type(self):
        """Get AnalyzeModel id type""" 
        return self.__analyze_model_id

    ### Used dataset
    def __set_used_dataset_property(self, id_value, new_data):
        """Set Used Dataset property. Creates/overwrites current data.""" 
        return self.__set_node_property(self.__used_dataset_type, self.__used_dataset_id, id_value, self.__dataset_property, new_data)

    ### Result Blueprint

    # if datasets for result are present in database when pressing analyse
    # def add_result_blueprint_node(self, dataset_ids, blueprint_ids, datamodel_ids):
    #     """Create Result-blueprint node. Avoids duplicates."""
    #     try:
    #         result_blueprint_id = self.__add_node(self.__result_blueprint_type, self.__result_blueprint_id)
            
            
    #         # copy nodes into used node versions and connect them to result
    #         for id in dataset_ids:
    #             used_dataset_id = self.__copy_node(self.__dataset_type, id, self.__used_dataset_type)
    #             if not self.__connect_used_dataset_to_result_blueprint(used_dataset_id, result_blueprint_id): return None

    #         for id in blueprint_ids:
    #             used_blueprint_id = self.__copy_node(self.__blueprint_type, id, self.__used_blueprint_type)
    #             if not self.__connect_used_blueprint_to_result_blueprint(used_blueprint_id, result_blueprint_id): return None

    #         for id in datamodel_ids:
    #             used_data_model_id = self.__copy_node(self.__data_model_type, id, self.__used_data_model_type)
    #             if not self.__connect_used_data_model_to_result_blueprint(used_data_model_id, result_blueprint_id): return None

    #         return result_blueprint_id
    #     except:
    #         return None
    
    """
    def add_result_blueprint_node(self, project_id, dataset_list, blueprint_ids, datamodel_ids):
        ""Create Result-blueprint node. Avoids duplicates.""
        # try:
            
        result_blueprint_id = self.__add_node(self.__result_blueprint_type, self.__result_blueprint_id)
        self.set_result_blueprint_property(result_blueprint_id, NodeProperties.ResultBlueprint.DATETIME, datetime.now().isoformat())
        
        # copy nodes into used node versions and connect them to result
        for file_name in dataset_list:
            used_dataset_id = self.__add_node(self.__used_dataset_type, self.__used_dataset_id)
            self.__set_used_dataset_property(used_dataset_id, file_name)
            self.__connect_used_dataset_to_result_blueprint(used_dataset_id, result_blueprint_id)

        for id in blueprint_ids:
            used_blueprint_id = self.__copy_node(self.__blueprint_type, self.__blueprint_id, id, self.__used_blueprint_type, self.__used_blueprint_id)
            self.__connect_used_blueprint_to_result_blueprint(used_blueprint_id, result_blueprint_id)

        for id in datamodel_ids:
            used_data_model_id = self.__copy_node(self.__data_model_type, self.__data_model_id, id, self.__used_data_model_type, self.__used_data_model_id)

            datamodel_dataset_ids = self.__lookup_node_neighbours(self.__data_model_type, self.__data_model_id, id, self.__dataset_type, self.__dataset_id, self.__connect_dataset_data_model) 
            if datamodel_dataset_ids != None:
                for datamodel_dataset_id in datamodel_dataset_ids:
                    new_used_dataset_id = self.__copy_node(self.__dataset_type, self.__dataset_id, datamodel_dataset_id, self.__used_dataset_type, self.__used_dataset_id)
                    self.__connect_used_dataset_to_used_data_model(new_used_dataset_id, used_data_model_id)

            self.__connect_used_data_model_to_result_blueprint(used_data_model_id, result_blueprint_id)

        self.__connect_result_blueprint_to_project(result_blueprint_id, project_id)

        return result_blueprint_id
        # except:
        #     return None
        """
    
    def add_result_blueprint_node(self):
        return self.__add_node(self.__result_blueprint_type, self.__result_blueprint_id)

    def set_result_blueprint_property(self, id_value, property_name: NodeProperties.ResultBlueprint, new_data):
        """Set Result-blueprint property. Creates/overwrites current data.""" 
        return self.__set_node_property(self.__result_blueprint_type, self.__result_blueprint_id, id_value, property_name.value, new_data)


    def remove_result_blueprint_property(self, id_value, property_name: NodeProperties.ResultBlueprint):
        """Removes specific Project property data (and property)""" 
        return self.__remove_property(self.__result_blueprint_type, self.__result_blueprint_id, id_value, property_name.value)


    def lookup_result_blueprint_property(self, id_value, property_name: NodeProperties.ResultBlueprint):
        """Return data of specific property from Result-blueprint""" 
        return self.__lookup_node_property(self.__result_blueprint_type, self.__result_blueprint_id, id_value, property_name.value)
    
    def lookup_result_blueprint_nodes(self, project_id):
        """Return list of result_blueprints from specific project""" 
        project_info = { "node_type" : self.__project_type, "id_type" : self.__project_id, "id_value" : project_id }
        return self.__lookup_nodes(self.__result_blueprint_type, self.__result_blueprint_id, NodeProperties.ResultBlueprint.DATETIME.value, project_info)

    def delete_result_blueprint(self, id_value):
        """Delete Result-blueprint node""" 
        return self.__delete_node_with_connections(self.__result_blueprint_type, self.__result_blueprint_id, id_value)
    

    def get_result_blueprint_id_type(self):
        """Get Result-blueprint id type""" 
        return self.__result_blueprint_id


