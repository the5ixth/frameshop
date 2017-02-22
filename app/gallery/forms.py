from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo


class UploadForm(FlaskForm):
    title = StringField('Title: ', validators=[DataRequired()])
    imgfile = FileField("Image File", validators=[FileRequired(),
                                                  FileAllowed(["jpg", "png", "jpeg"])])
    comment = TextAreaField('Comment: ', validators=[DataRequired()])
    price = IntegerField('Price :', validators=[])
    artist = StringField('Artist: ', validators=[])
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    email = StringField('Username: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit = SubmitField("Submit")


class SignupForm(FlaskForm):
    email = StringField('Username: ', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password', validators=[DataRequired()])
    submit = SubmitField("Submit")


class EditForm(FlaskForm):
    title = StringField('Title: ', validators=[DataRequired()])
    comment = TextAreaField('Comment: ', validators=[DataRequired()])
    price = IntegerField('Price :', validators=[])
    artist = StringField('Artist: ', validators=[])
    submit = SubmitField("Submit")

#class BlogForm(FlaskForm):
#    title = StringField('Title: ', validators=[DataRequired()])
#    body = TextAreaField('Body: ', validators=[DataRequired()])
#    submit = SubmitField('Submit')