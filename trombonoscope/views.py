from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from gestion.models import OssiaUser
from trombonoscope.forms import ChangeTrombonoscope


class ChangeTrombonoscope(LoginRequiredMixin, TemplateView):
    form_class = ChangeTrombonoscope
    template_name = "trombonoscope/changetrombonoscope.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.form_class(instance=self.request.user.profile)
        context["form"] = form
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(
            request.POST, request.FILES, instance=request.user.profile
        )
        if form.is_valid():
            form.save()
            return redirect("trombonoscope:view")
        context = self.get_context_data()
        context["form"] = form
        return render(request, self.template_name, context)


class Trombonoscope(LoginRequiredMixin, TemplateView):
    template_name = "trombonoscope/trombonoscope.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trombonoscope_vieux"] = OssiaUser.objects.filter(trombonoscope="o_v")
        context["trombonoscope_actuel"] = OssiaUser.objects.filter(
            trombonoscope="o_a"
        )
        return context
