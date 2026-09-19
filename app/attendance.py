from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from flask_login import login_required
#---------------------------------------------------------
from .exts import db
from .models import Subject, Semester
from .forms import AttendanceForm
#---------------------------------------------------------
import datetime

attendance_bp = Blueprint("attendance", __name__)

@attendance_bp.route("/attendance/mark", methods=["GET", "POST"])
@login_required
def mark_attendance():
    semester_id = session.get("current_semester_id")
    if Semester.query.filter_by(id=semester_id).first().uid == session.get("current_user_id"): #pyright:ignore
        subject_names = [i.name for i in Subject.query.filter_by(sid=semester_id).all()]
        subject_codes = [i.id for i in Subject.query.filter_by(sid=semester_id).all()]
        subjects = list(zip(subject_codes, subject_names))
        form = AttendanceForm()
        form.subject.choices = subjects
        if request.method == "POST":
            subject_code = request.form.get("subject")
            date_str = request.form.get("date")
            start_time_str = request.form.get("start_time")
            end_time_str = request.form.get("end_time")
            status = request.form.get("status")

            if not subject_code:
                flash("Please select a subject.", category="error")
                return redirect(url_for("attendance.mark_attendance"))
            elif not date_str:
                flash("Please select a date.", category="error")
                return redirect(url_for("attendance.mark_attendance"))
            elif not start_time_str:
                flash("Please select a start time.", category="error")
                return redirect(url_for("attendance.mark_attendance"))
            elif not end_time_str:
                flash("Please select an end time.", category="error")
                return redirect(url_for("attendance.mark_attendance"))
            elif datetime.datetime.strptime(start_time_str, "%H:%M") >= datetime.datetime.strptime(end_time_str, "%H:%M"):
                flash("Start time must be before end time.", category="error")
                return redirect(url_for("attendance.mark_attendance"))
            elif datetime.datetime.strptime(date_str, "%Y-%m-%d").date() < Semester.query.filter_by(id=semester_id).first().start_date or datetime.datetime.strptime(date_str, "%Y-%m-%d").date() > Semester.query.filter_by(id=semester_id).first().end_date: #pyright:ignore
                flash("Date must be within the semester duration.", category="error")
                return redirect(url_for("attendance.mark_attendance"))

            subject = Subject.query.filter_by(id=subject_code, sid=semester_id).first()
            if subject:
                attendance_list = list(subject.date_times)
                attendance_list.append([subject_code, date_str, start_time_str, end_time_str, status])
                subject.date_times = attendance_list

                present_count = sum(1 for record in attendance_list if record[4] == "present")
                total_count = len(attendance_list)
                subject.attendance = float((present_count / total_count) * 100) if total_count > 0 else 0

                db.session.add(subject)
                db.session.commit()
                flash("Attendance updated successfully.", category="success")
                return redirect(url_for("attendance.mark_attendance"))
            else:
                flash("Subject not found.", category="error")
                return redirect(url_for("attendance.mark_attendance"))
        return render_template("attendance.html", form=form)
    else:
        flash("Please select a valid semester to mark attendance.", category="warning")
        return redirect(url_for("semesters.list_semesters"))
