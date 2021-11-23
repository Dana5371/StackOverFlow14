from rest_framework import serializers
from account.models import MyUser
from .utils import send_activations_sms


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True, required=True)
    password_confirmation = serializers.CharField(min_length=8, write_only=True, required=True)

    class Meta:
        model = MyUser
        fields = ('phone_number', 'username', 'password', 'password_confirmation')


    def validate_phone_number(self, phone_number):
        if not phone_number.startswith('+996'):
            raise ValueError('You should have a kyrgyz number')
        return phone_number

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirmation = attrs.pop('password_confirmation')
        if password != password_confirmation:
            raise serializers.ValueError('Passwords do not match')
        return attrs

    def create(self, validated_data):
        user = MyUser.objects.create_user(**validated_data)
        send_activations_sms(str(user.phone_number), user.activation_code)
        return user
