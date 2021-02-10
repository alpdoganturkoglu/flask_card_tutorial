from flask import (Blueprint, flash, render_template, request, url_for, redirect)

from flask_login import login_required, login_user, logout_user, login_manager
from app.server import db
from app.models.user import User
from app.forms.user_form import RegisterForm, LoginForm
from app.server import login_manager
from werkzeug.security import check_password_hash, generate_password_hash

user_bp = Blueprint('user', __name__)


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            hashed_password = generate_password_hash(form.password.data)
            new_user = User(email=form.email.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('user.login'))
        else:
            flash('Invalid form')

    return render_template('/register.html', form=form)


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is None:
                flash('User Not found')
                return redirect(url_for('user.login'))
            else:
                if check_password_hash(user.password, form.password.data):
                    login_user(user)
                    return redirect(url_for('cards.index'))
                else:
                    flash('Wrong Password')
                    return redirect(url_for('user.login'))

    return render_template('/login.html', form=form)


@login_manager.user_loader
def load_user(id):
    if id is None:
        redirect('user.login')
    user = User.query.filter_by(id=id).first()
    if user:
        return user
    else:
        return None


@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.login'))
