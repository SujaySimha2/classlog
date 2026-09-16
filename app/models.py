from flask_login import UserMixin
from .exts import db, login_manager

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.String(5), primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    semesters = db.relationship('Semester', backref='user', lazy=True)
    subjects = db.relationship('Subject', backref='user', lazy=True)

class Semester(db.Model):
    __tablename__ = 'semesters'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    subjects = db.relationship('Subject', backref='semester', lazy=True)

class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    sid = db.Column(db.Integer, db.ForeignKey('semesters.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    code = db.Column(db.String(20), nullable=True)
    date_times = db.Column(db.JSON, nullable=True)
    attendance = db.Column(db.Integer, nullable=False, default=0)
    min_attendance = db.Column(db.Float, nullable=False, default=100.00)

@login_manager.user_loader
def load_user(uid):
    return User.query.get(str(uid))
