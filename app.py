from flask import Flask, jsonify, render_template, request
from pymongo import ASCENDING, DESCENDING
from flask_pymongo import PyMongo


# Create app
app = Flask(__name__)
app.config["MONGO_DBNAME"] = "moveit"
mongo = PyMongo(app)


@app.route("/")
def home():
    return render_template("home.html")

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
