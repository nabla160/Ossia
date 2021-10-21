import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from gestion.models import OssiaUser

ANSWERS = (
    ("oui", _("Oui")),
    ("non", _("Non")),
    ("pe", _("Peut-etre")),
)


class Event(models.Model):

    nom = models.CharField(max_length=100)
    nomcourt = models.CharField(max_length=9, verbose_name=_("Nom court"))
    date = models.DateField()
    debut = models.TimeField()
    fin = models.TimeField(blank=True, null=True)
    slug = models.CharField(
        max_length=7, editable=False, unique=True, default=uuid.uuid1
    )
    lieu = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    desc_users = models.TextField(
        blank=True,
        verbose_name=_("Infos (visible seulement des fanfaron·ne·s)"),
        null=True,
    )
    desc_users_en = models.TextField(
        blank=True,
        verbose_name=_("Infos en anglais (visible seulement des fanfaron·ne·s"),
        null=True,
    )
    CALENDRIER_CHOICES = [
        ("F", _("Visible seulement par les fanfarons")),
        ("T", _("Afficher dans le calendrier pour tous")),
        ("H", _("Hall of fame")),
        ("C", _("Visible seulement par les cheff·e·s")),
        ("D", _("Visible seulement par les cheff·e·s et sur l'agenda public")),
    ]
    calendrier = models.CharField(
        max_length=1,
        choices=CALENDRIER_CHOICES,
        default="F",
    )

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = _("Evenement")


class Participants(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    participant = models.ForeignKey(OssiaUser, on_delete=models.CASCADE)
    reponse = models.CharField(
        _("Réponse"), max_length=20, default="non", choices=ANSWERS
    )
    instrument = models.CharField(max_length=50, blank=True, null=True)
    dont_play_main = models.CharField(
        _("Je veux jouer d'un instrument different de mon instrument principal:"),
        default="Non",
        null=False,
        max_length=3,
        choices=[("Non", _("Non")), ("Oui", _("Oui"))],
    )
    details = models.CharField(max_length=50, blank=True)
