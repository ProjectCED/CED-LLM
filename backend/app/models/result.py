from app.database import Database
from app.database import NodeProperties

class Result:
    def __init__(self, name: str, filename: str, blueprintId: str, result: str, projectId: str):
        self.__name = name
        self.__filename = filename
        self.__blueprintId = blueprintId
        self.__result = result
        self.__projectId = projectId
        self.__database = Database()

    def save_result(self):
        resultId = self.__database.add_result_blueprint_node()
        self.__database.set_result_blueprint_property(resultId, NodeProperties.ResultBlueprint.NAME, self.__name)
        self.__database.set_result_blueprint_property(resultId, NodeProperties.ResultBlueprint.FILENAME, self.__filename)
        self.__database.set_result_blueprint_property(resultId, NodeProperties.ResultBlueprint.RESULT, self.__result)

        # Set result under a project
        self.__database.connect_result_blueprint_to_project(resultId, self.__projectId)

        # Temp
        self.__database.set_result_blueprint_property(resultId, NodeProperties.ResultBlueprint.USED_BLUEPRINT, self.__blueprintId)
        return resultId

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