from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from elasticsearch import Elasticsearch
from flask_user import UserManager
from flask_babelex import Babel

# Init Flask
app = Flask(__name__)

# Load Configuration from Config.py's class "Config"
app.config.from_object(Config)

# Init of Database modules
db = SQLAlchemy(app)

# Initialize Flask-BabelEx
babel = Babel(app)

# Initialize other things
from app import models

app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']])
print("sucessfully Initialized")

from app import search, mixin

# the db_session is a custom sessions for the case a modified session is needed
# in use for a custom search part with pure SQLAlchemy for the session
engine = create_engine('sqlite:///app/static/database/VKS_main.sqlite',
 convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

from app import routes
