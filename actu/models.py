from django.db import models
from django.utils.translation import gettext_lazy as _


class Actu(models.Model):

    text = models.TextField(_("Info"), null=True, blank=False)
    text_en = models.TextField(("Info en anglais"), null=True, blank=True)
    order = models.IntegerField(verbose_name=_("ordre"))

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = _("Actualité")
        verbose_name_plural = _("Actualités")
        ordering = ("order",)
