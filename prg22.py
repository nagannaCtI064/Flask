from flask import Flask, render_template, redirect, request, url_for,jsonify
from pymongo import MongoClient
from flask import Blueprint
import pickle
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client["users"]
col = db["data"]

main = Blueprint('main', __name__)

with open("D:/python/delivary_review_predict.pickle","rb") as f:
    model=pickle.load(f)
le=LabelEncoder()


@main.route("/", methods=["GET", "POST"])
def index():
    data = col.find()
    return render_template("index.html", data=data)

@main.route("/add_data", methods=["GET", "POST"])
def add_data():
    if request.method == "POST":
        id=request.form.get("_id")
        name = request.form.get("name")
        dob=request.form.get("dob")
        email=request.form.get("email")
        mobile = request.form.get("mobile")
        col.insert_one({"_id":id,"name": name,"dob":dob,"email":email,"mobile":mobile})
        return redirect(url_for("main.alert"))
    return render_template("add_data.html")

@main.route("/alert")
def alert():
    return render_template("alert.html")

@app.route("/retrive", methods=["GET", "POST"])
def retrive():
    if request.method == "POST":
        id=request.form.get("_id")
        name = request.form.get("name")
        data = col.find_one({"_id":id,"name": name})
        return render_template("retrive.html", data=data)
    return render_template("retrive.html")
@app.route("/delete",methods=["POST","GET"])
def delete():
    if request.method=="POST":
        id=request.form.get("_id")
        name=request.form.get("name")
        data=col.delete_one({"_id":id,"name":name})
        return render_template("alert.html",data=data)
    return render_template("delete.html")
@app.route("/get_details", methods=["POST", "GET"])
def get_details():
    if request.method == "POST":
        _id = request.form.get("_id")
        data = col.find_one({"_id": _id})
        return render_template("get_details.html", data=data)
    return render_template("get_details_form.html")


@app.route("/update", methods=["POST", "GET"])
def update():
    if request.method == "POST":
        _id = request.form.get("_id")
        name = request.form.get("name")
        dob = request.form.get("dob")
        email = request.form.get("email")
        mobile = request.form.get("mobile")
        
        filter_data = {"_id": _id}
        update_data = {"$set": {"name": name, "dob": dob, "email": email, "mobile": mobile}}
        col.update_one(filter_data, update_data)
        
        return render_template("update_success.html")  
    return render_template("update_form.html") 



app.register_blueprint(main)
if __name__ == "__main__":
    app.run(debug=True)
