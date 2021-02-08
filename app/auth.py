from flask import (Blueprint, flash, g, render_template, request, url_for, redirect)

from flask_login import current_user, login_required, login_user, logout_user, login_manager
from app.database import db
from app.models.user import User
from app.forms.user_form import Register, Login

user_bp = Blueprint('user', __name__)


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form = Register()

        # if form is validate
        if form.validate_on_submit():
            new_user = User(email=form.email.data, password=form.password.data)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('user.login'))

    return render_template('/register.html')


@user_bp.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        form = Login()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data)
            if user is None:
                flash('User Not found')
                return redirect('user.login')
            else:
                if user.password == form.password.data:
                    login_user(user)
                    return redirect(url_for('card.index'))
                else:
                    flash('User Not found')
                    return redirect('user.login')

    return render_template('/login.html')


@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('user.login')
