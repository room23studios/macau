import jwt

from django.conf import settings


def sign(payload):
    # TODO: use a public/private keypair
    return jwt.encode(payload, settings.JWT_SECRET, algorithm='HS512').decode('utf-8')
