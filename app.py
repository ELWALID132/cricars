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
from app import routes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = "TheSuperSecretKey"
app.config['UPLOAD_FOLDER'] = 'static/files'
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
# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
