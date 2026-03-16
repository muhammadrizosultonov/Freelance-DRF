from datetime import timedelta

from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegisterSerializer, LoginSerializer


class DetailSerializer(serializers.Serializer):
    detail = serializers.CharField()

    class Meta:
        ref_name = "AuthDetailResponse"


class RegisterView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer


class LongLivedLoginSerializer(LoginSerializer):
    access_token_lifetime = timedelta(hours=12)

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        refresh.access_token.set_exp(lifetime=self.access_token_lifetime)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data


class LongLivedLoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = LongLivedLoginSerializer


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    class Meta:
        ref_name = "LogoutRequest"


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Logout and blacklist refresh token",
        request_body=LogoutSerializer,
        responses={
            205: DetailSerializer,
            400: DetailSerializer,
            401: DetailSerializer,
        },
    )
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data["refresh"]

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response(
                {"detail": "Invalid or expired refresh token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({"detail": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
