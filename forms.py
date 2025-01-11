from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, IntegerField, DateField, SelectField, SubmitField, RadioField, FileField, TextAreaField
from wtforms.validators import DataRequired, length, EqualTo



class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    surname = StringField("Surname", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), length(min=8, max=30)])
    repeat_password = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField("Create Account")
    
class UserEdit(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    surname = StringField("Surname", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), length(min=8, max=30)])
    repeat_password = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField("Submit Changes")
    
class ServiceForm(FlaskForm):
    title = StringField("სათაური", validators=[DataRequired()])
    description = StringField("მოკლე აღწერა", validators=[DataRequired(), length(min=5, max=94)])
    details = TextAreaField("პროდუქტის დეტალური აღწერა", validators=[DataRequired()])
    price = IntegerField("ფასი", validators=[DataRequired()])
    imgurl = StringField("სურათის URL", validators=[DataRequired()])
    submit = SubmitField("სერვისის დამატება")

class CourseForm(FlaskForm):
    title = StringField("სათაური", validators=[DataRequired()])
    description = StringField("მოკლე აღწერა", validators=[DataRequired(), length(min=5, max=94)])
    details = TextAreaField("პროდუქტის დეტალური აღწერა", validators=[DataRequired()])
    price = IntegerField("ფასი", validators=[DataRequired()])
    imgurl = StringField("სურათის URL", validators=[DataRequired()])
    submit = SubmitField("კურსის დამატება")
    
class SoftwareForm(FlaskForm):
    title = StringField("სათაური", validators=[DataRequired()])
    description = StringField("მოკლე აღწერა", validators=[DataRequired(), length(min=5, max=94)])
    details = TextAreaField("პროდუქტის დეტალური აღწერა", validators=[DataRequired()])
    price = IntegerField("ფასი", validators=[DataRequired()])
    imgurl = StringField("სურათის URL", validators=[DataRequired()])
    submit = SubmitField("სოფტის დამატება")
    

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
    
    
    
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), length(min=5, max=21)])
    subtitle = StringField("Subtitle (Little Description About Vuln)", validators=[DataRequired(), length(min=5, max=94)])
    description = TextAreaField("Write full description of subject....", validators=[DataRequired()])
    imgurl = StringField("ENTER VALID IMAGE URL", validators=[DataRequired()])
    submit = SubmitField("Post")