__author__ = 'tung'

class Users:
    def __init__(self, username='', password=''):
        self._username=username
        self._password=password

    @property
    def username(self):
        return self._username
    @username.setter
    def username(self, name):
        self._username=name
    @property
    def password(self):
        return self._password
    @password.setter
    def password(self, password):
        self._password=password


