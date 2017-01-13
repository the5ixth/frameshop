from flask import Flask
from flask_sqlalchemy import SQLAlchemy


#mysql+mysqldb://<user>:<password>@<host>[:<port>]/<dbname>
application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:lornad@localhost:3306/photos'
db = SQLAlchemy(application)

class Photo(db.Model):
	__tablename__='photo'
	id = db.Column(db.Integer, primary_key=True)
	image = db.Column(db.String(50))
	title = db.Column(db.String(50))
	comment = db.Column(db.Text)
	price = db.Column(db.Integer)
	artist = db.Column(db.String(50))
	
	def init(self, id, image , title, comment ,price, artist):
		self.id = id
		self.image = image
		self.title = title
		self.comment = comment
		self.price = price
		self.artist = artist
	
	
def get_page(pagenum):
	photos = Photo.query.order_by(Photo.id.desc()).limit(15).offset((pagenum - 1 )* 15).all()
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

