import os

from flask import Flask

def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        FROM_EMAIL=os.environ.get('FROM_EMAIL'),
        MAILGUN_KEY=os.environ.get('MAILGUN_KEY'),
        MAILGUN_API_URL = os.environ.get('MAILGUN_API_URL'),
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        DATABASE_HOST=os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE_PASSWORD=os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE_USER=os.environ.get('FLASK_DATABASE_USER'),
        DATABASE=os.environ.get('FLASK_DATABASE'),
        DATABASE_PORT=os.environ.get('FLASK_DATABASE_PORT')
    )

    from . import db

    db.init_app(app)

    from . import mail

    app.register_blueprint(mail.bp)
    
    return app