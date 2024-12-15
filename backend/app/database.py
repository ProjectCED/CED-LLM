from neo4j import GraphDatabase
#from neo4j.exceptions import Neo4jError #using normal Exception
from dotenv import load_dotenv
from enum import Enum
from neo4j.time import DateTime
import time
import os
from uuid import UUID
from typing import Any

class NodeLabels(Enum):
    """
    All allowed node labels and their id variable name.
    """
    GLOBAL_SETTINGS = ("GlobalSettings", 'id')
    USER_SETTINGS = ("UserSettings", 'id')
    BLUEPRINT = ("Blueprint", 'id')
    PROJECT = ("Project", 'id')
    RESULT_BLUEPRINT = ("ResultBlueprint", 'id')
    USED_BLUEPRINT = ("UsedBlueprint", 'id')

    def __init__(self, label, id):
        self.label = label
        self.id = id
        

class _NodeRelationships(Enum):
    """
    All allowed relationships.

    Enum variables are not used. Just NodeLabels compared.
    """
    RESULT_BLUEPRINT_TO_PROJECT = (NodeLabels.RESULT_BLUEPRINT, NodeLabels.PROJECT, "BELONGS_TO")
    USED_BLUEPRINT_TO_RESULT_BLUEPRINT = (NodeLabels.USED_BLUEPRINT, NodeLabels.RESULT_BLUEPRINT, "USED_IN_ANALYSIS")
    PROJECT_TO_USER_SETTINGS = (NodeLabels.PROJECT, NodeLabels.USER_SETTINGS, "OWNED_BY")
    BLUEPRINT_TO_USER_SETTINGS = (NodeLabels.BLUEPRINT, NodeLabels.USER_SETTINGS, "OWNED_BY")

    def __init__(self, from_node, to_node, relationship):
        self.from_node = from_node
        self.to_node = to_node
        self.relationship = relationship


class NodeProperties:
    """
    All allowed property names for each node label.

    Add more properties here when needed, but check Database class init for reserved names for identifier usage before adding new property names.

    When adding properties that should be used with sorting the lists. They also need to be added to 'sorting_properties'-variable in __lookup_nodes().
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
        USER_NAME = "user_name"

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
        DATETIME = "datetime"

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
        DATETIME = "datetime"
        
        TEST_PASS = "test_pass"
        TEST_FAIL = "test_fail"


    class ResultBlueprint(Enum):
        # Result
        # example FOO = "foo"
        NAME = "name"
        FILENAME = "filename"
        RESULT = "result"
        DATETIME = "datetime"
        USED_BLUEPRINT = "used_blueprint"

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
        """
        Start up database driver and setup constraints.
        """

        self.__driver = GraphDatabase.driver(os.getenv('DB_URL'), auth=(os.getenv('DB_USERNAME'), os.getenv('DB_PASSWORD')))
        self.__name = os.getenv('DB_NAME')

        ### setup constraints
        # special, user_name must be unique
        self.__create_unique_constraints(NodeLabels.USER_SETTINGS, NodeProperties.UserSettings.USER_NAME.value)
        # node identifier should always be unique (adds index by default)
        for node_label in NodeLabels:
            self.__create_unique_constraints(node_label, node_label.id)



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
    
    def __create_unique_constraints(self, node_label:NodeLabels, property_name:str):
        """
        Create unique constraint for specific node property.

        Warning: Will not check property_name validity.

        Args:
            label (NodeLabels): Node label
            property_name (string): Node property

        Raises:
            RuntimeError: If database query error.

        Returns:
            None: This function does not return any value.
        """

        query_string = f"""
        CREATE CONSTRAINT {node_label.label}_{property_name}_unique IF NOT EXISTS
        FOR (n:{node_label.label})
        REQUIRE n.{property_name} IS UNIQUE
        """

        try:
            with self.__driver.session() as session:
                session.run(
                    query_string,
                    database=self.__name,
                )

        except Exception as e:
            error_string = str(e)
            raise RuntimeError( "Neo4j create_unique_constraints() error: " + error_string )
    

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
        if id_value != None and self.__does_node_exist(type, id_type, id_value):
            return None
        
        # Try again if randomUUID() fails to give an unique value
        attempts = 0
        while attempts < 3:

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
                records = []

                with self.__driver.session() as session:
                    result = session.run(
                        query_string,
                        database=self.__name,
                    )
                    for record in result:
                        records.append(record)

                return next(iter(records)).data()[id_type]
            
            except Exception as e:
                error_string = str(e)
                # retry for certain amount of times if randomUUID() is already in database
                if "ConstraintValidationFailed" in error_string and attempts < 3:
                    attempts += 1
                    time.sleep(1000)
                # If all 3 attempts fail, raise an error
                if attempts == 3:
                    raise RuntimeError(f"Neo4j add_node() failed to create node after 3 attempts: "  + error_string )
                else:
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
            with self.__driver.session() as session:
                session.run(
                    query_string,
                    old_data=new_data,
                    database=self.__name,
                )
            return True
        
        except Exception as e:
            error_string = str(e)
            raise RuntimeError( "Neo4j set_property_value() query failed: " + error_string )
    

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
            records = []

            with self.__driver.session() as session:
                result = session.run(
                    query_string,
                    database=self.__name,
                )
                for record in result:
                    records.append(record)

            try:
                return next(iter(records)).data()[property_name]
            except:
                return None
        
        except Exception as e:
            error_string = str(e)
            raise RuntimeError( "Neo4j lookup_node_property query failed: " + error_string )


    def __lookup_nodes(self, type, id_type, property_list, parent_info = None, sort_property = None, sort_direction = 'DESC'):
        """
        Lookup nodes and return list of them in a [[ID, property_list]] combo.
        Sorting the result by first found sorting property DESC (compared with sorting_properties). If no sorting property found, defaults to 'id' ASC.

        Args:
            type (string): Node label
            id_type (string): Node id(property)
            id_value (string): Value for the id
            property_list (list[string]): list of properties to lookup
            parent_info (dict, optional): Where relationship is pointing at
                Expected keys:
                - 'node_type' (string): Node label
                - 'id_type' (string): Node id(property)
                - 'id_value' (string): Value for the id
            sort_property (string, optional): sorting property
            sort_direction (string, optional): sorting direction ('DESC' or 'ASC')

        Raises:
            RuntimeError: If invalid sort_direction value.
            RuntimeError: If database query error.

        Returns:
            list[string, Any] or []:
                - [ID, property_name value] A list of found nodes with ID and wanted property combination.
                - [] if nothing was found.
        """
        # sorting string
        sorting_string = '' # this will be used if no sorting property detected
        if (sort_direction != 'DESC' and sort_direction != 'ASC'):
            raise RuntimeError( "__lookup_nodes() sort_direction invalid value: " + sort_direction )
        if sort_property:
            sorting_string = f"WITH n ORDER BY n.{sort_property} {sort_direction} "

        # make string from property list
        property_list_string = ''
        for item in property_list:
            property_list_string = property_list_string + ", n." + item

        query_string =''
        if parent_info == None:
            query_string += f"MATCH (n:{type}) "
            query_string += sorting_string
            query_string += f"RETURN COLLECT ([n.{id_type}{property_list_string}]) AS list "

        else:
            query_string += f"MATCH (n:{type}) - [] -> (:{parent_info['node_type']} {{{parent_info['id_type']}: '{parent_info['id_value']}'}}) "
            query_string += sorting_string
            query_string += f"RETURN COLLECT ([n.{id_type}{property_list_string}]) AS list "

        try:
            records = []

            with self.__driver.session() as session:
                result = session.run(
                    query_string,
                    database=self.__name,
                )
                for record in result:
                    records.append(record)
      
            try:
                # gives out [[ ]]
                double_list = next(iter(records)).data()['list']
                return double_list
            except:
                # TODO: this actually never happens, empty results will be []
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
                - False if node doesn't exists.
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
            with self.__driver.session() as session:
                session.run(
                    query_string,
                    database=self.__name,
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
            with self.__driver.session() as session:
                session.run(
                    query_string,
                    database=self.__name,
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
            with self.__driver.session() as session:
                session.run(
                    query_string,
                    database=self.__name,
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
            with self.__driver.session() as session:
                session.run(
                    query_string,
                    database=self.__name,
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

        # Try again if randomUUID() fails to give an unique value
        attempts = 0
        while attempts < 3:

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
                records = []

                with self.__driver.session() as session:
                    result = session.run(
                        query_string,
                        database=self.__name,
                    )
                    for record in result:
                        records.append(record)

                return next(iter(records)).data()[id_type]
            
            except Exception as e:
                error_string = str(e)
                # retry for certain amount of times if randomUUID() is already in database
                if "ConstraintValidationFailed" in error_string and attempts < 3:
                    attempts += 1
                    time.sleep(1000)
                # If all 3 attempts fail, raise an error
                if attempts == 3:
                    raise RuntimeError(f"Neo4j copy_node() failed to create node after 3 attempts: "  + error_string )
                else:
                    raise RuntimeError( "Neo4j copy_node() query failed: " + error_string )
                


   
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
            records = []

            with self.__driver.session() as session:
                result = session.run(
                    query_string,
                    database=self.__name,
                )
                for record in result:
                    records.append(record)

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
            records = []

            with self.__driver.session() as session:
                result = session.run(
                    query_string,
                    database=self.__name,
                )
                for record in result:
                    records.append(record)

            if not records:
                return False
            else:
                return True
            
        except Exception as e:
            error_string = str(e)
            raise RuntimeError( "Neo4j does_node_exist() query failed: " + error_string )


    def __helper_get_property_enum_and_validate(self, node_label:NodeLabels, property_name:Enum):
        """
        Helper function to dynamically get the property enum class for a node_label and validate the property_name.

        Parameters:
            node_label (NodeLabels): The node label to get the corresponding property enum class for.
            property_name (Enum): The property name to validate.

        Raises:
            ValueError: If the property enum class doesn't exist or the property_name is invalid.

        Returns:
            properties_enum_class (Enum): The corresponding property enum class for the node_label.
        """
        # Used variants should have access to normal variant enums
        alias_mapping = {
            NodeLabels.USED_BLUEPRINT: NodeLabels.BLUEPRINT
        }
        resolved_node_label = alias_mapping.get(node_label, node_label)

        # Dynamically get the corresponding property enum class
        properties_enum_class = getattr(NodeProperties, resolved_node_label.label, None)

        if not properties_enum_class:
            raise ValueError(f"No properties defined for node label {node_label.label}")
        
        # If property_name is passed as a string, we will dynamically retrieve the property
        if isinstance(property_name, str):
            # Check if the property exists in the enum class
            property_enum = getattr(properties_enum_class, property_name, None)

            if not property_enum:
                raise ValueError(
                    f"Invalid property '{property_name}' for node label '{node_label.label}'. "
                    f"Expected one of: {[e.name for e in properties_enum_class]}"
                )
        
            return property_enum
        
        # Check if the property_name is valid for the given node_label
        if not isinstance(property_name, properties_enum_class):
            raise ValueError(
                f"Invalid property '{property_name}' for node label '{node_label.label}'. "
                f"Expected one of: {[e.name for e in properties_enum_class]}"
            )

        return properties_enum_class

    ### Add node
    def add_node(self, node_label:NodeLabels):
        
        """
        Create a node. Also DATETIME is set as creation time for Blueprints, Projects and results.

        Args:
            node_label (NodeLabels): Node label
            user_name (string, optional): Used with creating UserSettings node

        Raises:
            RuntimeError: If database query error.
            ValueError: If the property_name is invalid for the given node_label (from DATETIME set)

        Returns:
            string or None:
                - string containing ID value for the created node.
                - None if node already exists.
        """
        # this node should only have one instance
        if node_label == NodeLabels.GLOBAL_SETTINGS:
            if self.__lookup_nodes(node_label.label, node_label.id, []) != []:
                return None

        id = self.__add_node(node_label.label, node_label.id)

        # only add DATETIME on following
        if node_label in [
            NodeLabels.BLUEPRINT,
            NodeLabels.PROJECT,
            NodeLabels.RESULT_BLUEPRINT,
        ]:
            # Make sure DATETIME is found for node_label
            datetime_property = self.__helper_get_property_enum_and_validate(node_label, 'DATETIME')
           
            self.set_node_property(id, node_label, datetime_property, DateTime.now())


        return id

    def set_node_property(self, id:UUID, node_label:NodeLabels, property_name: Enum, new_data: Any):
        """
        Create/modify node property data with new data.

        Args:
            id (UUID): Node identifier
            node_label (NodeLabels): Node label
            property_name (Enum): property name to create/modify
            new_data (Any): value for the property

        Raises:
            RuntimeError: If database query error.
            ValueError: If the property_name is invalid for the given node_label

        Returns:
            bool:
                - True when query succeeded.
                - False if node was not found or cannot be modified.
        """ 
        # not allowed to be modified
        if node_label in [
            NodeLabels.USED_BLUEPRINT,
        ]:
            return False

        # Check that node_label has property_name
        self.__helper_get_property_enum_and_validate(node_label, property_name)

        # Update datetime (modified), similar to add_node()
        if node_label in [
            NodeLabels.BLUEPRINT,
            NodeLabels.PROJECT,
            NodeLabels.RESULT_BLUEPRINT,
        ]:
            datetime_property = self.__helper_get_property_enum_and_validate(node_label, 'DATETIME')
            self.__set_node_property(node_label.label, node_label.id, id, datetime_property.value, DateTime.now())

        return self.__set_node_property(node_label.label, node_label.id, id, property_name.value, new_data)

    def remove_node_property(self, id:UUID, node_label:NodeLabels, property_name:Enum):
        """
        Removes specific node property data (and property)

        Args:
            id (UUID): Node identifier
            node_label (NodeLabels): Node label
            property_name (Enum): property name for removing

        Raises:
            RuntimeError: If database query error.
            ValueError: If the property_name is invalid for the given node_label.

        Returns:
            bool:
                - True when query succeeded.
                - False when property doesn't exist.
        """
        # Check that node_label has property_name
        self.__helper_get_property_enum_and_validate(node_label, property_name)

        return self.__remove_property(node_label.label, node_label.id, id, property_name.value)


    def lookup_node_property(self, id:UUID, node_label:NodeLabels, property_name:Enum):
        """
        Return data of specific property from settings
        
        Args:
            id (UUID): Node identifier
            node_label (NodeLabels): Node label
            property_name (Enum): property name for removing

        Raises:
            RuntimeError: If database query error.
            ValueError: If the property_name is invalid for the given node_label.

        Returns:
            Any or None:
                - Any if found, single node property data.
                - None if nothing was found.
        """ 
        # Check that node_label has property_name
        self.__helper_get_property_enum_and_validate(node_label, property_name)

        return self.__lookup_node_property(node_label.label, node_label.id, id, property_name.value)

    def delete_node(self, id:UUID, node_label:NodeLabels):
        """
        Delete node. For Project, ResultBlueprint and UserSettings, also all the connected nodes are deleted.

        Args:
            id (UUID): Node identifier
            node_label (NodeLabels): Node label
        
        Raises:
            RuntimeError: If database query error.
            
        Returns:
            bool:
                - True when query succeeded.
                - False when node doesn't exist or cannot be deleted.
        """
        # Deletion not allowed
        if node_label in [
            NodeLabels.USED_BLUEPRINT, # deleted when result is deleted
        ]:
            return False
        
        # Also delete connected nodes connected to it
        if node_label in [
            NodeLabels.USER_SETTINGS, # everything related to this user is deleted and anything beyond
            NodeLabels.PROJECT, # results also deleted and anything beyond
            NodeLabels.RESULT_BLUEPRINT, # used_blueprints also deleted
        ]:
            return self.__delete_node_with_connections(node_label.label, node_label.id, id)
        else:
            return self.__delete_node(node_label.label, node_label.id, id)


    def lookup_nodes(self, node_label:NodeLabels, parent_label:NodeLabels = None, parent_id:UUID = None):
        """
        Lookup nodes and return list of them in a [[ID, NAME, DATETIME],...] combo. Sorting the result by DATETIME DESC when present.

        Args:
            node_label (NodeLabels): Node label
            parent_label (NodeLabels, optional): Parent label for searching under specific node
            parent_id (UUID, optional): Id value of parent node

        Raises:
            RuntimeError: If database query error.
            RuntimeError: If an invalid sort_direction value is provided (should not occur).

        Returns:
            list[list[string]] or []:
                - list[list[string]] A list of found nodes with ID, NAME, DATETIME.iso()... etc combination.
                - [] if nothing was found.
        """
        property_list = []
        parent_info = None
        sort_property = None
        sort_direction = 'DESC'

        if node_label == NodeLabels.PROJECT:
            property_list = [
                NodeProperties.Project.NAME.value,
                NodeProperties.Project.DATETIME.value,
                ]
            sort_property = NodeProperties.Project.DATETIME.value

        elif node_label == NodeLabels.RESULT_BLUEPRINT:
            parent_info = { "node_type" : parent_label.label, "id_type" : parent_label.id, "id_value" : parent_id }
            property_list = [
                NodeProperties.ResultBlueprint.DATETIME.value,
                ]
            sort_property = NodeProperties.ResultBlueprint.DATETIME.value

        elif node_label == NodeLabels.BLUEPRINT:
            property_list = [
                NodeProperties.Blueprint.NAME.value,
                NodeProperties.Blueprint.DATETIME.value,
                ]
            sort_property = NodeProperties.Blueprint.DATETIME.value
            
        elif node_label == NodeLabels.USER_SETTINGS:
            property_list = [
                NodeProperties.UserSettings.NAME.value,
                NodeProperties.UserSettings.USER_NAME.value,
                ]
            sort_property = NodeProperties.UserSettings.USER_NAME.value
            sort_direction = 'ASC'
        
        elif node_label == NodeLabels.USED_BLUEPRINT:
            parent_info = { "node_type" : parent_label.label, "id_type" : parent_label.id, "id_value" : parent_id }
            property_list = [
                NodeProperties.Blueprint.NAME.value,
                NodeProperties.Blueprint.DATETIME.value,
                ]
            sort_property = NodeProperties.Blueprint.DATETIME.value
        
        elif node_label == NodeLabels.GLOBAL_SETTINGS:
            # just to get id
            pass
        return self.__lookup_nodes(node_label.label, node_label.id, property_list, parent_info, sort_property, sort_direction)
    

    def copy_node_to_node(self, from_id:UUID, from_label:NodeLabels, to_label:NodeLabels):
        """
        Copies node into another node. Only supports copies between Blueprint <-> Used_Blueprint.

        Args:
            id_value (string): Value for the "active" blueprint id

        Raises:
            RuntimeError: If database query error.
            RuntimeError: If copy not supported by design.

        Returns:
            string(UUID): string containing ID value for the created node. 
        """
        # allowed cases
        if from_label == NodeLabels.BLUEPRINT and to_label == NodeLabels.USED_BLUEPRINT:
            pass
        elif from_label == NodeLabels.USED_BLUEPRINT and to_label == NodeLabels.BLUEPRINT:
            pass
        else:
            raise RuntimeError( "Unsupported copy attempt: " + from_label.label + " to " + to_label.label)
        
        result = self.__copy_node(from_label.label, from_label.id, from_id, to_label.label, to_label.id)

        # give "_used" tag and fresh DATETIME when copying back to blueprint
        if from_label == NodeLabels.USED_BLUEPRINT and to_label == NodeLabels.BLUEPRINT:
            name = self.lookup_node_property(result, NodeLabels.BLUEPRINT, NodeProperties.Blueprint.NAME)
            self.set_node_property(result, NodeLabels.BLUEPRINT, NodeProperties.Blueprint.NAME, (name or "blueprint") + "_used")
            self.set_node_property(result, NodeLabels.BLUEPRINT, NodeProperties.Blueprint.DATETIME, DateTime.now())

        return result
        

    def connect_node_to_node(self, from_id:UUID, from_label:NodeLabels, to_id:UUID, to_label:NodeLabels):
        """
        Connect node to node with pre-defined relationship.

        Args:
            dataset_id_value (string): Value for the Dataset id
            data_model_id_value (string): Value for the DataModel id

        Raises:
            RuntimeError: If database query error.
            ValueError: If relationship was not found between nodes.

        Returns:
            bool:
                - True when query succeeded.
                - False when either of the nodes doesn't exist.
        """
        relationship_string = ''
        try:
            for relationship in _NodeRelationships:
                if relationship.from_node == from_label and relationship.to_node == to_label:
                    relationship_string = relationship.relationship
        except:
            raise ValueError(f"No relationship found between {from_label.label} and {to_label.label}")
        
        return self.__connect_with_relationship(from_label.label, from_label.id, from_id, to_label.label, to_label.id, to_id, relationship_string)

