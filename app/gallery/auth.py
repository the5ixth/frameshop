import os
import time
from werkzeug.utils import secure_filename
from flask import current_app, Blueprint, render_template, abort, request, flash, redirect, url_for
from .. import login_manager, bcrypt
from .forms import LoginForm, UploadForm, SignupForm, EditForm
from flask_login import current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required

from .models import User, Photo

from .. import db

user = current_user

auth_flask_login = Blueprint('auth_flask_login', __name__, template_folder='templates')


@auth_flask_login.route('/register', methods=["GET", "POST"])
def register():
    form = SignupForm()
    if form.validate_on_submit():
        userdb = User()
        form.populate_obj(userdb)
        pw_hash = bcrypt.generate_password_hash(form.password.data)
        userdb.password = pw_hash
        db.session.add(userdb)
        db.session.commit()
        return redirect(url_for('auth_flask_login.login'))
    return render_template('register.html', form=form, user=user)


@auth_flask_login.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usr = User.query.get(form.email.data)
        if usr:
            if bcrypt.check_password_hash(usr.password, form.password.data):
                usr.authenticated = True
                db.session.add(usr)
                db.session.commit()
                login_user(usr, remember=True)
                return redirect(url_for('auth_flask_login.upload'))
    return render_template("login.html", form=form, user=user)


@auth_flask_login.route("/logout", methods=["GET"])
@login_required
def logout():
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('main.about'))


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')


@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve
    """
    return User.query.get(user_id)


@auth_flask_login.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        ph = Photo()
        form.populate_obj(ph)
        filename = time.strftime("%y%j") + "_" + time.strftime("%d%H%S") + \
                   "_" + secure_filename(ph.imgfile.filename[-5:])
        ph.imgfilename = filename
        form.imgfile.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'],
                                            filename))
        db.session.add(ph)
        db.session.commit()
        return redirect(url_for("auth_flask_login.upload"))
    return render_template("upload.html", form=form, user=user)


@auth_flask_login.route('/delete/image/<int:num>')
@login_required
def delete(num):
    ph = Photo.query.get(num)
    db.session.delete(ph)
    db.session.commit()
    return redirect(url_for('main.about'))


@auth_flask_login.route('/edit/image/<int:num>', methods={'GET', 'POST'})
@login_required
def edit(num):
    photo = Photo.query.get(num)
    form = EditForm()
    if form.validate_on_submit():
        ph = Photo().query.get(num)
        form.populate_obj(ph)
        db.session.add(ph)
        db.session.commit()
        return redirect(url_for("main.about"))
    return render_template("edit.html", photo=photo, form=form, user=user)
