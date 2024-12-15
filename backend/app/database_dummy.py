from app.database import Database, NodeProperties, NodeLabels
from neo4j.time import DateTime

# just for show questions, don't use these
blueprint_questions = [
    '',
    'Lorem Ipsum sed do eiusmod tempor incididunt ut labore et dolore magna aliqua, vel iusto odio dignissim qui blandit praesent luptatum zzril?',
    'Lorem Ipsum consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua, enim ad minim veniam?',
    'Lorem Ipsum ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat?',
    'Lorem Ipsum Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur?',
]

# Just for show data model, don't use these
data_model_node_labels = [
    'AuraTangle',
    'LinkageMist',
    'GlyphShade',
    'BloomEmber',
    'PathwayTwist',
]
data_model_node_relationships = [
    'ECHOES_WITH',
    'FLOWS_TOWARD',
    'LOOPS_INTO',
    'LINKS_THROUGH',
]

class DatabaseDummy:
    '''Creates pre-filled dummy database
    
    Warning. This will first clear the database.
    '''
    def __init__(self):
        '''
        When editing:
        - be sure to have all names unique for this example to work
        - When adding new example properties to tuples, need to also add code line for it further down.
        '''
        self.db = Database()

        ### clear all
        self.__clear()

        ### global settings
        #example:
        # font and size
        # __global = ('verdana', '10')
        __global = ()
        self.__global(__global)

        ### user settings
        # [(name,
        #   email)]
        __users = [
            (
                'John Smith',
                'john.smith@example.com',
                ),
            (
                'Jane Doe',
                'jane.doe@example.com',
                ),
            (
                'Emily Johnson',
                'emily.johnson@example.com',
                ),
            (
                'Michael Brown',
                'michael.brown@example.com',
                ),
        ]
        self.__users(__users)

        ### blueprints
        # [(name,
        #   description,
        #   questions)]
        __blueprints = [
            (
                'Eduskunta ',
                'A collaborative framework designed to enhance educational dialogue and decision-making through structured discussions and feedback.',
                [],
                ),
            (
                'Brainstorm Blueprint',
                'A creative framework that uses guided questions to spark innovative ideas and foster collaborative thinking.',
                blueprint_questions,
                ),
            (
                'Thought Explorer',
                'A stimulating guide that encourages deep reflection and discovery through targeted questions and open-ended inquiries.',
                blueprint_questions,
                ),
            (
                'Inquiry Adventure',
                'An engaging toolkit designed to inspire curiosity and exploration through a series of thought-provoking questions.',
                blueprint_questions,
                ),
            (
                'Dialogue Design',
                'A structured approach that fosters meaningful conversations by providing a framework of insightful questions and prompts.',
                blueprint_questions,
                ),
            (
                'Idea Igniter',
                'A creative catalyst that sparks inspiration and generates innovative ideas through targeted prompts and questions.',
                blueprint_questions,
                ),
            (
                'Question Quest',
                'A playful exploration that drives discovery and insight through a series of engaging and thought-provoking questions.',
                blueprint_questions,
                ),
        ]
        self.__blueprints(__blueprints)

        ### projects
        # [(name)]
        __projects = [
            (
                'Eduskunta',
                ),
            (
                'Performance Review',
                ),
            (
                'Operations Enhancement',
                ),
            (
                'Quality Improvement',
                ),
            (
                'Compliance Assessment',
                ),
        ]
        self.__projects(__projects)

        ### Result-Blueprint
        # references __project names
        # references __blueprint names
        # [(project-name,
        #   blueprint-name,
        #   datetime.iso(),
        #   result,
        #   filename,
        #   name)]
        __result_blueprints = [
            (
                __projects[1][0],
                __blueprints[1][0],
                DateTime(2024, 1, 12, 14, 25, 36, 0),
                'Lorem Ipsum sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
                'employee_performance_review_2024.pdf',
                '14:25 12-1-2024',
                ),
            (
                __projects[1][0],
                __blueprints[2][0],
                DateTime(2024, 3, 5, 9, 13, 45, 0), 
                'Lorem Ipsum nulla facilisi, sed dapibus leo a quam ullamcorper, eu hendrerit odio condimentum.',
                'performance_evaluation_summary_Q1_2023.txt',
                '9:13 5-3-2024',
                ),
            (
                __projects[1][0],
                __blueprints[3][0],
                DateTime(2024, 4, 18, 22, 57, 12, 0),
                'Lorem Ipsum consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
                'annual_performance_feedback_2023.cvs',
                '22:57 18-4-2024',
                ),
            (
                __projects[2][0],
                __blueprints[4][0],
                DateTime(2024, 6, 7, 7, 30, 0, 0),
                'Lorem Ipsum sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
                'efficiency_metrics_analysis_2023.txt',
                '7:30 7-6-2024'
                ),
            (
                __projects[3][0],
                __blueprints[5][0],
                DateTime(2024, 8, 14, 16, 45, 22, 0),
                'Lorem Ipsum sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
                'customer_feedback_analysis_2024.txt',
                '16:45 14-8-2024',
                ),
            (
                __projects[4][0],
                __blueprints[2][0],
                DateTime(2024, 10, 3, 11, 8, 9, 0),
                'Lorem Ipsum sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
                'efficiency_metrics_analysis_2023.txt',
                '11:08 3-10-2024',
                ),
            (
                __projects[4][0],
                __blueprints[4][0],
                DateTime(2024, 11, 21, 20, 19, 40, 0),
                'Lorem Ipsum sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
                'compliance_assessment_report_2024.txt',
                '20:19 21-11-2024',
                ),
        ]
        self.__result_blueprint(__result_blueprints)


    def __clear(self):
        '''Clear database'''
        self.db.debug_clear_all()

    def __global(self, tuple):
        '''Global settings'''
        self.db.add_node(NodeLabels.GLOBAL_SETTINGS)
        # example
        #self.db.set_global_settings_property(NodeProperties.GlobalSettings.FONT, tuple[0])

    def __users(self, users):
        '''User Settings'''
        for user in users:
            id = self.db.add_node(NodeLabels.USER_SETTINGS)
            self.db.set_node_property(id, NodeLabels.USER_SETTINGS,NodeProperties.UserSettings.NAME, user[0])
            self.db.set_node_property(id, NodeLabels.USER_SETTINGS,NodeProperties.UserSettings.USER_NAME, user[1])
            ### add more here

    def __blueprints(self, blueprints):
        '''Blueprints'''
        for blueprint in blueprints:
            id = self.db.add_node(NodeLabels.BLUEPRINT)

            if not blueprint[0] == None:
                self.db.set_node_property(id, NodeLabels.BLUEPRINT, NodeProperties.Blueprint.NAME, blueprint[0])

            if not blueprint[1] == None:
                self.db.set_node_property(id, NodeLabels.BLUEPRINT, NodeProperties.Blueprint.DESCRIPTION, blueprint[1])

            if not blueprint[2] == None:
                self.db.set_node_property(id, NodeLabels.BLUEPRINT, NodeProperties.Blueprint.QUESTIONS, blueprint[2])
            ### add more here

    def __projects(self, projects):
        '''Projects'''
        for project in projects:
            id = self.db.add_node(NodeLabels.PROJECT)

            if not project[0] == None:
                self.db.set_node_property(id, NodeLabels.PROJECT, NodeProperties.Project.NAME, project[0])
            ### add more here


    def __result_blueprint(self, results):
        '''Result-Blueprint'''
        projects = self.db.lookup_nodes(NodeLabels.PROJECT)
        blueprints = self.db.lookup_nodes(NodeLabels.BLUEPRINT)
        for result in results:
            result_id = self.db.add_node(NodeLabels.RESULT_BLUEPRINT)

            # search blueprint id
            blueprint_id = None
            for blue_id, blue_name, blue_datetime in blueprints:
                if blue_name == result[1]:
                    blueprint_id = blue_id

            # connect results to specific projects
            for project_id, project_name, project_datetime in projects:
                if project_name == result[0]:
                    # result -> project
                    self.db.connect_node_to_node(result_id, NodeLabels.RESULT_BLUEPRINT, project_id, NodeLabels.PROJECT)
                    # used blueprint -> result
                    used_blue_id = self.db.copy_node_to_node(blueprint_id, NodeLabels.BLUEPRINT, NodeLabels.USED_BLUEPRINT)
                    self.db.connect_node_to_node(used_blue_id, NodeLabels.USED_BLUEPRINT, result_id, NodeLabels.RESULT_BLUEPRINT)

                    # properties
                    if not result[3] == None:
                        self.db.set_node_property(result_id, NodeLabels.RESULT_BLUEPRINT, NodeProperties.ResultBlueprint.RESULT, result[3])

                    if not result[4] == None:
                        self.db.set_node_property(result_id, NodeLabels.RESULT_BLUEPRINT, NodeProperties.ResultBlueprint.FILENAME, result[4])

                    if not result[5] == None:
                        self.db.set_node_property(result_id, NodeLabels.RESULT_BLUEPRINT, NodeProperties.ResultBlueprint.NAME, result[5])
                    ### add more here

                    # datetime has to be last as it will get overwritten otherwise by .now()
                    if not result[2] == None:
                        self.db.set_node_property(result_id, NodeLabels.RESULT_BLUEPRINT, NodeProperties.ResultBlueprint.DATETIME, result[2])
