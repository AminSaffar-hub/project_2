from django.contrib.auth.views import (
    LoginView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import path

# import both app modules
from login import views as user_views

from . import views

urlpatterns = [
    # login
    path(
        "login/",
        LoginView.as_view(
            template_name="login/login.html", redirect_authenticated_user=True
        ),
        name="login",
    ),
    path("register/", user_views.register, name="register"),
    # logout
    path("logout/", views.logout_view, name="logout"),
    # user profile
    path("profile/", user_views.profile, name="profile"),
    path("profile/edit/", user_views.edit_profile, name="edit_profile"),
    path("profile/password/", user_views.change_password, name="change_password"),
    # reset password
    path(
        "reset_password/",
        PasswordResetView.as_view(
            template_name="login/resetpassword.html",
            email_template_name="login/reset_password_email.html",
        ),
        name="password_reset",
    ),
    path(
        "reset_password/done/",
        PasswordResetDoneView.as_view(template_name="login/text.html"),
        name="password_reset_done",
    ),
    path(
        "reset_password/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(template_name="login/change_password.html"),
        name="password_reset_confirm",
    ),
    # redirect to login
    path(
        "reset_password/complete/",
        user_views.CustomPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
