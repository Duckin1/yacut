import csv
from datetime import datetime
from random import choice
from string import ascii_letters, digits

import click
from flask import Flask, abort, flash, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional

from yacut import db

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
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'), ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(max=16), Optional()]
    )
    submit = SubmitField('Создать')


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        if not short:
            short = get_unique_short_id()
        elif URLMap.query.filter_by(short=short).first():
            flash(f'Имя {short} уже занято!')
            return render_template('index.html', form=form)
        url_map = URLMap(
            original=form.original_link.data,
            short=short,
        )
        db.session.add(url_map)
        db.session.commit()
        return render_template('index.html', form=form, short=short)
    return render_template('index.html', form=form)


@app.route('/<string:custom_id>')
def redirect_view(custom_id):
    url_map = URLMap.query.filter_by(short=custom_id).first_or_404()
    return redirect(url_map.original)


def get_unique_short_id():
    letters_digits = ascii_letters + digits
    random_string = ''.join(
        choice(letters_digits) for _ in range(6)
    )
    if URLMap.query.filter_by(short=random_string).first():
        random_string = get_unique_short_id()
    return random_string


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run()
