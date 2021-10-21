from django.urls import path

from trombonoscope import views

app_name = "trombonoscope"
urlpatterns = [
    path("", views.Trombonoscope.as_view(), name="view"),
    path("modif_profil", views.ChangeTrombonoscope.as_view(), name="change"),
]
