from flask import Flask
from config import config_types
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():
	app = Flask(__name__)
	app.config.from_object(config_types["dev"])
	
	db.init_app(app)
	
	from .gallery import main
	app.register_blueprint(main)
	
	with app.app_context():
		db.drop_all()
		db.create_all()
		
	return app


