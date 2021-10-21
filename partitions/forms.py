from django import forms

from .models import PartitionSet


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


class UploadMorceauForm(forms.Form):
    titre = forms.CharField(max_length=100)
    auteur = forms.CharField(max_length=100)


class ChefEditMorceauForm(forms.ModelForm):
    class Meta:
        model = PartitionSet
        fields = ("category", "download_unlogged", "infos", "url", "infos_en")
