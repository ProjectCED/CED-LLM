from app.database import Database, NodeProperties

class Blueprint:
    def __init__(self, name: str, description: str, questions: list):
        self.__blueprint_id = None
        self.__name = name
        self.__description = description
        self.__questions = questions
        self.__database = Database()

    def save_blueprint(self):
        self.__blueprint_id = self.__database.add_blueprint_node()
        self.__database.set_blueprint_property(self.__blueprint_id, NodeProperties.Blueprint.NAME, self.__name)
        self.__database.set_blueprint_property(self.__blueprint_id, NodeProperties.Blueprint.DESCRIPTION, self.__description)
        self.__database.set_blueprint_property(self.__blueprint_id, NodeProperties.Blueprint.QUESTIONS, self.__questions)
        return self.__blueprint_id