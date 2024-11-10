import pytest
from app.database import Database, NodeProperties


@pytest.fixture(scope="module")
def db():
    database = Database()
    yield database

@pytest.fixture(autouse=True)
def clear_database(db):
    db.debug_clear_all()

def test_add_user(db):
    id = db.add_user_settings_node('alice')
    db.set_user_settings_property('alice', NodeProperties.UserSettings.NAME, 'Alice')

    result = db.lookup_user_settings_property('alice', NodeProperties.UserSettings.NAME)
    assert result == 'Alice'
