from flask import Flask, render_template, request, redirect, url_for # Import necessary modules

app = Flask(__name__) # Initialize the Flask application

# Sample data for users (replace with a proper database in a real application)
users = [{'email': 'user1', 'password': 'password1'},
         {'email': 'user2', 'password': 'password2'}]

# Routes for different pages
@app.route('/') # Define the route for the home page
def home():
    return render_template('home.html') # Render the home page template

@app.route('/about') # Define the route for the about page
def about():
    return render_template('about.html') # Render the about page template
@app.route('/addinfo')
def info():
    return render_template('addinfo.html')
@app.route('/login', methods=['GET', 'POST']) # Define the route for the login page
def login():
    if request.method == 'POST': # If the request method is POST
        email = request.form['email'] # Get the email from the form
        password = request.form['password'] # Get the password from the form

        # Validate login (replace with proper validation)
        for user in users: # Loop through the list of users
            if user['email'] == email and user['password'] == password: # If the email and password match
                # Redirect to home page after successful login
                return redirect(url_for('home')) # Redirect to the home page

        # If login fails, show an error message
        return render_template('login.html', error='Invalid email or password') # Render the login page with an error message

    # If the request is a GET request, render the login page
    return render_template('login.html') # Render the login page template

@app.route('/signup', methods=['GET', 'POST']) # Define the route for the signup page
def signup():
    if request.method == 'POST': # If the request method is POST
        email = request.form['email'] # Get the email from the form
        password = request.form['password'] # Get the password from the form
        confirm_password = request.form['confirm_password'] # Get the confirmed password from the form

        # Check if the password length is at least 8 characters
        if len(password) < 8:
            return render_template('signup.html', error='Password must be at least 8 characters long') # Render the signup page with an error message

        # Check if passwords match
        if password != confirm_password:
            return render_template('signup.html', error='Passwords do not match') # Render the signup page with an error message

        # Add user to the list (replace with proper user registration)
        users.append({'email': email, 'password': password}) # Add the user to the list

        return redirect(url_for('info')) 

    # If the request is a GET request, render the signup page
    return render_template('signup.html') # Render the signup page template

if __name__ == '__main__':
    app.run(debug=True) # Run the Flask application in debug mode