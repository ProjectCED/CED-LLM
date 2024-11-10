from neo4j import GraphDatabase
#from neo4j.exceptions import Neo4jError #using normal Exception
from dotenv import load_dotenv
from enum import Enum
from datetime import datetime
import os

class NodeProperties:
    """All allowed property names for each node label.

    Add more properties here when needed, but check Database class init for reserved names for identifier usage before adding new property names.
    """
    class GlobalSettings(Enum):
        # Settings
        # example FOO = "foo"
        TEST_PASS = "test_pass"
        TEST_FAIL = "test_fail"


    class UserSettings(Enum):
        # User settings
        # example FOO = "foo"
        NAME = "name"

        TEST_PASS = "test_pass"
        TEST_FAIL = "test_fail"


    # has only one property, enforced by function call
    #class Dataset(Enum):
        # Dataset
        # example FOO = "foo"
    #    FILE_NAME = "file_name"


    class DataModel(Enum):
        # Data model
        # example FOO = "foo"
        NAME = "name"
        NODE_LABELS = "node_labes"
        RELATIONSHIP_TYPES = "relationship_types"

        TEST_PASS = "test_pass"
        TEST_FAIL = "test_fail"


    class Blueprint(Enum):
        # Blueprint
        # example FOO = "foo"
        NAME = "name"
        DESCRIPTION = "description"
        QUESTIONS = "questions"

        TEST_PASS = "test_pass"
        TEST_FAIL = "test_fail"
    

    class AnalyzeModel(Enum):
        # Analyze model
        # example FOO = "foo"
        NAME = "name"
        KEYWORDS = "keywords"

        TEST_PASS = "test_pass"
        TEST_FAIL = "test_fail"


    class Project(Enum):
        # Project
        # example FOO = "foo"
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

class DatabaseMeta(type):
    """
    A metaclass for creating singleton classes.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]    


class Database(metaclass=DatabaseMeta):
    """
    Manages database query's from backend to Neo4j database.

    Enforced to be Singleton class.
    """
    def __init__(self) -> None:
        """Start up database driver.
        Setup (according to database design v4):
          - labels
          - identifier names
          - relationship types
        """

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
        self.__connect_project_user_settings = 'OWNED_BY'
        self.__connect_blueprint_user_settings = 'OWNED_BY'


    def debug_clear_all(self):
        """
        DEBUG: Clear the whole database
        
        Returns:
            string: "Database cleared"
        """
        self.__driver.execute_query(
            "MATCH (n) DETACH DELETE n",
            database_= self.__name,
        )
        return "Database cleared"


    def debug_show_all(self):
        """
        DEBUG: Print the whole database in console.


        Returns:
            string: "Whole database printed out in console"
        """
        records, summary, keys = self.__driver.execute_query(
            "MATCH (n) RETURN n",
            database_= self.__name,
        )
        
        for record in records:
            print(record)

        return "Whole database printed out in console"
    

    def __add_node(self, type, id_type, id_value = None):
        """
        Create a node.

        Args:
            type (string): Node label
            id_type (string): Node property for id usage
            id_value (string, optional): Value for the id

        Raises:
            RuntimeError: If database query error.

        Returns:
            string or None:
                - string containing ID value for the created node.
                - None if node already exists.
        """
        # check if node already exists
        if self.__does_node_exist(type, id_type, id_value):
            return None

        if id_value == None:
            query_string = (
                "CREATE (n:" + type + " {" + id_type + ": randomUUID()}) "
                "RETURN n." + id_type + " AS " + id_type
            )
        else:
            id_value = str(id_value)
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
        
        except Exception as e:
            error_string = str(e)
            raise RuntimeError( "Neo4j add_node() query failed: " + error_string )
            

    def __set_node_property(self, type, id_type, id_value, property_name, new_data):
        """
        Create/modify specific node property with new data.

        Args:
            type (string): Node label
            id_type (string): Node id(property)
            id_value (string): Value for the id
            property_name (string): property name to create/modify
            new_data (Any): value for the property

        Raises:
            RuntimeError: If database query error.

        Returns:
            bool:
                - True when query succeeded.
                - False if node was not found.
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
            return True
        
        except Exception as e:
            error_string = str(e)
            raise RuntimeError( "Neo4j set_property_value() query failed: " + error_string )
    

    def __lookup_whole_node(self, type, id_type, id_value):
        """
        Lookup a node and return all it's data

        Args:
            type (string): Node label
            id_type (string): Node id(property)
            id_value (string): Value for the id

        Raises:
            RuntimeError: If database query error.            

        Returns:
            Any: whole node data or None otherwise.
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
        except Exception as e:
            error_string = str(e)
            raise RuntimeError( "Neo4j lookup_whole_node() query failed: " + error_string )


    def __lookup_node_property(self, type, id_type, id_value, property_name):
        """
        Lookup individual property value from a node.

        Args:
            type (string): Node label
            id_type (string): Node id(property)
            id_value (string): Value for the id
            property_name (string): property name to return it's value

        Raises:
            RuntimeError: If database query error.   

        Returns:
            Any or None:
                - Any if found, single node property data.
                - None if nothing was found.
        """
        id_value = str(id_value)
        query_string = (
            "MATCH (n:" + type + " {" + id_type + ": '" + id_value + "'}) "
            "RETURN n." + property_name + " AS " + property_name
        )

        try:
            records, summary, keys = self.__driver.execute_query(
                query_string,
                database_= self.__name,
            )
            
            try:
                return next(iter(records)).data()[property_name]
            except:
                return None
        
        except Exception as e:
            error_string = str(e)
            raise RuntimeError( "Neo4j lookup_node_property query failed: " + error_string )


    def __lookup_nodes(self, type, id_type, property_name, parent_info = None):
        """
        Lookup nodes and return list of them in a [[ID, property_name]] combo.

        Args:
            type (string): Node label
            id_type (string): Node id(property)
            id_value (string): Value for the id
            property_name (string): property name to create/modify
            parent_info (dict, optional): Where relationship is pointing at
                Expected keys:
                - 'node_type' (string): Node label
                - 'id_type' (string): Node id(property)
                - 'id_value' (string): Value for the id

        Raises:
            RuntimeError: If database query error.   

        Returns:
            list[string, Any] or None:
                - [ID, property_name value] A list of found nodes with ID and wanted property combination.
                - None if nothing was found.
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

        try:
            records, summary, keys = self.__driver.execute_query(
                query_string,
                database_= self.__name,
            )
        
            try:
                # gives out [[ ]]
                double_list = next(iter(records)).data()['list']
                return double_list
            except:
                return None
        
        except Exception as e:
            error_string = str(e)
            raise RuntimeError( "Neo4j lookup_nodes() query failed: " + error_string )
        
        
    def __delete_node_with_connections(self, label, id_type, id_value, exclude_relationships = None):
        """
        Delete node and all related nodes with incoming relationships 0..n deep. Possible to exclude relationships.

        Args:
            label (string): Node label
            id_type (string): Node id(property)
            id_value (string): Value for the id
            exclude_relationships (string or list[string], optional): Relationships to exclude from deletion

        Raises:
            RuntimeError: If database query error.
            TypeError: If exclude_relationships is wrong type.

        Returns:
            bool:
                - True when query succeeded.
                - False if node exists.
        """
        # check if node exists
        if not self.__does_node_exist(label, id_type, id_value):
            return False

        id_value = str(id_value)

        # Supporting: None, string list, single string
        # TODO: something wrong here if trying to use exclusion
        if exclude_relationships == None:
            query_string = (
                "MATCH (n:" + label + " {" + id_type + ": '" + id_value + "'}) <- [*0..] - (d) "
                "DETACH DELETE n "
                "WITH DISTINCT d "
                "DETACH DELETE d"
            )
        elif isinstance(exclude_relationships,list) and all(isinstance(item,str) for item in list):
            exclude_relationships = "','".join(exclude_relationships)
            query_string = (
                "MATCH (n:" + label + " {" + id_type + ": '" + id_value + "'}) <- [r*0..] - (d) "
                "WHERE NONE ( rel IN r WHERE type(rel) IN ['"+ exclude_relationships + "']) "
                "DETACH DELETE n "
                "WITH DISTINCT d "
                "DETACH DELETE d"
            )
        elif isinstance(exclude_relationships,str):
            query_string = (
                "MATCH (n:" + label + " {" + id_type + ": '" + id_value + "'}) <- [r*0..] - (d) "
                "WHERE NONE ( rel IN r WHERE type(rel) = '"+ exclude_relationships + "') "
                "DETACH DELETE n "
                "WITH DISTINCT d "
                "DETACH DELETE d"
            )
        else:
            return TypeError( "Invalid exclude_relationships type: " + type(exclude_relationships) )
        
        try:
            self.__driver.execute_query(
                query_string,
                database_= self.__name,
            )

            return True

        except Exception as e:
            error_string = str(e)
            raise RuntimeError( "Neo4j delete_node_with_connections() query failed: " + error_string )


    def __delete_node(self, type, id_type, id_value):
        """
        Delete a node and it's connections

        Args:
            type (string): Node label
            id_type (string): Node id(property)
            id_value (string): Value for the id

        Raises:
            RuntimeError: If database query error.
            
        Returns:
            bool:
                - True when query succeeded.
                - False when node doesn't exist.
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

            return True

        except Exception as e:
            error_string = str(e)
            raise RuntimeError( "Neo4j delete_node() query failed: " + error_string )
    

    def __remove_property(self, type, id_type, id_value, property_name):
        """
        Remove a node property

        Args:
            type (string): Node label
            id_type (string): Node id(property)
            id_value (string): Value for the id
            property_name (string): property name for removing

        Raises:
            RuntimeError: If database query error.

        Returns:
            bool:
                - True when query succeeded.
                - False when property doesn't exist.
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

            return True

        except Exception as e:
            error_string = str(e)
            raise RuntimeError( "Neo4j remove_property() query failed: " + error_string )
    

    def __connect_with_relationship(self, type_a, id_type_a, id_value_a, type_b, id_type_b, id_value_b, relationship_type):
        """
        Connect node a to node b with specific relationship. (a)-[rel]->(b).

        Args:
            type_a (string): Node label for a
            id_type_a (string): Node id(property) for a
            id_value_a (string): Value for the id for a

            type_b (string): Node label for b
            id_type_b (string): Node id(property) for b
            id_value_b (string): Value for the id for b

            relationship_type (string): relationship type to connect with

        Raises:
            RuntimeError: If database query error.

        Returns:
            bool:
                - True when query succeeded.
                - False when either of the nodes doesn't exist.
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

            return True

        except Exception as e:
            error_string = str(e)
            raise RuntimeError( "Neo4j connect_with_relationship() query failed: " + error_string )

   
    def __copy_node(self, type, id_type, id_value, node_type_new, id_type_new, id_value_new = None):
        """return id of new node when copy succeeded, None if failed
        new id value is optional
        Copy node into a new node label.

        Args:
            type (string): Node label
            id_type (string): Node id(property)
            id_value (string): Value for the id

            node_type_new (string): Node label for new one
            id_type_new (string): Node id(property) for new one
            id_value_new (string, optional): Value for the id

        Raises:
            RuntimeError: If database query error.

        Returns:
            string: string containing ID value for the created node. 
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
        
        except Exception as e:
            error_string = str(e)
            raise RuntimeError( "Neo4j copy_node() query failed: " + error_string )


    def __lookup_node_neighbours(self, type_parent, id_type_parent, id_value_parent, type, id_type, relationship):
        """return return id of new node when copy succeeded, None if failed
        Lookup node neighbours with specific relationship. (n:)-[rel]->(parent:), return list of n.id

        Args:
            type_parent (string): Node label
            id_type_parent (string): Node id(property)
            id_value_parent (string): Value for the id

            type (string): Node label
            id_type (string): Node id(property)

            property_name (string): property name to create/modify
            new_data (Any): value for the property

        Raises:
            RuntimeError: If database query error.

        Returns:
            list[string] or None:
                - list[string] of ID values.
                - None if nothing was found.
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
            try:
                filter_to_list = next(iter(records)).data()['list']
                return filter_to_list
            
            except:
                return None

        except Exception as e:
            error_string = str(e)
            raise RuntimeError( "Neo4j lookup_node_neighbours() query failed: " + error_string )

    
    # def __lookup_connected_node_property(self, type_a, id_type_a, id_value_a, relationship_type, property_name):
    #     """
    #     TODO: only returns top result (single result)

    #     Lookup individual property value from a neighboring node that is connected by certain relationship.
    #     (:)<-[rel]-(b:). return b.<property_name>

    #     Args:
    #         type_a (string): Node label
    #         id_type_a (string): Node id(property)
    #         id_value_a (string): Value for the id
    #         relationship_type (string): relationship type
    #         property_name (string): property name to return it's value

    #     Raises:
    #         RuntimeError: If database query error.

    #     Returns:
    #         Any or None:
    #             - Any single node property data
    #             - None if nothing was found.
    #     """
    #     id_value_a = str(id_value_a)
    #     query_string = (
    #         "MATCH (a:" + type_a + " {" + id_type_a + ": '" + id_value_a + "'}) <- [:" + relationship_type + "] - (b) "
    #         "RETURN b." + property_name + " AS " + property_name
    #     )
        
    #     try:
    #         records, summary, keys = self.__driver.execute_query(
    #             query_string,
    #             database_= self.__name,
    #         )
    #         return next(iter(records)).data()[property_name]
    #     except Exception as e:
    #         error_string = str(e)
    #         raise RuntimeError( "Neo4j lookup_connected_node_property() query failed: " + e )
    
    def __does_property_exist(self, type, id_type, id_value, property_name):
        """
        Check if node with specific node label and property value exists

        Args:
            type (string): Node label
            id_type (string): Node id(property)
            id_value (string): Value for the id
            property_name (string): property name to check

        Raises:
            RuntimeError: If database query error.

        Returns:
            bool:
                - True if property was found.
                - False if not found.
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
            
        except Exception as e:
            error_string = str(e)
            raise RuntimeError( "Neo4j does_property_exist() query failed: " + error_string )
        
    def __does_node_exist(self, type, id_type, id_value):
        """
        Check if node exists with specific node label and id value

        Args:
            type (string): Node label
            id_type (string): Node id(property)
            id_value (string): Value for the id

        Raises:
            RuntimeError: If database query error.

        Returns:
            bool:
                - True if node was found.
                - False if not found.
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
            
        except Exception as e:
            error_string = str(e)
            raise RuntimeError( "Neo4j does_node_exist() query failed: " + error_string )


    
    ### Connections
    def connect_dataset_to_data_model(self, dataset_id_value, data_model_id_value):
        """
        Connect Dataset to DataModel

        Args:
            dataset_id_value (string): Value for the Dataset id
            data_model_id_value (string): Value for the DataModel id

        Raises:
            RuntimeError: If database query error.

        Returns:
            bool:
                - True when query succeeded.
                - False when either of the nodes doesn't exist.
        """
        return self.__connect_with_relationship(self.__dataset_type, self.__dataset_id, dataset_id_value, self.__data_model_type, self.__data_model_id, data_model_id_value, self.__connect_dataset_data_model)
    

    def connect_dataset_to_analyze_model(self, dataset_id_value, analyze_model_id_value):
        """
        Connect Dataset to AnalyzeModel

        Args:
            dataset_id_value (string): Value for the Dataset id
            analyze_model_id_value (string): Value for the AnalyzeModel id

        Raises:
            RuntimeError: If database query error.

        Returns:
            bool:
                - True when query succeeded.
                - False when either of the nodes doesn't exist.
        """
        return self.__connect_with_relationship(self.__dataset_type, self.__dataset_id, dataset_id_value, self.__analyze_model_type, self.__analyze_model_id, analyze_model_id_value, self.__connect_dataset_analyze_model)
    

    # probably useless
    #def connect_data_model_to_project(self, data_model_id_value, project_id_value):
    #    """Connect DataModel to Project"""
    #    return self.__connect_with_relationship(self.__data_model_type, self.__data_model_id, data_model_id_value, self.__project_type, self.__project_id, project_id_value, self.__connect_data_model_project)


    def connect_dataset_to_project(self, dataset_id_value, project_id_value):
        """
        Connect Dataset to Project

        Args:
            dataset_id_value (string): Value for the Dataset id
            project_id_value (string): Value for the Project id

        Raises:
            RuntimeError: If database query error.

        Returns:
            bool:
                - True when query succeeded.
                - False when either of the nodes doesn't exist.
        """
        return self.__connect_with_relationship(self.__dataset_type, self.__dataset_id, dataset_id_value, self.__project_type, self.__project_id, project_id_value, self.__connect_dataset_project)


    def connect_result_blueprint_to_project(self, result_id_value, project_id_value):
        """
        Connect ResultBlueprint to Project

        Args:
            result_id_value (string): Value for the ResultBlueprint id
            project_id_value (string): Value for the Project id

        Raises:
            RuntimeError: If database query error.

        Returns:
            bool:
                - True when query succeeded.
                - False when either of the nodes doesn't exist.
        """
        return self.__connect_with_relationship(self.__result_blueprint_type, self.__result_blueprint_id, result_id_value, self.__project_type, self.__project_id, project_id_value, self.__connect_result_project)
    

    def __connect_used_dataset_to_result_blueprint(self, used_dataset_id_value, result_id_value):
        """
        Connect UsedDataset to ResultBlueprint

        Args:
            used_dataset_id_value (string): Value for the UsedDataset id
            result_id_value (string): Value for the ResultBlueprint id

        Raises:
            RuntimeError: If database query error.

        Returns:
            bool:
                - True when query succeeded.
                - False when either of the nodes doesn't exist.
        """
        return self.__connect_with_relationship(self.__used_dataset_type, self.__used_dataset_id, used_dataset_id_value, self.__result_blueprint_type, self.__result_blueprint_id, result_id_value, self.__connect_used_dataset_result_blueprint)


    # todo: this is old result
    #def __connect_used_analyze_model_to_result(self, used_analyze_model_id_value, result_id_value):
    #    """Connect UsedAnalyzeModel to Result"""
    #    return self.__connect_with_relationship(self.__used_analyze_model_type, self.__used_analyze_model_id, used_analyze_model_id_value, self.__result_type, self.__result_id, result_id_value, self.__connect_used_analyze_model_result)
    

    def __connect_used_data_model_to_result_blueprint(self, used_data_model_id_value, result_id_value):
        """
        Connect UsedDataModel to ResultBlueprint

        Args:
            used_data_model_id_value (string): Value for the UsedDataModel id
            result_id_value (string): Value for the ResultBlueprint id

        Raises:
            RuntimeError: If database query error.

        Returns:
            bool:
                - True when query succeeded.
                - False when either of the nodes doesn't exist.
        """
        return self.__connect_with_relationship(self.__used_data_model_type, self.__used_data_model_id, used_data_model_id_value, self.__result_blueprint_type, self.__result_blueprint_id, result_id_value, self.__connect_used_data_model_result_blueprint)


    def connect_used_blueprint_to_result_blueprint(self, used_blueprint_id_value, result_id_value):
        """
        Connect UsedBlueprint to ResultBlueprint

        Args:
            used_blueprint_id_value (string): Value for the UsedBlueprint id
            result_id_value (string): Value for the ResultBlueprint id

        Raises:
            RuntimeError: If database query error.

        Returns:
            bool:
                - True when query succeeded.
                - False when either of the nodes doesn't exist.
        """
        return self.__connect_with_relationship(self.__used_blueprint_type, self.__used_blueprint_id, used_blueprint_id_value, self.__result_blueprint_type, self.__result_blueprint_id, result_id_value, self.__connect_used_blueprint_result_blueprint)


    def __connect_used_dataset_to_used_data_model(self, used_dataset_id_value, used_data_model_id_value):
        """
        Connect UsedDataset to UsedDataModel

        Args:
            used_dataset_id_value (string): Value for the UsedDataset id
            used_data_model_id_value (string): Value for the UsedDataModel id

        Raises:
            RuntimeError: If database query error.

        Returns:
            bool:
                - True when query succeeded.
                - False when either of the nodes doesn't exist.
        """
        return self.__connect_with_relationship(self.__used_dataset_type, self.__used_dataset_id, used_dataset_id_value, self.__used_data_model_type, self.__used_data_model_id, used_data_model_id_value, self.__connect_used_dataset_used_data_model)
    

    def __connect_used_dataset_to_used_analyze_model(self, used_dataset_id_value, used_analyze_model_id_value):
        """
        Connect UsedDataset to UsedAnalyzeModel
        Args:
            used_dataset_id_value (string): Value for the UsedDataset id
            used_analyze_model_id_value (string): Value for the UsedAnalyzeModel id

        Raises:
            RuntimeError: If database query error.

        Returns:
            bool:
                - True when query succeeded.
                - False when either of the nodes doesn't exist.
        """
        return self.__connect_with_relationship(self.__used_dataset_type, self.__used_dataset_id, used_dataset_id_value, self.__used_analyze_model_type, self.__used_analyze_model_id, used_analyze_model_id_value, self.__connect_used_dataset_used_analyze_model)
    

    def connect_project_to_user_settings(self, project_id_value, user_settings_id_value):
        """
        Connect Project to UserSettings
        Args:
            project_id_value (string): Value for the Project id
            user_settings_id_value (string): Value for the user_settings id

        Raises:
            RuntimeError: If database query error.

        Returns:
            bool:
                - True when query succeeded.
                - False when either of the nodes doesn't exist.
        """
        return self.__connect_with_relationship(self.__project_type, self.__project_id, project_id_value, self.__user_settings_type, self.__user_settings_id, user_settings_id_value, self.__connect_project_user_settings)


    def connect_blueprint_to_user_settings(self, blueprint_id_value, user_settings_id_value):
        """
        Connect Blueprint to UserSettings
        Args:
            blueprint_id_value (string): Value for the Blueprint id
            user_settings_id_value (string): Value for the user_settings id

        Raises:
            RuntimeError: If database query error.

        Returns:
            bool:
                - True when query succeeded.
                - False when either of the nodes doesn't exist.
        """
        return self.__connect_with_relationship(self.__blueprint_type, self.__blueprint_id, blueprint_id_value, self.__user_settings_type, self.__user_settings_id, user_settings_id_value, self.__connect_blueprint_user_settings)

    
    ### Global settings
    def add_global_settings_node(self):
        """
        Create a global settings node.

        Raises:
            RuntimeError: If database query error.

        Returns:
            string or None:
                - string containing ID value for the created node.
                - None if node already exists.
        """
        return self.__add_node(self.__global_settings_type, self.__global_settings_id, self.__global_settings_id_value)


    def set_global_settings_property(self, property_name: NodeProperties.GlobalSettings, new_data):
        """
        Create/modify global settings property data with new data.

        Args:
            property_name (string): property name to create/modify
            new_data (Any): value for the property

        Raises:
            RuntimeError: If database query error.

        Returns:
            bool:
                - True when query succeeded.
                - False if node was not found.
        """ 
        return self.__set_node_property(self.__global_settings_type, self.__global_settings_id, self.__global_settings_id_value, property_name.value, new_data)
    
        
    def remove_global_settings_property(self, property_name: NodeProperties.GlobalSettings):
        """
        Removes specific Settings property data (and property)

        Args:
            property_name (string): property name for removing

        Raises:
            RuntimeError: If database query error.

        Returns:
            bool:
                - True when query succeeded.
                - False when property doesn't exist.
        """ 
        return self.__remove_property(self.__global_settings_type, self.__global_settings_id, self.__global_settings_id_value, property_name.value)


    def lookup_global_settings_property(self, property_name: NodeProperties.GlobalSettings):
        """
        Return data of specific property from settings
        
        Args:
            property_name (string): property name to return it's value

        Raises:
            RuntimeError: If database query error.   

        Returns:
            Any or None:
                - Any if found, single node property data.
                - None if nothing was found.
        """ 
        return self.__lookup_node_property(self.__global_settings_type, self.__global_settings_id, self.__global_settings_id_value, property_name.value)
    

    def delete_global_settings(self):
        """
        Delete global settings node

        Raises:
            RuntimeError: If database query error.
            
        Returns:
            bool:
                - True when query succeeded.
                - False when node doesn't exist.
        """ 
        return self.__delete_node(self.__global_settings_type, self.__global_settings_id, self.__global_settings_id_value)
    

    def get_global_settings_id_type(self):
        """
        TODO: possibly not needed?

        Get global settings id type
        
        Returns:
            string: id name
        """ 
        return self.__global_settings_id
    

    ### User settings
    def add_user_settings_node(self, id_value):
        """
        Create a user settings node

        Args:
            id_type (string): Value for the id

        Raises:
            RuntimeError: If database query error.

        Returns:
            string or None:
                - string containing ID value for the created node.
                - None if node already exists.       
        """
        return self.__add_node(self.__user_settings_type, self.__user_settings_id, id_value)


    def set_user_settings_property(self, id_value, property_name: NodeProperties.UserSettings, new_data):
        """
        Create/modify user settings property data with new data.

        Args:
            id_value (string): Value for the id
            property_name (string): property name to create/modify
            new_data (Any): value for the property

        Raises:
            RuntimeError: If database query error.

        Returns:
            bool:
                - True when query succeeded.
                - False if node was not found.
        """ 
        return self.__set_node_property(self.__user_settings_type, self.__user_settings_id, id_value, property_name.value, new_data)
    
        
    def remove_user_settings_property(self, id_value, property_name: NodeProperties.UserSettings):
        """
        Removes specific user settings property data (and property)

        Args:
            id_value (string): Value for the id
            property_name (string): property name for removing

        Raises:
            RuntimeError: If database query error.

        Returns:
            bool:
                - True when query succeeded.
                - False when property doesn't exist.
        """ 
        return self.__remove_property(self.__user_settings_type, self.__user_settings_id, id_value, property_name.value)


    def lookup_user_settings_property(self, id_value, property_name: NodeProperties.UserSettings):
        """
        Return data of specific property from user settings
        
        Args:
            id_value (string): Value for the id
            property_name (string): property name to return it's value

        Raises:
            RuntimeError: If database query error.   

        Returns:
            Any or None:
                - Any if found, single node property data.
                - None if nothing was found.
        """ 
        return self.__lookup_node_property(self.__user_settings_type, self.__user_settings_id, id_value, property_name.value)
    

    def lookup_data_model_nodes(self):
        """
        Lookup user settings and return list of them in a [[ID, NAME]] combo.

        Raises:
            RuntimeError: If database query error.   

        Returns:
            list[string, string] or None:
                - list[string, string] A list of found nodes with ID and NAME combination.
                - None if nothing was found.
        """
        return self.__lookup_nodes(self.__user_settings_type, self.__user_settings_id, NodeProperties.UserSettings.NAME.value)
    

    def delete_user_settings(self, id_value):
        """
        Delete user settings node
        
        Args:
            id_value (string): Value for the id

        Raises:
            RuntimeError: If database query error.
            
        Returns:
            bool:
                - True when query succeeded.
                - False when node doesn't exist.
        """ 
        return self.__delete_node(self.__user_settings_type, self.__user_settings_id, id_value)
    

    def get_user_settings_id_type(self):
        """
        TODO: possibly not needed?

        Get user settings id type        

        Returns:
            string: id name
        """ 
        return self.__user_settings_id
    

    ### Project
    def add_project_node(self):
        """
        Create a Project node.

        Raises:
            RuntimeError: If database query error.

        Returns:
            string or None:
                - string containing ID value for the created node.
                - None if node already exists.
        """        
        return self.__add_node(self.__project_type, self.__project_id)


    def set_project_property(self, id_value, property_name: NodeProperties.Project, new_data):
        """
        Create/modify Project property data with new data.

        Args:
            id_value (string): Value for the id
            property_name (string): property name to create/modify
            new_data (Any): value for the property

        Raises:
            RuntimeError: If database query error.

        Returns:
            bool:
                - True when query succeeded.
                - False if node was not found.
        """ 
        return self.__set_node_property(self.__project_type, self.__project_id, id_value, property_name.value, new_data)
    
        
    def remove_project_property(self, id_value, property_name: NodeProperties.Project):
        """
        Removes specific Project property data (and property)

        Args:
            id_value (string): Value for the id
            property_name (string): property name for removing

        Raises:
            RuntimeError: If database query error.

        Returns:
            bool:
                - True when query succeeded.
                - False when property doesn't exist.
        """ 
        return self.__remove_property(self.__project_type, self.__project_id, id_value, property_name.value)


    def lookup_project_property(self, id_value, property_name: NodeProperties.Project):
        """
        Return data of specific property from Project
        
        Args:
            id_value (string): Value for the id
            property_name (string): property name to return it's value

        Raises:
            RuntimeError: If database query error.   

        Returns:
            Any or None:
                - Any if found, single node property data.
                - None if nothing was found.
        """ 
        return self.__lookup_node_property(self.__project_type, self.__project_id, id_value, property_name.value)
    

    def lookup_project_nodes(self):
        """
        Lookup Projects and return list of them in a [[ID, NAME]] combo.

        Raises:
            RuntimeError: If database query error.   

        Returns:
            list[string, string] or None:
                - list[string, string] A list of found nodes with ID and NAME combination.
                - None if nothing was found.
        """
        return self.__lookup_nodes(self.__project_type, self.__project_id, NodeProperties.Project.NAME.value)
    

    def delete_project(self, id_value):
        """
        Delete project node and it's related content (results, datasets...)
        
        Args:
            id_value (string): Value for the id

        Raises:
            RuntimeError: If database query error.
            
        Returns:
            bool:
                - True when query succeeded.
                - False when node doesn't exist.
        """ 
        return self.__delete_node_with_connections(self.__project_type, self.__project_id, id_value)
    

    def get_project_id_type(self):
        """
        TODO: possibly not needed?

        Get project id type

        Returns:
            string: id name
        """ 
        return self.__project_id
    


    ### Dataset
    def add_dataset_node(self):
        """
        Create a Dataset node.

        Raises:
            RuntimeError: If database query error.

        Returns:
            string or None:
                - string containing ID value for the created node.
                - None if node already exists.    
        """        
        return self.__add_node(self.__dataset_type, self.__dataset_id)


    def set_dataset_property(self, id_value, new_data):
        """
        Create/modify Dataset property data with new data.

        Args:
            id_value (string): Value for the id
            new_data (Any): value for the property

        Raises:
            RuntimeError: If database query error.

        Returns:
            bool:
                - True when query succeeded.
                - False if node was not found.
        """ 
        return self.__set_node_property(self.__dataset_type, self.__dataset_id, id_value, self.__dataset_property, new_data)
    
        
    def lookup_dataset_property(self, id_value):
        """
        Return data of specific property from Dataset
        
        Args:
            id_value (string): Value for the id
            property_name (string): property name to return it's value

        Raises:
            RuntimeError: If database query error.   

        Returns:
            Any or None:
                - Any if found, single node property data.
                - None if nothing was found.
        """ 
        return self.__lookup_node_property(self.__dataset_type, self.__dataset_id, id_value, self.__dataset_property)


    def lookup_dataset_nodes_data_model(self, parent_id_value):
        """
        Lookup Datasets and return list of them in a [[ID, file_name]] combo.

        Raises:
            RuntimeError: If database query error.   

        Returns:
            list[string, string] or None:
                - list[string, string] A list of found nodes with ID and NAME combination.
                - None if nothing was found.
        """
        parent_info = {'node_type': self.__data_model_type, 'id_type': self.__data_model_id, 'id_value': parent_id_value}
        return self.__lookup_nodes(self.__dataset_type, self.__dataset_id, self.__dataset_property, parent_info)


    def remove_dataset_property(self, id_value):
        """
        TODO: most likely useless function when dataset has only one locked property

        Remove data of specific property from Dataset

        Args:
            id_value (string): Value for the id

        Returns:
            bool: True when query succeeded, False otherwise.
        """
        return self.__remove_property(self.__dataset_type, self.__dataset_id, id_value, self.__dataset_property)
    

    def delete_dataset(self, id_value):
        """
        Delete Dataset node
        
        Args:
            id_value (string): Value for the id

        Raises:
            RuntimeError: If database query error.
            
        Returns:
            bool:
                - True when query succeeded.
                - False when node doesn't exist.
        """
        return self.__delete_node(self.__dataset_type, self.__dataset_id, id_value)
    

    def get_dataset_id_type(self):
        """
        TODO: possibly not needed?

        Get dataset id type

        Returns:
            string: id name
        """ 
        return self.__dataset_id
    

    ### DataModel
    def add_data_model_node(self):
        """
        Create a DataModel node.

        Raises:
            RuntimeError: If database query error.

        Returns:
            string or None:
                - string containing ID value for the created node.
                - None if node already exists.
        """
        return self.__add_node(self.__data_model_type, self.__data_model_id)


    def set_data_model_property(self, id_value, property_name: NodeProperties.DataModel, new_data):
        """
        Create/modify DataModel property data with new data.

        Args:
            id_value (string): Value for the id
            property_name (string): property name to create/modify
            new_data (Any): value for the property

        Raises:
            RuntimeError: If database query error.

        Returns:
            bool:
                - True when query succeeded.
                - False if node was not found.
        """ 
        return self.__set_node_property(self.__data_model_type, self.__data_model_id, id_value, property_name.value, new_data)
    
        
    def remove_data_model_property(self, id_value, property_name: NodeProperties.DataModel):
        """
        Removes specific DataModel property data (and property)
        
        Args:
            id_value (string): Value for the id
            property_name (string): property name for removing

        Raises:
            RuntimeError: If database query error.

        Returns:
            bool:
                - True when query succeeded.
                - False when property doesn't exist.
        """ 
        return self.__remove_property(self.__data_model_type, self.__data_model_id, id_value, property_name.value)


    def lookup_data_model_property(self, id_value, property_name: NodeProperties.DataModel):
        """
        Return data of specific property from DataModel

        Args:
            id_value (string): Value for the id
            property_name (string): property name to return it's value

        Raises:
            RuntimeError: If database query error.   

        Returns:
            Any or None:
                - Any if found, single node property data.
                - None if nothing was found.
        """ 
        return self.__lookup_node_property(self.__data_model_type, self.__data_model_id, id_value, property_name.value)
    
    def lookup_data_model_nodes(self):
        """
        Lookup DataModels and return list of them in a [[ID, NAME]] combo.

        Raises:
            RuntimeError: If database query error.   

        Returns:
            list[string, string] or None:
                - list[string, string] A list of found nodes with ID and NAME combination.
                - None if nothing was found.
        """
        return self.__lookup_nodes(self.__data_model_type, self.__data_model_id, NodeProperties.DataModel.NAME.value)
    

    def delete_data_model(self, id_value):
        """
        Delete DataModel node with related datasets
        
        Args:
            id_value (string): Value for the id

        Raises:
            RuntimeError: If database query error.
            
        Returns:
            bool:
                - True when query succeeded.
                - False when node doesn't exist.
        """ 
        return self.__delete_node_with_connections(self.__data_model_type, self.__data_model_id, id_value)
    

    def get_data_model_id_type(self):
        """
        TODO: possibly not needed?

        Get DataModel id type

        Returns:
            string: id name
        """ 
        return self.__data_model_id
    

    ### Blueprint
    def add_blueprint_node(self):
        """
        Create a Blueprint node.
        
        Raises:
            RuntimeError: If database query error.

        Returns:
            string or None:
                - string containing ID value for the created node.
                - None if node already exists.
        """
        return self.__add_node(self.__blueprint_type, self.__blueprint_id)


    def set_blueprint_property(self, id_value, property_name: NodeProperties.DataModel, new_data):
        """
        Create/modify Blueprint property data with new data.

        Args:
            id_value (string): Value for the id
            property_name (string): property name to create/modify
            new_data (Any): value for the property

        Raises:
            RuntimeError: If database query error.

        Returns:
            bool:
                - True when query succeeded.
                - False if node was not found.
        """ 
        return self.__set_node_property(self.__blueprint_type, self.__blueprint_id, id_value, property_name.value, new_data)
    
        
    def remove_blueprint_property(self, id_value, property_name: NodeProperties.Blueprint):
        """
        Removes specific Blueprint property data (and property)
        
        Args:
            id_value (string): Value for the id
            property_name (string): property name for removing

        Raises:
            RuntimeError: If database query error.

        Returns:
            bool:
                - True when query succeeded.
                - False when property doesn't exist.
        """ 
        return self.__remove_property(self.__blueprint_type, self.__blueprint_id, id_value, property_name.value)


    def lookup_blueprint_property(self, id_value, property_name: NodeProperties.DataModel):
        """
        Return data of specific property from Blueprint
        
        Args:
            id_value (string): Value for the id
            property_name (string): property name to return it's value

        Raises:
            RuntimeError: If database query error.   

        Returns:
            Any or None:
                - Any if found, single node property data.
                - None if nothing was found.
        """ 
        return self.__lookup_node_property(self.__blueprint_type, self.__blueprint_id, id_value, property_name.value)
    

    def lookup_blueprint_nodes(self):
        """
        Lookup Blueprints and return list of them in a [[ID, NAME]] combo.

        Raises:
            RuntimeError: If database query error.   

        Returns:
            list[string, string] or None:
                - list[string, string] A list of found nodes with ID and NAME combination.
                - None if nothing was found.
        """
        return self.__lookup_nodes(self.__blueprint_type, self.__blueprint_id, NodeProperties.Blueprint.NAME.value)
    

    def delete_blueprint(self, id_value):
        """
        Delete Blueprint node with related datasets
        
        Args:
            id_value (string): Value for the id

        Raises:
            RuntimeError: If database query error.
            
        Returns:
            bool:
                - True when query succeeded.
                - False when node doesn't exist.
        """ 
        return self.__delete_node_with_connections(self.__blueprint_type, self.__blueprint_id, id_value)
    

    def get_blueprint_id_type(self):
        """
        TODO: possibly not needed?

        Get Blueprint id type

        Returns:
            string: id name
        """ 
        return self.__blueprint_id


    ### AnalyzeModel
    def add_analyze_model_node(self):
        """
        Create a AnalyzeModel node.

        Raises:
            RuntimeError: If database query error.

        Returns:
            string or None:
                - string containing ID value for the created node.
                - None if node already exists.
        """
        return self.__add_node(self.__analyze_model_type, self.__analyze_model_id)


    def set_analyze_model_property(self, id_value, property_name: NodeProperties.AnalyzeModel, new_data):
        """
        Create/modify AnalyzeModel property data with new data.

        Args:
            id_value (string): Value for the id
            property_name (string): property name to create/modify
            new_data (Any): value for the property

        Raises:
            RuntimeError: If database query error.

        Returns:
            bool:
                - True when query succeeded.
                - False if node was not found.
        """ 
        return self.__set_node_property(self.__analyze_model_type, self.__analyze_model_id, id_value, property_name.value, new_data)
    
        
    def remove_analyze_model_property(self, id_value, property_name: NodeProperties.AnalyzeModel):
        """
        Removes specific AnalyzeModel property data (and property)
        
        Args:
            id_value (string): Value for the id
            property_name (string): property name for removing

        Raises:
            RuntimeError: If database query error.

        Returns:
            bool:
                - True when query succeeded.
                - False when property doesn't exist.
        """ 
        return self.__remove_property(self.__analyze_model_type, self.__analyze_model_id, id_value, property_name.value)


    def lookup_analyze_model_property(self, id_value, property_name: NodeProperties.AnalyzeModel):
        """
        Return data of specific property from AnalyzeModel
        
        Args:
            id_value (string): Value for the id
            property_name (string): property name to return it's value

        Raises:
            RuntimeError: If database query error.   

        Returns:
            Any or None:
                - Any if found, single node property data.
                - None if nothing was found.
        """ 
        return self.__lookup_node_property(self.__analyze_model_type, self.__analyze_model_id, id_value, property_name.value)
    

    def lookup_analyze_model_nodes(self):
        """
        Lookup AnalyzeModels and return list of them in a [[ID, NAME]] combo.

        Raises:
            RuntimeError: If database query error.   

        Returns:
            list[string, string] or None:
                - list[string, string] A list of found nodes with ID and NAME combination.
                - None if nothing was found.
        """
        return self.__lookup_nodes(self.__analyze_model_type, self.__analyze_model_id, NodeProperties.AnalyzeModel.NAME.value)


    def delete_analyze_model(self, id_value):
        """
        Delete AnalyzeModel node with related datasets
        
        Args:
            id_value (string): Value for the id

        Raises:
            RuntimeError: If database query error.
            
        Returns:
            bool:
                - True when query succeeded.
                - False when node doesn't exist.
        """ 
        return self.__delete_node_with_connections(self.__analyze_model_type, self.__analyze_model_id, id_value)
    
   
    def get_analyze_model_id_type(self):
        """
        TODO: possibly not needed?

        Get AnalyzeModel id type
        
        Returns:
            string: id name
        """ 
        return self.__analyze_model_id


    ### Used dataset
    def lookup_used_dataset_property(self, id_value):
        """
        Return data of specific property from UsedDataset
        
        Args:
            id_value (string): Value for the id
            property_name (string): property name to return it's value

        Raises:
            RuntimeError: If database query error.   

        Returns:
            Any or None:
                - Any if found, single node property data.
                - None if nothing was found.
        """ 
        return self.__lookup_node_property(self.__used_dataset_type, self.__used_dataset_id, id_value, self.__dataset_property)

    def __set_used_dataset_property(self, id_value, new_data):
        """
        Create/modify Used Dataset property data with new data.

        Args:
            id_value (string): Value for the id
            property_name (string): property name to create/modify
            new_data (Any): value for the property

        Raises:
            RuntimeError: If database query error.

        Returns:
            bool:
                - True when query succeeded.
                - False if node was not found.
        """ 
        return self.__set_node_property(self.__used_dataset_type, self.__used_dataset_id, id_value, self.__dataset_property, new_data)
    

    def lookup_used_dataset_nodes_used_data_model(self, parent_id_value):
        """
        Lookup Used Datasets relating to used data model
        and return list of them in a [[ID, file_name]] combo.

        Args:
            parent_id_value (string): Value for the id

        Raises:
            RuntimeError: If database query error.   

        Returns:
            list[string, string] or None:
                - list[string, string] A list of found nodes with ID and NAME combination.
                - None if nothing was found.
        """
        parent_info = {"node_type": self.__used_data_model_type, "id_type": self.__used_data_model_id, "id_value": parent_id_value}
        return self.__lookup_nodes(self.__used_dataset_type, self.__dataset_id, self.__dataset_property, parent_info)


    ### Used Blueprint
    def copy_to_used_blueprint_node(self, id_value):
        """
        Copies blueprint node into used-variant.

        Args:
            id_value (string): Value for the "active" blueprint id

        Raises:
            RuntimeError: If database query error.

        Returns:
            string: string containing ID value for the used-variant node. 
        """
        return self.__copy_node(self.__blueprint_type, self.__blueprint_id, id_value, self.__used_blueprint_type, self.__used_blueprint_id)

    def lookup_used_blueprint_property(self, id_value, property_name: NodeProperties.Blueprint):
        """
        Return data of specific property from UsedBlueprint
        
        Args:
            id_value (string): Value for the id
            property_name (string): property name to return it's value

        Raises:
            RuntimeError: If database query error.   

        Returns:
            Any or None:
                - Any if found, single node property data.
                - None if nothing was found.
        """ 
        return self.__lookup_node_property(self.__used_blueprint_type, self.__used_blueprint_id, id_value, property_name.value)

    
    ### Used datamodel
    def lookup_used_data_model_property(self, id_value, property_name: NodeProperties.DataModel):
        """
        Return data of specific property from UsedDataModel

        Args:
            id_value (string): Value for the id
            property_name (string): property name to return it's value

        Raises:
            RuntimeError: If database query error.   

        Returns:
            Any or None:
                - Any if found, single node property data.
                - None if nothing was found.
        """ 
        return self.__lookup_node_property(self.__used_data_model_type, self.__used_data_model_id, id_value, property_name.value)
    

    def lookup_used_data_model_nodes_result_blueprint(self, parent_id_value):
        """
        Lookup Used data models relating to ResultBlueprint
        and return list of them in a [[ID, NAME]] combo.

        Args:
            parent_id_value (string): Value for the id

        Raises:
            RuntimeError: If database query error.   

        Returns:
            list[string, string] or None:
                - list[string, string] A list of found nodes with ID and NAME combination.
                - None if nothing was found.
        """
        parent_info = {"node_type": self.__result_blueprint_type, "id_type": self.__result_blueprint_id, "id_value": parent_id_value}
        return self.__lookup_nodes(self.__used_data_model_type, self.__used_data_model_id, NodeProperties.DataModel.NAME.value, parent_info)


    ### Used Analyze Model
    def lookup_used_analyze_model_property(self, id_value, property_name: NodeProperties.AnalyzeModel):
        """
        Return data of specific property from UsedAnalyzeModel
        
        Args:
            id_value (string): Value for the id
            property_name (string): property name to return it's value

        Raises:
            RuntimeError: If database query error.   

        Returns:
            Any or None:
                - Any if found, single node property data.
                - None if nothing was found.
        """ 
        return self.__lookup_node_property(self.__used_analyze_model_type, self.__used_analyze_model_id, id_value, property_name.value)


    ### Result Blueprint

    # possibly useful when adding second result type
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
    
    '''
    def add_result_blueprint_node(self, project_id, blueprint_ids = None, dataset_list = None):
        """
        Create Result-blueprint node.
        
        Args:
            project_id (string): Parent project node id
            blueprint_ids (list of strings, optional): list of blueprint ids
            dataset_list (list of string, optional): dataset file names, will create Dataset-nodes
        
        Raises:
            RuntimeError: If database query error.

        Returns:
            string: string containing ID value for the created node.
        """

        result_blueprint_id = self.__add_node(self.__result_blueprint_type, self.__result_blueprint_id)

        self.set_result_blueprint_property(result_blueprint_id, NodeProperties.ResultBlueprint.DATETIME, datetime.now().isoformat())
        
        # copy nodes into used node versions and connect them to result
        # datasets
        for file_name in dataset_list:
            used_dataset_id = self.__add_node(self.__used_dataset_type, self.__used_dataset_id)
            self.__set_used_dataset_property(used_dataset_id, file_name)
            self.__connect_used_dataset_to_result_blueprint(used_dataset_id, result_blueprint_id)

        # blueprints
        for id in blueprint_ids:
            used_blueprint_id = self.__copy_node(self.__blueprint_type, self.__blueprint_id, id, self.__used_blueprint_type, self.__used_blueprint_id)
            self.__connect_used_blueprint_to_result_blueprint(used_blueprint_id, result_blueprint_id)

        # result -> project
        self.__connect_result_blueprint_to_project(result_blueprint_id, project_id)

        return result_blueprint_id
        '''
    
    def add_result_blueprint_node(self):
        """
        Made to be similar to add_project_node()
        """
        return self.__add_node(self.__result_blueprint_type, self.__result_blueprint_id)

    def set_result_blueprint_property(self, id_value, property_name: NodeProperties.ResultBlueprint, new_data):
        """
        Create/modify ResultBlueprint property data with new data.

        Args:
            id_value (string): Value for the id
            property_name (string): property name to create/modify
            new_data (Any): value for the property

        Raises:
            RuntimeError: If database query error.

        Returns:
            bool:
                - True when query succeeded.
                - False if node was not found.
        """ 
        return self.__set_node_property(self.__result_blueprint_type, self.__result_blueprint_id, id_value, property_name.value, new_data)


    def remove_result_blueprint_property(self, id_value, property_name: NodeProperties.ResultBlueprint):
        """
        Removes specific Project property data (and property)
    
        Args:
            id_value (string): Value for the id
            property_name (string): property name for removing

        Raises:
            RuntimeError: If database query error.

        Returns:
            bool:
                - True when query succeeded.
                - False when property doesn't exist.
        """ 
        return self.__remove_property(self.__result_blueprint_type, self.__result_blueprint_id, id_value, property_name.value)


    def lookup_result_blueprint_property(self, id_value, property_name: NodeProperties.ResultBlueprint):
        """
        Return data of specific property from Result-blueprint
        
        Args:
            id_value (string): Value for the id
            property_name (string): property name to return it's value

        Raises:
            RuntimeError: If database query error.   

        Returns:
            Any or None:
                - Any if found, single node property data.
                - None if nothing was found.
        """ 
        return self.__lookup_node_property(self.__result_blueprint_type, self.__result_blueprint_id, id_value, property_name.value)
    
    def lookup_result_blueprint_nodes(self, project_id):
        """
        Lookup ResultBlueprints from specific project and return list of them in a [[ID, DATETIME]] combo.

        Args:
            project_id (string): Value for the id

        Raises:
            RuntimeError: If database query error.   

        Returns:
            list[string, DATETIME.ISO] or None:
                - list[string, DATETIME.ISO] A list of found nodes with ID and DATETIME combination.
                - None if nothing was found.
        """ 
        project_info = { "node_type" : self.__project_type, "id_type" : self.__project_id, "id_value" : project_id }
        return self.__lookup_nodes(self.__result_blueprint_type, self.__result_blueprint_id, NodeProperties.ResultBlueprint.DATETIME.value, project_info)

    def delete_result_blueprint(self, id_value):
        """
        Delete Result-blueprint node and it's related content (used datasets/models/blueprints...)
        
        Args:
            id_value (string): Value for the id

        Raises:
            RuntimeError: If database query error.
            
        Returns:
            bool:
                - True when query succeeded.
                - False when node doesn't exist.
        """ 
        return self.__delete_node_with_connections(self.__result_blueprint_type, self.__result_blueprint_id, id_value)
    

    def get_result_blueprint_id_type(self):
        """
        TODO: possibly not needed?

        Get Result-blueprint id type
        
        Returns:
            string: id name
        """ 
        return self.__result_blueprint_id


