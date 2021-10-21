"""Ossia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from gestion import views as gestion_views

urlpatterns = []
urlpatterns += i18n_patterns(
    path("", gestion_views.Home.as_view(), name="home"),
    path("registration", gestion_views.Inscription.as_view(), name="registration"),
    path("rejoins", gestion_views.Rejoins.as_view(), name="rejoins"),
    path("change", gestion_views.ChangeMembre.as_view(), name="change_membre"),
    path("password", gestion_views.ChangePassword.as_view(), name="change_password"),
    path("thanks", gestion_views.Thanks.as_view(), name="thanks"),
    path("social", gestion_views.Social.as_view(), name="social"),
    path("chef", gestion_views.Chef.as_view(), name="chef"),
    path("profil", gestion_views.Profil.as_view(), name="profile"),
    path("changename", gestion_views.ChangeName.as_view(), name="change-doodle-name"),
    path("logout", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("login", gestion_views.MyLoginView.as_view(), name="login"),
    path("agenda/", include("calendrier.urls", namespace="calendrier")),
    path("partitions/", include("partitions.urls")),
    path(
        "admin/",
        admin.site.urls,
    ),
    path("trombonoscope/", include("trombonoscope.urls")),
    path("actu/", include("actu.urls")),
    path("avatar/", include("avatar.urls")),
    path("photos", gestion_views.PhotoList.as_view(), name="liste_photo"),
    path("add_photo", gestion_views.PhotoCreate.as_view(), name="add_photo"),
    path(
        "photo_edition/<int:pk>", gestion_views.PhotoUpdate.as_view(), name="edit_photo"
    ),
    path(
        "photo_delete/<int:pk>",
        gestion_views.PhotoDelete.as_view(),
        name="delete_photo",
    ),
    path("videos", gestion_views.VideoList.as_view(), name="liste_video"),
    path("add_video", gestion_views.VideoCreate.as_view(), name="add_video"),
    path(
        "video_edition/<int:pk>", gestion_views.VideoUpdate.as_view(), name="edit_video"
    ),
    path(
        "video_delete/<int:pk>",
        gestion_views.VideoDelete.as_view(),
        name="delete_video",
    ),
    prefix_default_language=False,
)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
