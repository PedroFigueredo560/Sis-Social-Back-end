from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# initialise flask api
app = Flask(__name__)

#configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://YourDatabaseUser:YourDatabasePassword@localhost/sis_social'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)