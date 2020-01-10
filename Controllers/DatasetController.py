from flask import Blueprint, flash, request, redirect, jsonify, Response
from flask import current_app as app
from app import db
from Models.Dataset import Dataset
import json
db = db.test


dataset = Blueprint("DatasetController", __name__, url_prefix="/dataset")
@dataset.route("/filter", methods=["GET","POST"])
def filter():
    datasets = []
    try:
        if request.form["search"] == "" or request.form["search"] == " ":
            raise
        else:
            cursors = db.dataset.find({ "$text": { "$search": request.form["search"] } },{ "score": { "$meta": "textScore" } }).sort([('score', {'$meta': 'textScore'})])
            for doc in cursors:
                dataset = {
                    'id':str(doc["_id"]),
                    'name':doc["name"],
                    'type':doc['type'],
                    'description':doc["description"],
                    'author':doc['author']
                }
                datasets.append(dataset)
            return json.dumps(datasets)
    except:
        cursors = db.dataset.find({})
        for doc in cursors:
            dataset = {'id':str(doc["_id"]),'name':doc["name"],'type':doc['type'],'description':doc["description"],'author':doc['author']}
            datasets.append(dataset)
        return json.dumps(datasets)
    
