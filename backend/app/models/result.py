from app.database import Database
from app.database import NodeProperties

class Result:
    def __init__(self, filename: str, used_blueprint_id, result):
        self.__result_id = None
        self.__filename = filename
        self.__used_blueprint_id = used_blueprint_id
        self.__result = result
        self.__database = Database()

    def save_result(self):
        self.__result_id = self.__database.add_result_blueprint_node()
        self.__database.set_result_blueprint_property(self.__result_id, NodeProperties.ResultBlueprint.FILENAME, self.__filename)
        self.__database.set_result_blueprint_property(self.__result_id, NodeProperties.ResultBlueprint.RESULT, self.__result)
        self.__database.set_result_blueprint_property(self.__result_id, NodeProperties.ResultBlueprint.USED_BLUEPRINT, self.__used_blueprint_id)
        self.__database.connect_used_blueprint_to_result_blueprint(self.__used_blueprint_id, self.__result_id)