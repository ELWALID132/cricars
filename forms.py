from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from models import User
# Define the RegisterForms form with email and password fields
class RegisterForms(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(
        min = 4, max = 20)],render_kw={"placeholder" :  "email"})
    password = PasswordField(validators=[InputRequired(), Length(
        min = 4, max = 20)],render_kw={"placeholder" :  "Password"})
    submit = SubmitField("Register")

    # Custom validation for email field
    def validate_username(self, email):
        """
        Check if the entered email already exists in the database.
        If it does, raise a ValidationError.
        """
        existing_user_username = User.query.filter_by(email=email.data).first()
        if existing_user_username:
            raise ValidationError("email already exists, Please choose another one")

# Define the LoginForms form with email and password fields
class LoginForms(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(
        min = 4, max = 20)],render_kw={"placeholder" :  "email"})
    password = PasswordField(validators=[InputRequired(), Length(
        min = 4, max = 20)],render_kw={"placeholder" :  "Password"})
    submit = SubmitField("Login")
