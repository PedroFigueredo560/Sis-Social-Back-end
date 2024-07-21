from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#initialise flask api
app = Flask(__name__)

#configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://your_username:your_password@localhost/sis_social'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)