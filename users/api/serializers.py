from rest_framework import serializers
from django.core.validators import MinLengthValidator
from ..models import BaseUser

class InputRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, validators=[
        MinLengthValidator(limit_value=10)
    ])
    confirm_password = serializers.CharField(write_only=True)


    def validate_email(self, email):
        if BaseUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('email already registered')
        return email
    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if not password or not confirm_password:
            raise serializers.ValidationError("Both password fields are required.")

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")

        return attrs
class OutputRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ("email",)


