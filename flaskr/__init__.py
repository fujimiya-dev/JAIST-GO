import os
from dotenv import load_dotenv
from flask import Flask

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
_flask_app = app
import flaskr.auth
import flaskr.app
app = _flask_app
