from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from actu.models import Actu
from gestion.mixins import ChefRequiredMixin


class ActuList(ChefRequiredMixin, ListView):
    model = Actu
    context_object_name = "actus"
    template_name = "actu/actualité.html"


class ActuCreate(ChefRequiredMixin, CreateView):
    model = Actu
    fields = ["text", "order", "text_en"]
    template_name = "actu/create_actu.html"
    success_url = reverse_lazy("actu:liste")

    def form_valid(self, form):
        actu = form.save(commit=False)
        actu.save()
        return HttpResponseRedirect(self.success_url)


class ActuUpdate(ChefRequiredMixin, UpdateView):
    model = Actu
    fields = ["text", "order", "text_en"]
    template_name = "actu/update_actu.html"
    success_url = reverse_lazy("actu:liste")


class ActuDelete(ChefRequiredMixin, DeleteView):
    model = Actu
    template_name = "actu/delete_actu.html"
    success_url = reverse_lazy("actu:liste")
