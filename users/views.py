from typing import Any, Self

from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseBase, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import CreateView, FormView, RedirectView, TemplateView

from users.forms import (
    LoginForm,
    RegisterForm,
    ResetPasswordConfirmForm,
    ResetPasswordForm,
)
from users.tokens import EmailVerificationTokenGenerator


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self: Self, form: RegisterForm) -> HttpResponseBase:
        messages.add_message(
            self.request,
            messages.INFO,
            "Your account has been created. Please check your email to verify your account.",
        )
        return super().form_valid(form)


class VerifyEmailView(RedirectView):
    url = reverse_lazy("users:login")

    def get(self: Self, request: HttpRequest, token: str, *args: Any, **kwargs: Any) -> HttpResponseBase:
        user = EmailVerificationTokenGenerator.check_token(token)

        if user:
            if user.email_verified:
                messages.add_message(request, messages.WARNING, "Your email is already verified.")
            else:
                user.email_verified = True
                user.save(update_fields=["email_verified"])
                messages.add_message(request, messages.SUCCESS, "Your email has been verified. You can now sign in.")

            return super().get(request, *args, **kwargs)
        else:
            raise PermissionDenied("Invalid token")


class ResetPasswordView(FormView):
    template_name = "users/reset_password.html"
    form_class = ResetPasswordForm
    success_url = reverse_lazy("users:reset-password-requested")

    def form_valid(self: Self, form: ResetPasswordForm) -> HttpResponse:
        try:
            form.save()
        except Http404:
            messages.add_message(self.request, messages.ERROR, "No user with this email address exists.")
            return self.form_invalid(form)
        return super().form_valid(form)


class ResetPasswordRequestedView(TemplateView):
    template_name = "users/reset_password_requested.html"


class ResetPasswordConfirmView(FormView):
    template_name = "users/reset_password_confirm.html"
    form_class = ResetPasswordConfirmForm
    success_url = reverse_lazy("users:login")

    token_generator = EmailVerificationTokenGenerator
    reset_url_token = "set-password"  # noqa: S105
    reset_session_key = "_reset_password_token"

    def __init__(self: Self, **kwargs: Any) -> None:
        self.valid_link = False
        self.user = None
        super().__init__(**kwargs)

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self: Self, *args: Any, **kwargs: Any) -> None:
        token = kwargs["token"]

        if token == self.reset_url_token:
            session_token = self.request.session.get(self.reset_session_key, "")
            if user := self.token_generator.check_token(session_token):
                # If the token is valid, display the password reset form.
                self.user = user
                self.valid_link = True
                return super().dispatch(*args, **kwargs)
        else:
            if self.token_generator.check_token(token):
                # Store the token in the session and redirect to the
                # password reset form at a URL without the token. That
                # avoids the possibility of leaking the token in the
                # HTTP Referer header.
                self.request.session[self.reset_session_key] = token
                redirect_url = self.request.path.replace(token, self.reset_url_token)
                return HttpResponseRedirect(redirect_url)

        # Display the "Password reset unsuccessful" page.
        return self.render_to_response(self.get_context_data())

    def get_form_kwargs(self: Self) -> dict[str, Any]:
        form_kwargs = super().get_form_kwargs()
        form_kwargs["user"] = self.user
        return form_kwargs

    def get_context_data(self: Self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["token"] = self.kwargs["token"]
        context["valid_link"] = self.valid_link
        return context

    def form_valid(self: Self, form: ResetPasswordConfirmForm) -> HttpResponse:
        form.save()
        del self.request.session[self.reset_session_key]
        messages.add_message(self.request, messages.SUCCESS, "Your password has been reset. You can now sign in.")
        return super().form_valid(form)


class LoginView(FormView):
    form_class = LoginForm
    template_name = "users/login.html"

    def form_valid(self: Self, form: LoginForm) -> HttpResponse:
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        if form.cleaned_data.get("remember_me", False):
            self.request.session.set_expiry(0)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self: Self) -> str:
        return reverse("tracking:dashboard", kwargs={"user_id": self.request.user.id})


class LogoutView(RedirectView):
    url = reverse_lazy("index")

    @method_decorator(never_cache)
    def dispatch(self: Self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        auth_logout(request)
        return super().dispatch(request, *args, **kwargs)
