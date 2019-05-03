import os
import redis
import secrets

_connection = None


def connection():
    global _connection
    if _connection is None:
        _connection = redis.Redis(host='localhost', port=6379)
    return _connection


def add_user(nick, room_pin):
    user_token = secrets.token_urlsafe()
    connection().lpush("rooms:" + str(room_pin) + ":users", user_token)
    connection().lpush("users:" + str(user_token) + ":nick", nick)
    return(user_token)
