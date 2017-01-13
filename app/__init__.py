from flask import Flask, render_template, request, flash
from flask_wtf import Form
from flask_wtf.file import FileField
from flask_wtf.csrf import CsrfProtect
from werkzeug import secure_filename
from wtforms import TextField, TextAreaField,IntegerField
import time
import os
import gall

UPLOAD_FOLDER = '/home/the5ixth/Desktop/frame/app/static/images'
ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg', 'gif'])
WTF_CSRF_CHECK_DEFAULT = False
csrf = CsrfProtect()

application = Flask(__name__)
csrf.init_app(application)

application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
application.config['SECRET_KEY'] = 'key'

class Page:	
	def __init__(self, page):
		self.current = page
		self.prev = page - 1
		self.prev2 = page - 2
		self.next = page + 1
		self.next2 = page + 2
	
	def show(self):
		print self.current
		print self.prev
		print self.next

#############################################
###		Upload Field
#############################################

class uploadForm(Form):
	title = TextField('Title: ')
	file = FileField()
	comment = TextAreaField('Comment: ')
	price = IntegerField('Price :')
	artist = TextField('Artist: ')

#############################################
##		random globals
#############################################
count = gall.count()
num_pages = ((count-1) / 15) + 1
remain = count - (( num_pages - 1 ) * 15 )

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#############################################
###		HTML pages
#############################################
print "count: "+ str(count)
print "number of pages: " + str(num_pages)
print "remainder: " + str(remain)

	
@application.route('/')
def about():
	page = Page(1)
	photos = gall.get_page(page.current)
	if photos:	
		if page.current == num_pages:
			row1 = []
			row2 = []
			row3 = []
			i = 0
			for photo in photos:
				if i == 0:
					row1.append(photo)
					i = 1
				elif i == 1:
					row2.append(photo)
					i = 2
				elif i == 2:
					row3.append(photo)
					i = 0
							
		else:
			row1 = photos[:6]
			row2 = photos[5:11]
			row3 = photos[10:]
		return render_template('about.html', photos=photos, count=count, row1=row1, row2=row2, row3=row3, page=page, num_pages=num_pages)
	else:
		gallery()
		
@application.route('/gallery/')
def gallery():
	page = Page(1)
	photos = gall.get_page(page.current)
	if photos:	
		if page.current == num_pages:
			row1 = []
			row2 = []
			row3 = []
			i = 0
			for photo in photos:
				if i == 0:
					row1.append(photo)
					i = 1
				elif i == 1:
					row2.append(photo)
					i = 2
				elif i == 2:
					row3.append(photo)
					i = 0
							
		else:
			row1 = photos[:6]
			row2 = photos[5:11]
			row3 = photos[10:]
		return render_template('index.html', photos=photos, count=count, row1=row1, row2=row2, row3=row3, page=page, num_pages=num_pages)
	else:
		gallery()
	
@application.route('/gallery/<page>')
def page(page):
	page = Page(int(page))
	photos = gall.get_page(page.current)
	if photos:	
		if page.current == num_pages:
			row1 = []
			row2 = []
			row3 = []
			i = 0
			for photo in photos:
				if i == 0:
					row1.append(photo)
					i = 1
				elif i == 1:
					row2.append(photo)
					i = 2
				elif i == 2:
					row3.append(photo)
					i = 0
							
		else:
			row1 = photos[:6]
			row2 = photos[5:11]
			row3 = photos[10:]
		return render_template('index.html', photos=photos, count=count, row1=row1, row2=row2, row3=row3, page=page, num_pages=num_pages)
	else:
		gallery()
		
@application.route('/gallery/image/<num>')
def view(num):
	photo = gall.get_image(int(num))
	return render_template('view.html', photo=photo)

@application.route('/upload', methods=['GET', 'POST'])
def upload():
	form = uploadForm()
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = (time.strftime("%Y%m%d_%H%M%S") + '.jpeg')
			file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
			next_id = gall.get_last() + 1			
			obj = gall.Photo()
			obj.id = next_id
			obj.image = filename 
			obj.title = request.form['title']
			obj.comment =  request.form['comment']
			obj.price = request.form['price']
			obj.artist = request.form['artist']
			gall.insert(obj)
			return render_template('upload.html', form=form)
		else:
			print "something fucking broke"
			return render_template('index.html')
	elif request.method == 'GET':
		return render_template('upload.html', form=form)
	else:
		print "something broke"
		return render_template('upload.html', form=form)



if(__name__)==('__main__'):
	application.run(debug=True)
