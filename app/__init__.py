from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from conf import config_types

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app(config="dev"):
    app = Flask(__name__)
    app.config.from_object(config_types[config])

    db.init_app(app)

    from .gallery import main, auth_flask_login
    app.register_blueprint(main)
    app.register_blueprint(auth_flask_login)

    login_manager.init_app(app)
    global bcrypt
    bcrypt = Bcrypt(app)

    with app.app_context():
        db.drop_all()
        db.create_all()

    return app


