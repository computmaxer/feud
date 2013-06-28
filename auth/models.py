from flask_mongoengine import Document
from mongoengine.fields import StringField
from mongoengine.fields import EmailField
from mongoengine.fields import BooleanField
from mongoengine.fields import ListField
from mongoengine.fields import ReferenceField
from mongoengine.fields import DateTimeField

from auth import utils as auth_utils

import datetime


class User(Document):
    username = StringField()
    name = StringField()
    password = StringField()
    salt = StringField()
    method = StringField()
    email = EmailField()
    created = DateTimeField(default=datetime.datetime.now)
    has_logged_in = BooleanField()
    photo_link = StringField()
    is_mod = BooleanField(default=False)

    def get_display_name(self):
        if self.name:
            return self.name

        if self.username:
            return self.username

        return self.email

    def get_id(self):
        return str(self.pk)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def update_password(self, new_password):
        hash, salt = auth_utils.encode_password(new_password)
        self.password = hash
        self.salt = salt
        self.save()
        return

    @classmethod
    def get_user_by_email(cls, email):
        return User.objects(email=email)

    @classmethod
    def create_placeholder_user(cls, email, name=None):
        user = User(email=email, name=name, has_logged_in=False)
        user.save()
        return user

    def __repr__(self):
        return "<User: email=%s, name=%s, is_mod=%s>" % (self.email, self.name, self.is_mod)
