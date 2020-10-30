import re

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
import bcrypt

from .models import User, Games, Picks
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    """
    login: Display the login page

    Returns:
        str: A rendering of login.html
    """
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    """
    login_post: Display the login page after a POST request

    Returns:
        str: A rendering of the home page if successful, or a rendering of the
        login page with a danger flash if the user/pass were incorrect
    """
    email = request.form.get('email')
    password = request.form.get('password').encode('utf-8')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not bcrypt.checkpw(password, user.password):
        flash('Email and password do not match.', 'danger')
        return redirect(
            url_for('auth.login')
        )  # if the user doesn't exist or password is wrong, reload the page

    # successful login: redirect to main.profile
    login_user(user, remember=remember)
    return redirect(url_for('main.index'))


@auth.route('/signup')
def signup():
    """
    signup: Display the signup page

    Returns:
        str: A rendering of the signup page
    """
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    """
    signup_post: Display the signup page after a POST request

    Returns:
        str: The signup page with a flashed message depending on the success of new user creation
    """
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name').strip()
    password = request.form.get('password')

    email_pattern = re.compile('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$')
    valid_email = email_pattern.match(email)
    valid_name = name != '' and len(name) <= 20
    valid_pass = len(password) >= 8

    valid_combo = valid_email and valid_name and valid_pass

    if not valid_combo:
        flash("Couldn't sign up this account for the following reasons:", 'danger')
        if not valid_email:
            flash("Email is invalid.", 'danger')
        if not valid_name:
            flash("Name is invalid. Must be between 1 and 20 characters", 'danger')
        if not valid_pass:
            flash("Password is invalid.", 'danger')
        return redirect(url_for('auth.signup'))

    # check to see if existing user with given email exists in db
    user = User.query.filter_by(email=email).first()

    # if user with same email exists, refresh signup page
    if user:
        flash(
            'An account with this email already exists. Go to the login page to log in.',
            'danger',
        )
        return redirect(url_for('auth.signup'))

    new_user = User(
        email=email,
        name=name,
        password=bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()),
        timezone='US/Pacific',
    )
    db.session.add(new_user)

    # add schedule with all blank picks for new user into Picks table
    games_list = Games.query.all()

    for game in games_list:
        new_empty_pick = Picks(
            user_id=new_user.id,
            name=new_user.name,
            week=game.week,
            game_id=game.game_id,
            game_date='2000-01-01',
            game_time='23:59',
            road_team=game.road_team,
            home_team=game.home_team,
            pick='',
        )
        db.session.add(new_empty_pick)
    db.session.commit()

    # return redirect to a login page so that new user can login
    flash("Successfuly created account. Proceed to login.", 'success')
    return redirect(url_for('auth.signup'))


@auth.route('/logout')
@login_required
def logout():
    """
    logout: Log a user out

    Returns:
        str: A rendering of the home page when not authenticated (links to login/signup)
    """
    logout_user()
    return redirect(url_for('main.index'))
