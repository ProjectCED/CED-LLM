from app.database import Database
from app.database import NodeProperties
from blueprint import Blueprint

class Result:
    def __init__(self, filename: str, used_blueprint: Blueprint, result):
        self.__result_id = None
        self.__filename = filename
        self.__used_blueprint = used_blueprint
        self.__result = result
        self.__database = Database()

    def save_result(self):
        self.__result_id = self.__database.add_result_blueprint_node()
        self.__database.set_result_blueprint_property(self.__result_id, NodeProperties.ResultBlueprint.FILENAME, self.__filename)
        self.__database.set_result_blueprint_property(self.__result_id, NodeProperties.ResultBlueprint.RESULT, self.__result)
        # connect used blueprint to result