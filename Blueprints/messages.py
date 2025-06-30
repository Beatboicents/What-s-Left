from flask import Blueprint, render_template, redirect, url_for, flash, session, abort, request
from models import User, Message # Will be imported after models.py is created
from forms import MessageForm # Will be imported after forms.py is created
from app import db # Will be imported after app.py is created
from sqlalchemy import or_

messages_bp = Blueprint('messages', __name__, url_prefix='/messages')

@messages_bp.before_request
def require_login():
    if 'user_id' not in session:
        flash("You need to be logged in to access messaging.", 'warning')
        return redirect(url_for('auth.login'))

@messages_bp.route('/send/<int:receiver_id>', methods=['GET', 'POST'])
def send_message(receiver_id):
    sender_id = session['user_id']
    sender = User.query.get(sender_id)
    receiver = User.query.get_or_404(receiver_id)

    if sender.id == receiver.id:
        flash("You cannot send a message to yourself.", 'danger')
        return redirect(url_for('main.home'))

    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(sender_id=sender.id, receiver_id=receiver.id, content=form.content.data)
        db.session.add(msg)
        db.session.commit()
        flash('Message sent!', 'success')
        return redirect(url_for('messages.inbox'))
    
    return render_template('messages/send_message.html', form=form, receiver=receiver)

@messages_bp.route('/inbox')
def inbox():
    user_id = session['user_id']
    user = User.query.get(user_id)

    # Get received messages (where current user is the receiver)
    received_messages = Message.query.filter_by(receiver_id=user_id)\
                                     .order_by(Message.timestamp.desc())\
                                     .all()
    
    # Get sent messages (where current user is the sender)
    sent_messages = Message.query.filter_by(sender_id=user_id)\
                                 .order_by(Message.timestamp.desc())\
                                 .all()

    return render_template('messages/inbox.html', 
                           received_messages=received_messages, 
                           sent_messages=sent_messages, 
                           user=user)

@messages_bp.route('/conversation/<int:other_user_id>')
def conversation(other_user_id):
    user_id = session['user_id']
    other_user = User.query.get_or_404(other_user_id)

    # Query messages between the two users
    messages_between_users = Message.query.filter(
        or_(
            (Message.sender_id == user_id and Message.receiver_id == other_user_id),
            (Message.sender_id == other_user_id and Message.receiver_id == user_id)
        )
    ).order_by(Message.timestamp.asc()).all()

    form = MessageForm() # Form to reply directly from conversation view

    return render_template('messages/conversation.html',
                           messages=messages_between_users,
                           other_user=other_user,
                           form=form)

@messages_bp.route('/reply/<int:other_user_id>', methods=['POST'])
def reply_to_conversation(other_user_id):
    user_id = session['user_id']
    sender = User.query.get(user_id)
    receiver = User.query.get_or_404(other_user_id)

    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(sender_id=sender.id, receiver_id=receiver.id, content=form.content.data)
        db.session.add(msg)
        db.session.commit()
        flash('Reply sent!', 'success')
    else:
        flash('Error sending reply: ' + str(form.errors), 'danger')

    return redirect(url_for('messages.conversation', other_user_id=other_user_id))
