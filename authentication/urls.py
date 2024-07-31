from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from authentication import views

urlpatterns = [
    path("register/", views.RegisterView.as_view()),
    path("token/", views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/jaas", views.RetrieveJaasToken.as_view(), name="jaas_jwt"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/check", TokenVerifyView.as_view(), name="token_check"),
    path("me/", views.UserInformation.as_view(), name="my_profile"),
    path("first_time/", views.FirstTimeLogin.as_view(), name="first_time_login"),
    path("setup/", views.UserSetup.as_view(), name="account_setup"),
]
