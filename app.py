from flask import Flask, render_template, request, redirect, url_for, session, flash # Importing necessary modules from Flask for web development
from werkzeug.security import generate_password_hash, check_password_hash # Importing password security functions
from passlib.hash import pbkdf2_sha256
from db.database import Database



app = Flask(__name__) # Creating a new Flask web server

# Create an instance of the Database class
db = Database()

# Call the create_table method to create the 'guests' table
db.create_table() 
app.secret_key = 'your_secret_key_here'

# For demonstration purposes, let's assume the user is authenticated
authenticated = True

# Route for home page
@app.route('/')
def home():
    return render_template('home.html', authenticated=authenticated)

# Route for signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Forget any user_id
    session.clear()
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure email was submitted
        if not request.form.get("email"):
            flash("Must provide email", "error")
            return redirect(url_for("signup"))
        
        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Must provide password", "error")
            return redirect(url_for("signup"))
        
        # Ensure confirm password was submitted
        elif not request.form.get("confirm_password"):
            flash("Must provide the confirm password", "error")
            return redirect(url_for("signup"))
        
        # Ensure that password and confirm password match
        elif request.form.get("password")!= request.form.get("confirm_password"):
            flash("The password and the confirm password must match", "error")
            return redirect(url_for("signup"))
        
        # Ensure that the chosen email is unique (does not exist in the database)
        val = (request.form.get("email"),)
        sql = "SELECT * FROM guests WHERE email = %s"
        cursor = db.connection.cursor()
        cursor.execute(sql, val)
        rows = cursor.fetchall()
        if len(rows) >= 1:
            flash("Email already exists", "error")
            return redirect(url_for("signup"))
        
        # Add user to database
        hashed_password = generate_password_hash(request.form.get("password"))
        sql = "INSERT INTO guests (email, password) VALUES (%s, %s)"
        val = (request.form.get("email"), hashed_password)
        cursor.execute(sql, val)
        db.connection.commit()
        
        # Login user automatically and remember session
        cursor.execute("SELECT * FROM guests WHERE email = %s", (request.form.get("email"),))
        rows = cursor.fetchall()
        session["user_id"] = rows[0][0]
        
        # Redirect to home page
        return redirect(url_for("home"))
    
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("signup.html")

# Login route
@app.route("/login", methods=['GET', 'POST'])
def login():
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
def rental():
   return render_template("rental.html")

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('home'))

# Route for search page
@app.route("/search")
def search():
   return render_template("home.html")

# Route for about page
@app.route("/about")
def about():
   return render_template("about.html")

# Running the Flask app
if __name__ == '__main__':
   app.run(debug=True)