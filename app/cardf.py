from flask import (Blueprint, flash, render_template, request, url_for, abort, redirect, request)
from flask_login import login_required, current_user

from datetime import datetime
from .models import db
from app.schema.card import CardSchema
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
    return render_template('/index.html', topic=topic, dif_tops=dif_tops, question=question, card_id=card_id, \
                           total_cards=total_cards)


@card_bp.route('/create_card', methods=('GET', 'POST'))
@login_required
def create_card():

    if request.method == 'POST':
        card_schema = CardSchema(topic=request.form['topic'], question=request.form['question'], typ=request.form['typ'])
        if card_schema.validate_form():
            new_card = Cards(topic=card_schema.topic, question=card_schema.topic, author=current_user, \
                             typ=card_schema.typ)
            db.session.add(new_card)
            db.session.commit()
            return redirect(url_for('cards.index'))
        else:
            return 'Invalid form', 400

    return render_template('/create_card.html')


def get_post(id):
    card = Cards.query.filter_by(id=id).first()

    if card is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    return card


@card_bp.route('/cards/<string:card_type>')
@card_bp.route('/cards')
@login_required
def show_cards(card_type=None):
    user = User.query.filter_by(id=current_user.id).first()
    cards = user.cards.all()
    card_view = []
    for card in cards:
        if card_type is None:
            card_view.append([card.id, card.topic, card.question])
        else:
            if card.typ == card_type:
                card_view.append([card.id, card.topic, card.question, card.typ])

    # going to return all cards info
    return render_template('show_cards.html', cards=card_view)


@card_bp.route('/<int:card_id>/update', methods=('GET', 'POST'))
@login_required
def update_card(card_id=None):
    card = get_post(card_id)
    if card is None:
        return 'Card Not found', 400
    if request.method == 'POST':
        card_schema = CardSchema(request.form['topic'], request.form['question'], request.form['typ'])
        if card_schema.validate_form():
            card.topic = card_schema.topic
            card.question = card_schema.question
            card.typ = card_schema.typ
            card.updated_time = datetime.utcnow()
            db.session.commit()
            return redirect(url_for('cards.index'))
        else:
            return "Invalid form", 400

    return render_template('/create_card.html', topic=card.topic, question=card.question, typ=card.typ)


# TO-DO: use POST method
@card_bp.route('/<int:card_id>/delete', methods=['GET'])
@login_required
def delete_card(card_id=None):
    card = get_post(card_id)
    if card is None:
        return 'Card Not found', 400
    db.session.delete(card)
    db.session.commit()
    return redirect(url_for('cards.show_cards'))
