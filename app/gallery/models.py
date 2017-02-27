from .. import db


class Photo(db.Model):
    __tablename__ = 'photos'
    id = db.Column(db.Integer, primary_key=True)
    imgfilename = db.Column(db.String(128))
    title = db.Column(db.String(50))
    comment = db.Column(db.Text)
    price = db.Column(db.Integer, default=0)
    artist = db.Column(db.String(50), default="")


class Blog(db.Model):
    __tablename__ = 'blog'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text)
    date = db.Column(db.String(50))


class Description(db.Model):
    __tablename__='description'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)


class User(db.Model):
    """An admin user capable of viewing reports.

    :param str email: email address of user
    :param str password: encrypted password for the user

    """
    __tablename__ = 'user'

    email = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(100))
    authenticated = db.Column(db.Boolean, default=False)
    error = db.Column(db.String(15))

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False



	
