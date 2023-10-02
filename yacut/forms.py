from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import CUSTOM_ID_REGEX


class URLForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = StringField(
        'Ваш вариант конца ссылки',
        validators=[
            Length(max=16),
            Optional(),
            Regexp(CUSTOM_ID_REGEX, message='Указано недопустимое имя для короткой ссылки')
        ]
    )
    submit = SubmitField('Создать')
