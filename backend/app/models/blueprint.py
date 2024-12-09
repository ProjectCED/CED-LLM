from app.database import Database, NodeProperties

class Blueprint:
    """
    Blueprint template class for creating and saving blueprint instances to the database.
    """
    def __init__(self, name: str, description: str, questions: list[str], blueprintId: str | None = None):
        """
        Constructor for Blueprint instances. Create an instance through this before saving.
        Also creates a reference to the database singleton.

        Args:
            name (string): User-given name of the blueprint.
            description (string): User-given description of the blueprint.
            questions (list[string]): Questions for the LLM through which to analyze and classify data.
            blueprintId (string, optional): UUID-type ID of the blueprint node in the database.
                Defaults to None, and is generated and returned through the database if not provided.
        """
        self.__blueprintId = blueprintId
        self.__name = name
        self.__description = description
        self.__questions = questions
        self.__database = Database()

    def save_blueprint(self) -> str:
        """
        Saves the blueprint to the database. If the blueprint already exists
        (ID provided through constructor), it is updated.

        Returns:
            string: UUID-type ID of the newly created blueprint node in the database.
        """
        # This check allows editing blueprint, no need to create a new node
        if self.__blueprintId is None:
            self.__blueprintId = self.__database.add_blueprint_node()
        self.__database.set_blueprint_property(self.__blueprintId, NodeProperties.Blueprint.NAME, self.__name)
        self.__database.set_blueprint_property(self.__blueprintId, NodeProperties.Blueprint.DESCRIPTION, self.__description)
        self.__database.set_blueprint_property(self.__blueprintId, NodeProperties.Blueprint.QUESTIONS, self.__questions)
        return self.__blueprintId