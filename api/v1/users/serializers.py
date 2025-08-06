from django.contrib.auth import authenticate
from rest_framework import serializers
from user.models import CustomUser
import re


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=12, write_only=True, required=True)
    password2 = serializers.CharField(max_length=12, write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2']

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('Password must be at least eight characters.')

        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError('Password must include at least one uppercase letter.')

        if not re.search(r'[a-zA-Z]', value):
            raise serializers.ValidationError('Password must include at least one letter.')

        if not re.search(r'\d', value):
            raise serializers.ValidationError('Password must include at least one digit.')

        return value  

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({'password2': 'Passwords do not match'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')

        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user

class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username_or_email = data.get('username_or_email')
        password = data.get('password')

        user = CustomUser.objects.filter(email=username_or_email).first() or \
               CustomUser.objects.filter(username=username_or_email).first()

        if user and user.check_password(password):
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled.")
            data['user'] = user
            return data

        raise serializers.ValidationError("Invalid credentials.")
