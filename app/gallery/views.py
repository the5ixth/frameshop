from flask import Blueprint, request, render_template, redirect, url_for, current_app
from flask_login import current_user
from .models import Photo
from sqlalchemy.sql.expression import func

main = Blueprint("main", __name__)

user = current_user


@main.route('/')
def about():
    photo = Photo.query.order_by(func.rand()).first()
    #posts = Blog.query.order_by(Blog.date).limit(3)
    return render_template('about.html', photo=photo, user=user)


@main.route('/gallery/')
def gallery():
    photos = Photo.query.order_by(Photo.id.desc()).paginate(per_page=15, page=request.args.get("page", 1, type=int))
    last_page = int(photos.total / 15 + 1)
    return render_template('gallery.html', photos=photos, last_page=last_page, user=user)


@main.route('/gallery/image/<int:num>')
def view(num):
    photo = Photo.query.get(num)
    return render_template('view.html', photo=photo, user=user)


#@main.route('/news')
#def news():
#    posts = Blog.query.order_by().paginate(per_page=10, page=request.args.get("page", 1, type=int))
#    last_page = int(posts.total / 10 + 1)
#    return render_template('news.html', posts=posts, last_page=last_page, user=user)
