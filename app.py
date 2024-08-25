from flask import Flask, render_template, flash, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, login_required, logout_user, LoginManager, current_user
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,  PasswordField, SubmitField, BooleanField, DateField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired, Email, EqualTo, Regexp
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
import os

# Initialize the Flask app
app = Flask(__name__)

# Initialize the Bcrypt library for password hashing
bcrypt = Bcrypt(app)

# Initialize the Flask-Login extension
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Specify the login view for unauthorized users

# Configuration for using a SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = "TheSuperSecretKey"

# Initialize the SQLAlchemy instance
db = SQLAlchemy(app)

# Add this function after initializing your app (after db = SQLAlchemy(app))
@app.context_processor
def inject_user():
    return dict(current_user=current_user)

# Define the Guest model
class guests(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

# Define the login form
class LoginForms(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(min=10, max=88)], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=88)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

class ContactForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter your email address", "class": "form-control mb-3"})
    subject = StringField('Subject', validators=[DataRequired()], render_kw={"placeholder": "What is this about", "class": "form-control mb-3"})
    message = TextAreaField('Message', validators=[DataRequired()], render_kw={"placeholder": "We are here to help you", "class": "form-control mb-3", "rows": 5})
    file = FileField('File', render_kw={"class": "form-control mb-3", "aria-describedby": "fileHelpId"})
    submit = SubmitField('Send', render_kw={"class": "btn btn-style"})

# Define the registration form
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
    
class ResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
# Load a user with the given user_id
@login_manager.user_loader
def load_user(user_id):
    return guests.query.get(int(user_id))

# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def home():
    form = RentalForm()
    return render_template("index.html", form=form)

# Route for the signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_guest = guests.query.filter_by(email=form.email.data).first()
        if existing_guest:
            flash('Error: This email is already being used. Please use a different email.', 'danger')
            return render_template("signup.html", form=form)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_guest = guests(email=form.email.data, password=hashed_password)
        db.session.add(new_guest)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'Error in {getattr(form, field).label.text}: {error}', 'danger')
    return render_template("signup.html", form=form)

# Route for the login page
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForms()
    if form.validate_on_submit():
        guest = guests.query.filter_by(email=form.email.data).first()
        if guest and bcrypt.check_password_hash(guest.password, form.password.data):
            login_user(guest)
            return redirect(url_for('rental'))
        else:
            flash('Login unsuccessful. Please check your email and password.', "danger")
    return render_template("login.html", form=form)

# Route for explore cars based on the search
@app.route("/explore")
def explore():
    form = RentalForm()
    return render_template("explore.html", form = form)
# Route for the rent my car page
@app.route("/rentmycar")
def rentmycar():
    return render_template("rentmycar.html")

# Route for the insurance page
@app.route("/insurance")
def insurance():
    return render_template("insurance.html")

# Route for the help page
@app.route("/help")
def help():
    return render_template("help.html")


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        email = form.email.data
        subject = form.subject.data
        message = form.message.data
        file = form.file.data

        # Handle the file upload here
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Handle the form data (e.g., save to database, send email, etc.)

        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('contact'))

    return render_template('contact.html', form=form)

# Route for reset password
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # Implement your password reset logic here
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

# Route for the addinfo page
@app.route('/addinfo')
def addinfo():
    return render_template("addinfo.html")

# Route for the rental page
@app.route('/rental')
@login_required  # Ensure that only logged-in users can access this route
def rental():
    return render_template("rental.html")

# Route for the logout page
@app.route('/logout')
@login_required  # Ensure that only logged-in users can access this route
def logout():
    logout_user()
    return redirect(url_for('home'))

# Route for the search page
@app.route("/search")
def search():
    return render_template("home.html")

# Route for the about page
@app.route("/about")
def about():
    return render_template("about.html")

# Route for the 404 error page
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Route for the 500 error page
@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
