import pytest
from app.database import Database, NodeProperties


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
def clear_database(db):
    """
    Automatically cleans up the database between tests.
    """
    db.debug_clear_all()


class TestAddNode:
    """Create node"""

    def test_global_settings(self,db):
        result = db.add_global_settings_node()
        assert result == 'Global'

    def test_user_settings(self,db):
        result = db.add_user_settings_node('alice')
        assert result == 'alice'

    def test_project(self,db):
        result = db.add_project_node()
        assert result != None

    def test_blueprint(self,db):
        result = db.add_blueprint_node()
        assert result != None

    def test_result_blueprint(self,db):
        result = db.add_result_blueprint_node()
        assert result != None

    def test_used_blueprint(self,db):
        id = db.add_blueprint_node()
        result = db.copy_to_used_blueprint_node(id)
        assert result != None       


class TestSetProperty:
    """Creating property"""

    def test_global_settings(self,db):
        db.add_global_settings_node()
        result = db.set_global_settings_property(NodeProperties.GlobalSettings.TEST_PASS, 'Verdana')
        assert result == True

    def test_user_settings(self,db):
        db.add_user_settings_node('alice')
        result = db.set_user_settings_property('alice', NodeProperties.UserSettings.TEST_PASS, 'Alice')
        assert result == True

    def test_project(self,db):
        id = db.add_project_node()
        result = db.set_project_property(id, NodeProperties.Project.TEST_PASS, 'foo')
        assert result == True

    def test_blueprint(self,db):
        id = db.add_blueprint_node()
        result = db.set_blueprint_property(id, NodeProperties.Blueprint.TEST_PASS, 'foo')
        assert result == True

    def test_result_blueprint(self,db):
        id = db.add_result_blueprint_node()
        result = db.set_result_blueprint_property(id, NodeProperties.ResultBlueprint.TEST_PASS, 'foo')
        assert result == True


class TestLookupPropertyFound:
    """Lookup property that is found"""

    def test_global_settings(self,db):
        db.add_global_settings_node()
        db.set_global_settings_property(NodeProperties.GlobalSettings.TEST_PASS, 'Verdana')
        result = db.lookup_global_settings_property(NodeProperties.GlobalSettings.TEST_PASS)
        assert result == 'Verdana'

    def test_user_settings(self,db):
        db.add_user_settings_node('alice')
        db.set_user_settings_property('alice', NodeProperties.UserSettings.TEST_PASS, 'Alice')
        result = db.lookup_user_settings_property('alice', NodeProperties.UserSettings.TEST_PASS)
        assert result == 'Alice'

    def test_project(self,db):
        id = db.add_project_node()
        db.set_project_property(id, NodeProperties.Project.TEST_PASS, 'foo')
        result = db.lookup_project_property(id, NodeProperties.Project.TEST_PASS)
        assert result == 'foo'

    def test_blueprint(self,db):
        id = db.add_blueprint_node()
        db.set_blueprint_property(id, NodeProperties.Blueprint.TEST_PASS, 'foo')
        result = db.lookup_blueprint_property(id, NodeProperties.Blueprint.TEST_PASS)
        assert result == 'foo'

    def test_result_blueprint(self,db):
        id = db.add_result_blueprint_node()
        db.set_result_blueprint_property(id, NodeProperties.ResultBlueprint.TEST_PASS, 'foo')
        result = db.lookup_result_blueprint_property(id, NodeProperties.ResultBlueprint.TEST_PASS)
        assert result == 'foo'

    def test_used_blueprint(self,db):
        id = db.add_blueprint_node()
        db.set_blueprint_property(id, NodeProperties.Blueprint.TEST_PASS, 'foo')
        id_2 = db.copy_to_used_blueprint_node(id)
        result = db.lookup_used_blueprint_property(id_2, NodeProperties.Blueprint.TEST_PASS)
        assert result == 'foo'


class TestLookupPropertyNotFound:
    """Lookup property that is not found"""

    def test_global_settings(self,db):
        db.add_global_settings_node()
        db.set_global_settings_property(NodeProperties.GlobalSettings.TEST_PASS, 'Verdana')
        result = db.lookup_global_settings_property(NodeProperties.GlobalSettings.TEST_FAIL)
        assert result == None

    def test_user_settings(self,db):
        db.add_user_settings_node('alice')
        db.set_user_settings_property('alice', NodeProperties.UserSettings.TEST_PASS, 'Alice')
        result = db.lookup_user_settings_property('alice', NodeProperties.UserSettings.TEST_FAIL)
        assert result == None

    def test_project(self,db):
        id = db.add_project_node()
        db.set_project_property(id, NodeProperties.Project.TEST_PASS, 'foo')
        result = db.lookup_project_property(id, NodeProperties.Project.TEST_FAIL)
        assert result == None

    def test_blueprint(self,db):
        id = db.add_blueprint_node()
        db.set_blueprint_property(id, NodeProperties.Blueprint.TEST_PASS, 'foo')
        result = db.lookup_blueprint_property(id, NodeProperties.Blueprint.TEST_FAIL)
        assert result == None

    def test_result_blueprint(self,db):
        id = db.add_result_blueprint_node()
        db.set_result_blueprint_property(id, NodeProperties.ResultBlueprint.TEST_PASS, 'foo')
        result = db.lookup_result_blueprint_property(id, NodeProperties.ResultBlueprint.TEST_FAIL)
        assert result == None

    def test_used_blueprint(self,db):
        id = db.add_blueprint_node()
        db.set_blueprint_property(id, NodeProperties.Blueprint.TEST_PASS, 'foo')
        id_2 = db.copy_to_used_blueprint_node(id)
        result = db.lookup_used_blueprint_property(id_2, NodeProperties.Blueprint.TEST_FAIL)
        assert result == None


class TestLookupPropertyNodeNotFound:
    """Lookup property node not found"""

    def test_user_settings(self,db):
        result = db.lookup_user_settings_property('wrong_id', NodeProperties.UserSettings.TEST_FAIL)
        assert result == None

    def test_project(self,db):
        result = db.lookup_project_property('wrong_id', NodeProperties.Project.TEST_FAIL)
        assert result == None

    def test_blueprint(self,db):
        result = db.lookup_blueprint_property('wrong_id', NodeProperties.Blueprint.TEST_FAIL)
        assert result == None

    def test_result_blueprint(self,db):
        result = db.lookup_result_blueprint_property('wrong_id', NodeProperties.ResultBlueprint.TEST_FAIL)
        assert result == None

    def test_used_blueprint(self,db):
        result = db.lookup_used_blueprint_property('wrong_id', NodeProperties.Blueprint.TEST_FAIL)
        assert result == None


class TestRemovePropertyFound:
    """Property remove"""

    def test_global_settings(self,db):
        db.add_global_settings_node()
        db.set_global_settings_property(NodeProperties.GlobalSettings.TEST_PASS, 'Verdana')
        result = db.remove_global_settings_property(NodeProperties.GlobalSettings.TEST_PASS)
        assert result == True

    def test_user_settings(self,db):
        db.add_user_settings_node('alice')
        db.set_user_settings_property('alice', NodeProperties.UserSettings.TEST_PASS, 'Alice')
        result = db.remove_user_settings_property('alice', NodeProperties.UserSettings.TEST_PASS)
        assert result == True

    def test_project(self,db):
        id = db.add_project_node()
        db.set_project_property(id, NodeProperties.Project.TEST_PASS, 'foo')
        result = db.remove_project_property(id, NodeProperties.Project.TEST_PASS)
        assert result == True

    def test_blueprint(self,db):
        id = db.add_blueprint_node()
        db.set_blueprint_property(id, NodeProperties.Blueprint.TEST_PASS, 'foo')
        result = db.remove_blueprint_property(id, NodeProperties.Blueprint.TEST_PASS)
        assert result == True

    def test_result_blueprint(self,db):
        id = db.add_result_blueprint_node()
        db.set_result_blueprint_property(id, NodeProperties.ResultBlueprint.TEST_PASS, 'foo')
        result = db.remove_result_blueprint_property(id, NodeProperties.ResultBlueprint.TEST_PASS)
        assert result == True


class TestRemovePropertyNotFound:
    """Remove property not found"""

    def test_global_settings(self,db):
        db.add_global_settings_node()
        db.set_global_settings_property(NodeProperties.GlobalSettings.TEST_PASS, 'Verdana')

        result = db.remove_global_settings_property(NodeProperties.GlobalSettings.TEST_FAIL)
        assert result == False
    def test_user_settings(self,db):
        db.add_user_settings_node('alice')
        db.set_user_settings_property('alice', NodeProperties.UserSettings.TEST_PASS, 'Alice')
        result = db.remove_user_settings_property('alice', NodeProperties.UserSettings.TEST_FAIL)
        assert result == False

    def test_project(self,db):
        id = db.add_project_node()
        db.set_project_property(id, NodeProperties.Project.TEST_PASS, 'foo')
        result = db.remove_project_property(id, NodeProperties.Project.TEST_FAIL)
        assert result == False

    def test_blueprint(self,db):
        id = db.add_blueprint_node()
        db.set_blueprint_property(id, NodeProperties.Blueprint.TEST_PASS, 'foo')
        result = db.remove_blueprint_property(id, NodeProperties.Blueprint.TEST_FAIL)
        assert result == False

    def test_result_blueprint(self,db):
        id = db.add_result_blueprint_node()
        db.set_result_blueprint_property(id, NodeProperties.ResultBlueprint.TEST_PASS, 'foo')
        result = db.remove_result_blueprint_property(id, NodeProperties.ResultBlueprint.TEST_FAIL)
        assert result == False


class TestRemovePropertyNodeNotFound:
    """Remove property node not found"""

    def test_user_settings(self,db):
        result = db.remove_user_settings_property('wrong_id', NodeProperties.UserSettings.TEST_FAIL)
        assert result == False

    def test_project(self,db):
        result = db.remove_project_property('wrong_id', NodeProperties.Project.TEST_FAIL)
        assert result == False

    def test_blueprint(self,db):
        result = db.remove_blueprint_property('wrong_id', NodeProperties.Blueprint.TEST_FAIL)
        assert result == False

    def test_result_blueprint(self,db):
        result = db.remove_result_blueprint_property('wrong_id', NodeProperties.ResultBlueprint.TEST_FAIL)
        assert result == False


class TestDeleteNode:
    """Delete node"""

    def test_global_settings(self,db):
        db.add_global_settings_node()
        result = db.delete_global_settings()
        assert result == True

    def test_user_settings(self,db):
        db.add_user_settings_node('alice')
        result = db.delete_user_settings('alice')
        assert result == True

    def test_project(self,db):
        id = db.add_project_node()
        result = db.delete_project(id)
        assert result == True

    def test_blueprint(self,db):
        id = db.add_blueprint_node()
        result = db.delete_blueprint(id)
        assert result == True

    def test_result_blueprint(self,db):
        id = db.add_result_blueprint_node()
        result = db.delete_result_blueprint(id)
        assert result == True


class TestDeleteNodeNotFound:
    """Delete node not found"""

    def test_global_settings(self,db):
        result = db.delete_global_settings()
        assert result == False

    def test_user_settings(self,db):
        result = db.delete_user_settings('wrong_id')
        assert result == False

    def test_project(self,db):
        result = db.delete_project('wrong_id')
        assert result == False

    def test_blueprint(self,db):
        id = db.add_blueprint_node()
        result = db.delete_blueprint('wrong_id')
        assert result == False

    def test_result_blueprint(self,db):
        id = db.add_result_blueprint_node()
        result = db.delete_result_blueprint('wrong_id')
        assert result == False


class TestRelationshipCreation:
    """Relationships between nodes"""

    def test_blueprint_user_settings(self,db):
        id_1 = db.add_blueprint_node()
        id_2 = db.add_user_settings_node('alice')
        result = db.connect_blueprint_to_user_settings(id_1, id_2)
        assert result == True

    def test_project_user_settings(self,db):
        id_1 = db.add_project_node()
        id_2 = db.add_user_settings_node('alice')
        result = db.connect_project_to_user_settings(id_1, id_2)
        assert result == True

    def test_result_blueprint_project(self,db):
        id_1 = db.add_result_blueprint_node()
        id_2 = db.add_project_node()
        result = db.connect_result_blueprint_to_project(id_1, id_2)
        assert result == True

    def test_used_blueprint_result_blueprint(self,db):
        id = db.add_blueprint_node()
        id_1 = db.copy_to_used_blueprint_node(id)
        id_2 = db.add_result_blueprint_node()
        result = db.connect_used_blueprint_to_result_blueprint(id_1, id_2)
        assert result == True


class TestRelationshipCreationBadToGood:
    """Relationships between bad to good nodes"""

    def test_blueprint_user_settings(self,db):
        id_2 = db.add_user_settings_node('alice')
        result = db.connect_blueprint_to_user_settings('wrong_id', id_2)
        assert result == False

    def test_project_user_settings(self,db):
        id_2 = db.add_user_settings_node('alice')
        result = db.connect_project_to_user_settings('wrong_id', id_2)
        assert result == False

    def test_result_blueprint_project(self,db):
        id_2 = db.add_project_node()
        result = db.connect_result_blueprint_to_project('wrong_id', id_2)
        assert result == False

    def test_used_blueprint_result_blueprint(self,db):
        id_2 = db.add_result_blueprint_node()
        result = db.connect_used_blueprint_to_result_blueprint('wrong_id', id_2)
        assert result == False


class TestRelationshipCreationGoodToBad:
    """Relationships between good to bad nodes"""

    def test_blueprint_user_settings(self,db):
        id_1 = db.add_blueprint_node()
        result = db.connect_blueprint_to_user_settings(id_1, 'wrong_id')
        assert result == False

    def test_project_user_settings(self,db):
        id_1 = db.add_project_node()
        result = db.connect_project_to_user_settings(id_1, 'wrong_id')
        assert result == False

    def test_result_blueprint_project(self,db):
        id_1 = db.add_result_blueprint_node()
        result = db.connect_result_blueprint_to_project(id_1, 'wrong_id')
        assert result == False

    def test_used_blueprint_result_blueprint(self,db):
        id = db.add_blueprint_node()
        id_1 = db.copy_to_used_blueprint_node(id)
        result = db.connect_used_blueprint_to_result_blueprint(id_1, 'wrong_id')
        assert result == False


class TestRelationshipCreationBadToBad:
    """Relationships between bad to bad nodes"""

    def test_blueprint_user_settings(self,db):
        result = db.connect_blueprint_to_user_settings('wrong_id', 'wrong_id')
        assert result == False

    def test_project_user_settings(self,db):
        result = db.connect_project_to_user_settings('wrong_id', 'wrong_id')
        assert result == False

    def test_result_blueprint_project(self,db):
        result = db.connect_result_blueprint_to_project('wrong_id', 'wrong_id')
        assert result == False

    def test_used_blueprint_result_blueprint(self,db):
        result = db.connect_used_blueprint_to_result_blueprint('wrong_id', 'wrong_id')
        assert result == False