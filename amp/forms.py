from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateTimeField, IntegerField, TimeField as WTFormsTimeField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo


class RegistrationForm(FlaskForm):
    fullName = StringField('Full Name', validators=[DataRequired(), Length(min=4, max=199)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password'), Length(min=6)])
    submit = SubmitField('Create Account')
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')