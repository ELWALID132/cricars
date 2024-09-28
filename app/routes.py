from flask import render_template, redirect, url_for, flash, request
from .extensions import db, bcrypt
from .models import guests
from .forms import RegisterForm, LoginForm, RentalForm, ResetPasswordForm, ContactForm
from flask_login import login_user, logout_user, login_required
import os 
from werkzeug.utils import secure_filename

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
        existing_guest = guests.query.filter_by(email=form.email.data).first()
        if existing_guest:
            flash('Error: This email is already being used. Please use a different email.', 'danger')
            return render_template("signup.html", form=form)
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_guest = guests(email=form.email.data, password=hashed_password)
        db.session.add(new_guest)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template("signup.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        guests = guests.query.filter_by(email=form.email.data).first()
        if guests and bcrypt.check_password_hash(guests.password, form.password.data):
            login_user(guests)  # Log in the user
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('next')  # Get the next parameter
            return redirect(next_page or url_for('home'))  # Redirect to the next page or home
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
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], filename)) 
        
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
