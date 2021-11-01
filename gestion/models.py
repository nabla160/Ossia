# -*- coding: utf-8 -*-

from colorful.fields import RGBColorField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
import os
from django.conf import settings


class Photo(models.Model):
    PHOTO_PLACEMENT = (
        ("home_join", _("Rejoignez nous")),
        ("home_contact", _("Nous Contacter")),
        ("home_rep", _("Répertoire de l'acceuil")),
        ("login", _("Connexion")),
        ("change_membre", _("Modification du profil")),
        ("inscription_membre", _("Inscription")),
        ("home", _("Calendrier connecté")),
        ("liste", _("Agenda public")),
        ("part", _("Répertoire")),
        ("instru", _("Instruments")),
        ("n", _("N'apparait pas")),
    )

    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        mb_limit = 1.0
        if filesize > mb_limit * 1024 * 1024:
            raise ValidationError("La taille max est %sMB" % str(mb_limit))

    name = models.CharField(max_length=127)
    cat = models.CharField(max_length=127, choices=PHOTO_PLACEMENT, default="n")
    auteur = models.CharField(
        max_length=127, verbose_name=_("Auteur de l'image"), null=True, blank=True
    )
    url = models.URLField(
        verbose_name=_("Lien vers le site de l'auteur"), null=True, blank=True
    )
    color = RGBColorField(_("Couleur du nom de l'auteur"), default="#ffffff")
    image = models.ImageField(
        upload_to="trombonoscope/deco", default=None, validators=[validate_image]
    )

    def __str__(self):
        return self.name

    def delete(self):
        os.remove(self.image.path)
        return super(Photo, self).delete()

    def save(self, *args, **kwargs):
        try:
            this = Photo.objects.get(id=self.id)
            if this.image.path != self.image.path:
                os.remove(this.image.path)
        except Photo.DoesNotExist:
            pass
        super(Photo, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Photo")
        verbose_name_plural = _("Photos")


class OssiaUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    is_ossia = models.BooleanField(_("Membre de l'Ossia"), default=True)
    is_chef = models.BooleanField(_("Chef Fanfare"), default=False)
    phone = models.CharField(
        _("Téléphone"),
        max_length=20,
        blank=True,
        help_text=_("seulement visible par les chef·fe·s"),
    )

    INSTRU_CHOICES = [
        ("Clarinette", _("Clarinette")),
        ("Euphonium", _("Euphonium")),
        ("Percussion", _("Percussion")),
        ("Piccolo", _("Piccolo")),
        ("Saxophone Alto", _("Saxophone Alto")),
        ("Saxophone Ténor", _("Saxophone Ténor")),
        ("Saxophone Baryton", _("Saxophone Baryton")),
        ("Souba", _("Souba")),
        ("Trombone", _("Trombone")),
        ("Trompette", _("Trompette")),
        ("Autre", _("Autre")),
        ("ne sais pas", _("Je ne sais pas encore")),
    ]

    COLORS_CHOICES = [
        ("#e4522f#ffffff", _("Orange et Blanc")),
        ("#ffffff#000000", _("Blanc et Noir")),
        ("#A8107C#000000", _("Rose et Noir")),
        ("#10A4A8#ffffff", _("Bleu et Blanc")),
        ("#26A810#000000", _("Vert et Noir")),
        ("#A81026#ffffff", _("Rouge et Blanc")),
        ("#E3E54C#000000", _("Jaune et Noir")),
        ("autre", _("Autre")),
    ]

    instru = models.CharField(
        _("Instrument joué"),
        max_length=40,
        blank=False,
        choices=INSTRU_CHOICES,
        default="ne sais pas",
    )
    instru_autre = models.CharField(
        _("Lequel ?"), null=True, max_length=100, blank=True
    )
    slug = models.CharField(max_length=7, editable=False, unique=True)
    doodlename = models.CharField(_("Nom pour le doodle"), max_length=30, blank=True)

    trombonoscope = models.CharField(
        _("Je souhaite apparaitre dans le trombonoscope:"),
        max_length=3,
        blank=False,
        null=True,
        choices=[
            ("non", _("Non")),
            ("o_a", _("Oui en tant que fanfaron actuel")),
            ("o_v", _("Oui en tant que vie·ille·ux")),
        ],
        default="non",
    )
    nom_trombonoscope = models.CharField(
        _("Nom affiché sur le trombonoscope"), max_length=30, blank=True
    )
    trombonoscope_colors = models.CharField(
        _("Couleur du profil"),
        max_length=40,
        blank=False,
        choices=COLORS_CHOICES,
        default="OrangeBlanc",
    )
    trombonoscope_fond = RGBColorField(
        _("Couleur de fond du profil"), default="#e4522f"
    )
    trombonoscope_texte = RGBColorField(
        _("Couleur du texte du profil"), default="#ffffff"
    )



    class Meta:
        verbose_name = _("Profil Musicien")
        verbose_name_plural = _("Profil Musicien")

    def __str__(self):
        return self.user.username

    def get_doodlename(self):
        if self.doodlename:
            return self.doodlename
        return self.user.username


class VideoGallery(models.Model):
    name = models.CharField(max_length=127)
    order = models.IntegerField(verbose_name=_("ordre"))
    url = models.URLField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Video")
        verbose_name_plural = _("Videos")
