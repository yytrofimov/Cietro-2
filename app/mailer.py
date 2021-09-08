from __init__ import *


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    msg = Message('CIERTO-2: Nollaa salasana',
               sender="yytrofimov@yandex.ru",
               recipients=[user.email])
    msg.body = render_template('emails/password_reset.txt',
                                         user=user, token=token)
    msg.html = render_template('emails/password_reset.html',
                                         user=user, token=token)
    mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def send_add_item_email(item, recipient_email: str):
    qr_code = qr.make_qr(item.activation_code)
    current_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    msg = Message(subject='CIERTO-2: Kohde lisätty',
                  sender='yytrofimov@yandex.ru',
                  recipients=[recipient_email])
    msg.body = render_template(
        'emails/add_item.txt', current_time=current_time, item=item)
    msg.html = render_template('emails/add_item.html', current_time=current_time, item=item)
    msg.attach('QR', "image/png", qr_code)
    mail.send(msg)
