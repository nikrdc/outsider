import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager
from flask_script import Manager, Shell, Server
from hashids import Hashids
import sendgrid

from models import db, User, Region, Place
import secrets
from views import index, region

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['DEBUG'] = False
app.config['SECRET_KEY'] = secrets.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db.init_app(app)
migrate = Migrate(app, models.db)
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, User=User, Region=Region, Place=Place)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

# Register blueprints
app.register_blueprint(index.blueprint)
app.register_blueprint(region.blueprint)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

hashids = Hashids(alphabet='abcdefghijklmnopqrstuvwxyz0123456789')
sg = sendgrid.SendGridClient(secrets.SENDGRID_USERNAME, secrets.SENDGRID_PASSWORD)

if __name__ == '__main__':
    manager.run()
