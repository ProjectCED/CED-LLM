from app.database import Database
from app.database import NodeProperties

class Result:
    def __init__(self, name: str, filename: str, blueprint_id: str, result: str):
        self.__name = name
        self.__filename = filename
        self.__blueprint_id = blueprint_id
        self.__result = result
        self.__database = Database()

    def save_result(self):
        result_id = self.__database.add_result_blueprint_node()
        self.__database.set_result_blueprint_property(result_id, NodeProperties.ResultBlueprint.NAME, self.__name)
        self.__database.set_result_blueprint_property(id, NodeProperties.ResultBlueprint.FILENAME, self.__filename)
        self.__database.set_result_blueprint_property(id, NodeProperties.ResultBlueprint.RESULT, self.__result)

        self.__database.set_result_blueprint_property(result_id, NodeProperties.ResultBlueprint.USED_BLUEPRINT, self.__blueprint_id)
        return result_id

        '''
        # If an automatic blueprint was used, blueprint id is null and we can return
        if self.__blueprint_id is None:
            return result_id, None

        # Copying blueprint to used variant
        used_blueprint_id = self.__database.copy_to_used_blueprint_node(self.__blueprint_id)
        self.__database.set_result_blueprint_property(result_id, NodeProperties.ResultBlueprint.USED_BLUEPRINT, used_blueprint_id)
        self.__database.connect_used_blueprint_to_result_blueprint(used_blueprint_id, result_id)

        return result_id, used_blueprint_id
        '''