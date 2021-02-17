from flask import (Blueprint, flash, render_template, request, url_for, redirect)
from flask_login import login_required, login_user, logout_user, LoginManager, current_user
from .models.user import User
from .schema.user import LoginSchema, RegisterSchema

user_bp = Blueprint('user', __name__)
login_manager = LoginManager()


@user_bp.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        request_form = RegisterSchema(request.form['email'], request.form['password'], request.form['password2'])
        if request_form.validate_register():
            new_user = User.register(email=request.form['email'], password=request.form['password'])
            if new_user is None:
                return 'Server Error', 500
            return redirect(url_for('user.login'))
        else:
            print(request_form.validate_password())
            return 'bad request!', 400

    return render_template('/register.html')


@user_bp.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        login_form = LoginSchema(request.form['email'], request.form['password'])
        if login_form.validate_login():
            user = User.query.filter_by(email=request.form['email']).first()
            if user is None:
                flash('User Not found')
                return redirect(url_for('user.login'), code=400)
            else:
                if user.check_password(request.form['password']):
                    if current_user.is_authenticated:
                        logout_user()
                    login_user(user)
                    return redirect(url_for('cards.index'))
                else:
                    flash('Wrong Password')
                    return redirect(url_for('user.login'), code=400)

    return render_template('/login.html')


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
