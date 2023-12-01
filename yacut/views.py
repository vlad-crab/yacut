from flask import abort, flash, redirect, render_template

from . import app, db
from .forms import LinkForm
from .models import URLMap
from .api_views import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = LinkForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if custom_id and URLMap.query.filter_by(short=custom_id).first():
            flash('Предложенный вариант короткой ссылки уже существует.', 'error')
            return render_template('index.html', form=form)
        urlmap = URLMap(
            short=form.custom_id.data or get_unique_short_id(6),
            original=form.original_link.data
        )
        db.session.add(urlmap)
        db.session.commit()
        flash('Ваша новая ссылка готова', 'success')
        flash(f'{urlmap.short}', 'url')
        return render_template('index.html', form=form)
    return render_template('index.html', form=form)


@app.route('/<string:url>', methods=['GET'])
def redirect_to_original(url):
    original_url = URLMap.query.filter_by(short=url).first()
    if original_url is None:
        abort(404)
    return redirect(original_url.original)
