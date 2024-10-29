from database import Database, NodeProperties

class DatabaseDummy:
    '''Create pre-filled dummy database'''
    def __init__(self):
        '''Initialize'''
        self.db = Database()

        # clear all
        self.__clear()

        # global settings
        self.__global()

        # user settings
        self.__users()

        # blueprints
        self.__blueprints()


    def __clear(self):
        '''Clear database'''
        self.db.debug_clear_all()

    def __global(self):
        '''Global settings'''
        self.db.add_global_settings_node()

    def __users(self):
        '''User Settings'''
        # [(name, email)]
        users = [
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
        for user in users:
            # Create nodes with email
            id = self.db.add_user_settings_node(user[1])
            self.db.set_user_settings_property(id, NodeProperties.UserSettings.NAME, user[0])

    def __blueprints(self):
        '''Blueprints'''
        # [(name, description)]
        blueprints = [
            (
                'Eduskunta',
                'A collaborative framework designed to enhance educational dialogue and decision-making through structured discussions and feedback.',
                ),
            (
                'Brainstorm Blueprint',
                'A creative framework that uses guided questions to spark innovative ideas and foster collaborative thinking.',
                ),
            (
                'Thought Explorer',
                'A stimulating guide that encourages deep reflection and discovery through targeted questions and open-ended inquiries.',
                ),
            (
                'Inquiry Adventure',
                'An engaging toolkit designed to inspire curiosity and exploration through a series of thought-provoking questions.',
                ),
            (
                'Dialogue Design',
                'A structured approach that fosters meaningful conversations by providing a framework of insightful questions and prompts.',
                ),
            (
                'Idea Igniter',
                'A creative catalyst that sparks inspiration and generates innovative ideas through targeted prompts and questions.',
                ),
            (
                'Question Quest',
                'A playful exploration that drives discovery and insight through a series of engaging and thought-provoking questions.',
                ),
        ]

        for blueprint in blueprints:
            id = self.db.add_blueprint_node()
            self.db.set_blueprint_property(id, NodeProperties.Blueprint.NAME, blueprint[0])
            self.db.set_blueprint_property(id, NodeProperties.Blueprint.DESCRIPTION, blueprint[1])


