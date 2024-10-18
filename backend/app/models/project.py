from app.database import Database, NodeProperties

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