from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, FileField, PasswordField, SubmitField, BooleanField, DateField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, InputRequired
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'TheSuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:walidEL@localhost'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/files'

# Initialize Extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Models


class Guest(db.Model, UserMixin):
    __tablename__ = 'guests'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return Guest.query.get(int(user_id))

# Forms


class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(
        min=10, max=88)], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=8, max=88)], render_kw={"placeholder": "Password"})
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
        validators=[DataRequired(), EqualTo(
            'password', message='Passwords must match')],
        render_kw={"placeholder": "Confirm password"}
    )
    agree_to_terms = BooleanField(
        'I agree to the terms and conditions', validators=[DataRequired()])
    submit = SubmitField("Sign Up")


class RentalForm(FlaskForm):
    place = StringField('Place', validators=[DataRequired()], render_kw={
                        "placeholder": "Enter an address, a train station...", "class": "form-control mb-2"})
    start_date = DateField('Start of rental', format='%Y-%m-%d', validators=[DataRequired(
    )], render_kw={"class": "mb-2 form-control", "placeholder": "Start of rental"})
    end_date = DateField('End of rental', format='%Y-%m-%d', validators=[DataRequired(
    )], render_kw={"class": "mb-2 form-control", "placeholder": "End of rental"})
    submit = SubmitField('Search', render_kw={
                         "class": "btn btn-outline-secondary btn-style col-md-12 sm-mt-3"})


class ContactForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={
                        "placeholder": "Enter your email address", "class": "form-control mb-3"})
    subject = StringField('Subject', validators=[DataRequired()], render_kw={
                          "placeholder": "What is this about", "class": "form-control mb-3"})
    message = TextAreaField('Message', validators=[DataRequired()], render_kw={
                            "placeholder": "We are here to help you", "class": "form-control mb-3", "rows": 5})
    file = FileField('File', render_kw={
                     "class": "form-control mb-3", "aria-describedby": "fileHelpId"})
    submit = SubmitField('Send', render_kw={"class": "btn btn-style"})


class ResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
# Routes


@app.route('/', methods=['GET', 'POST'])
def home():
    form = RentalForm()
    return render_template("index.html", form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        if not form.email.data:
            flash('Error: Email is required.', 'danger')
            return render_template("signup.html", form=form)
        if not form.password.data:
            flash('Error: Password is required.', 'danger')
            return render_template("signup.html", form=form)
        existing_guest = Guest.query.filter_by(email=form.email.data).first()
        if existing_guest:
            flash(
                'Error: This email is already being used. Please use a different email.', 'danger')
            return render_template("signup.html", form=form)
        hashed_password = bcrypt.generate_password_hash(
            form.password.data, 10).decode('utf-8')
        new_guest = Guest(email=form.email.data, password=hashed_password)
        db.session.add(new_guest)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template("signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        guest = Guest.query.filter_by(email=form.email.data).first()
        if guest and bcrypt.check_password_hash(guest.password, form.password.data):
            login_user(guest)  # Log in the user
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('next')  # Get the next parameter
            return redirect(next_page or url_for('home'))
        else:
            flash('Login unsuccessful. Please check your email and password.', "danger")
    return render_template("login.html", form=form)


@app.route("/explore")
def explore():
    form = RentalForm()
    return render_template("explore.html", form=form)


@app.route("/rentmycar")
def rentmycar():
    return render_template("rentmycar.html")


@app.route("/insurance")
def insurance():
    return render_template("insurance.html")


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

        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(os.path.abspath(os.path.dirname(
                __file__)), app.config['UPLOAD_FOLDER'], filename))

        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('contact'))

    return render_template('contact.html', form=form)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # Implement your password reset logic here
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/addinfo')
def addinfo():
    return render_template("addinfo.html")


@app.route('/rental')
@login_required
def rental():
    return render_template("rental.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()  # Log out the user
    return redirect(url_for('home'))  # Redirect to home

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

# Handle unauthorized access


@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to access this page.', 'warning')
    return redirect(url_for('login'))  # Redirect to login page


if __name__ == '__main__':
    app.run(debug=True)
