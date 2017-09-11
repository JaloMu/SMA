from .. import db


class Zones(db.Model):
    __tablename__ = 'zones'
    id = db.Column(db.Integer, primary_key=True)
    zone = db.Column(db.String(255), unique=True, nullable=False, index=True)
    dns = db.relationship('DNS', backref='zone', lazy='dynamic')


class DNS(db.Model):
    __tablename__ = "dns_records"
    id = db.Column(db.Integer, primary_key=True)
    zone_id = db.Column(db.Integer, db.ForeignKey('zones.id'), nullable=False)
    host = db.Column(db.String(255), nullable=False, index=True, server_default="@")
    type = db.Column(db.Enum('A','MX','CNAME','NS','SOA','PTR','TXT','AAAA','SVR','URL'), nullable=False, index=True)
    data = db.Column(db.String(255))
    ttl = db.Column(db.Integer, default=3600)
    mx_priority = db.Column(db.Integer)
    priority = db.Column(db.SmallInteger, nullable=False, default=255)
    refresh = db.Column(db.Integer, nullable=False, default=28800)
    retry = db.Column(db.Integer,nullable=False, default=14400)
    expire = db.Column(db.Integer, nullable=False, default=86400)
    minimum = db.Column(db.Integer, nullable=False, default=86400)
    serial = db.Column(db.BigInteger, nullable=False, default=2015050917)
    resp_person = db.Column(db.String(64), nullable=False, server_default="root.opensma.org")
    primary_ns = db.Column(db.String(64), nullable=False, server_default='ns.opensma.org')
