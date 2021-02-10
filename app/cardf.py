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
    cards_topics = [card.topic for card in cards]
    dif_tops = len(set(cards_topics))
    if len(cards) > 0:
        random_card = random.choice(cards)
        topic = random_card.topic
        question = random_card.question
        card_id = random_card.id
        dif_tops = dif_tops
        total_cards = len(cards)
    else:
        topic = ""
        question = ""
        card_id = 0
        dif_tops = 0
        total_cards = 0
    return render_template('/index.html', topic=topic,dif_tops=dif_tops, question=question, card_id=card_id, \
                           total_cards=total_cards)


@card_bp.route('/create_card', methods=('GET', 'POST'))
@login_required
def create_card():
    user = User.query.filter_by(id=current_user.id).first()
    form = CardForm()
    if request.method == 'POST':
        if form.validate_on_submit():

            new_card = Cards(topic=form.topic.data, question=form.question.data, author=user, typ=form.typ.data)
            db.session.add(new_card)
            db.session.commit()
            return redirect(url_for('cards.index'))
        else:
            flash('invalid form')

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
    card_view = []
    for card in cards:
        card_view.append([card.id, card.topic, card.question])
    # going to return all cards info
    return render_template('show_cards.html', cards=card_view)


@card_bp.route('/<int:card_id>/update', methods=('GET', 'POST'))
@login_required
def update_card(card_id=None):
    card = Cards.query.filter_by(id=card_id).first()
    if card is None:
        flash('Card not found')
    form = CardForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            card.topic = form.topic.data
            card.question = form.question.data
            card.typ = form.typ.data
            card.updated_time = datetime.utcnow()
            db.session.commit()
            return redirect(url_for('cards.index'))
        else:
            flash('invalid form')

    return render_template('/create_card.html', form=form, topic=card.topic, question=card.question, typ=card.typ)


@card_bp.route('/<int:card_id>/delete', methods=('GET', 'POST'))
@login_required
def delete_card(card_id=None):
    card = get_post(card_id)
    db.session.delete(card)
    db.session.commit()
    return redirect(url_for('cards.index'))
