from flask import Blueprint, flash, request, redirect, jsonify
from flask import current_app as app
from flask_pymongo import PyMongo

from Services.AuthenticationService import Authentication
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.utils import secure_filename

import pandas as pd
from pandas import dataframe


Authentication = Authentication()


app.config['MONGO_URI'] = 'mongodb://localhost:27017/fileupload'
mongo = PyMongo(app)

upload = Blueprint("UploadEndpoints",__name__, url_prefix="/upload")

ALLOWED_EXTENSIONS = set(['txt', 'csv'])

#Function that checks the file type 
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@upload.route("/", methods=["GET"])
def index():
    return DownloadController.get()


@upload.route('/create', methods=['POST'])
def upload_file():
    #empty string that is returned to indicate the result 
    result = ''
    if request.method == 'POST':
        #set a variable for the file requested 
        file = request.files['file']
        #retrieves the name from the request
        filename = request.form.get('filename')
        #If filename is an empty string, means that no file has been selected 
        if filename == '':
            result = jsonify({"result":"No file selected"})
        #Checks if the file exists and if it is an acceptable type 
        if file and allowed_file(filename):
            #convert from csv to pandas DataFrame
            df = pd.read_csv("filename")
            #saves the file to the mongo database
            df.write.format("mongo").mode("append").save()
            result = jsonify({"result":"File successfully uploaded to database"})
        else:
            result = jsonify({"result":"Allowed file types are .pdf, .txt"})
        return result
    
   

