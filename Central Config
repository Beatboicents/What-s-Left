import os

class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'whats_left.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret key for session management and form security
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)

    # Optional: Debug mode (set to False in production)
    DEBUG = True
