from flask import Blueprint, flash, redirect, render_template, request
from flask import session, url_for
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
# -----------------------------------------------------------------------
from datetime import timedelta
from random import choices
from string import ascii_uppercase, ascii_lowercase, digits
# ---------------------------------------------------------
from .exts import db
from .forms import SignUpForm, LoginForm
from .models import User
# from config import Config

auth = Blueprint("auth", __name__)

@auth.route("/auth/signup", methods=["GET", "POST"])
def signup():
    session["_flashes"] = []
    chars = ascii_uppercase + ascii_lowercase + digits
    if session.get("current_user_id") is None:
        if request.method == "POST":
            username = request.form.get("username")
            email = request.form.get("email")
            password: str = generate_password_hash(request.form.get("password")) # pyright: ignore
            id = "".join(choices(chars, k=5))
            if User.query.filter_by(email=email).first() is not None:
                flash("Email already exists!", category="error")
            else:
                user = User(id=id, username=username, email=email, password_hash=password) # pyright: ignore
                db.session.add(user)
                db.session.commit()
                return redirect(url_for("auth.login"))
        return render_template("signup.html", form=SignUpForm())

    else:
        return redirect("/")

    
@auth.route("/auth/login", methods=["GET", "POST"])
def login():
    session.permanent = True
    session.permanent_session_lifetime = timedelta(days=365) # pyright: ignore
    if session.get("current_user_id") is None:
        if request.method == "POST":
            email = request.form.get("email")
            password: str = request.form.get("password") # pyright: ignore
            user = User.query.filter_by(email=email).first()

            if user is not None and check_password_hash(user.password_hash, password):
                login_user(user)
                session["current_user_id"] = user.id
                return redirect("/")

            else:
                if user is None:
                    flash("Email cannot be found!", category="error")
                else:
                    if not check_password_hash(user.password_hash, password):
                        flash("Password is incorrect!", category="error")
        return render_template("login.html", form=LoginForm())
    else:
        return redirect("/")

@auth.route("/auth/logout")
@login_required
def logout():
    logout_user()
    session.pop("current_user_id", None)
    return redirect("/auth/login")
