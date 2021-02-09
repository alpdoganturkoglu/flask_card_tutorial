from flask import (Blueprint, flash, render_template, request, url_for, abort, redirect)
from flask_login import login_required, current_user

from datetime import datetime
from app.server import db
from app.forms.card_form import CardForm
import random
from app.models.user import User
from app.models.card import Cards

card_bp = Blueprint('cards', __name__)


@card_bp.route('/')
@login_required
def index():

    # gets user info
    user = User.query.filter_by(id=current_user.id).first()
    cards = user.cards.all()
    if len(cards)>0:
        random_card = random.choice(cards)
        topic = random_card.topic
        question = random_card.question
        card_id = random_card.id
    else:
        topic = ""
        question = ""
        card_id = 0
    return render_template('/index.html', topic=topic, question=question, card_id=card_id)


@card_bp.route('/create_card', methods=('GET', 'POST'))
@login_required
def create_card():
    user = User.query.filter_by(id=current_user.id).first()
    form = CardForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            topic = request.form.get('topic')
            question = request.form.get('question')
            error = None

            if not topic or not question:
                error = 'topic or question cannot be empty'
            if error is not None:
                flash(error)

            new_card = Cards(topic=form.topic.data, question=form.topic.data, author=user)
            db.session.add(new_card)
            db.session.commit()
            return redirect(url_for('cards.index'))

    return render_template('/create_card.html', form=form)


def get_post(id):
    card = Cards.query.filter_by(id=id).first()

    if card is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    return card

@card_bp.route('/cards')
@login_required
def show_cards(card_id=None):
    user = User.query.filter_by(id=current_user.id).first()
    cards = user.cards.all()

    # going to return all cards info
    return cards

@card_bp.route('/<int:card_id>/update', methods=('GET', 'POST'))
@login_required
def update_card(card_id=None):
    if card := Cards.query.filter_by(id=card_id) is None:
        flash('Card not found')

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
        flash('Card not found')
    db.session.delete(card)
    db.session.commit()
    return redirect(url_for('blog.index'))
