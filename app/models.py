from __init__ import *
from app.lib import types_checker
from lib.types_checker import check_types
from lib.codes_generator import generate_code

db.metadata.clear()


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.Text())
    last_name = db.Column(db.Text())
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.Text())
    company_id = db.Column(db.Integer())
    status = db.Column(db.Integer())

    @classmethod
    @check_types
    def validate_attrs(cls, email: str = None, company_id: str = None):
        if email and cls.get(email=email):
            raise e.UserEmailExists
        if company_id and not Company.get(id=company_id):
            raise e.CompanyDoesntExist

    @classmethod
    @check_types
    def register(cls, first_name: str, last_name: str, email: str, password: str, company_id: str):
        cls.validate_attrs(email=email, company_id=company_id)
        password = generate_password_hash(password)
        user = cls(first_name=first_name, last_name=last_name,
                   email=email, password=password, company_id=company_id, status=1)
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    @check_types
    def login(cls, email: str, password: str):
        user = cls.get(email=email)
        if not user:
            raise e.UserEmailDoesntExist
        if not check_password_hash(user.password, password):
            raise e.IncorrectPassword
        if not user.status:
            raise e.UserIsBlocked
        return user

    @check_types
    def set_password(self, new_password: str):
        self.password = generate_password_hash(new_password)
        db.session.commit()

    @classmethod
    @check_types
    def get(cls, email: str = None, id: int = None):
        user = None
        if email:
            user = cls.query.filter_by(email=email).first()
        if id:
            user = cls.query.filter_by(id=id).first()
        return user

    @property
    def items(self):
        return Item.get_user_items(self.id)

    def __str__(self):
        return "\n".join(
            str(_) for _ in [self.id, self.first_name, self.last_name, self.email, self.company_id, self.status])

    @check_types
    def get_reset_password_token(self, expires_in: int = 600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            Config.SECRET_KEY, algorithm='HS256')

    @classmethod
    @check_types
    def verify_reset_password_token(cls, token: str):
        try:
            id = jwt.decode(token, Config.SECRET_KEY,
                            algorithms=['HS256'])['reset_password']
        except jwt.exceptions.ExpiredSignatureError:
            raise e.TokenExpired
        user = cls.get(id=id)
        if not user:
            raise e.IncorrectToken
        return user

    @classmethod
    @check_types
    def get_company_users(cls, id: int):
        return cls.query.filter_by(company_id=id).all()


class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Text())
    address = db.Column(db.Text())
    reg_number = db.Column(db.Text(), unique=True)
    admin_id = db.Column(db.Integer())

    @classmethod
    @check_types
    def get(cls, reg_number: str = None, id: int = None):
        company = None
        if reg_number:
            company = cls.query.filter_by(reg_number=reg_number).first()
        if id:
            company = cls.query.filter_by(id=id).first()
        return company

    @classmethod
    @check_types
    def validate_attrs(cls, reg_number: str = None, invite_code: str = None):
        if reg_number and cls.get(reg_number=reg_number):
            raise e.CompanyExists
        if reg_number and invite_code and not InviteCode.validate_code(company_reg_number=reg_number, code=invite_code):
            raise e.IncorrectInviteCode

    def __str__(self):
        return "\n".join(str(_) for _ in [self.id, self.name, self.address, self.reg_number, self.admin_id])

    @classmethod
    @check_types
    def register(cls, name: str, address: str, reg_number: str, invite_code: str):
        cls.validate_attrs(reg_number=reg_number, invite_code=invite_code)
        company = Company(name=name, address=address,
                          reg_number=reg_number)
        db.session.add(company)
        db.session.commit()
        return company

    @check_types
    def set_admin(self, id: int):
        if User.get(id=id):
            self.admin_id = id
        db.session.commit()

    @property
    def items(self):
        return Item.get_company_items(self.id)

    @property
    def users(self):
        return User.get_company_users(self.id)


class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Text())
    user_id = db.Column(db.Integer())
    photo = db.Column(db.Text())
    company_id = db.Column(db.Integer())
    activation_code = db.Column(db.Text())

    def __str__(self):
        return "\n".join(str(_) for _ in [self.id, self.name, self.user_id, self.company_id])

    @classmethod
    @check_types
    def get(cls, id: int = None):
        item = None
        if id:
            item = cls.query.filter_by(id=id).first()
        return item

    @classmethod
    @check_types
    def validate_attrs(cls, company_id: int = None, user_id: int = None):
        if company_id and not Company.get(id=company_id):
            raise e.CompanyDoesntExist
        if user_id and not User.get(id=user_id):
            raise e.UserIdDoesntExist

    @classmethod
    @check_types
    def get_user_items(cls, id: int):
        return cls.query.filter_by(user_id=id).all()

    @classmethod
    @check_types
    def get_company_items(cls, id: int):
        return cls.query.filter_by(company_id=id).all()

    @classmethod
    @check_types
    def add(cls, name: str, company_id: int, photo: str = None):
        cls.validate_attrs(company_id=company_id)
        item = cls(name=name, photo=photo, company_id=company_id,
                   activation_code=generate_code(size=10))
        db.session.add(item)
        db.session.commit()
        return item

    @check_types
    def activate(self, user_id: int, activation_code: str):
        if self.user_id:
            raise e.ItemInUse
        if not activation_code == self.activation_code:
            raise e.IncorrectActivationCode
        self.user_id = user_id
        db.session.commit()

    @check_types
    def deactivate(self, user_id: int):
        if not self.user_id:
            raise e.ItemNotInUse
        if not self.user_id == user_id:
            raise e.NoEnoughRigths
        self.user_id = 0
        db.session.commit()

    @check_types
    @classmethod
    def delete(cls, id: int):
        item = cls.get(id=id)
        if not item:
            raise e.ItemDoesntExist
        if item.user_id:
            raise e.ItemInUse
        db.session.delete(item)
        db.session.commit()


class InviteCode(db.Model):
    __tablename__ = 'invitecode'
    id = db.Column(db.Integer(), primary_key=True)
    company_reg_number = db.Column(db.Text(), unique=True)
    code = db.Column(db.Text())

    def __str__(self):
        return "\n".join(str(_) for _ in [self.id, self.company_reg_number])

    @classmethod
    @check_types
    def validate_code(cls, company_reg_number: str, code: str):
        if cls.query.filter_by(company_reg_number=company_reg_number, code=code).first():
            return True
        return False

    @classmethod
    @check_types
    def validate_attrs(cls, reg_number: str = None):
        if reg_number and cls.query.filter_by(company_reg_number=reg_number).first():
            return True
        return False

    @classmethod
    @check_types
    def add(cls, company_reg_number: str):
        code = InviteCode(code=generate_code(),
                          company_reg_number=company_reg_number)
        if cls.validate_attrs(reg_number=company_reg_number):
            raise e.CompanyExists
        db.session.add(code)
        db.session.commit()
        return code


db.create_all()

if __name__ == "__main__":
    pass
