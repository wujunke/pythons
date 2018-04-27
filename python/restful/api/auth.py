#coding:utf-8
from django.contrib.auth.models import User


class UsernamePasswordAuth(object):

    def authenticate(self, username=None, password=None):
        print("UsernamePasswordAuth.authenticate")
        try:
            user = User.objects.get(username__iexact=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        print("UsernamePasswordAuth.get_user")
        try:
            user = User.objects.get(pk=user_id)
            return user
        except User.DoesNotExist:
            return None