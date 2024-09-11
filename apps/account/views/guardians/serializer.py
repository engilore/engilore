from rest_framework import serializers
from account.models import User


class GuardianSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
