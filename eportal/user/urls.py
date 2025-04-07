from django.urls import path
from . import views
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)



urlpatterns = [
    path("", views.welcome_page, name="welcome_page"),
    path("register/", views.register, name="register"),
    path(
        "reset_password/",
        PasswordResetView.as_view(template_name="reset_password.html"),
        name="reset_password",
    ),
    path(
        "reset_password_sent/",
        PasswordResetDoneView.as_view(template_name="reset_password_sent.html"),
        name="reset_password_sent",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(template_name="reset_password_confirm.html"),
        name="reset_password_confirm",
    ),
    path(
        "reset_password_complete/",
        PasswordResetCompleteView.as_view(template_name="reset_password_complete.html"),
        name="reset_password_complete",
    ),
    path("login/", views.log_in, name="login"),
    path("logout/", views.log_out, name="logout"),
    path("edit_user/", views.edit_user, name="edit_user"),
    path("student_dashboard/", views.student_dashboard, name="student_dashboard"),
    path("teacher_dashboard/", views.teacher_dashboard, name="teacher_dashboard"),
]
