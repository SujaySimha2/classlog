
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, DateField, TimeField, SelectField
from wtforms.validators import DataRequired


class SignUpForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField()


class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField()

class SemesterForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    start_date = DateField(validators=[DataRequired()], format="%d-%m-%Y")
    end_date = DateField(validators=[DataRequired()], format="%d-%m-%Y")
    submit = SubmitField()

class SubjectForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    code = StringField()
    min_attendance = StringField(validators=[DataRequired()])
    submit = SubmitField()

class AttendanceForm(FlaskForm):
    subject = SelectField("Select a subject", choices=[], validators=[DataRequired()])
    date = DateField(validators=[DataRequired()], format="%Y-%m-%d")
    start_time = TimeField(validators=[DataRequired()], format="%H:%M")
    end_time = TimeField(validators=[DataRequired()], format="%H:%M")
