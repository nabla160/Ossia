import os

from django.conf import settings
from django.db import models
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=127)
    order = models.IntegerField(verbose_name=_("ordre"))
    nom_en = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Categorie")
        verbose_name_plural = _("Categories")
        ordering = ("order",)


class Partition(models.Model):
    nom = models.CharField(max_length=100)
    part = models.FileField(upload_to="partitions/")
    morceau = models.ForeignKey("PartitionSet", on_delete=models.CASCADE)

    def __str__(self):
        return self.nom

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.part.name))
        super(Partition, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = _("Morceau")
        verbose_name_plural = _("Morceaux")
        ordering = (Lower("nom"),)


class PartitionSet(models.Model):
    nom = models.CharField(max_length=100)
    auteur = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, verbose_name=_("Type de partition")
    )
    download_unlogged = models.CharField(
        _("Téléchargeable non connecté ?"),
        default="n",
        choices=[("n", _("Non")), ("o", _("Oui"))],
        max_length=1,
    )
    infos = models.TextField(_("Infos utiles"), null=False, blank=True, default="")
    infos_en = models.TextField(
        "Infos utiles en anglais", null=False, blank=True, default=""
    )
    url = models.URLField(
        _("Url d'une video youtube"),
        null=True,
        blank=True,
        help_text=_(
            "Dans Youtube cliquer sur partager puis importer pour récuperer la bonne adresse"
        ),
    )

    def __str__(self):
        return "%s - %s [%s]" % (self.nom, self.auteur, self.category)

    class Meta:
        verbose_name = _("Morceau")
        verbose_name_plural = _("Morceaux")
        ordering = (Lower("nom"),)
