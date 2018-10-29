from flask import Flask, render_template, jsonify, request, redirect
import json

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

app.run(debug=True,host="0.0.0.0", port=5000)
