from flask import Flask, render_template, jsonify, request, redirect
import json

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("Schuelerliste.html")

@app.route("/sek")
def sek():
	schuelerliste = json.load(open("schuelerliste2.json"))
	abwesende = []
	for i in range(len(schuelerliste)):
		if schuelerliste[i]["status"] == "abwesend":
			abwesende.append(schuelerliste[i])

	return render_template("mp.html", liste=abwesende)

@app.route("/lehrer")
def all():
	Schuelerliste = json.load(open("schuelerliste2.json"))
	return render_template("mp1.html", liste=Schuelerliste)

@app.route("/change_state", methods={"POST"})
def change():
	schuelerliste = list(json.load(open("schuelerliste2.json")))
	anwesende = list(request.form.keys())
	for i in range(len(schuelerliste)):
		if schuelerliste[i]["name"] in anwesende:
			schuelerliste[i]["status"] = "anwesend"
		else:
			schuelerliste[i]["status"] = "abwesend"
	json.dump(schuelerliste, open("schuelerliste2.json", "w"))
	return redirect("/lehrer")


app.run(debug=True,host="0.0.0.0", port=5000)
