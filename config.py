import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or 'hard to guess string'
    FLASKY_POSTS_PER_PAGE = 20
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        'mysql+pymysql://sma:123456@192.16.1.10:3306/sma?charset=utf8'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        'mysql+pymysql://sma:123456@192.16.1.10:3306/sma?charset=utf8'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_RECORD_QUERIES = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        'mysql+pymysql://sma:123456@127.0.0.1:3306/sma?charset=utf8'


config = {
    'development': DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
