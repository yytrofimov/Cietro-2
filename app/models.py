from lib.types_checker import check_types
from lib.codes_generator import generate_code
from pg_database import Base, SessionLocal
from redis_database import redis_db
from sqlalchemy import Table, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, scoped_session
from werkzeug.security import check_password_hash, generate_password_hash
import exceptions as e
import string
from datetime import timedelta, datetime

postgre_db = scoped_session(SessionLocal)
Base.query = postgre_db.query_property()

users_roles = Table('users_roles', Base.metadata,
                    Column('user_id', ForeignKey('user.id')),
                    Column('role_id', ForeignKey('role.id'))
                    )


class User(Base):
    __tablename__ = "user"
    id = Column(Integer(), primary_key=True)
    first_name = Column(Text())
    last_name = Column(Text())
    email = Column(String(64), unique=True)
    password = Column(Text())
    company_id = Column(Integer())
    status = Column(Integer())
    roles = relationship("Role",
                         secondary=users_roles,
                         backref="parents")

    @classmethod
    @check_types
    def validate_attrs(cls, email: str = None, company_id: int = None):
        if email:
            try:
                user = cls.get(email=email)
                if user:
                    raise e.UserExists
            except e.UserDoesntExist:
                pass
        if company_id and not Company.get(id=company_id):
            raise e.CompanyDoesntExist

    @classmethod
    @check_types
    def register(cls, first_name: str, last_name: str, email: str, password: str, company_id: int, status: int):
        cls.validate_attrs(email=email, company_id=company_id)
        password = generate_password_hash(password)
        user = cls(first_name=first_name, last_name=last_name,
                   email=email, password=password, company_id=company_id, status=status)
        postgre_db.add(user)
        postgre_db.commit()
        return user

    @classmethod
    @check_types
    def login(cls, email: str, password: str):
        user = cls.get(email=email)
        if not check_password_hash(user.password, password):
            raise e.PasswordIsIncorrect
        if not user.status:
            raise e.UserIsBlocked
        return user

    @check_types
    def set_password(self, new_password: str):
        self.password = generate_password_hash(new_password)
        postgre_db.commit()

    @classmethod
    @check_types
    def get(cls, email: str = None, id: int = None):
        user = None
        if email:
            user = cls.query.filter_by(email=email).first()
            if not user:
                raise e.UserDoesntExist
        if id:
            user = cls.query.filter_by(id=id).first()
            if not user:
                raise e.UserDoesntExist
        return user

    @property
    def items(self):
        return Item.get_user_items(self.id)

    def __str__(self):
        return "\n".join(
            str(_) for _ in [self.id, self.first_name, self.last_name, self.email, self.company_id, self.status])

    @classmethod
    @check_types
    def get_company_users(cls, id: int):
        Company.get(id=id)
        return cls.query.filter_by(company_id=id).all()


class Role(Base):
    __tablename__ = "role"
    id = Column(Integer(), primary_key=True)
    name = Column(Integer(), unique=True)


class Company(Base):
    __tablename__ = 'company'
    id = Column(Integer(), primary_key=True)
    name = Column(Text())
    address = Column(Text())
    reg_number = Column(Text(), unique=True)
    admin_id = Column(Integer())

    @classmethod
    @check_types
    def get(cls, reg_number: str = None, id: int = None):
        company = None
        if reg_number:
            company = cls.query.filter_by(reg_number=reg_number).first()
            if not company:
                raise e.CompanyDoesntExist
        if id:
            company = cls.query.filter_by(id=id).first()
            if not company:
                raise e.CompanyDoesntExist
        return company

    @classmethod
    @check_types
    def validate_attrs(cls, reg_number: str = None, invite_code: str = None):
        if reg_number:
            try:
                company = cls.get(reg_number=reg_number)
                if company:
                    raise e.CompanyExists
            except e.CompanyDoesntExist:
                pass
        if reg_number and invite_code and not InviteCode.validate_code(company_reg_number=reg_number, code=invite_code):
            raise e.InviteCodeIsIncorrect

    def __str__(self):
        return "\n".join(str(_) for _ in [self.id, self.name, self.address, self.reg_number, self.admin_id])

    @classmethod
    @check_types
    def register(cls, name: str, address: str, reg_number: str, invite_code: str):
        cls.validate_attrs(reg_number=reg_number, invite_code=invite_code)
        company = Company(name=name, address=address,
                          reg_number=reg_number)
        postgre_db.add(company)
        postgre_db.commit()
        return company

    @check_types
    def set_admin(self, id: int):
        User.get(id=id)
        self.admin_id = id
        postgre_db.commit()

    @property
    def items(self):
        return Item.get_company_items(self.id)

    @property
    def users(self):
        return User.get_company_users(self.id)


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer(), primary_key=True)
    name = Column(Text())
    user_id = Column(Integer())
    photo = Column(Text())
    company_id = Column(Integer())
    activation_code = Column(Text())

    def __str__(self):
        return "\n".join(str(_) for _ in [self.id, self.name, self.user_id, self.company_id])

    @classmethod
    @check_types
    def get(cls, id: int = None):
        item = None
        if id:
            item = cls.query.filter_by(id=id).first()
            if not item:
                raise e.ItemDoesntExist
        return item

    @classmethod
    @check_types
    def validate_attrs(cls, company_id: int = None, user_id: int = None):
        if company_id:
            Company.get(id=company_id)
        if user_id:
            User.get(id=user_id)

    @classmethod
    @check_types
    def get_user_items(cls, id: int):
        User.get(id=id)
        return cls.query.filter_by(user_id=id).all()

    @classmethod
    @check_types
    def get_company_items(cls, id: int):
        Company.get(id=id)
        return cls.query.filter_by(company_id=id).all()

    @classmethod
    @check_types
    def add(cls, name: str, company_id: int, photo: str = None):
        cls.validate_attrs(company_id=company_id)
        item = cls(name=name, photo=photo, company_id=company_id,
                   activation_code=generate_code(size=10))
        postgre_db.add(item)
        postgre_db.commit()
        return item

    @check_types
    def activate(self, user_id: int, activation_code: str):
        if self.user_id:
            raise e.ItemInUse
        if not activation_code == self.activation_code:
            raise e.ActivationCodeIsIncorrect
        self.user_id = user_id
        postgre_db.commit()

    @check_types
    def deactivate(self, user_id: int):
        if not self.user_id:
            raise e.ItemNotInUse
        if not self.user_id == user_id:
            raise e.NoEnoughRights
        self.user_id = 0
        postgre_db.commit()

    @classmethod
    @check_types
    def delete(cls, id: int):
        item = cls.get(id=id)
        if item.user_id:
            raise e.ItemInUse
        postgre_db.delete(item)
        postgre_db.commit()


class InviteCode(Base):
    __tablename__ = 'invite_code'
    id = Column(Integer(), primary_key=True)
    company_reg_number = Column(Text(), unique=True)
    code = Column(Text())

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
            raise e.CompanyExists

    @classmethod
    @check_types
    def add(cls, company_reg_number: str):
        cls.validate_attrs(reg_number=company_reg_number)
        code = InviteCode(code=generate_code(),
                          company_reg_number=company_reg_number)
        postgre_db.add(code)
        postgre_db.commit()
        return code


class PasswordReset:

    @classmethod
    @check_types
    def get_user_token(cls, id: int):
        token = generate_code(size=256, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase)
        redis_db.setex(token, timedelta(minutes=5), id)
        return token

    @classmethod
    @check_types
    def verify_user_token(cls, token: str):
        user = User.get(id=cls.check_user_token(token))
        return user

    @staticmethod
    @check_types
    def check_attempts_by_email(email: str):
        return True if redis_db.get(email) else False

    @staticmethod
    @check_types
    def save_user_email(email: str):
        redis_db.setex(email, timedelta(minutes=5), "datetime.now().strftime('%Y-%m-%d')")

    @staticmethod
    @check_types
    def check_user_token(token: str):
        user_id = redis_db.get(token)
        if not user_id:
            raise e.TokenIsIncorrect
        return int(user_id)

    @staticmethod
    @check_types
    def delete_user_token(token: str):
        redis_db.delete(token)

# Base.metadata.create_all(engine)
