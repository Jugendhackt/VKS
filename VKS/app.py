from flask import Flask, render_template, request, redirect, session, Response
from functools import wraps
import json, time
import flask
app = Flask(__name__)

@app.route("/")
def index():
	return render_template("start.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/sek")
def sek():
	list_persons = list(json.load(open("list-9b.json")))
	absence = []
	for i in range(len(list_persons)):
		if list_persons[i]["status"] == "absent":
			absence.append(list_persons[i])

	return render_template("seki-view.html", list=absence)

@app.route("/teacher")
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
def classes_overview():
	all = list(json.load(open("classes_overview.json")))
	return render_template("overview.html", list=all)

@app.route("/overview-9b")
def overview():
	all = list(json.load(open("list-9b.json")))
	return render_template("overview-9b.html", list=all)

@app.route("/roadmap")
def roadmap():
	return render_template("roadmap.html")

@app.route("/entry")
def entry():
	content = json.load(open("content.json"))
	return render_template("entry.html", entrys=content)

@app.route("/entry-create")
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
def term_editor():
	return render_template("term-editor.html")

@app.route("/term-editor-processing", methods={"POST"})
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
