from django.urls import include, path

from users.auth_views import (
    LoginView,
    LogoutView,
    ResetPasswordConfirmView,
    ResetPasswordRequestedView,
    ResetPasswordView,
    VerifyEmailView,
)
from users.views import SettingsView

app_name = "users"

urlpatterns = [
    path("verify/<str:token>/", VerifyEmailView.as_view(), name="verify-email"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "resetpassword/",
        include(
            [
                path("", ResetPasswordView.as_view(), name="reset-password"),
                path("requested/", ResetPasswordRequestedView.as_view(), name="reset-password-requested"),
                path("<str:token>/", ResetPasswordConfirmView.as_view(), name="reset-password-confirm"),
            ]
        ),
    ),
    path("settings/", SettingsView.as_view(), name="settings"),
]
