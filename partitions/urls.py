from django.urls import path

from . import views

app_name = "partitions"
urlpatterns = [
    path("", views.Repertoire.as_view(), name="liste"),
    path("download", views.download_musecores, name="download_musecores"),
    path("<str:nom>/<str:auteur>/upload", views.Upload.as_view(), name="upload"),
    path("<str:nom>/<str:auteur>", views.Morceau.as_view(), name="listepart"),
    path("<str:nom>/<str:auteur>/see/<int:partition_id>", views.see, name="see"),
    path("<str:nom>/<str:auteur>/<int:partition_id>", views.download, name="download"),
    path(
        "<str:nom>/<str:auteur>/<int:id>/conf",
        views.ConfDelete.as_view(),
        name="conf_delete",
    ),
    path(
        "<str:nom>/<str:auteur>/<int:id>/delete",
        views.DeletePart.as_view(),
        name="delete",
    ),
    path(
        "<str:nom>/<str:auteur>/delete", views.DeleteMorc.as_view(), name="delete_morc"
    ),
    path(
        "<str:nom>/<str:auteur>/conf",
        views.ConfDeleteMorc.as_view(),
        name="conf_delete_morc",
    ),
    path("new", views.CreateMorc.as_view(), name="ajouter_morceau"),
]
