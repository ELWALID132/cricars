from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, BooleanField, DateField, FileField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired, Email, EqualTo, Regexp

class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(min=10, max=88)], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=88)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired(), Email(), Length(min=8, max=50)],
        render_kw={"placeholder": "Email"}
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=8, max=50)],
        render_kw={"placeholder": "Password"}
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password', message='Passwords must match')],
        render_kw={"placeholder": "Confirm password"}
    )
    agree_to_terms = BooleanField('I agree to the terms and conditions', validators=[DataRequired()])
    submit = SubmitField("Sign Up")

class RentalForm(FlaskForm):
    place = StringField('Place', validators=[DataRequired()], render_kw={"placeholder": "Enter an address, a train station...", "class": "form-control mb-2"})
    start_date = DateField('Start of rental', format='%Y-%m-%d', validators=[DataRequired()], render_kw={"class": "mb-2 form-control", "placeholder": "Start of rental"})
    end_date = DateField('End of rental', format='%Y-%m-%d', validators=[DataRequired()], render_kw={"class": "mb-2 form-control", "placeholder": "End of rental"})
    submit = SubmitField('Search', render_kw={"class": "btn btn-outline-secondary btn-style col-md-12 sm-mt-3"})

class ContactForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter your email address", "class": "form-control mb-3"})
    subject = StringField('Subject', validators=[DataRequired()], render_kw={"placeholder": "What is this about", "class": "form-control mb-3"})
    message = TextAreaField('Message', validators=[DataRequired()], render_kw={"placeholder": "We are here to help you", "class": "form-control mb-3", "rows": 5})
    file = FileField('File', render_kw={"class": "form-control mb-3", "aria-describedby": "fileHelpId"})
    submit = SubmitField('Send', render_kw={"class": "btn btn-style"})

class ResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')