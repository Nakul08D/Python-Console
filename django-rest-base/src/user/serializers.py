from rest_framework import serializers
from .tasks import create_keys_using_localstack
from .models import UserCredential
from src.user import models
import random
import string

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)
    name = serializers.CharField(required=False)

    class Meta:
        model = models.User
        fields = [
            "id",
            "name",
            "email",
            "mobile_number",
            "password",
            "confirm_password",
        ]

    def validate(self, data):
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise serializers.ValidationError({"password": "Passwords do not match."})

        return data

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data.pop("password", None)
        confirm_password = validated_data.pop("confirm_password", None)

        if not password:
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        if confirm_password and password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")

        if "name" not in validated_data or not validated_data["name"]:
            validated_data["name"] = validated_data["email"].split('@')[0]

        # Dispatch Celery task for creating keys and wait for the result
        task_result = create_keys_using_localstack.delay(email)

        try:
            credentials = task_result.get(timeout=10)  
        except Exception as e:
            raise serializers.ValidationError(f"Failed to generate credentials: {str(e)}")

        if not credentials:
            raise serializers.ValidationError("Failed to generate credentials.")

        user = models.User.objects.create_user(password=password, **validated_data)

        UserCredential.objects.create(
            user=user,
            access_key_id=credentials['AccessKeyId'],
            secret_access_key=credentials['SecretAccessKey']
        )
        self.context['password'] = password
        self.context['credentials'] = credentials

        return user

    def to_representation(self, instance):

        representation = super().to_representation(instance)

        if 'password' in self.context:
            representation['password'] = self.context['password']

        if 'credentials' in self.context:
            representation['credentials'] = self.context['credentials']

        return representation    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            raise serializers.ValidationError("Both email and password are required.")
        
        return data
class CodeExecutionSerializer(serializers.Serializer):
    code = serializers.CharField(
        help_text="Python code to be executed",
    )

    def validate_code(self, value):
        if not value.strip():
            raise serializers.ValidationError("Code cannot be empty.")
        return value
    
class UserCredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCredential
        fields = ['access_key_id', 'secret_access_key']
