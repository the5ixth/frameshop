from flask import Blueprint, request, render_template, redirect, url_for, current_app
from flask_login import current_user
from random import randint
from .models import Photo, User
import time
import os

from .. import db

main = Blueprint("main", __name__)



@main.route('/')
def about():
	auth=False
	count = Photo.query.count()
	if current_user.is_authenticated:
		auth = True
	return render_template('about.html', auth=auth)
	
@main.route('/gallery/')
def gallery():
	auth=False
	if current_user.is_authenticated:
		auth = True
	photos = Photo.query.order_by(Photo.id.desc()).paginate(per_page=15, page=request.args.get("page", 1, type=int))
	last_page = int(photos.total / 15 + 1)
	return render_template('gallery.html', photos=photos, last_page=last_page, auth=auth)

@main.route('/gallery/image/<int:num>')
def view(num):
	auth = False
	if current_user.is_authenticated:
		auth = True
	photo = Photo.query.get(num)
	return render_template('view.html', photo=photo, auth=auth)
	


