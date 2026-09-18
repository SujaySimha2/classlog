from flask import Blueprint, render_template, redirect, url_for, session, flash, request, abort
from flask_login import login_required
#---------------------------------------------------------
from .exts import db
from .models import Subject, Semester
from .forms import SubjectForm
#---------------------------------------------------------
from random import choices
from string import ascii_uppercase, ascii_lowercase, digits

subjects_bp = Blueprint("subjects", __name__)

@subjects_bp.route("/subjects/create", methods=["GET", "POST"])
@login_required
def create_subject():
    semester_id = session.get("current_semester_id")
    if Semester.query.filter_by(id=semester_id).first().uid == session.get("current_user_id"): #pyright:ignore
        session["_flashes"] = []
        chars = ascii_uppercase + ascii_lowercase + digits
        semester = Semester.query.filter_by(id=semester_id).first() #pyright:ignore
        if request.method == "POST":
            semester_id = session.get("current_semester_id")
            name = request.form.get("name")
            code = request.form.get("code")
            uid = session.get("current_user_id")
            id = "".join(choices(chars, k=5))

            if name == "":
                flash("Subject name cannot be empty.", category="error")
            else:
                subject = Subject(id=id, uid=uid, sid=semester_id, name=name, code=code) #pyright:ignore
                db.session.add(subject)
                db.session.commit()
                return redirect(url_for("subjects.manage_subjects"))
        return render_template("create_subject.html", form=SubjectForm(), semester=semester)
    else:
        return abort(403)

@subjects_bp.route("/subjects", methods=["GET"])
@login_required
def manage_subjects():
    return ""
