from flask import Flask, render_template, request, render_template_string, redirect, session, Response, g
import json, time
import flask
import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_user import *
from flask_babelex import Babel

# authentication
class ConfigClass(object):

    # Flask settings
	SECRET_KEY = 'Mach sie aus Wachs und Gold, My Fairlady'

    # Flask-SQLAlchemy settings
	SQLALCHEMY_DATABASE_URI = 'sqlite:///VKS.sqlite'    # File-based SQL database
	SQLALCHEMY_TRACK_MODIFICATIONS = False    # Avoids SQLAlchemy warning
	# Flask-User settings
	USER_APP_NAME = "VKS"
	USER_ENABLE_EMAIL = False
	USER_ENABLE_USERNAME = True
	USER_ENABLE_CHANGE_USERNAME = True
	USER_ENABLE_CHANGE_PASSWORD = True
# init of apps

app = Flask(__name__)
app.config.from_object(__name__+'.ConfigClass')

babel = Babel(app)

db = SQLAlchemy(app)


class User(db.Model, UserMixin):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
	username = db.Column(db.String(50, collation='NOCASE'), nullable=False, unique=True, server_default='')
	password = db.Column(db.String(255), nullable=False, server_default='')

    # User information
	first_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
	last_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')

	# Define the relationship to Role via UserRoles
	roles = db.relationship('Role', secondary='user_roles')

# Define the Role data-model
class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(50))

# Define the UserRoles association table
class UserRoles(db.Model):
	__tablename__ = 'user_roles'
	id = db.Column(db.Integer(), primary_key=True)
	user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
	role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

# Setup Flask-User and specify the User data-model
user_manager = UserManager(app, db, User)

db.create_all()

if not User.query.filter(User.username == 'admin').first():
	user = User(
		username = 'admin',
		password = user_manager.hash_password('Password1'),
    )
	user.roles.append(Role(name='user'))
	user.roles.append(Role(name='Admin'))
	user.roles.append(Role(name='Agent'))
	db.session.add(user)
	db.session.commit()
if not User.query.filter(User.username == 'Miller01').first():
	user = User (
	username ='Miller01',
	password = user_manager.hash_password('Password1'),
	)
	user.roles.append(Role(name='user'))
	user.roles.append(Role(name='teacher'))
	db.session.add(user)
	db.session.commit()

if not User.query.filter(User.username == 'Schmidt01').first():
	user = User(
	username = 'Schmidt01',
	password = user_manager.hash_password('Password1'),
	)
	user.roles.append(Role(name='user'))
	user.roles.append(Role(name='secretary'))
	db.session.add(user)
	db.session.commit()

@app.route("/")
def index():
	return render_template("start.html")

@app.route("/start-mobile")
def index_mobile():
	return render_template("start-mobile.html")

@app.route("/user-managment")
@login_required
def home_page():
    return render_template_string("""
            {% extends "flask_user_layout.html" %}
            {% block content %}
                <h2>{%trans%}Home page{%endtrans%}</h2>
                <p><a href={{ url_for('user.login') }}>{%trans%}Sign in{%endtrans%}</a></p>
                <p><a href={{ url_for('home_page') }}>{%trans%}Home Page{%endtrans%}</a> (accessible to anyone)</p>
                <p><a href={{ url_for('user.logout') }}>{%trans%}Sign out{%endtrans%}</a></p>
                <p><a href={{ url_for('user.change_password') }}>{%trans%}Change Password{%endtrans%}</a></p>
            {% endblock %}
            """)

@app.route("/admin-managment")
@roles_required('Admin')
def admin_page():
    return render_template_string("""
            {% extends "flask_user_layout.html" %}
            {% block content %}
                <h2>{%trans%}Home page{%endtrans%}</h2>
                <p><a href={{ url_for('user.register') }}>{%trans%}Register{%endtrans%}</a></p>
                <p><a href={{ url_for('user.login') }}>{%trans%}Sign in{%endtrans%}</a></p>
                <p><a href={{ url_for('home_page') }}>{%trans%}Home Page{%endtrans%}</a> (accessible to anyone)</p>
                <p><a href={{ url_for('user.logout') }}>{%trans%}Sign out{%endtrans%}</a></p>
                <p><a href={{ url_for('user.change_password') }}>{%trans%}Change Password{%endtrans%}</a></p>
            {% endblock %}
            """)
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.route("/sek")
@roles_required("user", ["secretary", "Admin"])
def sek():
	list_persons = list(json.load(open("list-9b.json")))
	absence = []
	for i in range(len(list_persons)):
		if list_persons[i]["status"] == "absent":
			absence.append(list_persons[i])

	return render_template("seki-view.html", list=absence)

@app.route("/teacher")
@roles_required("user", ["teacher", "Admin"])
def absence():
	list_persons = json.load(open("list-9b.json"))
	return render_template("teacher-view.html", list=list_persons)

@app.route("/change_state", methods={"POST"})
def change():
	list_persons = list(json.load(open("list-9b.json")))
	present = list(request.form.keys())
	for i in range(len(list_persons)):
		if list_persons[i]["name"] in present:
			list_persons[i]["status"] = "present"
		else:
			list_persons[i]["status"] = "absent"
	json.dump(list_persons, open("list-9b.json", "w"))
	return redirect("/teacher")

@app.route("/classes-overview")
@login_required
def classes_overview():
	all = list(json.load(open("classes_overview.json")))
	return render_template("overview.html", list=all)

@app.route("/overview-9b")
@login_required
def overview():
	all = list(json.load(open("list-9b.json")))
	return render_template("overview-9b.html", list=all)

@app.route("/roadmap")
def roadmap():
	return render_template("roadmap.html")

@app.route("/entry")
@login_required
def entry():
	content = json.load(open("content.json"))
	return render_template("entry.html", entrys=content)

@app.route("/entry-create")
@login_required
def entry_editor():
	return render_template("entry-editor.html")

@app.route("/create_entry", methods={"POST"})
def create_entry():
	all_entrys = json.load(open("content.json"))
	new_entry = {}
	new_entry_values = list(request.form.values())
	new_entry_key = list(request.form.keys())
	for i in range(len(new_entry_key)):
		value = new_entry_values[i]
		key = new_entry_key[i]
		new_entry.update({key: value})
	new_entry.update({"date":time.strftime("%d. %m. %Y")})
	new_entry.update({"time":time.strftime("%H") + ":" + time.strftime("%M")})
	all_entrys.append(new_entry)
	json.dump(all_entrys, open("content.json", "w"))
	return redirect("/entry")

@app.route("/calendar")
def calendar():
	list_terms = list(json.load(open("terms.json")))
	return render_template("calendar.html", list=list_terms)

@app.route("/term-editor")
@login_required
def term_editor():
	return render_template("term-editor.html")

@app.route("/term-editor-processing", methods={"POST"})
@login_required
def term_editor_process():
	all_terms = json.load(open("terms.json"))
	new_term = {}
	new_term_values = list(request.form.values())
	new_term_keys = list(request.form.keys())
	for i in range(len(new_term_values)):
		value = new_term_values[i]
		key = new_term_keys[i]
		new_term.update({key:value})
	new_term.update({"creation-date":time.strftime("%d. %m. %Y")})
	new_term.update({"creation-time":time.strftime("%H") + ":" + time.strftime("%M")})
	#author, creation-time and creation-date are just for traceabilty, if something is wrong
	all_terms.append(new_term)
	json.dump(all_terms, open("terms.json", "w"))
	return redirect("/calendar")

@app.route("/edit-term-load", methods={"POST"})
@login_required
def term_editor_2():
	all_terms = list(json.load(open("terms.json")))
	choosen_term = {}
	send_term = list(request.form.keys())
	for i in range(len(all_terms)):
		if all_terms[i]['name'] == send_term[0]:
			choosen_term = all_terms[i]
			print(all_terms[i])
	choosen_date = choosen_term['date']
	old_term = choosen_term
	old_term_number = all_terms.index(old_term)
	all_terms.remove(old_term)
	json.dump(all_terms, open("terms.json", "w"))
	return render_template("/term-editor-2.html", term=choosen_term)

@app.route("/edit-term-processing", methods={"POST"})
@login_required
def edit_term():
	all_terms = json.load(open("terms.json"))
	new_term = {}
	new_term_values = list(request.form.values())
	new_term_keys = list(request.form.keys())
	for i in range(len(new_term_values)):
		value = new_term_values[i]
		key = new_term_keys[i]
		new_term.update({key:value})
	new_term.update({"creation-date":time.strftime("%d. %m. %Y")})
	new_term.update({"creation-time":time.strftime("%H") + ":" + time.strftime("%M")})
	all_terms.append(new_term)
	json.dump(all_terms, open("terms.json", "w"))
	return redirect("/calendar")

app.run(debug=True, host="0.0.0.0", port=5000)
