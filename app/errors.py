from flask import redirect, flash, render_template, session, url_for
from app import app
import exceptions as e
from flask_wtf.csrf import CSRFError
from lib.types_checker import WrongType


@app.errorhandler(404)
def handle_404(e):
    return render_template('errors/error_404.html'), 404


@app.errorhandler(CSRFError)
def handle_csrf(e):
    return render_template('errors/error_404.html')


@app.errorhandler(e.UserDoesntExist)
def handle_user_doesnt_exist(e):
    flash('Käyttäjää ei ole olemassa')
    return redirect(session['requested_url'])


@app.errorhandler(e.PasswordIsIncorrect)
def handle_password_is_incorrect(e):
    flash('Väärä salasana')
    return redirect(session['requested_url'])


@app.errorhandler(e.UserIsBlocked)
def handle_user_is_blocked(e):
    flash('Tili on estetty')
    return redirect(session['requested_url'])


@app.errorhandler(e.CompanyDoesntExist)
def handle_company_doesnt_exist(e):
    flash('Tällaista yritystä ei ole rekisteröity')
    return redirect(session['requested_url'])


@app.errorhandler(e.TokenExpired)
def handle_token_expired(e):
    flash('Tunnus vanhentunut')
    return redirect(url_for('forgot_password'))


@app.errorhandler(e.TokenIsIncorrect)
def handle_token_is_incorrect(e):
    flash('Virheellinen merkki')
    return redirect(url_for('forgot_password'))


@app.errorhandler(e.TokenIsAlreadyRequested)
def handle_token_is_already_requested(e):
    flash('Olet jo pyytänyt! Tarkista saapuneet. Pyyntö voidaan lähettää 5 minuutin välein')
    return redirect(url_for('forgot_password'))


@app.errorhandler(e.NoEnoughRights)
def handle_no_enough_rights(e):
    flash('Ei oikeuksia')
    return redirect(session['requested_url'])


@app.errorhandler(e.ItemNotInUse)
def handle_item_not_in_use(e):
    flash('Tuote ei ole käytössä! Käytä vain sitä')
    return redirect(session['requested_url'])


@app.errorhandler(e.ItemInUse)
def handle_item_in_use(e):
    flash('Tuote käytössä')
    return redirect(session['requested_url'])


@app.errorhandler(e.ActivationCodeIsIncorrect)
def handle_activation_code_in_incorrect(e):
    flash('Väärä aktivointikoodi')
    return redirect(session['requested_url'])


@app.errorhandler(e.CompanyExists)
def handle_company_exists(e):
    flash('Yritys on jo rekisteröity')
    return redirect(session['requested_url'])


@app.errorhandler(e.InviteCodeIsIncorrect)
def handle_invite_code_is_incorrect(e):
    flash('Virheellinen kutsukoodi')
    return redirect(session['requested_url'])


@app.errorhandler(e.ItemDoesntExist)
def handle_item_doesnt_exist(e):
    flash('Kohdetta ei ole olemassa')
    return redirect(session['requested_url'])


@app.errorhandler(WrongType)
def handle_wrong_type(e):
    flash('Syötetty virheellisiä tietoja')
    return redirect(session['requested_url'])
