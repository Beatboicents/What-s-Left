from flask import Blueprint, render_template, session, redirect, url_for, flash
from models import User # Will be imported after models.py is created
import random
from forms import EditProfileForm # Will be imported after forms.py is created
from app import db # Will be imported after app.py is created

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/home')
def home():
    users = User.query.all()
    logged_in_user = None
    if 'user_id' in session:
        logged_in_user = User.query.get(session['user_id'])
    return render_template('home.html', users=users, logged_in_user=logged_in_user)

@main_bp.route('/profile/<int:user_id>')
def profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user/profile.html', user=user)

@main_bp.route('/profile/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_profile(user_id):
    if 'user_id' not in session or session['user_id'] != user_id:
        flash("You are not authorized to edit this profile.", 'warning')
        return redirect(url_for('main.home'))

    user = User.query.get_or_404(user_id)
    form = EditProfileForm()

    if form.validate_on_submit():
        user.bio = form.bio.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('main.profile', user_id=user.id))
    elif request.method == 'GET':
        form.bio.data = user.bio
    return render_template('user/edit_profile.html', form=form, user=user)


@main_bp.route('/api/vibe_check/<int:user_id>')
def vibe_check(user_id):
    # This remains an API endpoint, could be integrated into a profile page later
    user = User.query.get(user_id)
    if not user:
        return {'error': 'User not found'}, 404
    vibes = ['🔥 Hot & cold', '💀 Dead convo', '🤷‍♀️ Who even are you?', '🥱 Dry AF', '🎯 Surprisingly good']
    return {'vibe': random.choice(vibes)}
