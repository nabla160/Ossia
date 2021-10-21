import io
import os
import zipfile

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files import File
from django.db.models import Q
from django.http import Http404
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from gestion.mixins import ChefRequiredMixin
from gestion.models import Photo
from partitions.forms import UploadFileForm, UploadMorceauForm
from partitions.models import Category, Partition, PartitionSet

from .forms import ChefEditMorceauForm


def download_musecores(request):

    p = Partition.objects.filter(
        Q(part__contains=".mscz")
        & Q(
            Q(morceau__category__name="Partitions actives")
            | Q(morceau__category__name="Partitions optionnelles")
        )
    )

    zip_subdir = "Ossia_musescores"
    zip_filename = "%s.zip" % zip_subdir

    # Open StringIO to grab in-memory ZIP contents
    s = io.BytesIO()

    # The zip compressor
    zf = zipfile.ZipFile(s, "w")

    for part in p:
        fpath = part.part.path

        typ = ".mscz"
        # Calculate path for file in zip
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(
            zip_subdir,
            "%s_%s_%s.%s"
            % (
                slugify(part.morceau.nom),
                slugify(part.morceau.auteur),
                slugify(part.nom),
                typ,
            ),
        )

        # Add file, at correct path
        zf.write(fpath, zip_path)

    # Must close zip for all contents to be written
    zf.close()
    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp = HttpResponse(s.getvalue())
    # ..and correct content-disposition
    resp["Content-Disposition"] = "attachment; filename=%s" % zip_filename

    return resp


class Repertoire(TemplateView):
    template_name = "partitions/repertoire.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.prefetch_related(
            "partitionset_set"
        ).order_by("order")
        context["photo"] = Photo.objects.filter(cat="part").order_by("?").first()
        return context


class Morceau(LoginRequiredMixin, TemplateView):
    template_name = "partitions/part.html"
    form_class = ChefEditMorceauForm

    def get_context_data(self, **kwargs):
        context = super(Morceau, self).get_context_data(**kwargs)
        p = get_object_or_404(
            PartitionSet, nom=self.kwargs["nom"], auteur=self.kwargs["auteur"]
        )
        part = p.partition_set.all().order_by("nom")
        form = self.form_class(instance=p)
        infos = mark_safe(p.infos)
        infos_en = mark_safe(p.infos_en)

        context["p"] = p
        context["infos"] = infos
        context["infos_en"] = infos_en
        context["form"] = form
        context["part"] = part
        context["nom"] = self.kwargs["nom"]
        context["auteur"] = self.kwargs["auteur"]

        return context

    def post(self, request, *args, **kwargs):
        p = get_object_or_404(
            PartitionSet, nom=self.kwargs["nom"], auteur=self.kwargs["auteur"]
        )
        if request.user.profile.is_chef:
            form = self.form_class(request.POST, instance=p)
            if form.is_valid():
                form.save()
        context = self.get_context_data()
        return render(request, self.template_name, context)


class Upload(ChefRequiredMixin, TemplateView):
    form_class = UploadFileForm
    template_name = "partitions/upload.html"

    def get_context_data(self, **kwargs):
        context = super(Upload, self).get_context_data(**kwargs)
        form = self.form_class()

        context["nom"] = self.kwargs["nom"]
        context["auteur"] = self.kwargs["auteur"]
        context["form"] = form
        return context

    def post(self, request, *args, **kwargs):
        form = UploadFileForm(request.POST, request.FILES)
        error = False
        sauvegarde = False
        if form.is_valid():
            partition = Partition()
            partition.part = form.cleaned_data["file"]
            partition.nom = form.cleaned_data["title"]
            if "/" in partition.nom:
                error = _("Le caractère / n'est pas autorisé dans le nom")
                context = self.get_context_data()
                context["error"] = error
                return render(request, self.template_name, context)
            mor = get_object_or_404(
                PartitionSet, nom=self.kwargs["nom"], auteur=self.kwargs["auteur"]
            )
            partition.morceau = mor
            try:
                mor.partition_set.get(nom=partition.nom)
                error = _("Un morceau du même nom existe déjà")
            except Partition.DoesNotExist:
                partition.save()
                sauvegarde = True

        context = self.get_context_data()
        context["form"] = form
        context["error"] = error
        context["sauvegarde"] = sauvegarde
        return render(request, self.template_name, context)


def see(request, nom, auteur, partition_id):
    partition = get_object_or_404(Partition, id=partition_id)
    _, extension = os.path.splitext(partition.part.path)
    download_unlogged = partition.morceau.download_unlogged
    if download_unlogged == "o" or request.user.is_authenticated:
        if ".pdf" == extension:
            with open(partition.part.path, "rb") as f:
                myfile = File(f)
                response = HttpResponse(content=myfile.read())
                response["Content-Type"] = "application/pdf"
                response["Content-Disposition"] = "inline; filename=%s_%s_%s.pdf" % (
                    slugify(nom),
                    slugify(auteur),
                    slugify(partition.nom),
                )
            return response
        elif ".mp3" == extension:
            with open(partition.part.path, "rb") as f:
                myfile = File(f)
                response = HttpResponse()
                response.write(myfile.read())
                response["Content-Type"] = "audio/mp3"
                response["Content-Length"] = myfile.size
            return response
        else:
            p = get_object_or_404(PartitionSet, nom=nom, auteur=auteur)
            part = p.partition_set.all()
            return render(
                request,
                "partitions/part.html",
                {"p": p, "part": part, "nom": nom, "auteur": auteur},
            )
    else:
        return redirect("login")


class DeletePart(ChefRequiredMixin, TemplateView):
    model = PartitionSet

    def get(self, request, *args, **kwargs):
        p = get_object_or_404(
            self.model, nom=self.kwargs["nom"], auteur=self.kwargs["auteur"]
        )
        try:
            part = p.partition_set.get(id=self.kwargs["id"])
        except Partition.DoesNotExist:
            raise Http404
        part.delete()
        return redirect(
            "partitions:listepart", nom=self.kwargs["nom"], auteur=self.kwargs["auteur"]
        )


class CreateMorc(ChefRequiredMixin, TemplateView):
    form_class = UploadMorceauForm
    template_name = "partitions/new.html"

    def get_context_data(self, **kwargs):
        context = super(CreateMorc, self).get_context_data(**kwargs)
        context["form"] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        sauvegarde = False
        error = False
        if form.is_valid():
            partitionset = PartitionSet()
            partitionset.nom = form.cleaned_data["titre"]
            partitionset.auteur = form.cleaned_data["auteur"]
            if "/" in partitionset.auteur or "/" in partitionset.nom:
                error = _("Le caractère / n'est pas autorisé")
                context = self.get_context_data()
                context["error"] = error
                return render(request, self.template_name, context)
            try:
                PartitionSet.objects.get(
                    nom=partitionset.nom, auteur=partitionset.auteur
                )
                error = _("Un morceau du même nom existe déjà")
            except PartitionSet.DoesNotExist:
                # XXX. Hideous
                cat = Category.objects.first()
                try:
                    cat = Category.objects.get(name="Partitions à venir")
                except Category.DoesNotExist:
                    pass
                partitionset.category = cat
                partitionset.save()
                sauvegarde = True
                return redirect("partitions:liste")
        context = self.get_context_data()
        context["sauvegarde"] = sauvegarde
        context["error"] = error
        context["form"] = form
        return render(request, self.template_name, context)


class ConfDelete(ChefRequiredMixin, TemplateView):
    template_name = "partitions/conf_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nom"] = self.kwargs.get("nom")
        context["auteur"] = self.kwargs.get("auteur")
        context["id"] = self.kwargs.get("id")
        return context


class DeleteMorc(ChefRequiredMixin, TemplateView):
    model = PartitionSet

    def get(self, request, *args, **kwargs):
        p = get_object_or_404(
            self.model, nom=self.kwargs["nom"], auteur=self.kwargs["auteur"]
        )
        part = p.partition_set.all()
        for pa in part:
            pa.delete()
        p.delete()
        return redirect("partitions:liste")


class ConfDeleteMorc(ChefRequiredMixin, TemplateView):
    template_name = "partitions/conf_delete_morc.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nom"] = self.kwargs.get("nom")
        context["auteur"] = self.kwargs.get("auteur")
        return context


def download(request, nom, auteur, partition_id):

    partition = get_object_or_404(Partition, id=partition_id)
    download_unlogged = partition.morceau.download_unlogged
    if download_unlogged == "o" or request.user.is_authenticated:
        with open(partition.part.path, "rb") as f:
            myfile = File(f)
            response = HttpResponse(content=myfile.read())
            typ = os.path.splitext(myfile.name)[1][1:]
            response["Content-Type"] = "application/%s" % (typ,)
            response["Content-Disposition"] = "attachment; filename=%s_%s_%s.%s" % (
                slugify(nom),
                slugify(auteur),
                slugify(partition.nom),
                typ,
            )
        return response
    else:
        return redirect("login")
