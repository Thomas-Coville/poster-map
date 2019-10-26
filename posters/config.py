class Config(object):
    DEBUG = False
    TESTING = False
    MONGODB_SETTINGS = {'DB': 'posters'}

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True