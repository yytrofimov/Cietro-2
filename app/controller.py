from lib import mail_generator
from app import app, mail
from flask import redirect, flash, render_template, session, request, url_for
from models import *


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        if request.form['submit-button'] == 'login-button':
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.login(email=email, password=password)
            login(user.id)
            return after_login_redirect()
    else:
        if 'admin_id' in session or 'user_id' in session:
            return after_login_redirect()
        return render_template('login.html')


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        if request.form['submit-button'] == 'register-button':
            first_name = request.form.get('firstname')
            last_name = request.form.get('lastname')
            email = request.form.get('email')
            password = request.form.get('password')
            company_id = int(request.form.get('companyid'))
            user = User.register(first_name=first_name, last_name=last_name,
                                 email=email, password=password, company_id=company_id, status=1)
            login(user.id)
            return after_login_redirect()
    else:
        return render_template('register.html')


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == "GET":
        return render_template('forgot_password.html')
    else:
        email = request.form.get('email')
        if PasswordReset.check_attempts_by_email(email):
            raise e.TokenIsAlreadyRequested
        PasswordReset.save_user_email(email)
        try:
            user = User.get(email=email)
            msg = mail_generator.get_password_reset_email(
                token=PasswordReset.get_user_token(id=user.id),
                recipient_email=user.email)
            mail.send(msg)
        except e.UserDoesntExist:
            pass
        flash(
            'Jos tähän sähköpostiosoitteeseen on rekisteröity tili, lähetämme sähköpostin nollattavaksi')
        return redirect(url_for('forgot_password'))


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = PasswordReset.verify_user_token(token)
    if request.method == "GET":
        return render_template('reset_password.html')
    else:
        password = request.form.get('password')
        user.set_password(new_password=password)
        logout()
        flash('Salasanasi on palautettu!')
        PasswordReset.delete_user_token(token)
        return redirect(url_for('login'))


@app.route('/profile', methods=['POST', 'GET'])
def profile():
    if request.method == "GET":
        if 'admin_id' in session:
            return redirect(url_for('company'))
        if 'user_id' not in session:
            return redirect(url_for('login'))
        user = User.get(id=session['user_id'])
        company = Company.get(id=user.company_id)
        render_data = {
            'user_id': user.id,
            'user_first_name': user.first_name,
            'user_last_name': user.last_name,
            'user_items': user.items,
            'user_email': user.email,
            'company_name': company.name,
            'company_items': company.items,
        }
        return render_template('profile.html', **render_data)
    else:
        if request.form['submit-button'] == 'logout-button':
            logout()
        if request.form['submit-button'] == 'deactivateitem-button':
            item_id = int(request.form.get('itemid'))
            item = Item.get(item_id)
            item.deactivate(session['user_id'])
        if request.form['submit-button'] == 'activateitem-button':
            item_id = int(request.form.get('itemid'))
            activation_code = request.form.get('activationcode')
            item = Item.get(item_id)
            item.activate(
                user_id=session['user_id'], activation_code=activation_code)
        return redirect(url_for('profile'))


@app.route('/company_register', methods=['POST', 'GET'])
def company_register():
    if request.method == "POST":
        if request.form['submit-button'] == 'register-button':
            company_name = request.form.get('companyname')
            company_address = request.form.get('companyaddress')
            company_reg_number = request.form.get('companyregnumber')
            invite_code = request.form.get('invitecode')

            first_name = request.form.get('firstname')
            last_name = request.form.get('lastname')
            email = request.form.get('email')
            password = request.form.get('password')
            Company.validate_attrs(
                reg_number=company_reg_number, invite_code=invite_code)

            User.validate_attrs(email=email)
            company = Company.register(name=company_name, address=company_address,
                                       reg_number=company_reg_number, invite_code=invite_code)
            admin = User.register(first_name=first_name, last_name=last_name,
                                  email=email, password=password, company_id=company.id, status=1)
            company.set_admin(admin.id)
            login(admin.id)
            return after_login_redirect()
    else:
        return render_template('company_register.html')


@app.route('/company', methods=['POST', 'GET'])
def company():
    if request.method == "GET":
        if "admin_id" not in session:
            return redirect(url_for('login'))
        admin = User.get(id=session['admin_id'])
        company = Company.get(id=admin.company_id)
        render_data = {
            'admin_id': admin.id,
            'company_name': company.name,
            'company_id': company.id,
            'company_address': company.address,
            'company_reg_number': company.reg_number,
            'company_items': company.items,
            'company_total_items': len(company.items)
        }
        return render_template('company.html', **render_data)
    else:
        if request.form['submit-button'] == 'logout-button':
            logout()
        if request.form['submit-button'] == 'additem-button':
            item_name = request.form.get('itemname')
            item = Item.add(name=item_name, company_id=User.get(id=session['admin_id']).company_id)
            msg = mail_generator.get_add_item_email(
                item, User.get(id=session['admin_id']).email)
            mail.send(msg)
        if request.form['submit-button'] == 'deleteitem-button':
            item_id = int(request.form.get('itemid'))
            Item.delete(id=int(item_id))
        return redirect(url_for('company'))


@app.route('/faq')
def faq():
    return render_template('faq.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/privacy')
def privacy():
    return render_template('privacy.html')


@app.route('/feedback')
def feedback():
    return render_template('feedback.html')


def login(id: int):
    user = User.get(id=id)
    if user:
        company = Company.get(id=user.company_id)
        if user.id == company.admin_id:
            session['admin_id'] = id
        else:
            session['user_id'] = id
            if 'admin_id' in session:
                session.pop('admin_id')


def logout():
    if 'admin_id' in session:
        session.pop('admin_id')
    if 'user_id' in session:
        session.pop('user_id')


def after_login_redirect():
    if 'user_id' in session:
        return redirect(url_for('profile'))

    elif 'admin_id' in session:
        return redirect(url_for('company'))


@app.before_request
def save_requested_url():
    session['requested_url'] = request.base_url


@app.after_request
def apply_caching(response):
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["HTTP-HEADER"] = "VALUE"
    return response
