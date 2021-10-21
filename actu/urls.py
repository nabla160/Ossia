from django.urls import path

from actu import views

app_name = "actu"
urlpatterns = [
    path("", views.ActuList.as_view(), name="liste"),
    path("ajouter", views.ActuCreate.as_view(), name="add_actu"),
    path("edition/<int:pk>", views.ActuUpdate.as_view(), name="edit_actu"),
    path("supprimer/<int:pk>", views.ActuDelete.as_view(), name="delete_actu"),
]
