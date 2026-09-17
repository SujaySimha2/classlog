from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_required
#---------------------------------------------------------
from .exts import db
from .models import Semester
from .forms import SemesterForm
#---------------------------------------------------------
from random import choices
from string import ascii_uppercase, ascii_lowercase, digits
import datetime

semesters_bp = Blueprint("semesters", __name__)

@semesters_bp.route("/semesters/create", methods=["GET", "POST"])
@login_required
def create_semester():
    session["_flashes"] = []
    chars = ascii_uppercase + ascii_lowercase + digits
    #if session.get("current_user_id") is not None:
    if request.method == "POST":
        name = request.form.get("name")
        start_date_str = request.form.get("start_date")
        end_date_str = request.form.get("end_date")

        # Convert string dates to datetime objects
        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date() #pyright:ignore
        end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date() #pyright:ignore

        uid = session.get("current_user_id")
        id = "".join(choices(chars, k=5))
            
        if start_date >= end_date:
            flash("Start date must be before end date.", category="error")
        else:
            semester = Semester(id=id, uid=uid, name=name, start_date=start_date, end_date=end_date) #pyright:ignore
            db.session.add(semester)
            db.session.commit()
            return redirect(url_for("semesters.list_semesters"))
    return render_template("create_semester.html", form=SemesterForm())
    #else:
     #   flash("You need to be logged in to create a semester.")
      #  return redirect(url_for("auth.login"))

@semesters_bp.route("/semesters", methods=["GET"])
@login_required
def list_semesters():
    return ""
