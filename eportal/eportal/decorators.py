from django.shortcuts import redirect
from functools import wraps


def redirect_authenticated(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        elif request.user.role == "student":
            return redirect("student_dashboard")
        elif request.user.role == "teacher":
            return redirect("teacher_dashboard")

    return _wrapped_view


def login_required(view_func, redirect_url="welcome_page"):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(redirect_url)
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def student_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role == "student":
            return view_func(request, *args, **kwargs)
        return redirect("welcome_page")

    return _wrapped_view


def teacher_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role == "teacher":
            return view_func(request, *args, **kwargs)
        return redirect("welcome_page")

    return _wrapped_view
