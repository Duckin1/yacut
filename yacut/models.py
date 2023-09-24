from datetime import datetime

from yacut import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column()
    short = db.Column()
    timestamp = db.Column(db.String(256))
