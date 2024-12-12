from base.views import BaseViewSet
from src.user import filters, serializers
from .serializers import CodeExecutionSerializer
from src.user.models import User
from src.user import serializers
from .services import execute_aws_code
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action 
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from .models import UserCredential
from .serializers import UserCredentialSerializer
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema

class UserViewSet(BaseViewSet):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.exclude(is_superuser=True).all()
    filterset_class = filters.UserFilter
    http_method_names = ["get", "post", "patch", "put"]

    def get_permissions(self):
        if self.action in ['create', 'login']:
            return [AllowAny()]  
        return super().get_permissions()


    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            email=serializer.validated_data['email'], 
            password=serializer.validated_data['password']
        )


        if user is not None:
            refresh = RefreshToken.for_user(user)

            try:
                user_credentials = UserCredential.objects.get(user=user)
                credentials_serializer = UserCredentialSerializer(user_credentials)
                
            except UserCredential.DoesNotExist:
                return Response({"detail": "No AWS credentials found for this user."}, status=status.HTTP_404_NOT_FOUND)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'access_key_id': credentials_serializer.data['access_key_id'],
                'secret_access_key': credentials_serializer.data['secret_access_key'],
            }, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class CodeExecutionViewSet(BaseViewSet):
    http_method_names = ["post"]

    @swagger_auto_schema(request_body=CodeExecutionSerializer)
    def create(self, request, *args, **kwargs):
        serializer = CodeExecutionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_code = serializer.validated_data['code']
        # access_key_id = request.data.get('access_key_id')
        # secret_access_key = request.data.get('secret_access_key')

        stdout, stderr = execute_aws_code(user_code)

        return Response({
            'stdout': stdout,
            'stderr': stderr,
        }, status=status.HTTP_200_OK)