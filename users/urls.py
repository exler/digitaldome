from django.urls import path

from users.auth_views import LoginView, LogoutView
from users.views import SettingsView

app_name = "users"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("settings/", SettingsView.as_view(), name="settings"),
]
