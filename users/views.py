from datetime import timedelta

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegisterSerializer, LoginSerializer


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
