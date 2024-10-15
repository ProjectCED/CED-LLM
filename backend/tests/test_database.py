

#from ..app.database import database
#import sys
#sys.path.append('../app')
from app.database import Database, NodeProperties

# Supress neo4j warnings on error tests
import logging
logging.getLogger("neo4j").setLevel(logging.ERROR)

db = Database()

class db_test:
    def __init__(self) -> None:
        self.__success = 0
        self.__failed = 0

    def test_global_settings(self):
        success = 0
        failed = 0

        print( '### Global settings testing' )
        
        print( '<Creation>' )
        id_value = db.add_global_settings_node()
        if id_value == None:
            print( 'Failed' )
            failed += 1
        elif id_value == 'Global':
            success += 1
        else:
            print( 'Failed' )
            failed += 1

        print( '<Set property>' )
        if db.set_global_settings_property(NodeProperties.GlobalSettings.TEST_PASS, 'Verdana'):
            success += 1
        else:
            print( 'Failed' )
            failed += 1

        print( '<Lookup property>' )
        if db.lookup_global_settings_property(NodeProperties.GlobalSettings.TEST_PASS) == 'Verdana':
            success += 1
        else:
            print( 'Failed' )
            failed += 1
        
        print( '<Lookup non existent property>' )
        if db.lookup_global_settings_property(NodeProperties.GlobalSettings.TEST_FAIL) == None:
            success += 1
        else:
            print( 'Failed' )
            failed += 1
        
        print( '<Remove property>' )
        if db.remove_global_settings_property(NodeProperties.GlobalSettings.TEST_PASS):
            success += 1
        else:
            print( 'Failed' )
            failed += 1

        print( '<Remove non existent property>' )
        if db.remove_global_settings_property(NodeProperties.GlobalSettings.TEST_FAIL):
            print( 'Failed' )
            failed += 1
        else:
            success += 1

        print( '<Delete node>' )
        if db.delete_global_settings():
            success += 1
        else:
            print( 'Failed' )
            failed += 1

        self.__success += success
        self.__failed += failed

        print( '--------------------')
        print( 'Project testing:' )
        print( 'Success: ' + str(success) )
        print( 'Failed: ' + str(failed) )
        print( '--------------------')


    def test_user_settings(self):
        success = 0
        failed = 0

        print( '### User settings testing' )
        
        print( '<Creation>' )
        id_value = db.add_user_settings_node('jaak')
        if id_value == None:
            print( 'Failed' )
            failed += 1
        elif id_value == 'jaak':
            success += 1
        else:
            print( 'Failed' )
            failed += 1

        print( '<Set property>' )
        if db.set_user_settings_property(id_value, NodeProperties.UserSettings.TEST_PASS, 'Jaakko'):
            success += 1
        else:
            print( 'Failed' )
            failed += 1

        print( '<Lookup property>' )
        if db.lookup_user_settings_property(id_value, NodeProperties.UserSettings.TEST_PASS) == 'Jaakko':
            success += 1
        else:
            print( 'Failed' )
            failed += 1
        
        print( '<Lookup property from non existent node>' )
        if db.lookup_user_settings_property('wrong_node_id_value', NodeProperties.UserSettings.TEST_PASS) == None:
            success += 1
        else:
            print( 'Failed' )
            failed += 1
        
        print( '<Lookup non existent property>' )
        if db.lookup_user_settings_property(id_value, NodeProperties.UserSettings.TEST_FAIL) == None:
            success += 1
        else:
            print( 'Failed' )
            failed += 1
        
        print( '<Remove property>' )
        if db.remove_user_settings_property(id_value, NodeProperties.UserSettings.TEST_PASS):
            success += 1
        else:
            print( 'Failed' )
            failed += 1

        print( '<Remove property from non existent node>' )
        if db.remove_user_settings_property('wrong_node_id_value', NodeProperties.UserSettings.TEST_PASS):
            print( 'Failed' )
            failed += 1
        else:
            success += 1

        print( '<Remove non existent property>' )
        if db.remove_user_settings_property(id_value, NodeProperties.UserSettings.TEST_FAIL):
            print( 'Failed' )
            failed += 1
        else:
            success += 1

        print( '<Delete node>' )
        if db.delete_user_settings(id_value):
            success += 1
        else:
            print( 'Failed' )
            failed += 1

        print( '<Delete non existent node>' )
        if db.delete_user_settings('wrong_node_id_value'):
            print( 'Failed' )
            failed += 1
        else:
            success += 1

        self.__success += success
        self.__failed += failed
        
        print( '--------------------')
        print( 'User settings testing:' )
        print( 'Success: ' + str(success) )
        print( 'Failed: ' + str(failed) )
        print( '--------------------')


    def test_project(self):
        success = 0
        failed = 0

        print( '### Project testing' )
        
        print( '<Creation>' )
        id_value = db.add_project_node()
        if id_value == None:
            print( 'Failed' )
            failed += 1
        else:
            success += 1

        print( '<Set property>' )
        if db.set_project_property(id_value, NodeProperties.Project.TEST_PASS, 'Eduskunta'):
            success += 1
        else:
            print( 'Failed' )
            failed += 1

        print( '<Lookup property>' )
        if db.lookup_project_property(id_value, NodeProperties.Project.TEST_PASS) == 'Eduskunta':
            success += 1
        else:
            print( 'Failed' )
            failed += 1
        
        print( '<Lookup property from non existent node>' )
        if db.lookup_project_property('wrong_node_id_value', NodeProperties.Project.TEST_PASS) == None:
            success += 1
        else:
            print( 'Failed' )
            failed += 1
        
        print( '<Lookup non existent property>' )
        if db.lookup_project_property(id_value, NodeProperties.Project.TEST_FAIL) == None:
            success += 1
        else:
            print( 'Failed' )
            failed += 1
        
        print( '<Remove property>' )
        if db.remove_project_property(id_value, NodeProperties.Project.TEST_PASS):
            success += 1
        else:
            print( 'Failed' )
            failed += 1

        print( '<Remove property from non existent node>' )
        if db.remove_project_property('wrong_node_id_value', NodeProperties.Project.TEST_PASS):
            print( 'Failed' )
            failed += 1
        else:
            success += 1

        print( '<Remove non existent property>' )
        if db.remove_project_property(id_value, NodeProperties.Project.TEST_FAIL):
            print( 'Failed' )
            failed += 1
        else:
            success += 1

        print( '<Delete node>' )
        if db.delete_project(id_value):
            success += 1
        else:
            print( 'Failed' )
            failed += 1


        self.__success += success
        self.__failed += failed
        

        print( '--------------------')
        print( 'Project testing:' )
        print( 'Success: ' + str(success) )
        print( 'Failed: ' + str(failed) )
        print( '--------------------')


    def test_dataset(self):
        success = 0
        failed = 0


        print( '### Dataset testing' )
        print( '<Creation>' )
        id_value = db.add_dataset_node()
        if id_value == None:
            print( 'Failed' )
            failed += 1
        else:
            success += 1

        print( '<Set property>' )
        if db.set_dataset_property(id_value, 'puheet_2024.pdf'):
            success += 1
        else:
            print( 'Failed' )
            failed += 1

        print( '<Lookup property>' )
        if db.lookup_dataset_property(id_value) == 'puheet_2024.pdf':
            success += 1
        else:
            print( 'Failed' )
            failed += 1
        
        print( '<Lookup non existent node property>' )
        if db.lookup_dataset_property('wrong_node_id_value') == None:
            success += 1
        else:
            print( 'Failed' )
            failed += 1

        print( '<Remove property>' )
        if db.remove_dataset_property(id_value):
            success += 1
        else:
            print( 'Failed' )
            failed += 1

        print( '<Remove property from non existent node>' )
        if db.remove_dataset_property('wrong_id_value'):
            print( 'Failed' )
            failed += 1
        else:
            success += 1

        print( '<Remove non existent property>' )
        id_value_2 = db.add_dataset_node()
        if db.remove_dataset_property(id_value_2):
            print( 'Failed' )
            failed += 1
        else:
            success += 1

        print( '<Delete node>' )
        if db.delete_dataset(id_value):
            success += 1
        else:
            print( 'Failed' )
            failed += 1

        print( '<Delete non existent node>' )
        if db.delete_dataset('wrong_node_id_value'):
            print( 'Failed' )
            failed += 1
        else:
            success += 1

        # cleanup
        db.delete_dataset(id_value_2)


        self.__success += success
        self.__failed += failed


        print( '--------------------')
        print( 'Dataset testing:' )
        print( 'Success: ' + str(success) )
        print( 'Failed: ' + str(failed) )
        print( '--------------------')

    def test_data_model(self):
        success = 0
        failed = 0

        print( '### Data model testing' )
        
        print( '<Creation>' )
        id_value = db.add_data_model_node()
        if id_value == None:
            print( 'Failed' )
            failed += 1
        else:
            success += 1

        print( '<Set property>' )
        if db.set_data_model_property(id_value, NodeProperties.DataModel.TEST_PASS, 'puhe_malli'):
            success += 1
        else:
            print( 'Failed' )
            failed += 1

        print( '<Lookup property>' )
        if db.lookup_data_model_property(id_value, NodeProperties.DataModel.TEST_PASS) == 'puhe_malli':
            success += 1
        else:
            print( 'Failed' )
            failed += 1
        
        print( '<Lookup property from non existent node>' )
        if db.lookup_data_model_property('wrong_node_id_value', NodeProperties.DataModel.TEST_PASS) == None:
            success += 1
        else:
            print( 'Failed' )
            failed += 1
        
        print( '<Lookup non existent property>' )
        if db.lookup_data_model_property(id_value, NodeProperties.DataModel.TEST_FAIL) == None:
            success += 1
        else:
            print( 'Failed' )
            failed += 1
        
        print( '<Remove property>' )
        if db.remove_data_model_property(id_value, NodeProperties.DataModel.TEST_PASS):
            success += 1
        else:
            print( 'Failed' )
            failed += 1

        print( '<Remove property from non existent node>' )
        if db.remove_data_model_property('wrong_node_id_value', NodeProperties.DataModel.TEST_PASS):
            print( 'Failed' )
            failed += 1
        else:
            success += 1

        print( '<Remove non existent property>' )
        if db.remove_data_model_property(id_value, NodeProperties.DataModel.TEST_FAIL):
            print( 'Failed' )
            failed += 1
        else:
            success += 1

        print( '<Delete node>' )
        if db.delete_data_model(id_value):
            success += 1
        else:
            print( 'Failed' )
            failed += 1
        
        print( '<Delete non existent node>' )
        if db.delete_data_model('wrong_node_id_value'):
            print( 'Failed' )
            failed += 1
        else:
            success += 1


        self.__success += success
        self.__failed += failed


        print( '--------------------')
        print( 'Data model testing:' )
        print( 'Success: ' + str(success) )
        print( 'Failed: ' + str(failed) )
        print( '--------------------')


    def test_analyze_model(self):
        success = 0
        failed = 0

        print( '### Analyze model testing' )
        
        print( '<Creation>' )
        id_value = db.add_analyze_model_node()
        if id_value == None:
            print( 'Failed' )
            failed += 1
        else:
            success += 1

        print( '<Set property>' )
        if db.set_analyze_model_property(id_value, NodeProperties.AnalyzeModel.TEST_PASS, 'puhe_malli'):
            success += 1
        else:
            print( 'Failed' )
            failed += 1

        print( '<Lookup property>' )
        if db.lookup_analyze_model_property(id_value, NodeProperties.AnalyzeModel.TEST_PASS) == 'puhe_malli':
            success += 1
        else:
            print( 'Failed' )
            failed += 1
        
        print( '<Lookup property from non existent node>' )
        if db.lookup_analyze_model_property('wrong_node_id_value', NodeProperties.AnalyzeModel.TEST_PASS) == None:
            success += 1
        else:
            print( 'Failed' )
            failed += 1
        
        print( '<Lookup non existent property>' )
        if db.lookup_analyze_model_property(id_value, NodeProperties.AnalyzeModel.TEST_FAIL) == None:
            success += 1
        else:
            print( 'Failed' )
            failed += 1
        
        print( '<Remove property>' )
        if db.remove_analyze_model_property(id_value, NodeProperties.AnalyzeModel.TEST_PASS):
            success += 1
        else:
            print( 'Failed' )
            failed += 1

        print( '<Remove property from non existent node>' )
        if db.remove_analyze_model_property('wrong_node_id_value', NodeProperties.AnalyzeModel.TEST_PASS):
            print( 'Failed' )
            failed += 1
        else:
            success += 1

        print( '<Remove non existent property>' )
        if db.remove_analyze_model_property(id_value, NodeProperties.AnalyzeModel.TEST_FAIL):
            print( 'Failed' )
            failed += 1
        else:
            success += 1

        print( '<Delete node>' )
        if db.delete_analyze_model(id_value):
            success += 1
        else:
            print( 'Failed' )
            failed += 1
        
        print( '<Delete node>' )
        if db.delete_analyze_model('wrong_node_id_value'):
            print( 'Failed' )
            failed += 1
        else:
            success += 1


        self.__success += success
        self.__failed += failed


        print( '--------------------')
        print( 'Analyze model testing:' )
        print( 'Success: ' + str(success) )
        print( 'Failed: ' + str(failed) )
        print( '--------------------')

    def test_print_node_types(self):

        print( 'Node id types:' )
        print( 'Global settings:' )
        print( db.get_global_settings_id_type())
        print( 'User settings:' )
        print( db.get_user_settings_id_type())
        print( 'Project:' )
        print( db.get_project_id_type())
        print( 'Dataset:' )
        print( db.get_dataset_id_type())
        print( 'Data model:' )
        print( db.get_data_model_id_type())
        print( 'Analyze model:' )
        print( db.get_analyze_model_id_type())
        print( 'Result:' )
        print( db.get_result_id_type())

    def test_relatioships(self):
        success = 0
        failed = 0

        print( '### Relationship testing' )
        print( '<Creations>' )

        print( '<Dataset to...>' )
        dataset_id_value = db.add_dataset_node()

        print( '<... data model>' )
        data_model_id_value = db.add_data_model_node()
        if db.connect_dataset_to_data_model(dataset_id_value,data_model_id_value):
            success += 1
        else:
            print( 'Failed' )
            failed += 1
        
        print( '<... analyze model>' )
        analyze_model_id_value = db.add_analyze_model_node()
        if db.connect_dataset_to_analyze_model(dataset_id_value,analyze_model_id_value):
            success += 1
        else:
            print( 'Failed' )
            failed += 1
        
        print( '<... project>' )
        project_id_value = db.add_project_node()
        if db.connect_dataset_to_project(dataset_id_value,project_id_value):
            success += 1
        else:
            print( 'Failed' )
            failed += 1

        print( '<Data model to...>' )
        print( '<... project>' )
        if db.connect_data_model_to_project(data_model_id_value,project_id_value):
            success += 1
        else:
            print( 'Failed' )
            failed += 1


        print( '<Error testing>' )
        print( '<Bad dataset...>' )
        print( '<... data model>' )
        if db.connect_dataset_to_data_model('bad',data_model_id_value):
            print( 'Failed' )
            failed += 1
        else:
            success += 1
        
        print( '<... analyze model>' )
        if db.connect_dataset_to_analyze_model('bad',analyze_model_id_value):
            print( 'Failed' )
            failed += 1
        else:
            success += 1
        
        print( '<... project>' )
        if db.connect_dataset_to_project('bad',project_id_value):
            print( 'Failed' )
            failed += 1
        else:
            success += 1
        
        print( '<Dataset...>' )
        print( '<... bad data model>' )
        if db.connect_dataset_to_data_model(dataset_id_value,'bad'):
            print( 'Failed' )
            failed += 1
        else:
            success += 1
        
        print( '<... bad analyze model>' )
        if db.connect_dataset_to_analyze_model(dataset_id_value,'bad'):
            print( 'Failed' )
            failed += 1
        else:
            success += 1
        
        print( '<... bad project>' )
        if db.connect_dataset_to_project(dataset_id_value,'bad'):
            print( 'Failed' )
            failed += 1
        else:
            success += 1

        print( '<Bad to bad>' )
        if db.connect_dataset_to_project('bad','bad'):
            print( 'Failed' )
            failed += 1
        else:
            success += 1


        # cleanup
        db.delete_dataset(dataset_id_value)
        db.delete_data_model(data_model_id_value)
        db.delete_analyze_model(analyze_model_id_value)
        db.delete_project(project_id_value)


        self.__success += success
        self.__failed += failed


        print( '--------------------')
        print( 'Relationship testing:' )
        print( 'Success: ' + str(success) )
        print( 'Failed: ' + str(failed) )
        print( '--------------------')   


    def test_bulk(self):
        ### debug cleaning
        print( db.debug_clear_all() )

        self.test_print_node_types()

        self.test_global_settings()
        self.test_user_settings()
        self.test_dataset()
        self.test_data_model()
        self.test_analyze_model()
        self.test_project()

        self.test_relatioships()

        print( '--------------------')
        print( 'Bulk testing:' )
        print( 'Success: ' + str(self.__success) )
        print( 'Failed: ' + str(self.__failed) )
        print( '--------------------')   

