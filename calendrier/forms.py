from django import forms
from django.utils.translation import gettext_lazy as _

from calendrier.models import Event, Participants
from gestion.models import OssiaUser


class ModifEventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ["slug"]
        widgets = {
            "description": forms.Textarea(
                attrs={"placeholder": _("facultatif, balises html supportées")}
            ),
            "date": forms.TextInput(attrs={"placeholder": "jj/mm/aaaa"}),
            "debut": forms.TextInput(attrs={"placeholder": "hh:mm"}),
            "fin": forms.TextInput(attrs={"placeholder": _("hh:mm facultatif")}),
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ["slug"]
        widgets = {
            "nomcourt": forms.TextInput(attrs={"placeholder": _("9 caractères max")}),
            "description": forms.Textarea(
                attrs={"placeholder": _("facultatif, balises html supportées")}
            ),
            "date": forms.TextInput(attrs={"placeholder": "jj/mm/aaaa"}),
            "debut": forms.TextInput(attrs={"placeholder": "hh:mm"}),
            "fin": forms.TextInput(attrs={"placeholder": _("hh:mm facultatif")}),
        }


class ParticipantsForm(forms.ModelForm):
    class Meta:
        model = Participants
        fields = ("reponse",)


class ChangeDoodleName(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ChangeDoodleName, self).__init__(*args, **kwargs)
        self.fields["doodlename"].initial = self.instance.profile.get_doodlename()

    def save(self, *args, **kwargs):
        super(ChangeDoodleName, self).save(*args, **kwargs)
        self.instance.profile.doodlename = self.cleaned_data["doodlename"]
        self.instance.profile.save()
        self.instance.save()

    class Meta:
        model = OssiaUser
        fields = ("doodlename",)
