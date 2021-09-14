from flask import render_template
from flask_mail import Message
from app.lib import qr_generator
from datetime import datetime


def get_password_reset_email(token: str, recipient_email: str):
    msg = Message('CIERTO-2: Nollaa salasana',
                  sender="yytrofimov@yandex.ru",
                  recipients=[recipient_email])
    msg.body = render_template('emails/password_reset.txt', token=token)
    msg.html = render_template('emails/password_reset.html', token=token)
    return msg


def get_email(subject: str, sender: str, recipients: list, text_body: str, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    return msg


def get_add_item_email(item, recipient_email: str):
    qr_code = qr_generator.make_qr(item.activation_code)
    current_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    msg = Message(subject='CIERTO-2: Kohde lisätty',
                  sender='yytrofimov@yandex.ru',
                  recipients=[recipient_email])
    msg.body = render_template(
        'emails/add_item.txt', current_time=current_time, item=item)
    msg.html = render_template('emails/add_item.html', current_time=current_time, item=item)
    msg.attach('QR', "image/png", qr_code)
    return msg
