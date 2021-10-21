"""
Administration minimaliste du site de Ossia.
Les chefs peuvent modifier les utilisateurs et les evenements.
Les super-utilisateurs peuvent en plus ajouter ou supprimer ces objets et gerer
les permissions.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, Permission, User

from actu.models import Actu
from gestion.models import OssiaUser, Photo, VideoGallery


class UserProfileInline(admin.StackedInline):
    """Affichage du profil musicien dans la vue UserAdmin"""

    model = OssiaUser


def ProfileInfo(field, short_description, boolean=False):
    def getter(self):
        try:
            return getattr(self.profile, field)
        except OssiaUser.DoesNotExist:
            return ""

    getter.short_description = short_description
    getter.boolean = boolean
    return getter


User.profile_doodlename = ProfileInfo("doodlename", "Nom pour le doodle")
User.profile_phone = ProfileInfo("phone", "Téléphone")
User.profile_instru = ProfileInfo("instru", "Instrument joué")
User.profile_is_ern = ProfileInfo("is_ossia", "Musicien")
User.profile_is_chef = ProfileInfo("is_chef", "Chef Fanfare")
User.profile_get_mails = ProfileInfo("mails", "Recevoir les mails")


class UserProfileAdmin(UserAdmin):
    """
    Management des utilisateurs de ossia.
    Lors de la sauvegarde, les chefs se voient octroyees les permissions
    d'edition des comptes et evenements mais il ne peuvent pas en creer via
    l'interface admin.
    """

    list_display = [
        "username",
        "first_name",
        "last_name",
        "email",
        "profile_doodlename",
        "profile_phone",
        "profile_instru",
        "profile_is_ern",
        "profile_is_chef",
    ]
    list_display_links = ["username", "email", "first_name", "last_name"]
    list_filter = ["profile__instru"]
    ordering = ["username"]
    search_fields = [
        "username",
        "first_name",
        "last_name",
        "profile__phone",
        "profile__instru",
    ]
    inlines = [UserProfileInline]

    staff_fieldsets = [
        ("General", {"fields": ["username", "password", "first_name", "last_name"]}),
        ("Permissions", {"fields": ["is_active"]}),
    ]

    def get_fieldsets(self, request, user=None):
        """
        Les super utilisateurs ont toutes les infos.
        Les autres (e.g. les chefs) ne peuvent modifier qu'un nombre restreints
        de choses.
        """
        if not request.user.is_superuser:
            return self.staff_fieldsets
        return super(UserProfileAdmin, self).get_fieldsets(request, user)

    def save_model(self, request, user, form, change):
        """
        Ajoute le chef au group Chef.
        Le groupe est cree si necessaire.
        """
        chef_group, created = Group.objects.get_or_create(name="Chef")
        if created:
            # Si le groupe vient d'etre crée
            # On associe les bonnes permissions au groupe Chef
            perms = [
                ("change_user", "auth", "user"),
                ("change_event", "calendrier", "event"),
                ("change_ossiauser", "gestion", "ossiauser"),
            ]
            for nat_key in perms:
                perm = Permission.objects.get_by_natural_key(*nat_key)
                chef_group.permissions.add(perm)
            # On met tous les chef dans le groupe
            chef_group.user_set.set(User.objects.filter(profile__is_chef=True))
        # Les chefs sont dans le groupe Chef
        if user.profile.is_chef:
            print("J'aime la choucroute")
            user.is_staff = True
            user.groups.add(chef_group)
        user.save()


admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
admin.site.register(VideoGallery)
admin.site.register(Photo)
admin.site.register(Actu)
