from flask import Flask, request, current_app
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
app.config.from_object(Config)
app.app_context().push()
db = SQLAlchemy(app)
CORS(app, resources={r"/*": {"origins": "*"}})
