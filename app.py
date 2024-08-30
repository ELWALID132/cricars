from flask import Flask, render_template, flash, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, login_required, logout_user, LoginManager, current_user
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from itsdangerous import URLSafeTimedSerializer
from forms import LoginForm, RegisterForm, RentalForm, ContactForm, ResetPasswordForm
from models import Guest
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = "TheSuperSecretKey"
app.config['UPLOAD_FOLDER'] = 'static/files'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return Guest.query.get(int(user_id))

@app.context_processor
def inject_user():
    return dict(current_user=current_user)

def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

def verify_reset_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return None
    return email

@app.route('/', methods=['GET', 'POST'])
def home():
    form = RentalForm()
    return render_template("index.html", form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_guest = Guest.query.filter_by(email=form.email.data).first()
        if existing_guest:
            flash('Error: This email is already being used. Please use a different email.', 'danger')
            return render_template("signup.html", form=form)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_guest = Guest(email=form.email.data, password=hashed_password)
        db.session.add(new_guest)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'Error in {getattr(form, field).label.text}: {error}', 'danger')
    return render_template("signup.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        guest = Guest.query.filter_by(email=form.email.data).first()
        if guest and bcrypt.check_password_hash(guest.password, form.password.data):
            login_user(guest)
            return redirect(url_for('rental'))
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
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) 
        
        # Handle the form data (e.g., save to database, send email, etc.)

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
