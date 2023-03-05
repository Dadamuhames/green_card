from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.urls import resolve


class LoginRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        app_name = resolve(request.path).app_name
        
        if 'admins' == app_name and request.path != '/login':
            if not request.user.is_authenticated:
                return redirect('/login')
