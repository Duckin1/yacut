from random import choice
from string import ascii_letters, digits
from datetime import timedelta, datetime

from .models import URLMap
from . import db


def get_unique_short_id():
    letters_digits = ascii_letters + digits
    random_string = ''.join(
        choice(letters_digits) for _ in range(6)
    )
    if URLMap.query.filter_by(short=random_string).first():
        random_string = get_unique_short_id()
    return random_string


def clean_old_records():
    """Удаляет записи старше 30 дней из таблицы в базе данных."""
    cutoff_date = datetime.utcnow() - timedelta(days=30)
    URLMap.query.filter(URLMap.timestamp < cutoff_date).delete()
    db.session.commit()
