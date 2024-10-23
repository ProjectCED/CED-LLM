# runs from backend directory with "python -m tests.tests"
from tests.test_database import *

test_db = db_test()

if __name__ == "__main__":

    test_db.test_bulk()