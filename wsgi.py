from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

from Templates.sqlalchemy_db_uri import DB_URL



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Users(db.Model):
    id =  db.Column( db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column( db.String(50), nullable=False)
    Surname =  db.Column( db.String(50),nullable=False)
    Email =  db.Column( db.String(120), unique=True, nullable=False)
    password =  db.Column( db.String(128), nullable=False)
    birthdate =  db.Column( db.Date)
    date_signIn =db.Column( db.DateTime, default=datetime.utcnow)

