from flask import Flask


#mysql+mysqldb://<user>:<password>@<host>[:<port>]/<dbname>
application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:lornad@localhost:3306/photos'
db = SQLAlchemy(application)



