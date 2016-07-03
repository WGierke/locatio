from flask import Flask
from flask.ext.admin import Admin
from flask.ext.sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "alert4"
db = SQLAlchemy(app)
admin = Admin(app, name="locatio", template_mode='bootstrap3')
