from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_bcrypt import Bcrypt
from itsdangerous import URLSafeTimedSerializer
from models import guests  # Assuming your model is named `guests`

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = "TheSuperSecretKey"
app.config['UPLOAD_FOLDER'] = 'static/files'
app.config['SECURITY_PASSWORD_SALT'] = 'YourSecretSalt'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return guests.query.get(int(user_id))

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

# Import routes after all initializations to avoid circular imports
from routes import *

if __name__ == '__main__':
    app.run(debug=True)
