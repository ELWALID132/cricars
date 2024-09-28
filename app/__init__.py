from flask import Flask
from .config import Config
from .extensions import db, bcrypt, login_manager
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = "main.login"

    # Import and register blueprints after app is initialized
    from .routes import main
    app.register_blueprint(main)

    return app

@login_manager.user_loader
def load_user(user_id):
    from .models import guests  # Avoid circular import
    return guests.query.get(int(user_id))
