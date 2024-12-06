from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///betting_app.db'

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    # Import and register blueprints
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
