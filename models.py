from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_method

prices = ['Below $5', '$5 to $13', '$13 to $19', '$19 to $27', 'Over $27']

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    __searchable__ = ['name', 'username']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    username = db.Column(db.String(16))
    email = db.Column(db.String(64), unique=True)
    confirmed = db.Column(db.Boolean, default=False)
    time_joined = db.Column(db.DateTime)

    places = db.relationship('Place', backref='creator', lazy='dynamic')

    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True


class Region(db.Model):
    __tablename__ = 'regions'
    __searchable__ = ['name', 'shortname']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    shortname = db.Column(db.String(64), unique=True)
    timezone = db.Column(db.String(32))
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    zoom = db.Column(db.SmallInteger())

    places = db.relationship('Place', backref='region', lazy='dynamic')

    def __repr__(self):
        return '<Region %r>' % self.name


class Place(db.Model):
    __tablename__ = 'places'
    __searchable__ = ['name', 'description']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.Text())
    price_index = db.Column(db.SmallInteger())
    time_created = db.Column(db.DateTime)
    halfhours = db.Column(db.String(336))

    region_id = db.Column(db.Integer, db.ForeignKey('regions.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @hybrid_method
    def open_at(self, local_time):
        index = (local_time.day * 48) + (local_time.hour * 2)
        minute = local_time.minute
        if minute > 20:
            index += 1
        if minute > 50:
            index += 1
        if self.halfhours[index] == '1' and self.halfhours[index+1] == '1':
            return True
        else:
            return False

    def __repr__(self):
        return '<Place %r>' % self.name
