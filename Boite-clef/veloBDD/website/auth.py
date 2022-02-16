import os
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)
hash_method = os.getenv('HASH_METHOD')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if User.query.count() == 0:
        # S'il n'existe pas d'utilisateurs on réinitialise la base
        init()
    if request.method == 'POST':
        nom = request.form.get('nom')
        password = request.form.get('password')

        user = User.query.filter_by(nom=nom).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash("Vous n'avez pas de compte", category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':

        nom = request.form.get('nom')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(nom=nom).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(nom) < 4:
            flash('Nom trop court', category='error')

        elif password1 != password2:
            flash('Les mots de passes sont différents', category='error')
        elif len(password1) < 7:
            flash('Mot de passe trop court', category='error')
        else:
            new_user = User(nom=nom,
                            password=generate_password_hash(
                                password1, method=hash_method),
                            est_admin=False)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)


def init():
    from .models import Velo, User
    from werkzeug.security import generate_password_hash
    velo1 = Velo(numero=1, estPris=False)
    db.session.add(velo1)
    velo2 = Velo(numero=2, estPris=False)
    db.session.add(velo2)
    velo3 = Velo(numero=3, estPris=False)
    db.session.add(velo3)
    velo4 = Velo(numero=4, estPris=False)
    db.session.add(velo4)
    velo5 = Velo(numero=5, estPris=False)
    db.session.add(velo5)
    admin_name = os.getenv('ADMIN_NAME')
    admin_pwd = os.getenv('ADMIN_PWD')
    db.session.add(User(nom=admin_name,
                        password=generate_password_hash(
                            admin_pwd, method=hash_method),
                        est_admin=True))
    db.session.commit()
    print("Entries created")
