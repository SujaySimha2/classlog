import os
import dotenv

cwd = os.getcwd()
dotenv.load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{cwd}/db.sqlite"

class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_ENV = "development"
    ENV = "development"

class ProductionConfig(Config):
    DEBUG = False
    FLASK_ENV = "production"
    ENV = "production"

class TestConfig(Config):
    FLASK_SQLALCHEMY_URI = "sqlite://"
    DEBUG = False
    FLASK_ENV = "testing"
    ENV = "testing"
