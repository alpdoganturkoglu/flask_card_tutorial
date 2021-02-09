from flask import (Blueprint, flash, render_template, request, url_for, abort, redirect)
from flask_login import login_required, current_user

from datetime import datetime
from app.server import db
from app.models.user import User
from app.models.card import Cards

card_bp = Blueprint('cards', __name__)


@card_bp.route('/')
@login_required
def index():

    # gets user info
    user = User.query.filter_by(id=current_user.id)
    return render_template('/index.html')


@card_bp.route('/create_card', methods=('GET', 'POST'))
@login_required
def create_card():
    if request.method == 'POST':
        topic = request.form.get('topic')
        question = request.form.get('question')
        error = None

        if not topic or not question:
            error = 'topic or question cannot be empty'
        if error is not None:
            flash(error)

        new_card = Cards(topic=topic, question=question)
        db.session.add(new_card)
        db.session.commit()
        return redirect('cards.index')
    return render_template('/create_card.html')


def get_post(id):
    card = Cards.query.filter_by(id=id).first()

    if card is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    return card


@card_bp.route('/<int:card_id>/update', methods=('GET', 'POST'))
@login_required
def update_card(card_id=None):
    if card := Cards.query.filter_by(id=card_id) is None:
        flash('ID CANNOT BE NULL')

    if request.method == 'POST':
        topic = request.form.get('topic')
        question = request.form.get('question')
        error = None
        if not topic or not question:
            error = 'topic or question cannot be empty'
        if error is not None:
            flash(error)

        card.topic = topic
        card.question = question
        card.updated_time = datetime.utcnow()
        db.session.commit()
        return render_template('/index.html')
    return render_template('/update.html', card=card)


@card_bp.route('/<int:card_id>/delete', methods=('GET', 'POST'))
@login_required
def delete_card(card_id=None):
    if card := get_post(card_id) is None:
        flash('ID CANNOT BE NULL')
    db.session.delete(card)
    db.session.commit()
    return redirect(url_for('blog.index'))
