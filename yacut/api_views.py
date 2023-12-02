import string
from random import sample

from flask import request, jsonify, url_for
from http import HTTPStatus

from . import app, db
from .models import URLMap
from .error_handlers import InvalidAPIUsage

ALPHABET = string.ascii_lowercase + string.ascii_uppercase + string.digits


def get_unique_short_id(length):
    global ALPHABET
    short_id = ''.join(sample(ALPHABET, length))
    short_id_in_db = URLMap.query.filter_by(short=short_id).first()
    while short_id_in_db:
        short_id = ''.join(sample(ALPHABET, length))
        short_id_in_db = URLMap.query.filter(short=short_id).first()
    return short_id


def is_short_id_valid(short_id):
    global ALPHABET
    if not (0 <= len(short_id) <= 16):
        return False
    for symbol in short_id:
        if symbol not in ALPHABET:
            return False
    return True


def validate_api_id_request(data):
    """
    Raises an error if request is Invalid
    Returns custom_id if provided otherwise None
    """
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage(r'"url" является обязательным полем!')
    if 'custom_id' in data:
        urlmap = URLMap.query.filter_by(short=data['custom_id']).first()
        if urlmap:
            raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.')
        if data['custom_id'] and not is_short_id_valid(data['custom_id']):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
        return data['custom_id']


@app.route('/api/id/', methods=['POST'])
def create_shortcut():
    data = request.get_json()

    validate_api_id_request(data)

    unique_short_id = validate_api_id_request(data) or get_unique_short_id(6)

    urlmap = URLMap(
        original=data.get('url'),
        short=unique_short_id
    )
    db.session.add(urlmap)
    db.session.commit()
    return jsonify(
        {
            "url": urlmap.original,
            "short_link": url_for(
                'redirect_to_original', url=urlmap.short, _external=True
            )
        }
    ), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original(short_id):
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if urlmap is None:
        raise InvalidAPIUsage('Указанный id не найден', status_code=HTTPStatus.NOT_FOUND)
    return jsonify({'url': urlmap.original}), HTTPStatus.OK
