from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateTimeField, IntegerField, TimeField as WTFormsTimeField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, ValidationError