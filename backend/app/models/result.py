from app.database import Database
from app.database import NodeProperties
from blueprint import Blueprint

class Result:
    def __init__(self, filename: str, blueprint_id, result):
        self.__result_id = None
        self.__filename = filename
        self.__blueprint_id = blueprint_id
        self.__result = result
        self.__database = Database()

    def save_result(self):
        self.__result_id = self.__database.add_result_blueprint_node()
        self.__database.set_result_blueprint_property(self.__result_id, NodeProperties.ResultBlueprint.FILENAME, self.__filename)
        self.__database.set_result_blueprint_property(self.__result_id, NodeProperties.ResultBlueprint.RESULT, self.__result)
        used_blueprint_id = self.__database.copy_to_used_blueprint_node(self.__blueprint_id)
        self.__database.connect_used_blueprint_to_result_blueprint(self.__blueprint_id, self.__result_id)