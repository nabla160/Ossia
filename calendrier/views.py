import random
import string
from calendar import monthrange
from collections import defaultdict
from datetime import date, datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic import DeleteView, TemplateView, UpdateView

from actu.models import Actu
from calendrier.calend import EventCalendar
from calendrier.forms import (ChangeDoodleName, EventForm, ModifEventForm,
                              ParticipantsForm)
from calendrier.models import Event, Participants
from gestion.mixins import ChefRequiredMixin
from gestion.models import Photo


def generer(*args):
    caracteres = string.ascii_letters + string.digits
    aleatoire = [random.choice(caracteres) for _ in range(6)]
    return "".join(aleatoire)


def named_month(pMonthNumber):
    return date(1900, pMonthNumber, 1).strftime("%B")


class Agenda(TemplateView):
    template_name = "calendrier/agenda.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("calendrier:home")
        return super(Agenda, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lToday = datetime.today()
        context["photo"] = Photo.objects.filter(cat="liste").order_by("?").first()
        context["events_a_venir"] = (
            Event.objects.filter(date__gte=lToday)
            .exclude(calendrier__iexact="F")
            .exclude(calendrier__iexact="C")
            .order_by("date")
        )
        context["events_passe"] = (
            Event.objects.filter(date__lt=lToday)
            .filter(calendrier__iexact="H")
            .order_by("-date")
        )
        return context


class Calendar(LoginRequiredMixin, TemplateView):
    template_name = "calendrier/home.html"

    @property
    def pYear(self):
        return self.kwargs["pYear"]

    @property
    def pMonth(self):
        return self.kwargs["pMonth"]

    def get_context_data(self, **kwargs):
        context = super(Calendar, self).get_context_data(**kwargs)
        actu = Actu.objects.all()
        photo = Photo.objects.filter(cat="home").order_by("?").first()
        lToday = datetime.now()
        lYear = int(lToday.year)
        lMonth = int(lToday.month)
        lCalendarFromMonth = datetime(lYear, lMonth, 1)
        lCalendarToMonth = datetime(lYear, lMonth, monthrange(lYear, lMonth)[1])
        lEvents = Event.objects.filter(
            date__gte=lCalendarFromMonth, date__lte=lCalendarToMonth
        ).exclude(calendrier__iexact="C").exclude(calendrier__iexact="D")
        lEvents_chef = Event.objects.filter(
            date__gte=lCalendarFromMonth, date__lte=lCalendarToMonth
        )
        lCalendar = EventCalendar(lEvents).formatmonth(lYear, lMonth)
        lCalendar_chef = EventCalendar(lEvents_chef).formatmonth(lYear, lMonth)
        lPreviousYear = lYear
        lPreviousMonth = lMonth - 1
        if lPreviousMonth == 0:
            lPreviousMonth = 12
            lPreviousYear -= 1
        lNextYear = lYear
        lNextMonth = lMonth + 1
        if lNextMonth == 13:
            lNextMonth = 1
            lNextYear = lYear + 1
        lYearAfterThis = lYear + 1
        lYearBeforeThis = lYear - 1

        events_a_venir_not_answered = (
            Event.objects.filter(date__gte=lToday)
            .exclude(participants__participant=self.request.user.profile)
            .exclude(calendrier__iexact="C")
            .exclude(calendrier__iexact="D")
            .order_by("date")
        )
        events_a_venir_answered_yes = (
            Event.objects.filter(date__gte=lToday)
            .filter(
                Q(participants__participant=self.request.user.profile)
                & Q(participants__reponse="oui")
            )
            .exclude(calendrier__iexact="C")
            .exclude(calendrier__iexact="D")
            .order_by("date")
        )
        events_a_venir_answered_no = (
            Event.objects.filter(date__gte=lToday)
            .filter(
                Q(participants__participant=self.request.user.profile)
                & Q(participants__reponse="non")
            )
            .exclude(calendrier__iexact="C")
            .exclude(calendrier__iexact="D")
            .order_by("date")
        )
        events_a_venir_answered_pe = (
            Event.objects.filter(date__gte=lToday)
            .filter(
                Q(participants__participant=self.request.user.profile)
                & Q(participants__reponse="pe")
            )
            .exclude(calendrier__iexact="C")
            .exclude(calendrier__iexact="D")
            .order_by("date")
        )
        events_a_venir_chef = (
            Event.objects.filter(date__gte=lToday)
            .filter(calendrier__in=["C"])
            .order_by("date")
        )
        events_a_venir_chef_public = (
            Event.objects.filter(date__gte=lToday)
            .filter(calendrier__in=["D"])
            .order_by("date")
        )

        context["Calendar"] = mark_safe(lCalendar)
        context["Calendar_chef"] = mark_safe(lCalendar_chef)
        context["Month"] = lMonth
        context["MonthName"] = named_month(lMonth)
        context["Year"] = lYear
        context["PreviousMonth"] = lPreviousMonth
        context["PreviousMonthName"] = named_month(lPreviousMonth)
        context["PreviousYear"] = lPreviousYear
        context["NextMonth"] = lNextMonth
        context["NextMonthName"] = named_month(lNextMonth)
        context["NextYear"] = lNextYear
        context["YearBeforeThis"] = lYearBeforeThis
        context["YearAfterThis"] = lYearAfterThis
        context["events_a_venir_answered_yes"] = events_a_venir_answered_yes
        context["events_a_venir_answered_no"] = events_a_venir_answered_no
        context["events_a_venir_answered_pe"] = events_a_venir_answered_pe
        context["events_a_venir_not_answered"] = events_a_venir_not_answered
        context["events_a_venir_chef"] = events_a_venir_chef
        context["events_a_venir_chef_public"] = events_a_venir_chef_public
        context["actu"] = actu
        context["photo"] = photo
        return context


class Home(Calendar):
    lToday = datetime.now()


class ViewEvent(LoginRequiredMixin, TemplateView):
    template_name = "calendrier/view_event.html"

    def get_context_data(self, **kwargs):
        context = super(ViewEvent, self).get_context_data(**kwargs)
        event = get_object_or_404(Event, id=self.kwargs["id"])
        participants = event.participants_set.all()


        # Restricted event, only erneso users can see it
        if not self.request.user.is_authenticated and not event.calendrier:
            return redirect(reverse("calendrier:home"))

        # Count the number of occurences of each instrument
        instrument_count = defaultdict(lambda: (0, 0, [], [], []))
        for participant in participants:
            instru = participant.participant.instru
            if instru == "Autre":
                instru = participant.participant.instru_autre
            if participant.dont_play_main == "Oui":
                instru = participant.instrument

            sure, maybe, namesoui, namespe, namesnon = instrument_count[instru]

            if participant.reponse == "oui":

                namesoui += [participant.participant.get_doodlename()]
                instrument_count[instru] = (
                    sure + 1,
                    maybe,
                    namesoui,
                    namespe,
                    namesnon,
                )
            elif participant.reponse == "pe":
                namespe += [participant.participant.get_doodlename()]
                instrument_count[instru] = (
                    sure,
                    maybe + 1,
                    namesoui,
                    namespe,
                    namesnon,
                )
            else:
                namesnon += [participant.participant.get_doodlename()]
                instrument_count[instru] = (sure, maybe, namesoui, namespe, namesnon)

        instrument_count = [
            (instrument, sure, maybe, namesoui, namespe, namesnon)
            for instrument, (
                sure,
                maybe,
                namesoui,
                namespe,
                namesnon,
            ) in instrument_count.items()
        ]

        context["event"] = event
        context["instrument_count"] = instrument_count
        context["participants"] = participants
        context["nboui"] = len(participants.filter(reponse="oui"))
        context["nbpe"] = len(participants.filter(reponse="pe"))
        context["nbnon"] = len(participants.filter(reponse="non"))
        context["chef_only"] = (event.calendrier == "C")|(event.calendrier == "D")
        return context


class ChangeName(LoginRequiredMixin, TemplateView):
    form_class = ChangeDoodleName
    template_name = "calendrier/changename.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class(instance=self.request.user)
        context["id"] = self.kwargs["id"]
        return context

    def post(self, request, *args, **kwargs):
        success = False
        requbis = request.POST.copy()
        form = self.form_class(requbis, instance=request.user)
        if form.is_valid():
            form.save()
            success = True
            return redirect("calendrier:view-event", id=self.kwargs["id"])
        else:
            context = self.get_context_data()
            context["success"] = success
            return render(request, self.template_name, context)


class CreateEvent(LoginRequiredMixin, TemplateView):
    form_class = EventForm
    template_name = "calendrier/create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            temp = True
            while temp:
                code = generer()
                try:
                    Event.objects.get(slug=code)
                except Event.DoesNotExist:
                    temp = False
            date = form.cleaned_data["date"]
            date = date.strftime("%d/%m/%Y")
            obj = form.save(commit=False)
            obj.slug = code
            obj.save()
            id = obj.id
            return redirect("calendrier:view-event", id=id)
        else:
            context = self.get_context_data()
            return render(request, self.template_name, context)


class ReponseEvent(LoginRequiredMixin, TemplateView):
    form_class = ParticipantsForm
    template_name = "calendrier/reponse.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ev = get_object_or_404(Event, id=self.kwargs["id"])
        try:
            context["form"] = self.form_class(
                instance=Participants.objects.get(
                    event=ev, participant=self.request.user.profile
                )
            )
        except Participants.DoesNotExist:
            context["form"] = self.form_class()
        context["ev"] = get_object_or_404(Event, id=self.kwargs["id"])
        context["id"] = self.kwargs["id"]
        context["chef_only"]  = (context["ev"].calendrier == "C")|(context["ev"].calendrier == "D")
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        ev = get_object_or_404(Event, id=self.kwargs["id"])
        part = request.user.profile
        if form.is_valid():
            try:
                p = Participants.objects.get(event=ev, participant=part)
                p.delete()
            except Participants.DoesNotExist:
                pass
            obj = form.save(commit=False)
            obj.event = ev
            obj.participant = part
            obj.save()
            return redirect("calendrier:view-event", id=self.kwargs["id"])
        else:
            context = self.get_context_data()
            return render(request, self.template_name, context)


class EventUpdate(ChefRequiredMixin, UpdateView):
    model = Event
    template_name = "calendrier/update.html"
    form_class = ModifEventForm

    def get_context_data(self, **kwargs):
        ctx = super(EventUpdate, self).get_context_data(**kwargs)
        ctx["id"] = self.get_object().id
        return ctx

    def get_success_url(self):
        return reverse("calendrier:view-event", kwargs={"id": self.get_object().id})


class EventDelete(ChefRequiredMixin, DeleteView):
    model = Event
    template_name = "calendrier/delete.html"
    success_url = reverse_lazy("calendrier:home")

    def get_context_data(self, **kwargs):
        ctx = super(EventDelete, self).get_context_data(**kwargs)
        ctx["id"] = self.get_object().id
        return ctx
