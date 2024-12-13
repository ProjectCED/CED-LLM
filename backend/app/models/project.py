from app.database import Database, NodeProperties, NodeLabels
from app.models.result import Result

class Project:
    """
    Project template class for creating and saving project instances to the database.
    """
    def __init__(self, name: str):
        """ 
        Constructor for Project instances. Create an instance through this before saving.
        Also creates a reference to the database singleton.
        
        Args:
            name (string): User-given name of the project.
        """
        self.__name = name
        self.__database = Database()

    def save_project(self) -> str:
        """
        Saves the project to the database.

        Returns:
            string: UUID-type ID of the newly created project node in the database.
        """
        projectId = self.__database.add_node(NodeLabels.PROJECT)
        self.__database.set_node_property(projectId, NodeLabels.PROJECT, NodeProperties.Project.NAME, self.__name)
        return projectId