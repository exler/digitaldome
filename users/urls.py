from django.urls import include, path

from users.views import (
    LoginView,
    LogoutView,
    RegisterView,
    ResetPasswordConfirmView,
    ResetPasswordRequestedView,
    ResetPasswordView,
    VerifyEmailView,
)

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
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
]
