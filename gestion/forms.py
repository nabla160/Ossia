from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from gestion.models import OssiaUser


class RegistrationFormUser(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "email",
        )


class ChangeFormUser(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
        )


class ChangeMembreForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(ChangeMembreForm, self).clean()
        instru = cleaned_data.get("instru")
        instru_autre = cleaned_data.get("instru_autre")
        if (instru == "Autre") and not (instru_autre):
            raise forms.ValidationError(_("Préçisez quel autre instrument"))

        return cleaned_data

    class Meta:
        model = OssiaUser
        fields = (
            "phone",
            "instru",
            "instru_autre",
        )


class InscriptionMembreForm(ChangeMembreForm):
    validation = forms.CharField(max_length=100, widget=forms.PasswordInput)

    class Meta:
        model = OssiaUser
        fields = (
            "phone",
            "instru",
            "instru_autre",
        )
