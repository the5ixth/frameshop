from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class UploadForm(FlaskForm):
	title = StringField('Title: ', validators=[DataRequired()])
	imgfile = FileField("Image File", validators=[FileRequired(),
												  FileAllowed(["jpg", "png"])])
	comment = TextAreaField('Comment: ', validators=[DataRequired()])
	price = IntegerField('Price :', validators=[])
	artist = StringField('Artist: ', validators=[])
	submit = SubmitField("Submit")
