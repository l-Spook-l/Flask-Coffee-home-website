from os import environ


class Configuration(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///shop.db'
    SECRET_KEY = "8eGcbMi8ZxoeW26JcKt3"

    # SECURITY_PASSWORD_SALT = environ.get("SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634')
    # SECURITY_PASSWORD_HASH = 'sha512_crypt'

    # SECURITY_REGISTERABLE = True
    # SECURITY_REGISTER_URL = '/create_account'
