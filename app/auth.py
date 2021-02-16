from flask import (Blueprint, flash, render_template, request, url_for, redirect)
from flask_login import login_required, login_user, logout_user, LoginManager
from .models import db
from .models.user import User
from app.forms.user_form import RegisterForm, LoginForm

user_bp = Blueprint('user', __name__)
login_manager = LoginManager()


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User.register(email=form.email.data, password=form.password.data)
            if new_user is None:
                return 'Server Error', 500
            return redirect(url_for('user.login'))
        else:
            return 'bad request!', 400

    return render_template('/register.html', form=form)


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is None:
                flash('User Not found')
                return redirect(url_for('user.login'),code=400)
            else:
                if user.check_password(form.password.data):
                    login_user(user)
                    return redirect(url_for('cards.index'))
                else:
                    flash('Wrong Password')
                    return redirect(url_for('user.login'), code=400)

    return render_template('/login.html', form=form)


@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.login'))


@login_manager.user_loader
def load_user(id):
    if id is None:
        redirect('user.login')
    user = User.query.filter_by(id=id).first()
    if user:
        return user
    else:
        return None