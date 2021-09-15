from dotenv import load_dotenv

load_dotenv('../.env')

import redis

import os

redis_db = redis.Redis(host=os.environ.get("REDIS_DATABASE_HOST"),
                       port=os.environ.get("REDIS_DATABASE_PORT"),
                       password=os.environ.get("REDIS_DATABASE_PASSWORD"))

