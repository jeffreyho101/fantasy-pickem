import re

from flask import Blueprint, render_template, redirect, url_for, request, flash
import bcrypt

from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name').strip()
    password = request.form.get('password')

    email_pattern = re.compile('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$')
    valid_email = email_pattern.match(email)
    valid_name = name != ''
    valid_pass = password != ''

    valid_combo = valid_email and valid_name and valid_pass
    # TODO: check for valid password being 8+ chars, etc...??
    if not valid_combo:
        flash("Couldn't sign up this account for the following reasons:")
        if not valid_email:
            flash("Email is invalid.")
        if not valid_name:
            flash("Name is invalid.")
        if not valid_pass:
            flash("Password is invalid.")
        return redirect(url_for('auth.signup'))

    # check to see if existing user with given email exists in db
    user = User.query.filter_by(email=email).first()

    # if user exists, refresh signup page
    # TODO: throw an error popup saying that an email already exists for this user
    if user:
        flash(
            'An account with this email already exists. Go to the login page to log in.'
        )
        return redirect(url_for('auth.signup'))

    new_user = User(
        email=email,
        name=name,
        password=bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()),
    )
    db.session.add(new_user)
    db.session.commit()

    # TODO: throw popup printing successful account made

    # return redirect to a login page so that new user can login
    flash("Successfuly created account. Proceed to login.")
    return redirect(url_for('auth.signup'))


@auth.route('/logout')
def logout():
    return 'Logout'
