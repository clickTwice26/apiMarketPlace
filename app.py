from flask import Flask, render_template, abort, session, flash, request
from flask_sqlalchemy import SQLAlchemy
import colorama as cma
import logging
import datetime as dt
from amp.constants import *
import redis
from flask_limiter import Limiter
from flask_migrate import Migrate
from datetime import datetime, timedelta
from amp.models import db, User
from amp.forms import *
import amp.schemas as Schemas
cma.init()

app = Flask(__name__)
# code from previous project
app.config['SECRET_KEY'] = "kahjdslkahsdkjhasdjkhasjdkjashdjkashdjasd"
app.config['SESSION_TYPE'] = 'filesystem'  # Store session data on the filesystem
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///apiMarketPlace.db"
redis_connection = redis.Redis(host='localhost', port=6379, db=0)

db.init_app(app)  # Initialize the database with the app
migrate = Migrate(app, db, render_as_batch=True)
def getSessionUsername():
    
    return session.get("username")
limiter = Limiter(
    key_func=getSessionUsername,
    app = app,
    storage_uri="redis://localhost:6379"
)
# db = (app)
class ReverseFileHandler(logging.FileHandler):
    def __init__(self, filename, mode='a', encoding=None, delay=False):
        super().__init__(filename, mode, encoding, delay)

    def emit(self, record):
        try:
            if self.stream is None:
                self.stream = self._open()
            self.stream.close()
            with open(self.baseFilename, 'r+', encoding=self.encoding) as f:
                content = f.read()
                f.seek(0, 0)
                f.write(self.format(record) + '\n' + content)
        except Exception:
            self.handleError(record)

today = dt.date.today()
logFileName = f"{LOG_FOLDER_NAME}/{today.month:02d}-{today.day:02d}-{today.year}.log"
logging.basicConfig(level=logging.DEBUG, format=DEFAULT_CONSOLE_LOG_FORMAT)
logger = logging.getLogger("marketPlace")
file_handler = ReverseFileHandler(logFileName)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(DEFAULT_LOG_FORMAT)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

@app.route("/")
def index():
    return "Welcome to apiBazar"

@app.route("/login")
def loginPage():
    
    return "Login Page"

@app.route("/createAccount")
def registrationPage():
    return "Registration Page"

@app.route("/logout")
def logout():
    session.clear()
    return "Logged out"



if __name__ == "__main__":
    app.run(debug=True, host="localhost", port="9999")