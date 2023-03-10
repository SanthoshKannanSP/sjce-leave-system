from flask_pymongo import PyMongo
from flask_mongoengine import MongoEngine

from app import app


mongo = PyMongo(app)

# Setup Mongo Engine
db = MongoEngine()
db.init_app(app)

# Vanilla Variables
student_detail_van      = mongo.db.student_detail
leave_form_van          = mongo.db.leave_form
login_detail_van        = mongo.db.login_detail_van
admin_login_van         = mongo.db.admin_login

