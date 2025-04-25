from flask import (
    Blueprint, render_template, request, flash, url_for, redirect, current_app
)

import requests

from app.db import get_db

bp = Blueprint('mail', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
def index():
    search = request.args.get('search')
    db, c = get_db()
    if search is None:
        c.execute("SELECT * FROM email")
    else:
        c.execute("SELECT * FROM email WHERE content like %s", ('%' + search + '%',))
    mails = c.fetchall()

    return render_template('mails/index.html', mails = mails)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        email = request.form.get('email')
        subject = request.form.get('subject')
        content = request.form.get('content')
        errors = []

        if not email:
            errors.append('Email es obligatorio')
        if not subject:
            errors.append('Asunto es obligatorio')
        if not content:
            errors.append('Contenido es obligatorio')

        if len(errors) == 0:
            send(email, subject, content)
            db , c = get_db()
            c.execute("INSERT INTO email (email, subject, content) VALUES (%s, %s, %s)", (email, subject, content))
            db.commit()

            return redirect(url_for('mail.index'))
        else:
            for error in errors:
                flash(error)
    return render_template('mails/create.html')

def send(to, subject, content):
    api_key = current_app.config['MAILGUN_KEY']
    api_url = current_app.config['MAILGUN_API_URL']
    from_email = current_app.config['FROM_EMAIL']

    resp = requests.post(api_url,auth=('api',api_key),data={'from': from_email, 'to': to, 'subject': subject, 'text': content})
    
    if resp.status_code == 200:
        print('Enviado correctamente')
    else:
        print('Error al enviar correo, razón: ' + resp.text )