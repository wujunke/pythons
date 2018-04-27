from django.contrib.auth.models import User, Group
from rest_framework import serializers



class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False,max_length=1024)
    password = serializers.CharField(required=False,max_length=1024)
    class Meta:
        model = User
        fields = ('id' , 'username','password')