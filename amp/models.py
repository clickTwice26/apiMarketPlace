from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()



class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), unique=False, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    loginToken = db.Column(db.String(200), unique=True, nullable=False)
    creditBalance = db.Column(db.Numeric(), default=100)
    lastLoginTime = db.Column(db.String(100), default="null")
    status = db.Column(db.String(50), default='active') #[active, locked, banned]
    level = db.Column(db.Integer, default=1)
    xPoints = db.Column(db.Integer, default=0)

