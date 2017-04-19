from flask import Flask, jsonify, render_template, request
import os

from pymongo import ASCENDING, DESCENDING
from flask_pymongo import PyMongo


# Create app
app = Flask(__name__)
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME") or "moveit"
mongo = PyMongo(app)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/today")
def today():
    data = mongo.db.movements.find(
        projection={"_id": False,"date": True}, 
        sort=[("date", DESCENDING)]
    )
    data = list(data)
    return render_template("today.html", data=data)

@app.route("/history")
def history():
    data = mongo.db.movements.find(
        projection={"_id": False,"date": True}, 
        sort=[("date", DESCENDING)]
    )
    data = list(data)
    return render_template("history.html", data=data)

@app.route("/add-movement", methods=["POST"])
def add_movement():
    data = request.get_json(force=True)
    for movement in data["moves"]:
        mongo.db.movements.insert_one({"date": movement})
    return jsonify({'success':True}), 201
