from .. import db
from datetime import datetime


class IDC(db.Model):
    __tablename__ = 'idces'
    id = db.Column(db.Integer, primary_key=True)
    idcName = db.Column(db.String(64), unique=True, nullable=False, index=True)
    address = db.Column(db.String(256), nullable=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    duty_calls = db.Column(db.String(11), unique=True, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    bandwidth = db.Column(db.Integer, nullable=True)
    cobinet = db.relationship('Cobinetes', backref='idces', lazy='dynamic')

    def __repr__(self):
        return '<IDC %r>' % self.idcName

    def __str__(self):
        return self.__repr__()


class Cobinetes(db.Model):
    __tablename__ = "cobinetes"
    id = db.Column(db.Integer, primary_key=True)
    cobName = db.Column(db.String(64), unique=True, nullable=False, index=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    term = db.Column(db.Integer, nullable=False)
    idc_id = db.Column(db.Integer, db.ForeignKey('idces.id'), nullable=False)
    comment = db.Column(db.String(128), nullable=True)
    server = db.relationship('Equipmentes', backref='cobinet', lazy='dynamic')

    def __repr__(self):
        return '<Cobinetes %r>' % self.cobName

    def __str__(self):
        return self.__repr__()


class Equipmentes(db.Model):
    __tablename__ = 'equipmentes'
    id = db.Column(db.Integer, primary_key=True)
    vendor = db.Column(db.String(64), unique=True, nullable=False, index=True)
    model = db.Column(db.String(64), unique=True, nullable=False, index=True)
    sn = db.Column(db.Integer, nullable=False, unique=True)
    cob_id = db.Column(db.Integer, db.ForeignKey('cobinetes.id'), nullable=False)

    def __repr__(self):
        return '<Equipmentes {} - {}>'.format(self.vendor, self.model)

    def __str__(self):
        return self.__repr__()
