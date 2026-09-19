from flask import Blueprint, render_template, redirect, url_for, flash, request, session, abort
from flask_login import login_required
#---------------------------------------------------------
from .exts import db
from .models import Semester, Subject
#---------------------------------------------------------
import math

index = Blueprint('index', __name__)

@index.route('/')
@login_required
def index_page():
    semester_id = session.get("current_semester_id")
    if Semester.query.filter_by(id=semester_id).first() and Semester.query.filter_by(id=semester_id).first().uid == session.get("current_user_id"): #pyright:ignore
        subjects = Subject.query.filter_by(sid=semester_id).all()
        classes_can_skip = []
        classes_to_recover = []
        for subject in subjects:
            if subject.date_times != []:
                present_count = sum(1 for record in subject.date_times if record[4] == "present")
                total_count = len(subject.date_times)
                can_skip = (100*present_count - subject.min_attendance*total_count) / subject.min_attendance
                try:    
                    to_recover = (subject.min_attendance*total_count - 100*present_count) / (100 - subject.min_attendance)
                except ZeroDivisionError:
                    to_recover = -1
                classes_can_skip.append(math.floor(can_skip))
                classes_to_recover.append(math.ceil(to_recover))
                continue
            else:
                classes_can_skip.append(0)
                classes_to_recover.append(0)
                continue

        return render_template('index.html', subjects=subjects, classes_can_skip=classes_can_skip, classes_to_recover=classes_to_recover, current_semester=Semester.query.filter_by(id=semester_id).first()) #pyright:ignore
    else:
        flash("Please select a valid semester to view subjects.", category="warning")
        return redirect(url_for("semesters.list_semesters"))
