import random
import string

from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (CreateView, DeleteView, ListView,
                                  TemplateView, UpdateView)
import os

from calendrier.forms import ChangeDoodleName
from gestion.forms import (ChangeFormUser, ChangeMembreForm,
                           InscriptionMembreForm, RegistrationFormUser)
from gestion.mixins import ChefRequiredMixin
from gestion.models import OssiaUser, Photo, VideoGallery
from partitions.models import Category


def generer(*args):
    caracteres = string.ascii_letters + string.digits
    aleatoire = [random.choice(caracteres) for i in range(6)]
    return "".join(aleatoire)


class Home(TemplateView):
    template_name = "gestion/index.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("calendrier:home")
        return super(Home, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.filter(
            name="Partitions actives"
        ).prefetch_related("partitionset_set")
        context["videos"] = VideoGallery.objects.all().order_by("order")
        context["photo_rep"] = (
            Photo.objects.filter(cat="home_rep").order_by("?").first()
        )
        context["photo_join"] = (
            Photo.objects.filter(cat="home_join").order_by("?").first()
        )
        context["photo_contact"] = (
            Photo.objects.filter(cat="home_contact").order_by("?").first()
        )
        return context


class MyLoginView(LoginView):

    template_name = "gestion/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["photo"] = Photo.objects.filter(cat="login").order_by("?").first()
        return context


class Rejoins(TemplateView):
    template_name = "gestion/rejoins.html"

class Thanks(TemplateView):
    template_name = "gestion/thanks.html"


class Social(LoginRequiredMixin, TemplateView):
    template_name = "gestion/social.html"


class Profil(LoginRequiredMixin, TemplateView):
    template_name = "gestion/profile.html"


class Chef(ChefRequiredMixin, TemplateView):
    template_name = "gestion/chef.html"


class ChangeName(LoginRequiredMixin, TemplateView):
    form_class = ChangeDoodleName
    template_name = "gestion/changename.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class(instance=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        requbis = request.POST.copy()
        form = self.form_class(requbis, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("change_membre")

        context = self.get_context_data()
        context["form"] = form
        return render(request, self.template_name, context)


class ChangeMembre(LoginRequiredMixin, TemplateView):
    comp_form_class = ChangeMembreForm
    user_form_class = ChangeFormUser
    template_name = "gestion/change.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comp_form = self.comp_form_class(instance=self.request.user.profile)
        user_form = self.user_form_class(instance=self.request.user)
        context["comp_form"] = comp_form
        context["user_form"] = user_form
        context["photo"] = (
            Photo.objects.filter(cat="change_membre").order_by("?").first()
        )
        return context

    def post(self, request, *args, **kwargs):
        success = False
        comp_form = self.comp_form_class(request.POST, instance=request.user.profile)
        user_form = self.user_form_class(request.POST, instance=request.user)
        if user_form.is_valid() and comp_form.is_valid():
            user_form.save()
            comp_form.save()
            success = True

        context = self.get_context_data()
        context["success"] = success
        context["comp_form"] = comp_form
        context["user_form"] = user_form
        return render(request, self.template_name, context)


class ChangePassword(LoginRequiredMixin, TemplateView):
    form_class = PasswordChangeForm
    template_name = "gestion/changepasswd.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class(self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        requbis = request.POST.copy()
        success = False
        form = self.form_class(request.user, data=requbis)
        if form.is_valid():
            form.save()
            success = True
        context = self.get_context_data()
        context["success"] = success
        context["form"] = form
        return render(request, self.template_name, context)


class Inscription(TemplateView):
    user_form_class = RegistrationFormUser
    comp_form_class = InscriptionMembreForm
    template_name = "gestion/registration.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comp_form"] = self.comp_form_class()
        context["user_form"] = self.user_form_class()
        context["photo"] = (
            Photo.objects.filter(cat="inscription_membre").order_by("?").first()
        )
        return context

    def post(self, request, *args, **kwargs):
        user_form = self.user_form_class(request.POST)
        comp_form = self.comp_form_class(request.POST)
        if user_form.is_valid() and comp_form.is_valid():

            if not (
                comp_form.cleaned_data["validation"] == settings.ACCOUNT_CREATION_PASS
            ):
                error = _("Le champ Validation ne correspond pas à celui attendu")
                context = self.get_context_data()
                context["user_form"] = user_form
                context["comp_form"] = comp_form
                context["error"] = error
                return render(request, self.template_name, context)
            member = user_form.save(commit=False)
            temp = True
            while temp:
                code = generer()
                try:
                    OssiaUser.objects.get(slug=code)
                except OssiaUser.DoesNotExist:
                    temp = False
            member.save()
            (profile, k) = OssiaUser.objects.get_or_create(user=member, slug=code)
            comp_form = self.comp_form_class(request.POST, instance=profile)
            obj = comp_form.save(commit=False)
            obj.slug = code
            obj.save()
            return redirect("thanks")
        else:
            context = self.get_context_data()
            context["user_form"] = user_form
            context["comp_form"] = comp_form
            return render(request, self.template_name, context)


class PhotoList(ChefRequiredMixin, ListView):
    model = Photo
    context_object_name = "photos"
    ordering = "cat"
    template_name = "gestion/photo.html"


class PhotoCreate(ChefRequiredMixin, CreateView):
    model = Photo
    fields = ["name", "cat", "auteur", "url", "color", "image"]
    template_name = "gestion/create_photo.html"
    success_url = reverse_lazy("liste_photo")

    def form_valid(self, form):
        photo = form.save(commit=False)
        photo.save()
        return HttpResponseRedirect(self.success_url)


class PhotoUpdate(ChefRequiredMixin, UpdateView):
    model = Photo
    fields = ["name", "cat", "auteur", "url", "color", "image"]
    template_name = "gestion/update_photo.html"
    success_url = reverse_lazy("liste_photo")


class PhotoDelete(ChefRequiredMixin, DeleteView):
    model = Photo
    template_name = "gestion/delete_photo.html"
    success_url = reverse_lazy("liste_photo")


class VideoList(ChefRequiredMixin, ListView):
    model = VideoGallery
    ordering = "order"
    context_object_name = "videos"
    template_name = "gestion/video.html"


class VideoCreate(ChefRequiredMixin, CreateView):
    model = VideoGallery
    fields = ["name", "url", "order"]
    template_name = "gestion/create_video.html"
    success_url = reverse_lazy("liste_video")

    def form_valid(self, form):
        video = form.save(commit=False)
        video.save()
        return HttpResponseRedirect(self.success_url)


class VideoUpdate(ChefRequiredMixin, UpdateView):
    model = VideoGallery
    fields = ["name", "url", "order"]
    template_name = "gestion/update_video.html"
    success_url = reverse_lazy("liste_video")


class VideoDelete(ChefRequiredMixin, DeleteView):
    model = VideoGallery
    template_name = "gestion/delete_video.html"
    success_url = reverse_lazy("liste_video")
