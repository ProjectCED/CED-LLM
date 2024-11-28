import pytest
from app.database import Database, NodeProperties
from datetime import datetime
from uuid import UUID

pytestmark = pytest.mark.database

@pytest.fixture(scope="module")
def db():
    """
    Fixture that sets up a real database connection for the entire module.
    This connection will be shared across all tests in this module.

    Tests is done by using database() public functions and it's queries,
    instead of making separate queries from here.

    Returns:
        database object
    """
    database = Database()
    yield database


@pytest.fixture(autouse=True)
def clear_database(db:Database):
    """
    Automatically cleans up the database between tests.
    """
    db.debug_clear_all()


class TestAddNode:
    """Create node
    
    1. create node
    check returned id-string
    """
    def test_global_settings(self,db:Database):
        result = db.add_global_settings_node()
        assert result == 'Global'

    def test_user_settings(self,db:Database):
        result = db.add_user_settings_node('alice')
        assert result == 'alice'

    def test_project(self,db:Database):
        result = db.add_project_node()
        assert UUID(result,version=4)

    def test_blueprint(self,db:Database):
        result = db.add_blueprint_node()
        assert UUID(result,version=4)

    def test_blueprint_2(self,db:Database):
        id = db.add_blueprint_node()
        used_id = db.copy_to_used_blueprint_node(id)
        result = db.copy_to_blueprint_node(used_id)
        assert UUID(result,version=4)
        
    def test_result_blueprint(self,db:Database):
        result = db.add_result_blueprint_node()
        assert UUID(result,version=4)

    def test_used_blueprint(self,db:Database):
        id = db.add_blueprint_node()
        result = db.copy_to_used_blueprint_node(id)
        assert UUID(result,version=4)

       


class TestSetProperty:
    """Creating property
    
    1. create node
    2. set property
    check returned bool
    """

    def test_global_settings(self,db:Database):
        db.add_global_settings_node()
        result = db.set_global_settings_property(NodeProperties.GlobalSettings.TEST_PASS, 'Verdana')
        assert result == True

    def test_user_settings(self,db:Database):
        db.add_user_settings_node('alice')
        result = db.set_user_settings_property('alice', NodeProperties.UserSettings.TEST_PASS, 'Alice')
        assert result == True

    def test_project(self,db:Database):
        id = db.add_project_node()
        result = db.set_project_property(id, NodeProperties.Project.TEST_PASS, 'foo')
        assert result == True

    def test_blueprint(self,db:Database):
        id = db.add_blueprint_node()
        result = db.set_blueprint_property(id, NodeProperties.Blueprint.TEST_PASS, 'foo')
        assert result == True

    def test_result_blueprint(self,db:Database):
        id = db.add_result_blueprint_node()
        result = db.set_result_blueprint_property(id, NodeProperties.ResultBlueprint.TEST_PASS, 'foo')
        assert result == True


class TestLookupPropertyFound:
    """Lookup property that is found
    
    1. create node
    2. set property
    3. lookup property
    check returned property value
    """

    def test_global_settings(self,db:Database):
        db.add_global_settings_node()
        db.set_global_settings_property(NodeProperties.GlobalSettings.TEST_PASS, 'Verdana')
        result = db.lookup_global_settings_property(NodeProperties.GlobalSettings.TEST_PASS)
        assert result == 'Verdana'

    def test_user_settings(self,db:Database):
        db.add_user_settings_node('alice')
        db.set_user_settings_property('alice', NodeProperties.UserSettings.TEST_PASS, 'Alice')
        result = db.lookup_user_settings_property('alice', NodeProperties.UserSettings.TEST_PASS)
        assert result == 'Alice'

    def test_project(self,db:Database):
        id = db.add_project_node()
        db.set_project_property(id, NodeProperties.Project.TEST_PASS, 'foo')
        result = db.lookup_project_property(id, NodeProperties.Project.TEST_PASS)
        assert result == 'foo'

    def test_blueprint(self,db:Database):
        id = db.add_blueprint_node()
        db.set_blueprint_property(id, NodeProperties.Blueprint.TEST_PASS, 'foo')
        result = db.lookup_blueprint_property(id, NodeProperties.Blueprint.TEST_PASS)
        assert result == 'foo'

    def test_result_blueprint(self,db:Database):
        id = db.add_result_blueprint_node()
        db.set_result_blueprint_property(id, NodeProperties.ResultBlueprint.TEST_PASS, 'foo')
        result = db.lookup_result_blueprint_property(id, NodeProperties.ResultBlueprint.TEST_PASS)
        assert result == 'foo'

    def test_used_blueprint(self,db:Database):
        id = db.add_blueprint_node()
        db.set_blueprint_property(id, NodeProperties.Blueprint.TEST_PASS, 'foo')
        id_2 = db.copy_to_used_blueprint_node(id)
        result = db.lookup_used_blueprint_property(id_2, NodeProperties.Blueprint.TEST_PASS)
        assert result == 'foo'


class TestLookupPropertyNotFound:
    """Lookup property that is not found
    
    1. create node
    2. lookup non-existent property
    check returned property value
    """

    def test_global_settings(self,db:Database):
        db.add_global_settings_node()
        result = db.lookup_global_settings_property(NodeProperties.GlobalSettings.TEST_FAIL)
        assert result == None

    def test_user_settings(self,db:Database):
        db.add_user_settings_node('alice')
        result = db.lookup_user_settings_property('alice', NodeProperties.UserSettings.TEST_FAIL)
        assert result == None

    def test_project(self,db:Database):
        id = db.add_project_node()
        result = db.lookup_project_property(id, NodeProperties.Project.TEST_FAIL)
        assert result == None

    def test_blueprint(self,db:Database):
        id = db.add_blueprint_node()
        result = db.lookup_blueprint_property(id, NodeProperties.Blueprint.TEST_FAIL)
        assert result == None

    def test_result_blueprint(self,db:Database):
        id = db.add_result_blueprint_node()
        result = db.lookup_result_blueprint_property(id, NodeProperties.ResultBlueprint.TEST_FAIL)
        assert result == None

    def test_used_blueprint(self,db:Database):
        id = db.add_blueprint_node()
        id_2 = db.copy_to_used_blueprint_node(id)
        result = db.lookup_used_blueprint_property(id_2, NodeProperties.Blueprint.TEST_FAIL)
        assert result == None


class TestLookupPropertyNodeNotFound:
    """Lookup property node not found
    
    1. lookup property from non-existent node
    check returned property value
    """

    def test_user_settings(self,db:Database):
        result = db.lookup_user_settings_property('wrong_id', NodeProperties.UserSettings.TEST_FAIL)
        assert result == None

    def test_project(self,db:Database):
        result = db.lookup_project_property('wrong_id', NodeProperties.Project.TEST_FAIL)
        assert result == None

    def test_blueprint(self,db:Database):
        result = db.lookup_blueprint_property('wrong_id', NodeProperties.Blueprint.TEST_FAIL)
        assert result == None

    def test_result_blueprint(self,db:Database):
        result = db.lookup_result_blueprint_property('wrong_id', NodeProperties.ResultBlueprint.TEST_FAIL)
        assert result == None

    def test_used_blueprint(self,db:Database):
        result = db.lookup_used_blueprint_property('wrong_id', NodeProperties.Blueprint.TEST_FAIL)
        assert result == None


class TestRemovePropertyFound:
    """Property remove
    
    1. create node
    2. set property
    3. remove property
    check returned bool and lookup of TEST_PASS
    """

    def test_global_settings(self,db:Database):
        db.add_global_settings_node()
        db.set_global_settings_property(NodeProperties.GlobalSettings.TEST_PASS, 'Verdana')
        result_1 = db.remove_global_settings_property(NodeProperties.GlobalSettings.TEST_PASS)
        result_2 = db.lookup_global_settings_property(NodeProperties.GlobalSettings.TEST_PASS)
        assert (
            result_1 == True 
            and result_2 == None
        )

    def test_user_settings(self,db:Database):
        db.add_user_settings_node('alice')
        db.set_user_settings_property('alice', NodeProperties.UserSettings.TEST_PASS, 'Alice')
        result_1 = db.remove_user_settings_property('alice', NodeProperties.UserSettings.TEST_PASS)
        result_2 = db.lookup_user_settings_property('alice', NodeProperties.UserSettings.TEST_PASS)
        assert (
            result_1 == True 
            and result_2 == None
        )

    def test_project(self,db:Database):
        id = db.add_project_node()
        db.set_project_property(id, NodeProperties.Project.TEST_PASS, 'foo')
        result_1 = db.remove_project_property(id, NodeProperties.Project.TEST_PASS)
        result_2 = db.lookup_project_property(id, NodeProperties.Project.TEST_PASS)
        assert (
            result_1 == True 
            and result_2 == None
        )

    def test_blueprint(self,db:Database):
        id = db.add_blueprint_node()
        db.set_blueprint_property(id, NodeProperties.Blueprint.TEST_PASS, 'foo')
        result_1 = db.remove_blueprint_property(id, NodeProperties.Blueprint.TEST_PASS)
        result_2 = db.lookup_blueprint_property(id, NodeProperties.Blueprint.TEST_PASS)
        assert (
            result_1 == True 
            and result_2 == None
        )

    def test_result_blueprint(self,db:Database):
        id = db.add_result_blueprint_node()
        db.set_result_blueprint_property(id, NodeProperties.ResultBlueprint.TEST_PASS, 'foo')
        result_1 = db.remove_result_blueprint_property(id, NodeProperties.ResultBlueprint.TEST_PASS)
        result_2 = db.lookup_result_blueprint_property(id, NodeProperties.ResultBlueprint.TEST_PASS)
        assert (
            result_1 == True 
            and result_2 == None
        )


class TestRemovePropertyNotFound:
    """Remove property not found
    
    1. create node
    2. remove non-existent property
    check returned bool
    """

    def test_global_settings(self,db:Database):
        db.add_global_settings_node()
        result = db.remove_global_settings_property(NodeProperties.GlobalSettings.TEST_FAIL)
        assert result == False
    def test_user_settings(self,db:Database):
        db.add_user_settings_node('alice')
        result = db.remove_user_settings_property('alice', NodeProperties.UserSettings.TEST_FAIL)
        assert result == False

    def test_project(self,db:Database):
        id = db.add_project_node()
        result = db.remove_project_property(id, NodeProperties.Project.TEST_FAIL)
        assert result == False

    def test_blueprint(self,db:Database):
        id = db.add_blueprint_node()
        result = db.remove_blueprint_property(id, NodeProperties.Blueprint.TEST_FAIL)
        assert result == False

    def test_result_blueprint(self,db:Database):
        id = db.add_result_blueprint_node()
        result = db.remove_result_blueprint_property(id, NodeProperties.ResultBlueprint.TEST_FAIL)
        assert result == False


class TestRemovePropertyNodeNotFound:
    """Remove property node not found
    
    1. Remove property from non-existent node
    check returned bool
    """

    def test_user_settings(self,db:Database):
        result = db.remove_user_settings_property('wrong_id', NodeProperties.UserSettings.TEST_FAIL)
        assert result == False

    def test_project(self,db:Database):
        result = db.remove_project_property('wrong_id', NodeProperties.Project.TEST_FAIL)
        assert result == False

    def test_blueprint(self,db:Database):
        result = db.remove_blueprint_property('wrong_id', NodeProperties.Blueprint.TEST_FAIL)
        assert result == False

    def test_result_blueprint(self,db:Database):
        result = db.remove_result_blueprint_property('wrong_id', NodeProperties.ResultBlueprint.TEST_FAIL)
        assert result == False


class TestDeleteNode:
    """Delete node
    
    1. create node
    2. add property TEST_PASS    
    3. delete node
    check returned bool and search for TEST_PASS
    """

    def test_global_settings(self,db:Database):
        db.add_global_settings_node()
        db.set_global_settings_property(NodeProperties.GlobalSettings.TEST_PASS, 'foo')
        result_1 = db.delete_global_settings()
        result_2 = db.lookup_global_settings_property(NodeProperties.GlobalSettings.TEST_PASS)
        assert (
            result_1 == True 
            and result_2 == None
        )

    def test_user_settings(self,db:Database):
        db.add_user_settings_node('alice')
        db.set_user_settings_property('alice', NodeProperties.UserSettings.TEST_PASS, 'foo')
        result_1 = db.delete_user_settings('alice')
        result_2 = db.lookup_user_settings_property(id, NodeProperties.UserSettings.TEST_PASS)
        assert (
            result_1 == True 
            and result_2 == None
        )

    def test_project(self,db:Database):
        id = db.add_project_node()
        db.set_project_property(id, NodeProperties.Project.TEST_PASS, 'foo')
        result_1 = db.delete_project(id)
        result_2 = db.lookup_project_property(id, NodeProperties.Project.TEST_PASS)
        assert (
            result_1 == True 
            and result_2 == None
        )

    def test_blueprint(self,db:Database):
        id = db.add_blueprint_node()
        db.set_blueprint_property(id, NodeProperties.Blueprint.TEST_PASS, 'foo')
        result_1 = db.delete_blueprint(id)
        result_2 = db.lookup_blueprint_property(id, NodeProperties.Blueprint.TEST_PASS)
        assert (
            result_1 == True 
            and result_2 == None
        )

    def test_result_blueprint(self,db:Database):
        id = db.add_result_blueprint_node()
        db.set_result_blueprint_property(id, NodeProperties.ResultBlueprint.TEST_PASS, 'foo')
        result_1 = db.delete_result_blueprint(id)
        result_2 = db.lookup_result_blueprint_property(id, NodeProperties.ResultBlueprint.TEST_PASS)
        assert (
            result_1 == True 
            and result_2 == None
        )


class TestDeleteNodeAdvanced:
    """Delete node and nodes connected to it: (deleted too) -[rel]-> (deleted)
    
    1. create "parent" node
    2. create nodes and connect them to "parent" node
    3. set something in TEST_PASS
    3. delete "parent" node
    check that "child" nodes don't exist (check TEST_PASS)
    """

    def test_user_settings(self,db:Database):
        """
        1. create user
        2. create project
        3. create blueprint
        4. create result
        5. create used_blueprint
        6. delete user
        check if any is found(project,blueprint,result,used_blueprint)
        """
        db.add_user_settings_node('alice')

        id_project = db.add_project_node()
        db.set_project_property(id_project, NodeProperties.Project.TEST_PASS, 'foo')
        db.connect_project_to_user_settings(id_project,'alice')

        id_blueprint = db.add_blueprint_node()
        db.set_blueprint_property(id_blueprint, NodeProperties.Blueprint.TEST_PASS, 'foo')
        db.connect_blueprint_to_user_settings(id_blueprint,'alice')

        id_result = db.add_result_blueprint_node()
        db.set_result_blueprint_property(id_result, NodeProperties.ResultBlueprint.TEST_PASS, 'foo')
        db.connect_result_blueprint_to_project(id_result,id_project)

        id_used_blueprint = db.copy_to_used_blueprint_node(id_blueprint)
        db.connect_used_blueprint_to_result_blueprint(id_used_blueprint,id_result)

        db.delete_user_settings('alice')

        result_1 = db.lookup_blueprint_property(id_blueprint, NodeProperties.Blueprint.TEST_PASS)
        result_2 = db.lookup_project_property(id_project, NodeProperties.Project.TEST_PASS)
        result_3 = db.lookup_result_blueprint_property(id_result, NodeProperties.ResultBlueprint.TEST_PASS)
        result_4 = db.lookup_used_blueprint_property(id_used_blueprint, NodeProperties.Blueprint.TEST_PASS)

        assert (
            result_1 == None 
            and result_2 == None 
            and result_3 == None 
            and result_4 == None
        )
    
    def test_project(self,db:Database):
        """
        1. create project
        2. create blueprint
        3. create 2 results
        4. create used_blueprint for each result
        5. delete project
        check if any is found(result,used_blueprint)
        """
        id_project = db.add_project_node()

        id_blueprint = db.add_blueprint_node()
        db.set_blueprint_property(id_blueprint, NodeProperties.Blueprint.TEST_PASS, 'foo')
        db.connect_blueprint_to_user_settings(id_blueprint,'alice')

        id_result_1 = db.add_result_blueprint_node()
        db.set_result_blueprint_property(id_result_1, NodeProperties.ResultBlueprint.TEST_PASS, 'foo')
        db.connect_result_blueprint_to_project(id_result_1,id_project)

        id_used_blueprint_1 = db.copy_to_used_blueprint_node(id_blueprint)
        db.connect_used_blueprint_to_result_blueprint(id_used_blueprint_1,id_result_1)

        id_result_2 = db.add_result_blueprint_node()
        db.set_result_blueprint_property(id_result_2, NodeProperties.ResultBlueprint.TEST_PASS, 'foo')
        db.connect_result_blueprint_to_project(id_result_2,id_project)

        id_used_blueprint_2 = db.copy_to_used_blueprint_node(id_blueprint)
        db.connect_used_blueprint_to_result_blueprint(id_used_blueprint_2,id_result_2)

        db.delete_project(id_project)

        result_1 = db.lookup_result_blueprint_property(id_result_1, NodeProperties.ResultBlueprint.TEST_PASS)
        result_2 = db.lookup_used_blueprint_property(id_used_blueprint_1, NodeProperties.Blueprint.TEST_PASS)
        result_3 = db.lookup_result_blueprint_property(id_result_2, NodeProperties.ResultBlueprint.TEST_PASS)
        result_4 = db.lookup_used_blueprint_property(id_used_blueprint_2, NodeProperties.Blueprint.TEST_PASS)

        assert (
            result_1 == None 
            and result_2 == None 
            and result_3 == None 
            and result_4 == None
        )

    def test_result_blueprint(self,db:Database):
        """
        1. create result
        2. create blueprint
        4. create used_blueprint
        5. delete result
        check if any is found(used_blueprint)
        """
        id_result = db.add_result_blueprint_node()

        id_blueprint = db.add_blueprint_node()
        db.set_blueprint_property(id_blueprint, NodeProperties.Blueprint.TEST_PASS, 'foo')

        id_used_blueprint = db.copy_to_used_blueprint_node(id_blueprint)
        db.connect_used_blueprint_to_result_blueprint(id_used_blueprint,id_result)

        db.delete_result_blueprint(id_result)

        result_1 = db.lookup_used_blueprint_property(id_used_blueprint, NodeProperties.Blueprint.TEST_PASS)

        assert result_1 == None


class TestDeleteNodeNotFound:
    """Delete node not found
    
    1. delete non-existent node
    check returned bool
    """

    def test_global_settings(self,db:Database):
        result = db.delete_global_settings()
        assert result == False

    def test_user_settings(self,db:Database):
        result = db.delete_user_settings('wrong_id')
        assert result == False

    def test_project(self,db:Database):
        result = db.delete_project('wrong_id')
        assert result == False

    def test_blueprint(self,db:Database):
        id = db.add_blueprint_node()
        result = db.delete_blueprint('wrong_id')
        assert result == False

    def test_result_blueprint(self,db:Database):
        id = db.add_result_blueprint_node()
        result = db.delete_result_blueprint('wrong_id')
        assert result == False


class TestRelationshipCreationGoodToGood:
    """Relationships between nodes
    
    1. create nodes
    2. connect nodes
    check returned bool
    """

    def test_blueprint_user_settings(self,db:Database):
        id_1 = db.add_blueprint_node()
        id_2 = db.add_user_settings_node('alice')
        result = db.connect_blueprint_to_user_settings(id_1, id_2)
        assert result == True

    def test_project_user_settings(self,db:Database):
        id_1 = db.add_project_node()
        id_2 = db.add_user_settings_node('alice')
        result = db.connect_project_to_user_settings(id_1, id_2)
        assert result == True

    def test_result_blueprint_project(self,db:Database):
        id_1 = db.add_result_blueprint_node()
        id_2 = db.add_project_node()
        result = db.connect_result_blueprint_to_project(id_1, id_2)
        assert result == True

    def test_used_blueprint_result_blueprint(self,db:Database):
        id = db.add_blueprint_node()
        id_1 = db.copy_to_used_blueprint_node(id)
        id_2 = db.add_result_blueprint_node()
        result = db.connect_used_blueprint_to_result_blueprint(id_1, id_2)
        assert result == True


class TestRelationshipCreationBadToGood:
    """Relationships between bad to good nodes
    
    1. only create second node
    2. connect nodes
    check returned bool
    """

    def test_blueprint_user_settings(self,db:Database):
        id_2 = db.add_user_settings_node('alice')
        result = db.connect_blueprint_to_user_settings('wrong_id', id_2)
        assert result == False

    def test_project_user_settings(self,db:Database):
        id_2 = db.add_user_settings_node('alice')
        result = db.connect_project_to_user_settings('wrong_id', id_2)
        assert result == False

    def test_result_blueprint_project(self,db:Database):
        id_2 = db.add_project_node()
        result = db.connect_result_blueprint_to_project('wrong_id', id_2)
        assert result == False

    def test_used_blueprint_result_blueprint(self,db:Database):
        id_2 = db.add_result_blueprint_node()
        result = db.connect_used_blueprint_to_result_blueprint('wrong_id', id_2)
        assert result == False


class TestRelationshipCreationGoodToBad:
    """Relationships between good to bad nodes
    
    1. only create first node
    2. connect nodes
    check returned bool
    """

    def test_blueprint_user_settings(self,db:Database):
        id_1 = db.add_blueprint_node()
        result = db.connect_blueprint_to_user_settings(id_1, 'wrong_id')
        assert result == False

    def test_project_user_settings(self,db:Database):
        id_1 = db.add_project_node()
        result = db.connect_project_to_user_settings(id_1, 'wrong_id')
        assert result == False

    def test_result_blueprint_project(self,db:Database):
        id_1 = db.add_result_blueprint_node()
        result = db.connect_result_blueprint_to_project(id_1, 'wrong_id')
        assert result == False

    def test_used_blueprint_result_blueprint(self,db:Database):
        id = db.add_blueprint_node()
        id_1 = db.copy_to_used_blueprint_node(id)
        result = db.connect_used_blueprint_to_result_blueprint(id_1, 'wrong_id')
        assert result == False


class TestRelationshipCreationBadToBad:
    """Relationships between bad to bad nodes
    
    1. connect non-existent nodes
    check returned bool
    """

    def test_blueprint_user_settings(self,db:Database):
        result = db.connect_blueprint_to_user_settings('wrong_id', 'wrong_id')
        assert result == False

    def test_project_user_settings(self,db:Database):
        result = db.connect_project_to_user_settings('wrong_id', 'wrong_id')
        assert result == False

    def test_result_blueprint_project(self,db:Database):
        result = db.connect_result_blueprint_to_project('wrong_id', 'wrong_id')
        assert result == False

    def test_used_blueprint_result_blueprint(self,db:Database):
        result = db.connect_used_blueprint_to_result_blueprint('wrong_id', 'wrong_id')
        assert result == False


class TestNodeLookups:
    """Node lookups
    
    1. add nodes
    2. add names
    check lookup nodes result (NAME and/or DATETIME)
    """
    def helper_datetime_checker(self,date_string):
        try:
            print(datetime.fromisoformat(date_string))
            return True
        except:
            return False

    def test_lookup_project_nodes(self,db:Database):
        id_1 = db.add_project_node()
        db.set_project_property(id_1,NodeProperties.Project.NAME,'foo_1')
        id_2 = db.add_project_node()
        db.set_project_property(id_2,NodeProperties.Project.NAME,'foo_2')

        result = db.lookup_project_nodes()

        assert (
            UUID(result[0][0],version=4)
            and UUID(result[1][0],version=4)
            and result[0][1] == 'foo_1' 
            and result[1][1] == 'foo_2'
            and self.helper_datetime_checker(result[0][2]) == True 
            and self.helper_datetime_checker(result[1][2]) == True
        )

    def test_lookup_blueprint_nodes(self,db:Database):
        id_1 = db.add_blueprint_node()
        db.set_blueprint_property(id_1,NodeProperties.Blueprint.NAME,'foo_1')
        id_2 = db.add_blueprint_node()
        db.set_blueprint_property(id_2,NodeProperties.Blueprint.NAME,'foo_2')

        result = db.lookup_blueprint_nodes()

        assert (
            UUID(result[0][0],version=4)
            and UUID(result[1][0],version=4)
            and result[0][1] == 'foo_1' 
            and result[1][1] == 'foo_2'
            and self.helper_datetime_checker(result[0][2]) == True 
            and self.helper_datetime_checker(result[1][2]) == True
        )

    def test_lookup_result_blueprint_nodes(self,db:Database):
        id = db.add_project_node()

        id_1 = db.add_result_blueprint_node()
        db.connect_result_blueprint_to_project(id_1,id)
        id_2 = db.add_result_blueprint_node()
        db.connect_result_blueprint_to_project(id_2,id)

        result = db.lookup_result_blueprint_nodes(id)

        assert (
            UUID(result[0][0],version=4)
            and UUID(result[1][0],version=4)
            and self.helper_datetime_checker(result[0][1]) == True 
            and self.helper_datetime_checker(result[1][1]) == True
        )



