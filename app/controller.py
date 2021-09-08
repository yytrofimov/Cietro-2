from __init__ import *
from errors import *
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
            try:
                user = User.login(email=email, password=password)
                login(user.id)
                return after_login_redirect()
            except e.UserEmailDoesntExist:
                flash('Tiliä tällaisella postilla ei ole')
            except e.IncorrectPassword:
                flash('Väärä salasana')
            except e.UserIsBlocked:
                flash('Tili on estetty')
            return (redirect(url_for('login')))
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
            company_id = request.form.get('companyid')
            try:
                user = User.register(first_name=first_name, last_name=last_name,
                                     email=email, password=password, company_id=company_id)
                login(user.id)
                return after_login_redirect()
            except e.UserEmailExists:
                flash('Tällainen posti on jo rekisteröity')
            except e.CompanyDoesntExist:
                flash('Tällaista yritystä ei ole rekisteröity')
            return redirect(url_for('register'))

    else:
        return render_template('register.html')


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == "GET":
        return render_template('forgot_password.html')
    else:
        email = request.form.get('email')
        try:
            mailer.send_password_reset_email(User.get(email=email))
        except e.UserEmailDoesntExist:
            pass
        else:
            flash(
                'Jos tähän sähköpostiosoitteeseen on rekisteröity tili, lähetämme sähköpostin nollattavaksi')
            return redirect(url_for('forgot_password'))


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        user = User.verify_reset_password_token(token)
        session['user_id'] = user.id
    except e.TokenExpired:
        flash('Token expired')
        return redirect(url_for('forgot_password'))
    except e.IncorrectToken:
        flash('Invalid token')
        return redirect(url_for('forgot_password'))
    if request.method == "GET":
        return render_template('reset_password.html')
    else:
        password = request.form.get('password')
        user.set_password(new_password=password)
        logout()
        flash('Salasanasi on palautettu!')
        return redirect(url_for('login'))


@app.route('/profile', methods=['POST', 'GET'])
def profile():
    if 'admin_id' in session:
        return (redirect(url_for('company')))
    if 'user_id' not in session:
        return (redirect(url_for('login')))
    if request.method == "GET":
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
            item_id = request.form.get('itemid')
            item = Item.get(item_id)
            if not item:
                flash('No such item')
                return(redirect(url_for('profile')))
            try:
                item.deactivate(session['user_id'])
            except e.NoEnoughRigths:
                flash('Ei oikeuksia')
                return(redirect(url_for('profile')))
            except e.ItemNotInUse:
                flash('Tuote ei ole käytössä! Käytä vain sitä')
                return(redirect(url_for('profile')))
        if request.form['submit-button'] == 'activateitem-button':
            item_id = request.form.get('itemid')
            activation_code = request.form.get('activationcode')
            item = Item.get(item_id)
            if not item:
                flash('Ei sellaista kohdetta')
                return(redirect(url_for('profile')))
            try:
                item.activate(
                    user_id=session['user_id'], activation_code=activation_code)
            except e.ItemInUse:
                flash('Tuote käytössä')
                return(redirect(url_for('profile')))
            except e.IncorrectActivationCode:
                flash('Väärä aktivointikoodi')
                return(redirect(url_for('profile')))
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
            try:
                Company.validate_attrs(
                    reg_number=company_reg_number, invite_code=invite_code)
            except e.CompanyExists:
                flash('Yritys on jo rekisteröity')
                return redirect(url_for('company_register'))
            except e.IncorrectInviteCode:
                flash('Virheellinen kutsukoodi')
                return redirect(url_for('company_register'))
            try:
                User.validate_attrs(email=email)
            except e.UserEmailExists:
                flash('Tällainen posti on jo rekisteröity')
                return redirect(url_for('company_register'))
            company = Company.register(name=company_name, address=company_address,
                                       reg_number=company_reg_number, invite_code=invite_code)
            admin = User.register(first_name=first_name, last_name=last_name,
                                  email=email, password=password, company_id=company.id)
            company.set_admin(admin.id)
            login(admin.id)
            return after_login_redirect()
    else:
        return render_template('company_register.html')


@app.route('/company', methods=['POST', 'GET'])
def company():
    if "admin_id" not in session:
        return (redirect(url_for('login')))
    if request.method == "GET":
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
            mailer.send_add_item_email(
                item, User.get(id=session['admin_id']).email)

        if request.form['submit-button'] == 'deleteitem-button':
            item_id = request.form.get('itemid')
            try:
                Item.delete(id=item_id)
            except e.ItemDoesntExist:
                flash('Kohdetta ei ole olemassa')
            except e.ItemInUse:
                flash('Tuote käytössä')
                redirect(url_for('company'))
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


@app.route('/generate_invite_code', methods=['POST'])
def generate_invite_code():
    if request.method == "POST":
        code = InviteCode().add_code(
            company_reg_number=request.values['company_reg_number'])
        if code:
            message_subject = "Your invite code"
            message_body = """\
                Company registration number: {},
                Company invitecode: {}""".format(code.company_reg_number, code.code)
            mail.send_a_message(
                request.values['email'], message_body=message_body, message_subject=message_subject)
        return "", 405


def login(id):
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
