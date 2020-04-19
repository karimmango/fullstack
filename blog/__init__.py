from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from blog.helpers import salting
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, LoginManager, UserMixin, logout_user
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand




app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://baf5f9532c112a:3706b1a5@eu-cdbr-west-02.cleardb.net/heroku_f500c00e9456035'#database link
engine = create_engine('mysql://baf5f9532c112a:3706b1a5@eu-cdbr-west-02.cleardb.net/heroku_f500c00e9456035')
connection= engine.raw_connection()
cursor= connection.cursor()
db=SQLAlchemy(app)
login_manager= LoginManager(app)

migrate= Migrate(app, db)
manager= Manager(app)

manager.add_command('db', MigrateCommand)

bcrypt=Bcrypt(app)

from blog import routes