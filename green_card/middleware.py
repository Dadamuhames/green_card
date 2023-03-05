from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.urls import resolve


class LoginRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            return redirect('/login')
