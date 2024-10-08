from django.contrib import messages
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetCompleteView
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _

from login.forms import (
    CustomPasswordChangeForm,
    EditProfileForm,
    EditProfileFormReadOnly,
    RegistrationForm,
)


def logout_view(request):
    logout(request)
    messages.success(
        request, _("Disconnected successfully.")
    )  # Add your desired message here.
    return redirect("/")


def register(request):
    """registers users"""

    # redirect user to home if user is already signed in
    if request.user.is_authenticated:
        return redirect("/")

    # if request is post
    if request.method == "POST":
        # get the post form
        form = RegistrationForm(request.POST)

        # check to see if the form is valid
        if form.is_valid():
            # if it is valid, save and redirect to home
            form.save()
            messages.success(request, _("Account created successfully."))
            return redirect("/")
        else:
            # form is not valid and return form with error
            args = {"form": form}
            return render(request, "login/register.html", args)
    # if request is not post, user probably wants the webpage with a empty form
    else:
        # give user clean register form
        form = RegistrationForm()
        args = {"form": form}
        return render(request, "login/register.html", args)


@login_required
def profile(request):
    """view profile if logged in"""
    form = EditProfileFormReadOnly(instance=request.user)
    args = {"form": form}
    return render(request, "login/profile.html", args)


@login_required
def edit_profile(request):
    """edit profile if logged in"""

    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

            # renders success message
            messages.success(request, _("Profile modified successfully."))
            return redirect(reverse("profile"))
        else:
            # form for in valid error
            args = {"form": form}
            return render(request, "login/edit_profile.html", args)

    else:
        # give user edit profile form
        form = EditProfileForm(instance=request.user)
        args = {"form": form}
        return render(request, "login/edit_profile.html", args)


@login_required
def change_password(request):
    """request change in password if user is logged in"""

    if request.method == "POST":
        form = CustomPasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, _("Password modified successfully."))
            return redirect(reverse("profile"))
        else:
            # form for in valid error
            args = {"form": form}
            return render(request, "login/change_password.html", args)

    else:
        # give user change password form
        form = CustomPasswordChangeForm(user=request.user)
        args = {"form": form}
        return render(request, "login/change_password.html", args)


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        messages.success(self.request, _("Password modified successfully."))
        return redirect(reverse("login"))


def redirect_to_home(request):
    return redirect("/")


# errors, maybe move to different app??
def error_400_view(request, exception):
    return render(request, "errors/400.html")


def error_403_view(request, exception):
    return render(request, "errors/403.html")


def error_404_view(request, exception):
    return render(request, "errors/404.html")


def error_500_view(request):
    return render(request, "errors/500.html")
