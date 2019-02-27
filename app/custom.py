from wtforms.validators import ValidationError
from flask_user import UserManager
from flask_user.db_adapters import DbAdapterInterface
from sqlalchemy.orm.session import Session as SessionBase
from flask_sqlalchemy import *
from app import app, db


class CustomUserManager(UserManager):
    def username_validator(self, form, field):
        username = field.data

        if len(username) < app.config["USER_USERNAME_MIN_LEN"]:
            print(len(username))
            raise ValidationError(
                                ("Der Nutzername sollte mindestens " + \
                                 str(app.config["USER_USERNAME_MIN_LEN"]) + \
                                 " Zeichen lang sein"))

        if len(username) > app.config["USER_USERNAME_MAX_LEN"]:
            raise ValidationError(
                                ("Der Nutzername sollte maximal " \
                                + app.config["USER_USERNAME_MAX_LEN"] + \
                                 " Zeichen Lang sein"))

        valid_chars = "abcdefghijklmnopqrstuvwxyzAB \
            CDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._"
        chars = list(username)
        for char in chars:
            if char not in valid_chars:
                raise ValidationError(
               ("Der Nutzername sollte nur Buchstaben, Nummern, '-', '.' und '_' enthalten"))

    def password_validator(self, form, field):
        # Konvertierung des Strings
        password = list(field.data)
        password_length = len(password)

        # Zählt die benötigten Zeichen
        lowers = uppers = digits = 0
        for ch in password:
            if ch.islower(): lowers += 1
            if ch.isupper(): uppers += 1
            if ch.isdigit(): digits += 1

        # Password must have one lowercase letter, one uppercase letter and one digit
        is_valid = password_length >= app.config["USER_PASSWORD_MIN_LEN"] and lowers and uppers and digits
        if not is_valid:
            raise ValidationError(
                ("Passwörter müssen mindestens " + str(app.config["USER_PASSWORD_MIN_LEN"]) + " Zeichen lang sein sowie einen Kleinbuchstaben, einen Großbuchstaben und eine Zahl enthalten"))

    def hash_password(self, password):
        """Convenience method that calls self.password_manager.hash_password(password)."""
        return self.password_manager.hash_password(password)
