from flask import Flask, render_template, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os # Import os for path handling if needed for db path

# Initialize Flask app and SQLAlchemy DB
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Import models *after* db is initialized to avoid circular imports
from models import User, Message

# Import and register blueprints
from blueprints.auth import auth_bp
from blueprints.main import main_bp
from blueprints.messages import messages_bp

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(messages_bp)

# Context processor to make 'current_user' available in all templates
@app.context_processor
def inject_user():
    current_user = None
    if 'user_id' in session:
        current_user = User.query.get(session['user_id'])
    return dict(current_user=current_user)

# CLI Command to initialize the database
@app.cli.command('init-db')
def init_db_command():
    """Clear existing data and create new tables."""
    with app.app_context():
        db.drop_all() # Optional: To clear old data, remove if you want to keep data
        db.create_all()
        print('Initialized the database.')

# Custom error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # This block runs the application directly.
    # For initial database setup, you should run `flask init-db` once.
    # db.create_all() is called by the init-db command.
    app.run(debug=True)
