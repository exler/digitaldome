from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.http import urlencode


def redirect_with_params(url: str, **kwargs: str) -> HttpResponseRedirect:
    if kwargs:
        url += f"?{urlencode(kwargs)}"
    return redirect(url)
