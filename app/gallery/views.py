import time

from flask import Blueprint, request, render_template, redirect, url_for, current_app
from flask_login import current_user
from .models import Photo, Description, Comments
from .forms import CommentForm
from sqlalchemy.sql.expression import func
from .. import db

main = Blueprint("main", __name__, static_url_path='/static', static_folder='/static')

user = current_user


@main.route('/')
def about():
    desc = Description.query.first()
    photo = Photo.query.order_by(func.rand()).first()
    #posts = Blog.query.order_by(Blog.date).limit(3)
    return render_template('about.html', photo=photo, user=user, desc=desc)


@main.route('/gallery/')
def gallery():
    photos = Photo.query.order_by(Photo.id.desc()).paginate(per_page=15, page=request.args.get("page", 1, type=int))
    last_page = int(photos.total / 15 + 1)
    num = 3
    if photos.has_prev:
        if photos.prev_num - 1 > 0 :
            num += 1
        num +=1
    if photos.has_next:
        if photos.next_num + 1 < photos.pages:
            num += 1
        num += 1
    percent = 100/num
    return render_template('gallery.html', photos=photos, last_page=last_page, user=user, percent=percent)


@main.route('/gallery/image/<int:num>', methods=['GET', 'POST'])
def view(num):
    form = CommentForm()
    photo = Photo.query.get(num)
    if not user:
        comment = Comments.query.order_by(Comments.date.desc())\
                          .filter(Comments.photoid == photo.id)\
                          .filter(Comments.hidden == False)\
                          .paginate(per_page=5, page=request.args.get('page', 1, type=int))
    else:
        comment = Comments.query.order_by(Comments.date.desc())\
                          .filter(Comments.photoid == photo.id)\
                          .paginate(per_page=5, page=request.args.get('page', 1, type=int))
    last_page = int(comment.total / 5 + 1)
    num = 0
    if comment.has_prev:
         num += 1
    if comment.has_next:
        num +=1
    percent = 100/ (num + 3)
    if request.method == 'POST':
        if form.validate_on_submit:
            new_comment = Comments()
            form.populate_obj(new_comment)
            new_comment.date = time.strftime("%Y/%m/%d, %H:%M:%S")
            new_comment.photoid = photo.id
            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for('main.view', num=photo.id))
    return render_template('view.html', photo=photo, user=user, comments=comment, form=form, last_page=last_page, percent=percent)


#@main.route('/news')
#def news():
#    posts = Blog.query.order_by().paginate(per_page=10, page=request.args.get("page", 1, type=int))
#    last_page = int(posts.total / 10 + 1)
#    return render_template('news.html', posts=posts, last_page=last_page, user=user)
