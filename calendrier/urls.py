from django.urls import path

from . import views
from .views import EventDelete, EventUpdate

app_name = "calendrier"
urlpatterns = [
    path("", views.Agenda.as_view(), name="liste"),
    path("calendar", views.Home.as_view(), name="home"),
    path("new", views.CreateEvent.as_view(), name="create_event"),
    path("edition/<int:pk>", EventUpdate.as_view(), name="edit_event"),
    path("supprimer/<int:pk>", EventDelete.as_view(), name="delete_event"),
    path("<int:id>/changename", views.ChangeName.as_view(), name="change-doodle-name"),
    path("<int:id>/reponse", views.ReponseEvent.as_view(), name="reponse"),
    path("<int:pYear>/<int:pMonth>", views.Calendar.as_view(), name="view-month"),
    path("<int:id>", views.ViewEvent.as_view(), name="view-event"),
]
