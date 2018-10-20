from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("inde2.html")
@app.route('/templates/')
@app.route('/templates/<name>')
def templates(name=None):
	return render_template('mp.html', name=name)

@app.route("/sek")
def list():
	schuelerliste = json.load(open("schuelerliste2.json"))
	abwesende = []
	for i in range(len(schuelerliste)):
		if schuelerliste[i]["status"] == "abwesend":
			abwesende.append(schuelerliste[i])

	return render_template("mp1.html", liste=abwesende)
@app.route("/list")
def all():
	Schuelerliste = json.load(open("schuelerliste2.json"))
	return render_template("mp1.html", liste=Schuelerliste)

app.run(debug=True)
