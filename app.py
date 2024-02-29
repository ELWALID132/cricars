from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key

# In-memory user storage (replace this with a database in a production app)
users = []

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validate password length
        if len(password) < 8:
            flash('Password must be at least 8 characters long', 'error')
            return redirect(url_for('signup'))

        # Validate password match
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('signup'))

        # Store the user in memory (you should store it in a database in a production app)
        hashed_password = generate_password_hash(password, method='sha256')
        users.append({'username': username, 'password': hashed_password})
        flash('Account created successfully', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Find the user in memory (you should query a database in a production app)
        user = next((user for user in users if user['username'] == username), None)

        if user and check_password_hash(user['password'], password):
            flash('Login successful', 'success')
            # Implement session handling here
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    # Implement logout functionality (clear session, etc.)
    flash('Logged out successfully', 'success')
    return redirect(url_for('home'))

@app.route("/search")
def search():
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)
