"""
Created on 10 September 2026 16∶30∶12 IST

@uthor: $ujay $imha
"""

from flask import Flask
from config import DevelopmentConfig
from .exts import db, migrate, login_manager
from .main import index

def register_blueprints(app):
    app.register_blueprint(index)

def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

def create_app(config=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config)

    register_blueprints(app)
    register_extensions(app)

    return app
