from captcha.fields import ReCaptchaField

from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML
from crispy_forms.layout import Layout, Field

from django.utils.translation import gettext as _
from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordResetForm,
)
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    """registration for the website"""

    email = forms.EmailField(required=True)
    captcha = ReCaptchaField(label="")

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            HTML(
                '<h4 class="text-center pb-5">{register}</h4>'.format(
                    register=_("Register")
                )
            ),
            Field(
                "first_name",
            ),
            Field(
                "last_name",
            ),
            Field("username", wrapper_class=""),
            Field(
                "email",
            ),
            Field(
                "password1",
            ),
            Field(
                "password2",
            ),
            Field(
                "captcha",
            ),
            HTML(
                '<button class="btn btn-primary w-100" type="submit">'
                "{register}</button>".format(register=_("Register"))
            ),
        )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",  # optional
            "last_name",  # optional
            "email",
            "password1",
            "password2",  # password confirmation
            "captcha",
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]

        # if successful, save the user to database
        if commit:
            user.save()

        return user


class EditProfileForm(forms.ModelForm):
    """editting a profile"""

    class Meta:
        """you can only change your email, first and last name when editing your profile"""

        model = User
        fields = ("email", "first_name", "last_name")


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordResetForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            HTML(
                '<h4 class="text-center pb-5">{reset_password}</h4>'.format(
                    reset_password=_("Reset password")
                )
            ),
            Field(
                "email",
            ),
            HTML(
                '<button class="btn btn-primary w-100" type="submit">'
                "{reset_password}</button>".format(reset_password=_("Reset Password"))
            ),
        )


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            HTML('<h4 class="text-center pb-5">{login}</h4>'.format(login=_("Login"))),
            Field(
                "username",
            ),
            Field(
                "password",
            ),
            HTML(
                '<p class="register">{forget_password_text}</p>'.format(
                    forget_password_text="Did you forget your password? Click this "
                    '<a href="{{password_reset_url}}">link</a>'
                )
            ),
            HTML(
                '<p class="register">{registration_text}</p>'.format(
                    registration_text='Not a member? <a href="{{register_url}}">'
                    "Register</a> for free now."
                )
            ),
            HTML(
                '<button class="btn btn-primary w-100" type="submit">'
                "{login}</button>".format(login=_("Login"))
            ),
        )
