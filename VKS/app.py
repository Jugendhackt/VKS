from flask import Flask, render_template, jsonify, request, redirect
import json
import time

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("schuelerliste.html")

@app.route("/sek")
def sek():
	schuelerliste = json.load(open("schuelerliste-9b.json"))
	abwesende = []
	for i in range(len(schuelerliste)):
		if schuelerliste[i]["status"] == "abwesend":
			abwesende.append(schuelerliste[i])

	return render_template("seki-view.html", liste=abwesende)

@app.route("/lehrer")
def absence():
	Schuelerliste = json.load(open("schuelerliste-9b.json"))
	return render_template("teacher-view.html", liste=Schuelerliste)

@app.route("/change_state", methods={"POST"})
def change():
	schuelerliste = list(json.load(open("schuelerliste-9b.json")))
	anwesende = list(request.form.keys())
	for i in range(len(schuelerliste)):
		if schuelerliste[i]["name"] in anwesende:
			schuelerliste[i]["status"] = "anwesend"
		else:
			schuelerliste[i]["status"] = "abwesend"
	json.dump(schuelerliste, open("schuelerliste-9b.json", "w"))
	return redirect("/lehrer")

@app.route("/style.css")
def style():
	return render_template("style.css")

@app.route("/jahrgaenge-uebersicht")
def all():
	return render_template("overview.html")

@app.route("/overview-9b")
def overview():
	all = json.load(open("schuelerliste-9b.json"))
	return render_template("overview-9b.html", liste=all)

@app.route("/roadmap")
def roadmap():
	return render_template("roadmap.html")

@app.route("/entry")
def entry():
	content = json.load(open("content.json"))
	return render_template("entry.html", einträge=content)

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
	list = json.load(open("terms.json"))
	return render_template("calendar.html", kalender=list)

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
	choosen_date = new_term['date']
	splited = choosen_date.split(". ")
	date = splited[2] + "-" + splited[1] + "-" + splited[0]
	new_term.update({'date': date})
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
	# Umstellung des Datums, damit es input="date" richtig lesen kann
	choosen_date = choosen_term['date']
	# Entfernen des alten Eintrags
	old_term = choosen_term
	old_term_number = all_terms.index(old_term)
	all_terms.remove(old_term)
	json.dump(all_terms, open("terms.json", "w"))
	return render_template("/term-editor-2.html", term1=choosen_term)

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

app.run(debug=True,host="0.0.0.0", port=5000)
