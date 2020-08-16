from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datetime import datetime

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html', current_user=current_user)


@main.route('/profile', endpoint='profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/week_picks', endpoint='week_picks')
@login_required
def standings():
    return render_template('week_picks.html')


@main.route('/standings', endpoint='standings')
@login_required
def standings():
    return render_template('standings.html')

