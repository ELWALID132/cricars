from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user ,login_required , logout_user , LoginManager , current_user
from flask_bcrypt import Bcrypt
from .models import User
from .forms import RegisterForms, LoginForms
# Initialize the Flask app
app = Flask(__name__)

# Initialize the Bcrypt library for password hashing
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Add configuration for using a SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Set a secret key for the app
app.config['SECRET_KEY'] = "TheSuperSecretKey"

# Initialize the SQLAlchemy instance
db = SQLAlchemy(app)

# Route for home page
@app.route('/')
def home():
    return render_template('index.html')


# Create a route for the login page
@app.route("/login", methods = ["GET", "POST"])
def login():
    form = LoginForms()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user : 
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user , login_manager)
                return redirect(url_for('rental'))
        else:
            flash('Login unsuccessful. Please check your email and password.')

    return render_template("login.html", form = form)

# Create a route for the register page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForms()

    if form.validate_on_submit():
        # Hash the entered password
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        # Create a new User instance with the entered email and hashed password
        new_user = User(email = form.email.data, password = hashed_password)
        # Add the new User instance to the database session
        db.session.add(new_user)
        # Commit the changes to the database
        db.session.commit()
        # Redirect to the login page
        return redirect(url_for('login'))
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("signup.html")


    # Check if the request method is POST
    if request.method == "POST":
        # Get email and password from the form
        email = request.form.get("email")
        password = request.form.get("password")

        # Check if email is provided
        if not email:
            flash("Email must be provided", "error")
            return redirect(url_for("login"))

        # Check if password is provided
        elif not password:
            flash("Password must be provided", "error")
            return redirect(url_for("login"))

        # Query the database to check if the email exists
        sql = "SELECT * FROM guests WHERE email = %s"
        db.mycursor.execute(sql, (email,))
        user = db.mycursor.fetchone()

        # Check if the email exists in the database
        if not user:
            flash("Incorrect email or password", "error")
            return redirect(url_for("login"))

        # Verify the password
        if not pbkdf2_sha256.verify(password, user[2]):  # Assuming password is at index 2
            flash("Incorrect email or password", "error")
            return redirect(url_for("login"))

        # Store the user ID in the session
        session["user_id"] = user[0]

        # Redirect the user to the home page
        return redirect(url_for("home"))

    # If the request method is GET, render the login template
    else:
        return render_template("login.html")
# Route for rent my car page
@app.route("/rentmycar")
def rentmycar():
   return render_template("rentmycar.html")

# Route for reset password page
@app.route("/resetpassword")
def resetpassword():
   return render_template("resetpassword.html")

# Route for insurance page
@app.route("/insurance")
def insurance():
   return render_template("insurance.html")

# Route for help page
@app.route("/help")
def help():
   return render_template("help.html")

# Route for contact page
@app.route("/contact")
def contact():
   return render_template("contact.html")

# Route for addinfo page
@app.route('/addinfo')
def addinfo():
   return render_template("addinfo.html")

# Route for rental page
@app.route('/rental')
@login_required
def rental():
   return render_template("rental.html")

# Create a route for the logout page
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Route for search page
@app.route("/search")
def search():
   return render_template("home.html")

# Route for about page
@app.route("/about")
def about():
   return render_template("about.html")

# Create a route for the 404 error page
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Create a route for the 500 error page
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

# Run the Flask app
if __name__ == '__main__':
   app.run(debug=True)