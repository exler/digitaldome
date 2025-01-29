from typing import Any, Self

from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseBase, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView

from users.auth_forms import LoginForm


class LoginView(FormView):
    form_class = LoginForm
    template_name = "users/login.html"

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )

            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self: Self, form: LoginForm) -> HttpResponse:
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        if form.cleaned_data.get("remember_me", False):
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self: Self) -> str:
        return reverse("tracking:dashboard", kwargs={"user_id": self.request.user.id})


class LogoutView(RedirectView):
    url = reverse_lazy("index")

    @method_decorator(never_cache)
    def dispatch(self: Self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        auth_logout(request)
        return super().dispatch(request, *args, **kwargs)
