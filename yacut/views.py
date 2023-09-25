import csv
from datetime import datetime
from random import randrange

import click
from flask import Flask, abort, flash, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'SECRET KEY'

db = SQLAlchemy(app)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256))
    short = db.Column(db.String(16), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=BASE_URL + self.short,
        )

    def from_dict(self, data):
        setattr(self, 'original', data['url'])
        setattr(self, 'short', data['custom_id'])


class URLForm(FlaskForm):
    original_link = StringField('Original Link', validators=[URL()])
    custom_id = StringField('Custom Short ID', validators=[Length(max=16)])
    submit = SubmitField('Shorten URL')


@app.route('/')
def index_view():
    quantity = yacut.query.count()
    if not quantity:
        abort(404)
    offset_value = randrange(quantity)
    opinion = yacut.query.offset(offset_value).first()
    return render_template('index.html', opinion=opinion)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run()
