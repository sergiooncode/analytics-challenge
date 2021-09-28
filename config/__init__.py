import os


class Config:
    @staticmethod
    def init_app(app):
        """
        If some configuration needs to initialize the app in some way use this function
        :param app: Flask app
        :return:
        """
        pass


class LocalConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    ENV = "local"


class TestConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENV = "test"


config = {"development": LocalConfig, "test": TestConfig, "default": LocalConfig}
