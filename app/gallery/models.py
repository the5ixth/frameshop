from .. import db


class Photo(db.Model):
	__tablename__='photos'
	id = db.Column(db.Integer, primary_key=True)
	imgfilename = db.Column(db.String(50))
	title = db.Column(db.String(50))
	comment = db.Column(db.Text)
	price = db.Column(db.Integer, default=0)
	artist = db.Column(db.String(50), default="")
	
	
def get_page(pagenum):

	return photos
	
def get_image(imagenum):
	image = Photo.query.filter_by(id=imagenum).first()
	return image

def insert(obj):
	db.session.add(obj)
	db.session.commit()	
	return 0

def get_last():
	last = Photo.query.order_by(Photo.id.desc()).first()
	return last.id
	
def count():
	count = Photo.query.count()
	return count
