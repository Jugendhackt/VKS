import os

# Config for os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "not_secrEt53454325_SecrT_kEy"
    # File-based SQL database
    SQLALCHEMY_DATABASE_URI = "sqlite:///static/database/VKS_main.sqlite" or \
        "sqlite:///" + os.path.join(basedir, "VKS_Fallback.sqlite")
    # Avoids SQLAlchemy warning (Can Help by Database Processing Debugging)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Elasticsearch Url for Full text search in databse
    ELASTICSEARCH_URL = "http://localhost:9200"
    # Flask-User settings
    USER_APP_NAME = "VKS (recode)"
    USER_ENABLE_EMAIL = False
    USER_ENABLE_USERNAME = True
    USER_ENABLE_CHANGE_USERNAME = True
    USER_ENABLE_CHANGE_PASSWORD = True
    USER_ENABLE_REGISTER = False
