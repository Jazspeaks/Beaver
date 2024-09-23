from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, FieldList, FormField, DateField, HiddenField, FileField
from wtforms.validators import DataRequired, Email, Optional
from flask_wtf.file import FileAllowed


class SignupForm(FlaskForm):
    username = StringField('نام کاربری', validators=[DataRequired()])
    email = StringField('ایمیل', validators=[DataRequired(), Email()])
    password = PasswordField('رمز عبور', validators=[DataRequired()])
    submit = SubmitField('ورود')

class LoginForm(FlaskForm):
    email = StringField('ایمیل', validators=[DataRequired(), Email()])
    password = PasswordField('رمز عبور', validators=[DataRequired()])
    submit = SubmitField('ورود')

class EntryForm(FlaskForm):
    entry = StringField('Entry', validators=[DataRequired()])

class CVForm(FlaskForm):
    full_name = StringField('نام و نام خانوادگی', validators=[DataRequired()])
    email = StringField('ایمیل', validators=[DataRequired()])
    phone_number = StringField('تلفن همراه', validators=[Optional()])
    date_of_birth = DateField('تاریخ تولد', validators=[Optional()])
    job_title = StringField('موقعیت شغلی', validators=[Optional()])
    description = TextAreaField('مختصری از من', validators=[Optional()])
    
    education = FieldList(FormField(EntryForm), min_entries=0, max_entries=20)
    experience = FieldList(FormField(EntryForm), min_entries=0, max_entries=20)
    projects = FieldList(FormField(EntryForm), min_entries=0, max_entries=20)
    skills = FieldList(FormField(EntryForm), min_entries=0, max_entries=20)
    certifications = FieldList(FormField(EntryForm), min_entries=0, max_entries=20)
    interests = FieldList(FormField(EntryForm), min_entries=0, max_entries=20)
    references = FieldList(FormField(EntryForm), min_entries=0, max_entries=20)
    
    submit = SubmitField('Submit')
    add_field = SubmitField('Add Field')
    remove_field = SubmitField('Remove Field')
    
class PostForm(FlaskForm):
    title = TextAreaField('عنوان')
    content = TextAreaField('توضیحات')
    media = FileField('آپلود فایل', validators=[FileAllowed(['jpg','jpeg' , 'png', 'gif', 'mp4'])])
    submit = SubmitField('پست')