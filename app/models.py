from app import app, db, search
from app.mixin import SearchableMixin
from flask_user import UserMixin
import hashlib

# Define custom User Model with flask_user"s UserMixin
class User(db.Model, UserMixin, SearchableMixin):
	__tablename__ = "user"
	__searchable__ = ["username", "first_name", "last_name"]

	id = db.Column(db.Integer, primary_key=True)

	# User avatar
	def avatar(self, size):
		digest = hashlib.sha1(self.username.encode("utf-8")).hexdigest()
		return "https://www.gravatar.com/avatar/{}?d=identicon&s={}".format(
		digest, size)

	# User authentication information
	username = db.Column(db.String(50), nullable=False, unique=True)
	password = db.Column(db.String(255), nullable=False)

	# User information
	first_name = db.Column(db.String(100), nullable=False, server_default='')
	last_name = db.Column(db.String(100), nullable=False, server_default='')
	active = db.Column("is_active", db.Boolean(), nullable=False, server_default="1")
	last_seen = db.Column(db.String(100), nullable=False, server_default="unknown")
	level = db.Column(db.String(100))
	level_specific = db.Column(db.String(100), server_default="")
	description = db.Column(db.String(255))
	shool_class = db.Column(db.String(10))

	# Relationships
	roles = db.relationship('Role', secondary='user_roles', \
	backref = db.backref('user', lazy='dynamic'))


	def __repr__(self):
		return '<User {}>'.format(self.username)

# Define the Role data model
class Role(db.Model):
	__tablename__ = "role"

	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(50), unique=True, nullable=False)

# Define the UserRoles data model
class UserRoles(db.Model):
	__tablename__ = "user_roles"

	id = db.Column(db.Integer(), primary_key=True)
	user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
	role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))


# Define the Entry Model with custom SearchableMixin
# creation date/ time are only for full time view
class entrys(db.Model, SearchableMixin):
	__tablename__ = "entrys"
	__searchable__ = ["name", "content"]
	id = db.Column(db.Integer(), primary_key=True, unique=True)
	author = db.Column(db.String(255))
	name = db.Column(db.String(150), server_default="")
	creation_date = db.Column(db.String(20), server_default="")
	creation_time = db.Column(db.String(), server_default="")
	content = db.Column(db.Text(), server_default="")

# Define the Term Model with custom SearchableMixin
# creation date/ time are only for full view
class terms(db.Model, SearchableMixin):
	__tablename__ = "terms"
	__searchable__ = ["name", "destination_day", "description"]
	id = db.Column(db.Integer(), primary_key=True, unique=True)
	name = db.Column(db.String(150))
	author = db.Column(db.String(255))
	creation_date = db.Column(db.String(20), server_default="")
	creation_time = db.Column(db.String(), server_default="")
	destination_day = db.Column(db.String(20), server_default="")
	description = db.Column(db.Text(), server_default="")

class logins(db.Model):
	__tablename__ = "logins"
	__searchable__ = ["time", "name", "user_id"]
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(255), server_default="")
	time_pr = db.Column(db.DateTime())
	time = db.Column(db.String(20), server_default="")
	ip = db.Column(db.String(255), server_default="")

# init of tabels
db.create_all()
