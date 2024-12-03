from app.database import Database, NodeProperties
from app.models.result import Result

class Project:
    def __init__(self, name: str):
        self.__projectId = None
        self.__name = name
        self.__database = Database()

    def save_project(self):
        self.__projectId = self.__database.add_project_node()
        self.__database.set_project_property(self.__projectId, NodeProperties.Project.NAME, self.__name)
        return self.__projectId