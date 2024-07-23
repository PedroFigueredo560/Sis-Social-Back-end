from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

#initialise flask api
app = Flask(__name__)
CORS(app, origins='http://localhost:5173/')


#configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://your_username:your_password@localhost/sis_social'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)