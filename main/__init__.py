# main/__init__.py
from flask import Flask
from .extensions import db
from .route import register_routes  # import the function that registers all routes

def create_app():
    app = Flask(__name__)
    
    # Configurations
    app.config['SECRET_KEY'] = 'supersecretkey'  # Required for sessions & flash
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fleetflow.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)

    # Register all routes
    register_routes(app)

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app