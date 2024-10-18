from app.database import Database, NodeProperties
from result import Result
"""
class Project:
    def __init__(self, name, analyzed_files):
        self.__name = name
        self.__analyzed_files = analyzed_files
        self.__database = Database()
        
    def save_project(self):
        id_value = self.__database.add_project_node()
        self.__database.set_project_property(id_value, NodeProperties.Project.NAME, self.__name)
        self.save_analyzed_files(id_value)
        
    def save_analyzed_files(self, project_id):
        for file in self.__analyzed_files:
            file_id = self.__database.add_dataset_node(file)
            self.__database.connect_dataset_to_project(file_id, project_id)
        
            # Create result_blueprint node and add LLM result to it
            result_id = self.__database.add_result_blueprint_node(project_id, [file], [], [])
            self.__database.set_result_blueprint_property(result_id, NodeProperties.ResultBlueprint.RESULT, 'LLM text response here')
            """

class Project:
    def __init__(self, name: str, results: list):
        self.__project_id = None
        self.__name = name
        self.__results = results
        self.__database = Database()

    def save_project(self):
        self.__project_id = self.__database.add_project_node()
        self.__database.set_project_property(self.__project_id, NodeProperties.Project.NAME, self.__name)
        for result in self.__results:
            self.add_result(result)

    def add_result(self, result: Result):
        self.__database.connect_result_blueprint_to_project(result.__result_id, self.__project_id)





"""
bp1 = Blueprint("blueprint1", ["question1?", "question2?"])
bp1.save_blueprint()

...
...
...

# get selected blueprint? (first connect id to UI element and later get bp1 by id?)
result1 = Result("file1.pdf", bp1, "This file contains... (from LLM)")
result1.save_result()

...

project1 = Project("Project 1", [ result1 ])
project1.save_project()


result2 = Result("file2.pdf", bp1, "This file contains... (from LLM)")
project1.add_result(result2)
"""