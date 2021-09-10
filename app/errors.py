from __init__ import *


@app.errorhandler(404)
def handle_404(e):
    return render_template('errors/error_404.html'), 404


@app.errorhandler(CSRFError)
def handle_csrf(e):
    return render_template('errors/error_404.html')


@app.errorhandler(e.UserDoesntExist)
def handle_user_email_doesnt_exist(e):
    flash('TKäyttäjää ei ole olemassa')
    return redirect(session['requested_url'])


@app.errorhandler(e.IncorrectPassword)
def handle_user_incorrect_password(e):
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
    return redirect(session['requested_url'])


@app.errorhandler(e.IncorrectToken)
def handle_incorrect_token(e):
    flash('Virheellinen merkki')
    return redirect(session['requested_url'])


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


@app.errorhandler(e.IncorrectActivationCode)
def handle_incorrect_activation_code(e):
    flash('Väärä aktivointikoodi')
    return redirect(session['requested_url'])


@app.errorhandler(e.CompanyExists)
def handle_company_exists(e):
    flash('Yritys on jo rekisteröity')
    return redirect(session['requested_url'])


@app.errorhandler(e.IncorrectInviteCode)
def handle_incorrect_invite_code(e):
    flash('Virheellinen kutsukoodi')
    return redirect(session['requested_url'])


@app.errorhandler(e.ItemDoesntExist)
def handle_item_doesnt_exist(e):
    flash('Kohdetta ei ole olemassa')
    return redirect(session['requested_url'])


@app.errorhandler(e.WrongType)
def handle_item_doesnt_exist(e):
    flash('Syötetty virheellisiä tietoja')
    return redirect(session['requested_url'])
