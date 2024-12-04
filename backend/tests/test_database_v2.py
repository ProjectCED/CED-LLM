"""
Database testing. Combined unit- and integration-testing. 

Tests is done by using database() public functions and it's queries instead of creating new connection in this module.

Modules tested:
- Database public functions
- Partially Database private functions (that used by public functions)
- Communication with real database.

Usage:
- "$env:PYTHONPATH = (Get-Location).Path" command in backend-folder (windows11)
- "pytest -m database -p no:warnings" command in backend-folder

Note: make sure database is up and running either:
- Through Neo4j Desktop (official app)
- Editing neo4j ports back in in docker-compose.yml and launching with "docker-compose up neo4j --build"

"""

import pytest
from app.database import Database, NodeProperties, NodeLabels, NodeRelationships
from datetime import datetime
from uuid import UUID
import uuid

pytestmark = pytest.mark.database2

random_UUID = uuid.uuid4()

@pytest.fixture(scope="module")
def db():
    """
    Fixture that sets up a real database connection for the entire module.
    This connection will be shared across all tests in this module.

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
    check returned id
    """
    def test_global_settings(self,db:Database):
        result = db.add_node(NodeLabels.GLOBAL_SETTINGS)
        assert UUID(result,version=4)

    def test_user_settings(self,db:Database):
        result = db.add_node(NodeLabels.USER_SETTINGS)
        assert UUID(result,version=4)

    def test_project(self,db:Database):
        result = db.add_node(NodeLabels.PROJECT)
        assert UUID(result,version=4)

    def test_blueprint(self,db:Database):
        result = db.add_node(NodeLabels.BLUEPRINT)
        assert UUID(result,version=4)

    def test_blueprint_2(self,db:Database):
        """
        Test blueprint created by copying used blueprint

        1. create blueprint
        2. create used variant by copying blueprint
        3. create blueprint by copying used variant back
        check returned id
        """
        id = db.add_node(NodeLabels.BLUEPRINT)
        used_id = db.copy_node_to_node(id, NodeLabels.BLUEPRINT, NodeLabels.USED_BLUEPRINT)
        result = db.copy_node_to_node(used_id, NodeLabels.USED_BLUEPRINT, NodeLabels.BLUEPRINT)
        assert UUID(result,version=4)
        
    def test_result_blueprint(self,db:Database):
        result = db.add_node(NodeLabels.RESULT_BLUEPRINT)
        assert UUID(result,version=4)

    def test_used_blueprint(self,db:Database):
        """
        Test used blueprint creation

        1. create blueprint
        2. create used one by copying from blueprint
        3. check returned id
        """
        id = db.add_node(NodeLabels.BLUEPRINT)
        result = db.copy_node_to_node(id, NodeLabels.BLUEPRINT, NodeLabels.USED_BLUEPRINT)
        assert UUID(result,version=4)

       


class TestSetPropertyLookProperty:
    """
    Creating property and lookup property
    
    1. create node
    2. set property
    3. lookup said property
    check returned bool and lookup value
    """

    def test_global_settings(self,db:Database):
        id = db.add_node(NodeLabels.GLOBAL_SETTINGS)
        result = db.set_property(id, NodeLabels.GLOBAL_SETTINGS, NodeProperties.GlobalSettings.TEST_PASS, 'Verdana')
        result_2 = db.lookup_node_property(id, NodeLabels.GLOBAL_SETTINGS, NodeProperties.GlobalSettings.TEST_PASS)
        assert (
            result == True
            and result_2 == 'Verdana'
        )

    def test_user_settings(self,db:Database):
        id = db.add_node(NodeLabels.USER_SETTINGS)
        result = db.set_property(id, NodeLabels.USER_SETTINGS, NodeProperties.UserSettings.TEST_PASS, 'Alice')
        result_2 = db.lookup_node_property(id, NodeLabels.USER_SETTINGS, NodeProperties.UserSettings.TEST_PASS)
        assert (
            result == True
            and result_2 == 'Alice'
        )

    def test_project(self,db:Database):
        id = db.add_node(NodeLabels.PROJECT)
        result = db.set_node_property(id, NodeLabels.PROJECT, NodeProperties.Project.TEST_PASS, 'foo')
        result_2 = db.lookup_node_property(id, NodeLabels.USER_SETTINGS, NodeProperties.Project.TEST_PASS)
        assert (
            result == True
            and result_2 == 'foo'
        )

    def test_blueprint(self,db:Database):
        id = db.add_node(NodeLabels.BLUEPRINT)
        result = db.set_node_property(id, NodeLabels.BLUEPRINT, NodeProperties.Blueprint.TEST_PASS, 'foo')
        result_2 = db.lookup_node_property(id, NodeLabels.USER_SETTINGS, NodeProperties.Blueprint.TEST_PASS)
        assert (
            result == True
            and result_2 == 'foo'
        )

    def test_result_blueprint(self,db:Database):
        id = db.add_node(NodeLabels.RESULT_BLUEPRINT)
        result = db.set_node_property(id, NodeLabels.RESULT_BLUEPRINT, NodeProperties.ResultBlueprint.TEST_PASS, 'foo')
        result_2 = db.lookup_node_property(id, NodeLabels.USER_SETTINGS, NodeProperties.ResultBlueprint.TEST_PASS)
        assert (
            result == True
            and result_2 == 'foo'
        )

    def test_used_blueprint(self,db:Database):
        """
        Just look up property from used_blueprint

        1. create blueprint
        2. set property
        3. create used variant
        4. lookup used variant property
        check lookup value
        """
        id = db.add_node(NodeLabels.BLUEPRINT)
        db.set_node_property(id, NodeLabels.BLUEPRINT, NodeProperties.Blueprint.TEST_PASS, 'foo')
        id_2 = db.copy_node_to_node(id, NodeLabels.BLUEPRINT, NodeLabels.USED_BLUEPRINT)
        result = db.lookup_node_property(id_2, NodeLabels.USED_BLUEPRINT, NodeProperties.Blueprint.TEST_PASS)
        assert result == 'foo'


# class TestLookupPropertyFound:
#     """Lookup property that is found
    
#     1. create node
#     2. set property
#     3. lookup property
#     check returned property value
#     """

#     def test_global_settings(self,db:Database):
#         db.add_global_settings_node()
#         db.set_global_settings_property(NodeProperties.GlobalSettings.TEST_PASS, 'Verdana')
#         result = db.lookup_global_settings_property(NodeProperties.GlobalSettings.TEST_PASS)
#         assert result == 'Verdana'

#     def test_user_settings(self,db:Database):
#         db.add_user_settings_node('alice')
#         db.set_user_settings_property('alice', NodeProperties.UserSettings.TEST_PASS, 'Alice')
#         result = db.lookup_user_settings_property('alice', NodeProperties.UserSettings.TEST_PASS)
#         assert result == 'Alice'

#     def test_project(self,db:Database):
#         id = db.add_project_node()
#         db.set_project_property(id, NodeProperties.Project.TEST_PASS, 'foo')
#         result = db.lookup_project_property(id, NodeProperties.Project.TEST_PASS)
#         assert result == 'foo'

#     def test_blueprint(self,db:Database):
#         id = db.add_blueprint_node()
#         db.set_blueprint_property(id, NodeProperties.Blueprint.TEST_PASS, 'foo')
#         result = db.lookup_blueprint_property(id, NodeProperties.Blueprint.TEST_PASS)
#         assert result == 'foo'

#     def test_result_blueprint(self,db:Database):
#         id = db.add_result_blueprint_node()
#         db.set_result_blueprint_property(id, NodeProperties.ResultBlueprint.TEST_PASS, 'foo')
#         result = db.lookup_result_blueprint_property(id, NodeProperties.ResultBlueprint.TEST_PASS)
#         assert result == 'foo'




class TestLookupPropertyNotFound:
    """Lookup property that is not found
    
    1. create node
    2. lookup non-existent property
    check returned property value
    """

    def test_global_settings(self,db:Database):
        id = db.add_node(NodeLabels.GLOBAL_SETTINGS)
        result = db.lookup_node_property(id, NodeLabels.GLOBAL_SETTINGS, NodeProperties.GlobalSettings.TEST_FAIL)
        assert result == None

    def test_user_settings(self,db:Database):
        id = db.add_node(NodeLabels.USER_SETTINGS)
        result = db.lookup_node_property(id, NodeLabels.USER_SETTINGS, NodeProperties.UserSettings.TEST_FAIL)
        assert result == None

    def test_project(self,db:Database):
        id = db.add_node(NodeLabels.PROJECT)
        result = db.lookup_node_property(id, NodeLabels.PROJECT, NodeProperties.Project.TEST_FAIL)
        assert result == None

    def test_blueprint(self,db:Database):
        id = db.add_node(NodeLabels.BLUEPRINT)
        result = db.lookup_node_property(id, NodeLabels.BLUEPRINT, NodeProperties.Blueprint.TEST_FAIL)
        assert result == None

    def test_result_blueprint(self,db:Database):
        id = db.add_node(NodeLabels.RESULT_BLUEPRINT)
        result = db.lookup_node_property(id, NodeLabels.RESULT_BLUEPRINT, NodeProperties.ResultBlueprint.TEST_FAIL)
        assert result == None

    def test_used_blueprint(self,db:Database):
        id = db.add_node(NodeLabels.USED_BLUEPRINT)
        id_2 = db.copy_to_used_blueprint_node(id)
        result = db.lookup_node_property(id_2, NodeLabels.USED_BLUEPRINT, NodeProperties.Blueprint.TEST_FAIL)
        assert result == None


class TestLookupPropertyNodeNotFound:
    """Lookup property node not found
    
    1. lookup property from non-existent node
    check returned property value
    """

    def test_global_settings(self,db:Database):
        result = db.lookup_node_property(random_UUID, NodeLabels.GLOBAL_SETTINGS, NodeProperties.GlobalSettings.TEST_FAIL)
        assert result == None

    def test_user_settings(self,db:Database):
        result = db.lookup_node_property(random_UUID, NodeLabels.USER_SETTINGS, NodeProperties.UserSettings.TEST_FAIL)
        assert result == None

    def test_project(self,db:Database):
        result = db.lookup_node_property(random_UUID, NodeLabels.PROJECT, NodeProperties.Project.TEST_FAIL)
        assert result == None

    def test_blueprint(self,db:Database):
        result = db.lookup_node_property(random_UUID, NodeLabels.BLUEPRINT, NodeProperties.Blueprint.TEST_FAIL)
        assert result == None

    def test_result_blueprint(self,db:Database):
        result = db.lookup_node_property(random_UUID, NodeLabels.RESULT_BLUEPRINT, NodeProperties.ResultBlueprint.TEST_FAIL)
        assert result == None

    def test_used_blueprint(self,db:Database):
        result = db.lookup_node_property(random_UUID, NodeLabels.USED_BLUEPRINT, NodeProperties.Blueprint.TEST_FAIL)
        assert result == None


class TestRemovePropertyFound:
    """
    Test that property was removed

    1. create node
    2. set property
    3. remove property
    check returned bool and lookup of TEST_PASS
    """

    def test_global_settings(self,db:Database):
        id = db.add_node(NodeLabels.GLOBAL_SETTINGS)
        db.set_node_property(id, NodeLabels.GLOBAL_SETTINGS, NodeProperties.GlobalSettings.TEST_PASS, 'Verdana')
        result_1 = db.remove_node_property(id, NodeLabels.GLOBAL_SETTINGS, NodeProperties.GlobalSettings.TEST_PASS)
        result_2 = db.lookup_node_property(id, NodeLabels.GLOBAL_SETTINGS, NodeProperties.GlobalSettings.TEST_PASS)
        assert (
            result_1 == True 
            and result_2 == None
        )

    def test_user_settings(self,db:Database):
        id = db.add_node(NodeLabels.USER_SETTINGS)
        db.set_node_property(id, NodeLabels.USER_SETTINGS, NodeProperties.UserSettings.TEST_PASS, 'Alice')
        result_1 = db.remove_node_property(id, NodeLabels.USER_SETTINGS, NodeProperties.UserSettings.TEST_PASS)
        result_2 = db.lookup_node_property(id, NodeLabels.USER_SETTINGS, NodeProperties.UserSettings.TEST_PASS)
        assert (
            result_1 == True 
            and result_2 == None
        )

    def test_project(self,db:Database):
        id = db.add_node(NodeLabels.PROJECT)
        db.set_node_property(id, NodeLabels.PROJECT, NodeProperties.Project.TEST_PASS, 'foo')
        result_1 = db.remove_node_property(id, NodeLabels.PROJECT, NodeProperties.Project.TEST_PASS)
        result_2 = db.lookup_node_property(id, NodeLabels.PROJECT, NodeProperties.Project.TEST_PASS)
        assert (
            result_1 == True 
            and result_2 == None
        )

    def test_blueprint(self,db:Database):
        id = db.add_node(NodeLabels.BLUEPRINT)
        db.set_node_property(id, NodeLabels.BLUEPRINT, NodeProperties.Blueprint.TEST_PASS, 'foo')
        result_1 = db.remove_node_property(id, NodeLabels.BLUEPRINT, NodeProperties.Blueprint.TEST_PASS)
        result_2 = db.lookup_node_property(id, NodeLabels.BLUEPRINT, NodeProperties.Blueprint.TEST_PASS)
        assert (
            result_1 == True 
            and result_2 == None
        )

    def test_result_blueprint(self,db:Database):
        id = db.add_node(NodeLabels.RESULT_BLUEPRINT)
        db.set_node_property(id, NodeLabels.RESULT_BLUEPRINT, NodeProperties.ResultBlueprint.TEST_PASS, 'foo')
        result_1 = db.remove_node_property(id, NodeLabels.RESULT_BLUEPRINT, NodeProperties.ResultBlueprint.TEST_PASS)
        result_2 = db.lookup_node_property(id, NodeLabels.RESULT_BLUEPRINT, NodeProperties.ResultBlueprint.TEST_PASS)
        assert (
            result_1 == True 
            and result_2 == None
        )


class TestRemovePropertyNotFound:
    """
    Test removing of non-existent property
    
    1. create node
    2. remove non-existent property
    check returned bool
    """

    def test_global_settings(self,db:Database):
        id = db.add_node(NodeLabels.GLOBAL_SETTINGS)
        result = db.remove_node_property(id, NodeLabels.GLOBAL_SETTINGS, NodeProperties.GlobalSettings.TEST_FAIL)
        assert result == False
    def test_user_settings(self,db:Database):
        id = db.add_node(NodeLabels.USER_SETTINGS)
        result = db.remove_node_property(id, NodeLabels.USER_SETTINGS, NodeProperties.UserSettings.TEST_FAIL)
        assert result == False

    def test_project(self,db:Database):
        id = db.add_node(NodeLabels.PROJECT)
        result = db.remove_node_property(id, NodeLabels.PROJECT, NodeProperties.Project.TEST_FAIL)
        assert result == False

    def test_blueprint(self,db:Database):
        id = db.add_node(NodeLabels.BLUEPRINT)
        result = db.remove_node_property(id, NodeLabels.BLUEPRINT, NodeProperties.Blueprint.TEST_FAIL)
        assert result == False

    def test_result_blueprint(self,db:Database):
        id = db.add_node(NodeLabels.RESULT_BLUEPRINT)
        result = db.remove_node_property(id, NodeLabels.RESULT_BLUEPRINT, NodeProperties.ResultBlueprint.TEST_FAIL)
        assert result == False


class TestRemovePropertyNodeNotFound:
    """
    Test removing property that wasn't found
    
    1. Remove property from non-existent node
    check returned bool
    """

    def test_user_settings(self,db:Database):
        result = db.remove_node_property(random_UUID, NodeLabels.USER_SETTINGS, NodeProperties.UserSettings.TEST_FAIL)
        assert result == False

    def test_project(self,db:Database):
        result = db.remove_node_property(random_UUID, NodeLabels.PROJECT, NodeProperties.Project.TEST_FAIL)
        assert result == False

    def test_blueprint(self,db:Database):
        result = db.remove_node_property(random_UUID, NodeLabels.BLUEPRINT, NodeProperties.Blueprint.TEST_FAIL)
        assert result == False

    def test_result_blueprint(self,db:Database):
        result = db.remove_node_property(random_UUID, NodeLabels.RESULT_BLUEPRINT, NodeProperties.ResultBlueprint.TEST_FAIL)
        assert result == False


class TestDeleteNode:
    """
    Test node deletion
    
    1. create node
    2. add property TEST_PASS    
    3. delete node
    check returned bool and search for TEST_PASS
    """

    def test_global_settings(self,db:Database):
        id = db.add_node(NodeLabels.GLOBAL_SETTINGS)
        db.set_global_settings_property(id, NodeLabels.GLOBAL_SETTINGS, NodeProperties.GlobalSettings.TEST_PASS, 'foo')
        result_1 = db.delete_node(id, NodeLabels.GLOBAL_SETTINGS)
        result_2 = db.lookup_node_property(id, NodeLabels.GLOBAL_SETTINGS, NodeProperties.GlobalSettings.TEST_PASS)
        assert (
            result_1 == True 
            and result_2 == None
        )

    def test_user_settings(self,db:Database):
        id = db.add_node(NodeLabels.USER_SETTINGS)
        db.set_user_settings_property(id, NodeLabels.USER_SETTINGS, NodeProperties.UserSettings.TEST_PASS, 'foo')
        result_1 = db.delete_node(id, NodeLabels.USER_SETTINGS)
        result_2 = db.lookup_node_property(id, NodeLabels.USER_SETTINGS, NodeProperties.UserSettings.TEST_PASS)
        assert (
            result_1 == True 
            and result_2 == None
        )

    def test_project(self,db:Database):
        id = db.add_node(NodeLabels.PROJECT)
        db.set_project_property(id, NodeLabels.PROJECT, NodeProperties.Project.TEST_PASS, 'foo')
        result_1 = db.delete_node(id, NodeLabels.PROJECT)
        result_2 = db.lookup_node_property(id, NodeLabels.PROJECT, NodeProperties.Project.TEST_PASS)
        assert (
            result_1 == True 
            and result_2 == None
        )

    def test_blueprint(self,db:Database):
        id = db.add_node(NodeLabels.BLUEPRINT)
        db.set_blueprint_property(id, NodeLabels.BLUEPRINT, NodeProperties.Blueprint.TEST_PASS, 'foo')
        result_1 = db.delete_node(id, NodeLabels.BLUEPRINT)
        result_2 = db.lookup_node_property(id, NodeLabels.BLUEPRINT, NodeProperties.Blueprint.TEST_PASS)
        assert (
            result_1 == True 
            and result_2 == None
        )

    def test_result_blueprint(self,db:Database):
        id = db.add_node(NodeLabels.RESULT_BLUEPRINT)
        db.set_result_blueprint_property(id, NodeLabels.BLUEPRINT, NodeProperties.ResultBlueprint.TEST_PASS, 'foo')
        result_1 = db.delete_node(id, NodeLabels.RESULT_BLUEPRINT)
        result_2 = db.lookup_node_property(id, NodeLabels.RESULT_BLUEPRINT, NodeProperties.ResultBlueprint.TEST_PASS)
        assert (
            result_1 == True 
            and result_2 == None
        )


class TestDeleteNodeAdvanced:
    """
    Test that nodes connected to certain nodes also are deleted. (also deleted) -[rel]-> (deleted)
    
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
        id_user = db.add_node(NodeLabels.USER_SETTINGS)
        db.set_node_property(id_user, NodeLabels.USER_SETTINGS, NodeProperties.UserSettings.TEST_PASS, 'foo')

        id_project = db.add_node(NodeLabels.PROJECT)
        db.set_node_property(id_project, NodeLabels.PROJECT, NodeProperties.Project.TEST_PASS, 'foo')
        db.connect_node_to_node(id_project, NodeLabels.PROJECT, id_user, NodeLabels.USER_SETTINGS)

        id_blueprint = db.add_node(NodeLabels.BLUEPRINT)
        db.set_node_property(id_blueprint, NodeLabels.BLUEPRINT, NodeProperties.Blueprint.TEST_PASS, 'foo')
        db.connect_node_to_node(id_blueprint, NodeLabels.BLUEPRINT, id_user, NodeLabels.USER_SETTINGS)

        id_result = db.add_node(NodeLabels.RESULT_BLUEPRINT)
        db.set_node_property(id_result, NodeLabels.RESULT_BLUEPRINT, NodeProperties.ResultBlueprint.TEST_PASS, 'foo')
        db.connect_node_to_node(id_result, NodeLabels.RESULT_BLUEPRINT, id_project, NodeLabels.PROJECT)

        id_used_blueprint = db.copy_node_to_node(id_blueprint, NodeLabels.BLUEPRINT, NodeLabels.USED_BLUEPRINT)
        db.connect_node_to_node(id_used_blueprint, NodeLabels.USED_BLUEPRINT, id_result, NodeLabels.RESULT_BLUEPRINT)

        db.delete_node(id_user, NodeLabels.USER_SETTINGS)

        result_1 = db.lookup_node_property(id_blueprint, NodeLabels.BLUEPRINT, NodeProperties.Blueprint.TEST_PASS)
        result_2 = db.lookup_node_property(id_project, NodeLabels.PROJECT, NodeProperties.Project.TEST_PASS)
        result_3 = db.lookup_node_property(id_result, NodeLabels.RESULT_BLUEPRINT, NodeProperties.ResultBlueprint.TEST_PASS)
        result_4 = db.lookup_node_property(id_used_blueprint, NodeLabels.USED_BLUEPRINT, NodeProperties.Blueprint.TEST_PASS)

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
        id_project = db.add_node(NodeLabels.PROJECT)

        id_blueprint = db.add_node(NodeLabels.BLUEPRINT)
        db.set_node_property(id_blueprint, NodeLabels.BLUEPRINT, NodeProperties.Blueprint.TEST_PASS, 'foo')

        id_result_1 = db.add_node(NodeLabels.RESULT_BLUEPRINT)
        db.set_node_property(id_result_1, NodeLabels.RESULT_BLUEPRINT, NodeProperties.ResultBlueprint.TEST_PASS, 'foo')
        db.connect_node_to_node(id_result_1, NodeLabels.RESULT_BLUEPRINT, id_project, NodeLabels.PROJECT)

        id_result_2 = db.add_node(NodeLabels.RESULT_BLUEPRINT)
        db.set_node_property(id_result_2, NodeLabels.RESULT_BLUEPRINT, NodeProperties.ResultBlueprint.TEST_PASS, 'foo')
        db.connect_node_to_node(id_result_2, NodeLabels.RESULT_BLUEPRINT, id_project, NodeLabels.PROJECT)

        id_used_blueprint_1 = db.copy_node_to_node(id_blueprint, NodeLabels.BLUEPRINT, NodeLabels.USED_BLUEPRINT)
        db.connect_node_to_node(id_used_blueprint_1, NodeLabels.USED_BLUEPRINT, id_result_1, NodeLabels.RESULT_BLUEPRINT)

        id_used_blueprint_2 = db.copy_node_to_node(id_blueprint, NodeLabels.BLUEPRINT, NodeLabels.USED_BLUEPRINT)
        db.connect_node_to_node(id_used_blueprint_2, NodeLabels.USED_BLUEPRINT, id_result_2, NodeLabels.RESULT_BLUEPRINT)

        db.delete_node(id_project, NodeLabels.PROJECT)

        result_1 = db.lookup_node_property(id_result_1, NodeLabels.RESULT_BLUEPRINT, NodeProperties.ResultBlueprint.TEST_PASS)
        result_2 = db.lookup_node_property(id_used_blueprint_1, NodeLabels.USED_BLUEPRINT, NodeProperties.Blueprint.TEST_PASS)
        result_3 = db.lookup_node_property(id_result_2, NodeLabels.RESULT_BLUEPRINT, NodeProperties.ResultBlueprint.TEST_PASS)
        result_4 = db.lookup_node_property(id_used_blueprint_2, NodeLabels.USED_BLUEPRINT, NodeProperties.Blueprint.TEST_PASS)

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
        id_result = db.add_node(NodeLabels.RESULT_BLUEPRINT)

        id_blueprint = db.add_node(NodeLabels.BLUEPRINT)
        db.set_blueprint_property(id_blueprint, NodeLabels.BLUEPRINT, NodeProperties.Blueprint.TEST_PASS, 'foo')

        id_used_blueprint = db.copy_node_to_node(id_blueprint, NodeLabels.BLUEPRINT, NodeLabels.USED_BLUEPRINT)
        db.connect_node_to_node(id_used_blueprint, NodeLabels.USED_BLUEPRINT, id_result, NodeLabels.RESULT_BLUEPRINT)

        db.delete_node(id_result, NodeLabels.RESULT_BLUEPRINT)

        result_1 = db.lookup_node_property(id_used_blueprint, NodeLabels.USED_BLUEPRINT, NodeProperties.Blueprint.TEST_PASS)

        assert result_1 == None


class TestDeleteNodeNotFound:
    """
    Test to delete node that isn't found
    
    1. delete non-existent node
    check returned bool
    """

    def test_global_settings(self,db:Database):
        result = db.delete_node(random_UUID, NodeLabels.GLOBAL_SETTINGS)
        assert result == False

    def test_user_settings(self,db:Database):
        result = db.delete_node(random_UUID, NodeLabels.USER_SETTINGS)
        assert result == False

    def test_project(self,db:Database):
        result = db.delete_node(random_UUID, NodeLabels.PROJECT)
        assert result == False

    def test_blueprint(self,db:Database):
        result = db.delete_node(random_UUID, NodeLabels.BLUEPRINT)
        assert result == False

    def test_result_blueprint(self,db:Database):
        result = db.delete_node(random_UUID, NodeLabels.RESULT_BLUEPRINT)
        assert result == False


class TestRelationshipCreationGoodToGood:
    """
    Testing positive relationship cases (good->good)
    
    1. create nodes
    2. connect nodes
    check returned bool
    """

    def test_blueprint_user_settings(self,db:Database):
        id_1 = db.add_node(NodeLabels.BLUEPRINT)
        id_2 = db.add_node(NodeLabels.USER_SETTINGS)
        result = db.connect_node_to_node(id_1, NodeLabels.BLUEPRINT, id_2, NodeLabels.USER_SETTINGS)
        assert result == True

    def test_project_user_settings(self,db:Database):
        id_1 = db.add_node(NodeLabels.PROJECT)
        id_2 = db.add_node(NodeLabels.USER_SETTINGS)
        result = db.connect_node_to_node(id_1, NodeLabels.PROJECT, id_2, NodeLabels.USER_SETTINGS)
        assert result == True

    def test_result_blueprint_project(self,db:Database):
        id_1 = db.add_node(NodeLabels.BLUEPRINT)
        id_2 = db.add_node(NodeLabels.PROJECT)
        result = db.connect_node_to_node(id_1, NodeLabels.BLUEPRINT, id_2, NodeLabels.PROJECT)
        assert result == True

    def test_used_blueprint_result_blueprint(self,db:Database):
        id = db.add_node(NodeLabels.BLUEPRINT)
        id_1 = db.copy_node_to_node(id, NodeLabels.BLUEPRINT, NodeLabels.USED_BLUEPRINT)
        id_2 = db.add_node(NodeLabels.RESULT_BLUEPRINT)
        result = db.connect_node_to_node(id_1, NodeLabels.USED_BLUEPRINT, id_2, NodeLabels.RESULT_BLUEPRINT)
        assert result == True


class TestRelationshipCreationBadToGood:
    """Relationships between bad to good nodes
    
    1. only create second node
    2. connect nodes
    check returned bool
    """

    def test_blueprint_user_settings(self,db:Database):
        id_2 = db.add_node(NodeLabels.USER_SETTINGS)
        result = db.connect_node_to_node(random_UUID, NodeLabels.BLUEPRINT, id_2, NodeLabels.USER_SETTINGS)
        assert result == False

    def test_project_user_settings(self,db:Database):
        id_2 = db.add_node(NodeLabels.USER_SETTINGS)
        result = db.connect_node_to_node(random_UUID, NodeLabels.PROJECT, id_2, NodeLabels.USER_SETTINGS)
        assert result == False

    def test_result_blueprint_project(self,db:Database):
        id_2 = db.add_node(NodeLabels.PROJECT)
        result = db.connect_node_to_node(random_UUID, NodeLabels.BLUEPRINT, id_2, NodeLabels.PROJECT)
        assert result == False

    def test_used_blueprint_result_blueprint(self,db:Database):
        id_2 = db.add_node(NodeLabels.RESULT_BLUEPRINT)
        result = db.connect_node_to_node(random_UUID, NodeLabels.USED_BLUEPRINT, id_2, NodeLabels.RESULT_BLUEPRINT)
        assert result == False


class TestRelationshipCreationGoodToBad:
    """Relationships between good to bad nodes
    
    1. only create first node
    2. connect nodes
    check returned bool
    """

    def test_blueprint_user_settings(self,db:Database):
        id_1 = db.add_node(NodeLabels.BLUEPRINT)
        result = db.connect_node_to_node(id_1, NodeLabels.BLUEPRINT, random_UUID, NodeLabels.USER_SETTINGS)
        assert result == False

    def test_project_user_settings(self,db:Database):
        id_1 = db.add_node(NodeLabels.PROJECT)
        result = db.connect_node_to_node(id_1, NodeLabels.PROJECT, random_UUID, NodeLabels.USER_SETTINGS)
        assert result == False

    def test_result_blueprint_project(self,db:Database):
        id_1 = db.add_node(NodeLabels.BLUEPRINT)
        result = db.connect_node_to_node(id_1, NodeLabels.BLUEPRINT, random_UUID, NodeLabels.PROJECT)
        assert result == False

    def test_used_blueprint_result_blueprint(self,db:Database):
        id = db.add_node(NodeLabels.BLUEPRINT)
        id_1 = db.copy_node_to_node(id, NodeLabels.BLUEPRINT, NodeLabels.USED_BLUEPRINT)
        result = db.connect_node_to_node(id_1, NodeLabels.USED_BLUEPRINT, random_UUID, NodeLabels.RESULT_BLUEPRINT)
        assert result == False


class TestRelationshipCreationBadToBad:
    """Relationships between bad to bad nodes
    
    1. connect non-existent nodes
    check returned bool
    """

    def test_blueprint_user_settings(self,db:Database):
        result = db.connect_node_to_node(random_UUID, NodeLabels.BLUEPRINT, random_UUID, NodeLabels.USER_SETTINGS)
        assert result == False

    def test_project_user_settings(self,db:Database):
        result = db.connect_node_to_node(random_UUID, NodeLabels.PROJECT, random_UUID, NodeLabels.USER_SETTINGS)
        assert result == False

    def test_result_blueprint_project(self,db:Database):
        result = db.connect_node_to_node(random_UUID, NodeLabels.BLUEPRINT, random_UUID, NodeLabels.PROJECT)
        assert result == False

    def test_used_blueprint_result_blueprint(self,db:Database):
        result = db.connect_node_to_node(random_UUID, NodeLabels.USED_BLUEPRINT, random_UUID, NodeLabels.RESULT_BLUEPRINT)
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
        id_1 = db.add_node(NodeLabels.PROJECT)
        db.set_node_property(id_1, NodeLabels.PROJECT, NodeProperties.Project.NAME, 'foo_1')
        id_2 = db.add_node(NodeLabels.PROJECT)
        db.set_node_property(id_2, NodeLabels.PROJECT, NodeProperties.Project.NAME, 'foo_2')

        result = db.lookup_nodes(NodeLabels.PROJECT)

        assert (
            UUID(result[0][0],version=4)
            and UUID(result[1][0],version=4)
            and result[0][1] == 'foo_2' # order matters
            and result[1][1] == 'foo_1'
            and self.helper_datetime_checker(result[0][2]) == True 
            and self.helper_datetime_checker(result[1][2]) == True
        )

    def test_lookup_blueprint_nodes(self,db:Database):
        id_1 = db.add_node(NodeLabels.BLUEPRINT)
        db.set_node_property(id_1,NodeLabels.BLUEPRINT,NodeProperties.Blueprint.NAME,'foo_1')
        id_2 = db.add_node(NodeLabels.BLUEPRINT)
        db.set_node_property(id_2,NodeLabels.BLUEPRINT,NodeProperties.Blueprint.NAME,'foo_2')

        result = db.lookup_nodes(NodeLabels.BLUEPRINT)

        assert (
            UUID(result[0][0],version=4)
            and UUID(result[1][0],version=4)
            and result[0][1] == 'foo_2' # order matters
            and result[1][1] == 'foo_1'
            and self.helper_datetime_checker(result[0][2]) == True 
            and self.helper_datetime_checker(result[1][2]) == True
        )

    def test_lookup_result_blueprint_nodes(self,db:Database):
        id = db.add_node(NodeLabels.PROJECT)

        id_1 = db.add_node(NodeLabels.RESULT_BLUEPRINT)
        db.connect_node_to_node(id_1,NodeLabels.RESULT_BLUEPRINT,id,NodeLabels.PROJECT)
        id_2 = db.add_node(NodeLabels.RESULT_BLUEPRINT)
        db.connect_node_to_node(id_2,NodeLabels.RESULT_BLUEPRINT,id,NodeLabels.PROJECT)

        result = db.lookup_nodes(NodeLabels.RESULT_BLUEPRINT,NodeLabels.PROJECT,id)

        assert (
            UUID(result[0][0],version=4)
            and UUID(result[1][0],version=4)
            and result[0][0] == id_2 # order matters
            and result[1][0] == id_1
            and self.helper_datetime_checker(result[0][1]) == True 
            and self.helper_datetime_checker(result[1][1]) == True
        )



