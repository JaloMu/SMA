from .. import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    user = db.relationship('Users', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = ('User', 'Admin', 'Super')
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class Sections(db.Model):
    __tablename__ = 'sections'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    comment = db.Column(db.String(128), nullable=True)
    user = db.relationship('Users', backref='section', lazy='dynamic')
    team = db.relationship('Teams', backref='section', lazy='dynamic')


class Teams(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    comment = db.Column(db.String(128), nullable=True)
    sections_id = db.Column(db.Integer, db.ForeignKey('sections.id'), nullable=False)
    user = db.relationship('Users', backref='team', lazy='dynamic')


class UserGroups(db.Model):
    __tablename__ = 'usergroups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    comment = db.Column(db.String(128), nullable=True)
    user = db.relationship('Users', backref='usergroup', lazy='dynamic')


class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    uuid = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(64), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(11), unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    position = db.Column(db.String(64))
    ssh_key_pwd = db.Column(db.String(128))
    last_login = db.Column(db.DateTime, nullable=False, default=datetime.now())
    is_active = db.Column(db.Boolean, default=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), default=1, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('usergroups.id'))
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    create_user = db.Column(db.String(64), nullable=False, server_default="sma")
    updata_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updata_user = db.Column(db.String(64), nullable=False, server_default="sma")

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def reset_password(self, new_password):
        self.password = new_password
        db.session.add(self)
        db.session.commit()
        return True

    def __repr__(self):
        return '<User %r>' % self.username

    def __str__(self):
        return self.__repr__()


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
