from flask import Flask, render_template, abort, session, flash, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_migrate import Migrate
from datetime import datetime, timedelta

from wtforms.validators import email

from amp.models import db, User
from amp.forms import *
from amp.constants import *
import colorama as cma
import logging
import datetime as dt
import redis
import amp.schemas as Schemas
from amp.program import newUsernameGenerator, tokenGen, cTime

cma.init()

app = Flask(__name__)
# code from previous project
app.config['SECRET_KEY'] = "kahjdslkahsdkjhasdjkhasjdkjashdjkashdjasd"
app.config['SESSION_TYPE'] = 'filesystem'  # Store session data on the filesystem
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///apiMarketPlace.db"
redis_connection = redis.Redis(host='localhost', port=6379, db=0)

db.init_app(app)
migrate = Migrate(app, db, render_as_batch=True)
app.app_context().push()
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
    return render_template("index.html")

@app.route("/login")
def loginPage():
    
    return "Login Page"

@app.route("/createAccount", methods=["GET", "POST"])
def registrationPage():
    registrationForm = RegistrationForm()
    if request.method == "POST":
        if registrationForm.validate_on_submit():
            userExists = User.query.filter_by(email=registrationForm.email.data).first()
            if userExists:
                flash("account already exists with this email", "warning")
                return "duplicate account"

            newUsername = newUsernameGenerator(emailAddress=registrationForm.email.data, fullName=registrationForm.fullName.data)
            newLoginToken = tokenGen(type="login")
            try:
                newUser = User(
                    username = newUsername,
                    email = registrationForm.email.data,
                    password = registrationForm.password.data,
                    loginToken = newLoginToken,
                    lastLoginTime = cTime("both")
                )
                db.session.add(newUser)
                db.session.commit()
                flash("account created successfully", "success")
            except Exception as error:
                logger.error(error)
                db.session.rollback()
                flash("account creation failed. try again!", "danger")
            finally:
                db.session.close()
            return redirect(url_for("loginPage"))
        else:
            return "error"
    return render_template("registration.html", form=registrationForm)

@app.route("/logout")
def logout():
    session.clear()
    return "Logged out"



if __name__ == "__main__":
    app.run(debug=True, host="localhost", port="9999")
