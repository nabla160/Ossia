from django import forms

from .models import PartitionSet


class UploadFileForm(forms.Form):
    file=forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


class UploadMorceauForm(forms.Form):
    titre = forms.CharField(max_length=100)
    auteur = forms.CharField(max_length=100)


class ChefEditMorceauForm(forms.ModelForm):
    class Meta:
        model = PartitionSet
        fields = ("category", "infos", "infos_en")
