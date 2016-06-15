from flask_login import UserMixin

from manage import db


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
    timezone = db.Column()

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

    def __repr__(self):
        return '<Place %r>' % self.name

prices = [5, 13, 19, 27]
