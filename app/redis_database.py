from dotenv import load_dotenv

load_dotenv('../.env')

import redis
from lib.types_checker import check_types
import exceptions as e
from datetime import timedelta, datetime
import os

redis_db = redis.Redis(host=os.environ.get("REDIS_DATABASE_HOST"),
                       port=os.environ.get("REDIS_DATABASE_PORT"),
                       password=os.environ.get("REDIS_DATABASE_PASSWORD"))


class PasswordReset:
    @staticmethod
    @check_types
    def check_requests_by_email(email: str):
        return True if redis_db.get(email) else False

    @staticmethod
    @check_types
    def save_user_email(user_email: str):
        redis_db.setex(user_email, timedelta(minutes=5), "datetime.now().strftime('%Y-%m-%d')")

    @staticmethod
    @check_types
    def save_user_token(token: str, user_id: int):
        redis_db.setex(token, timedelta(minutes=5), user_id)

    @staticmethod
    @check_types
    def check_token(token: str):
        user_id = redis_db.get(token)
        if not user_id:
            raise e.TokenIsIncorrect
        return int(user_id)

    @staticmethod
    @check_types
    def delete_token(token: str):
        redis_db.delete(token)
