import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    SECRET_KEY = os.getenv("SECRET_KEY") or "hard to guess "
    SQLALCHEMY_COMMIT_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = "Flasky"
    FLASKY_MAIL_SENDER = "Flasky Admin <779107975@qq.com>"
    FLASKY_ADMIN = os.getenv("FLASKY_ADMIN")

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = "smtp.qq.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    # MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_PASSWORD = "zuhhszjaokwpbefj"
    SQLALCHEMY_DATABASE_URI = "mysql://think:123456@192.168.31.60/test"


class TestConfig(Config):
    Testing = True
    SQLALCHEMY_DATABASE_URI = os.getenv("SQL_TEST_URI")


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("SQL_PRO_URI")


config = {
    "development": DevelopmentConfig,
    "testing": TestConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}