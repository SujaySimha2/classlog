"""
Created on 10 September 2026 16∶30∶12 IST

@uthor: $ujay $imha
"""

from flask import Flask
from config import DevelopmentConfig
from .exts import db, migrate, login_manager
from .main import index
from .auth import auth
from .semesters import semesters_bp
from .subjects import subjects_bp
from .attendance import attendance_bp
from .models import *

def register_blueprints(app):
    app.register_blueprint(index)
    app.register_blueprint(auth)
    app.register_blueprint(semesters_bp)
    app.register_blueprint(subjects_bp)
    app.register_blueprint(attendance_bp)

def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login" #pyright:ignore

def create_app(config=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config)

    register_blueprints(app)
    register_extensions(app)

    return app
