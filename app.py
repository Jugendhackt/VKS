from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_user import *
from models import *
from routes import *
from elasticsearch import Elasticsearch
from config import ConfigClass

# init of flask
app = Flask(__name__)

# init of config class for apps
app.config.from_object(__name__+'.ConfigClass')

# Init of elasticsearch
app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
	if app.config['ELASTICSEARCH_URL'] else None
