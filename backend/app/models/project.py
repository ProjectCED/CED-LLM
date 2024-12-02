from app.database import Database, NodeProperties
from app.models.result import Result

class Project:
    def __init__(self, name: str):
        self.__project_id = None
        self.__name = name
        self.__database = Database()

    def save_project(self):
        self.__project_id = self.__database.add_project_node()
        self.__database.set_project_property(self.__project_id, NodeProperties.Project.NAME, self.__name)
        return self.__project_id

    def add_result(self, result: Result):
        if self.__project_id is None:
            raise ValueError("Project must be saved before adding results")
        self.__database.connect_result_blueprint_to_project(result.__result_id, self.__project_id)