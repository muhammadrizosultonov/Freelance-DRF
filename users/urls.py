from django.urls import path
from .views import RegisterView, LoginView, LongLivedLoginView, LogoutView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("login/long/", LongLivedLoginView.as_view(), name="login-long"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
