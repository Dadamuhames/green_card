from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.urls import resolve


class LoginRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path == '/':
            return redirect("/clients")

        if not request.user.is_authenticated and request.path != '/login':
            return redirect('/login')

        if request.user.is_authenticated and not request.user.is_superuser:
            if request.user.info.is_operator and request.get_full_path() == '/clients':
                return redirect("/clients?status=new")

