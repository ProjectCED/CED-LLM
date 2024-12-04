from app.database import Database, NodeProperties, NodeLabels, NodeRelationships

# just for show questions, don't use these
blueprint_questions = [
    'Lorem Ipsum dolor sit amet, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat?',
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

class DatabaseDummy2:
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
                None,
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
        #   filename)]
        __result_blueprints = [
            (
                __projects[1][0],
                __blueprints[1][0],
                '2023-05-15T09:45:15',
                'Lorem Ipsum sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
                'employee_performance_review_2024.pdf',
                ),
            (
                __projects[1][0],
                __blueprints[2][0],
                '2022-01-01T00:00:00',
                'Lorem Ipsum nulla facilisi, sed dapibus leo a quam ullamcorper, eu hendrerit odio condimentum.',
                'performance_evaluation_summary_Q1_2023.txt',
                ),
            (
                __projects[1][0],
                __blueprints[3][0],
                '2021-12-31T23:59:59',
                'Lorem Ipsum consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
                'annual_performance_feedback_2023.cvs',
                ),
            (
                __projects[2][0],
                __blueprints[4][0],
                '2021-09-15T19:00:00',
                'Lorem Ipsum sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
                'efficiency_metrics_analysis_2023.txt',
                ),
            (
                __projects[3][0],
                __blueprints[5][0],
                '2022-03-10T11:30:45',
                'Lorem Ipsum sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
                'customer_feedback_analysis_2024.txt',
                ),
            (
                __projects[4][0],
                __blueprints[2][0],
                '2023-06-20T16:45:00',
                'Lorem Ipsum sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
                'efficiency_metrics_analysis_2023.txt',
                ),
            (
                __projects[4][0],
                __blueprints[4][0],
                '2024-11-01T08:15:30',
                'Lorem Ipsum sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
                'compliance_assessment_report_2024.txt',
                ),
        ]
        self.__result_blueprint(__result_blueprints)

        # ### Data models
        # # [(name,
        # #   node_labels,
        # #   node_relationships)]
        # __datamodels = [
        #     (
        #         'Eduskunta',
        #         None,
        #         None,
        #         ),
        #     (
        #         'Wayfinder Realm',
        #         data_model_node_labels,
        #         data_model_node_relationships,
        #         ),
        #     (
        #         'SoftTag Grove',
        #         data_model_node_labels,
        #         data_model_node_relationships,
        #         ),
        #     (
        #         'Ramble Field',
        #         data_model_node_labels,
        #         data_model_node_relationships,
        #         ),
        #     (
        #         'Freespace Catalog',
        #         data_model_node_labels,
        #         data_model_node_relationships,
        #         ),
        # ]
        # self.__datamodels(__datamodels)
                


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
            # add more here

    def __blueprints(self, blueprints):
        '''Blueprints'''
        for blueprint in blueprints:
            id = self.db.add_blueprint_node()

            if not blueprint[0] == None:
                self.db.set_node_property(id, NodeLabels.BLUEPRINT, NodeProperties.Blueprint.NAME, blueprint[0])

            if not blueprint[1] == None:
                self.db.set_node_property(id, NodeLabels.BLUEPRINT, NodeProperties.Blueprint.DESCRIPTION, blueprint[1])

            if not blueprint[2] == None:
                self.db.set_node_property(id, NodeLabels.BLUEPRINT, NodeProperties.Blueprint.QUESTIONS, blueprint[2])
            # add more here

    # def __datamodels(self, datamodels):
    #     '''Datamodels'''
    #     for datamodel in datamodels:
    #         id = self.db.add_data_model_node()
    #         if not datamodel[0] == None:
    #             self.db.set_data_model_property(id, NodeProperties.DataModel.NAME, datamodel[0])

    #         if not datamodel[1] == None:
    #             self.db.set_data_model_property(id, NodeProperties.DataModel.NODE_LABELS, datamodel[1])

    #         if not datamodel[2] == None:
    #             self.db.set_data_model_property(id, NodeProperties.DataModel.RELATIONSHIP_TYPES, datamodel[2])
    #         # add more here

    def __projects(self, projects):
        '''Projects'''
        for project in projects:
            id = self.db.add_project_node()

            if not project[0] == None:
                self.db.set_node_property(id, NodeLabels.PROJECT, NodeProperties.Project.NAME, project[0])
            # add more here


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
                    if not result[2] == None:
                        self.db.set_node_property(result_id, NodeLabels.RESULT_BLUEPRINT, NodeProperties.ResultBlueprint.DATETIME, result[2])

                    if not result[3] == None:
                        self.db.set_node_property(result_id, NodeLabels.RESULT_BLUEPRINT, NodeProperties.ResultBlueprint.RESULT, result[3])

                    if not result[4] == None:
                        self.db.set_node_property(result_id, NodeLabels.RESULT_BLUEPRINT, NodeProperties.ResultBlueprint.FILENAME, result[4])
                    # add more here
