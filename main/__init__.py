# main/__init__.py
from flask import Flask
from .extensions import db
from .route import register_routes  

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'supersecretkey' 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fleetflow.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    register_routes(app)
    with app.app_context():
        db.create_all()

    return app