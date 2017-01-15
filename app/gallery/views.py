from flask import Blueprint, request, render_template, redirect, url_for, current_app
from werkzeug.utils import secure_filename
from random import randint
from .models import Photo
from .forms import UploadForm
import time
import os

from .. import db

main = Blueprint("main", __name__)
		
	
@main.route('/')
def about():
	count = Photo.query.count()
	num = randint(1,count)
	photo = Photo.query.get(num)
	return render_template('about.html', photo=photo)
	
@main.route('/gallery/')
def gallery():
	photos = Photo.query.order_by(Photo.id.desc()).paginate(per_page=15, page=request.args.get("page", 1, type=int))
	last_page = int(photos.total / 15 + 1)
	return render_template('gallery.html', photos=photos, last_page=last_page)	

@main.route('/gallery/image/<int:num>')
def view(num):
	photo = Photo.query.get(num)
	return render_template('view.html', photo=photo)

@main.route('/upload', methods=['GET', 'POST'])
def upload():
	form = UploadForm()
	if form.validate_on_submit():
		ph = Photo()
		form.populate_obj(ph)
		filename = time.strftime("%y%j") + "_" + time.strftime("%d%H%S") + "_" + secure_filename(ph.imgfile.filename[-5:])
		ph.imgfilename = filename
		form.imgfile.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'],
									 	    filename))
		db.session.add(ph)
		db.session.commit()
		return redirect(url_for("main.about"))
	return render_template("upload.html", form=form)
		
		
		

