from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from account.models import User
from account.validators import validate_username, validate_password, capitalize_name


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'password',
            'first_name',
            'last_name',
            'is_guardian',
            'is_admin'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'username': {'required': True}
        }

    def validate_username(self, value):
        return validate_username(value)

    def validate_password(self, value):
        return validate_password(value)

    def validate(self, data):
        if 'first_name' in data:
            data['first_name'] = capitalize_name(data['first_name'])
        if 'last_name' in data:
            data['last_name'] = capitalize_name(data['last_name'])

        return data

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance