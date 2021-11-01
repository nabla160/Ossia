from django import forms

from gestion.models import OssiaUser


class ChangeTrombonoscope(forms.ModelForm):
    def save(self, *args, **kwargs):
        super(ChangeTrombonoscope, self).save(*args, **kwargs)

        trombonoscope_colors = self.cleaned_data["trombonoscope_colors"]
        if trombonoscope_colors != "autre":

            self.instance.trombonoscope_fond = trombonoscope_colors[:7]
            self.instance.trombonoscope_texte = trombonoscope_colors[7:]
        self.instance.save()

    class Meta:
        model = OssiaUser
        fields = (
            "trombonoscope",
            "nom_trombonoscope",
            "trombonoscope_colors",
            "trombonoscope_fond",
            "trombonoscope_texte",
        )
