from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class RequirePasswordMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        url_password_set = reverse("password_set")
        if (
            request.path != url_password_set
            and request.user.is_authenticated
            and not request.user.password
        ):
            return redirect("password_set")
        return response
