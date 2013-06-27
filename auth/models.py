from mongoengine import Document
from mongoengine import StringField
from mongoengine import EmailField
from mongoengine import BooleanField
from mongoengine import ListField
from mongoengine import ReferenceField
from mongoengine import DateTimeField

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

    def get_display_name(self):
        if self.name:
            return self.name

        if self.username:
            return self.username

        return self.email

    def get_id(self):
        return self.pk

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
        return User.objects(email=email).get()

    @classmethod
    def create_placeholder_user(cls, email, name=None):
        user = User(email=email, name=name, has_logged_in=False)
        user.save()
        return user
