from app.database import Database, NodeProperties

class Blueprint:
    def __init__(self, name: str, description: str, questions: list):
        self.__blueprintId = None
        self.__name = name
        self.__description = description
        self.__questions = questions
        self.__database = Database()

    def save_blueprint(self):
        self.__blueprintId = self.__database.add_blueprint_node()
        self.__database.set_blueprint_property(self.__blueprintId, NodeProperties.Blueprint.NAME, self.__name)
        self.__database.set_blueprint_property(self.__blueprintId, NodeProperties.Blueprint.DESCRIPTION, self.__description)
        self.__database.set_blueprint_property(self.__blueprintId, NodeProperties.Blueprint.QUESTIONS, self.__questions)
        return self.__blueprintId