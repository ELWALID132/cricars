from flask import Flask, render_template, request, redirect, url_for, flash # Importing necessary modules from Flask for web development
from werkzeug.security import generate_password_hash, check_password_hash # Importing password security functions

app = Flask(__name__) # Creating a new Flask web server

# List to store user information
users = []

# Route for home page
@app.route('/')
def home():
   return render_template("home.html")

# Route for rent my car page
@app.route("/rentmycar")
def renttmycar():
   return render_template("rentmycar.html")

# Route for reset password page
@app.route("/resetpassword")
def resetpassword():
   return render_template("resetpassword.html")

# Route for insurnece page
@app.route("/insurnece")
def insurnece():
   return render_template("insurnece.html")

# Route for help page
@app.route("/help")
def help():
   return render_template("help.html")

# Route for contact page
@app.route("/contact")
def contact():
   return render_template("contact.html")

# Route for signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
   if request.method == 'POST':
      # Getting user input from signup form
       username = request.form['email']
       password = request.form['password']
       confirm_password = request.form['confirm_password']

       # Validating password length
       if len(password) < 8:
           flash('Password must be at least 8 characters long', 'error')
           return redirect(url_for('signup'))

       # Validating password confirmation
       if password != confirm_password:
           flash('Passwords do not match', 'error')
           return redirect(url_for('signup'))

       # Hashing password for security
       hashed_password = generate_password_hash(password, method='sha256')

       # Adding user information to the users list
       users.append({'username': username, 'password': hashed_password})

       # Displaying success message
       flash('Account created successfully', 'success')
       return redirect(url_for('login'))

   return render_template('signup.html')

# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
   if request.method == 'POST':
       # Getting user input from login form
       username = request.form['username']
       password = request.form['password']

       # Searching for user in the users list
       user = next((user for user in users if user['username'] == username), None)

       # Checking if user exists and password is correct
       if user and check_password_hash(user['password'], password):
           flash('Login successful', 'success')
           return redirect(url_for('home'))
       else:
           flash('Invalid username or password', 'error')

   return render_template('login.html')

# Route for addinfo page
@app.route('/addinfo')
def addinfo():
   return render_template("addinfo.html")

# Route for rental page
@app.route('/rental')
def rental():
   return render_template("rental.html")

# route for insurance

# Route for logout
@app.route('/logout')
def logout():
   flash('Logged out successfully', 'success')
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