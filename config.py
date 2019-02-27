import os

# Config for os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # Version
    APP_VERSION = "0.0.2"

    SECRET_KEY = os.environ.get("SECRET_KEY") or "not_secrEt53454325_SecrT_kEy"
    # File-based SQL database
    SQLALCHEMY_DATABASE_URI = "sqlite:///static/database/VKS_main.sqlite" or \
        "sqlite:///" + os.path.join(basedir, "VKS_Fallback.sqlite")

    # Avoids SQLAlchemy warning (Is usable for Database Debugging at SQLAlchemy)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Elasticsearch Server Url for Full text search in databse
    ELASTICSEARCH_URL = "http://localhost:9200"

    # Flask-User settings
    USER_APP_NAME = "Communicatio"
    USER_ENABLE_EMAIL = False
    USER_ENABLE_USERNAME = True
    USER_ENABLE_CHANGE_USERNAME = True
    USER_ENABLE_CHANGE_PASSWORD = True
    USER_ENABLE_REGISTER = True
    USER_LOGIN_TEMPLATE =  "flask_user/login.html"
    USER_REGISTER_TEMPLATE= "flask_user/register.html"

    # Settings for user data validation and databse settings
    # The Minimal length of the Password is not affecting
    # the flask user registration at this point but is set at 6 by default
    # We don't recommend set password length under 6
    USER_USERNAME_MAX_LEN = 100
    USER_USERNAME_MIN_LEN = 5
    USER_FIRST_NAME_MAX_LEN = 100
    USER_FIRST_NAME_MIN_LEN = 5
    USER_LAST_NAME_MAX_LEN = 100
    USER_LAST_NAME_MIN_LEN = 5
    USER_PASSWORD_MAX_LEN = 255
    USER_PASSWORD_MIN_LEN = 6

    # Settings for report databse Settings and form validation
    # Settings must be in Integers or strings with only numbers
    # The Sender filed length is set by the username settings
    REPORT_NAME_MAX_LEN = 255
    REPORT_NAME_MIN_LEN = 5
    REPORT_THEME_MAX_LEN = 255
    REPORT_THEME_MIN_LEN = 5
    REPORT_DESC_MAX_LEN = 255
    REPORT_DESC_MIN_LEN = 5

    # Options for functions like login tracing etc.
    # Is Set with Bol Values (True/ False)
    TRACE_LOGIN = True
    ABOUT_US = False
    FLASK_MIGRATE = True

    # If you disable it the user with the name guest will deleted if it exists
    # If you enable before the first run nothing will happen
    GUEST_USER = False

    # Custom Templates for not by default enabled routes
    ABOUT_US_TEMPLATE = ""
