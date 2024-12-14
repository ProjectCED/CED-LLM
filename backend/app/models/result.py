from app.database import Database
from app.database import NodeProperties, NodeLabels

class Result:
    """
    Result template class for creating and saving analysis result instances to the database.
    """
    def __init__(self, name: str, filename: str, blueprintId: str, result: str, projectId: str):
        """
        Constructor for Result instances. Create an instance through this before saving.
        Also creates a reference to the database singleton.

        Args:
            name (string): User-given name of the result.
            filename (string): Name of the analyzed file, if one was used.
                Can be null if the result was generated from text.
            blueprintId (string): UUID-type ID of the blueprint used to create the result.
            result (string): The analysis result text generated by the LLM.
            projectId (string): UUID-type ID of the project under which the result was created.
        """
        self.__name = name
        self.__filename = filename
        self.__blueprintId = blueprintId
        self.__result = result
        self.__projectId = projectId
        self.__database = Database()

    def save_result(self) -> str:
        """
        Saves the result to the database. Also connects the result to the proper project node.

        Returns:
            string: UUID-type ID of the newly created result node in the database.
        """
        resultId = self.__database.add_node(NodeLabels.RESULT_BLUEPRINT)
        self.__database.set_node_property(resultId, NodeLabels.RESULT_BLUEPRINT, NodeProperties.ResultBlueprint.NAME, self.__name)
        self.__database.set_node_property(resultId, NodeLabels.RESULT_BLUEPRINT, NodeProperties.ResultBlueprint.FILENAME, self.__filename)
        self.__database.set_node_property(resultId, NodeLabels.RESULT_BLUEPRINT, NodeProperties.ResultBlueprint.RESULT, self.__result)

        # Set result under a project
        self.__database.connect_node_to_node(resultId, NodeLabels.RESULT_BLUEPRINT, self.__projectId, NodeLabels.PROJECT)

        # Make used blueprint and connect it to result
        usedBlueprintId = self.__database.copy_node_to_node(self.__blueprintId, NodeLabels.BLUEPRINT, NodeLabels.USED_BLUEPRINT)
        self.__database.connect_node_to_node(usedBlueprintId, NodeLabels.USED_BLUEPRINT, resultId, NodeLabels.RESULT_BLUEPRINT)
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