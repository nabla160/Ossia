from datetime import timedelta

from django.contrib.auth import get_user_model
from django.template.defaultfilters import urlencode
from django.test import Client, TestCase
from django.utils import timezone

from gestion.models import OssiaUser

from ..models import Event

User = get_user_model()


def new_user(username, ossia=False, chef=False):
    u = User.objects.create_user(username=username)
    OssiaUser.objects.create(user=u, slug=username, is_chef=chef, is_ossia=ossia)
    return u


class TestViews(TestCase):
    # TODO: test forms

    def setUp(self):
        # User with different access level and their clients
        chef = new_user("chef", ossia=True, chef=True)
        chef_c = Client()
        chef_c.force_login(chef)
        ossia = new_user("ossia", ossia=True)
        ossia_c = Client()
        ossia_c.force_login(ossia)
        self.client_matrix = [(chef, chef_c), (ossia, ossia_c), (None, Client())]
        # A private and a public event
        now = timezone.now()
        later = now + timedelta(seconds=3600)
        self.priv_event = Event.objects.create(
            nom="private event",
            nomcourt="privevt",
            date=now.date(),
            debut=now.time(),
            fin=later.time(),
            slug="privevt",
            lieu="somewhere",
            calendrier=False,
        )
        self.pub_event = Event.objects.create(
            nom="public event",
            nomcourt="pubevt",
            date=now.date(),
            debut=now.time(),
            fin=later.time(),
            slug="pubevt",
            lieu="somewhere",
            calendrier=True,
        )

    # Everyone can see theses pages

    def _everyone_can_get(self, url, redirect_url=None):
        """Shorthand for checking that every kind of user can get a page"""
        for _, client in self.client_matrix:
            resp = client.get(url)
            if redirect_url:
                self.assertRedirects(resp, redirect_url)
            else:
                self.assertEqual(200, resp.status_code)

    def test_get_home(self):
        url = "/calendar/"
        self._everyone_can_get(url)

    def test_get_calendar(self):
        year, month = 2017, 5
        url = "/calendar/{}/{}".format(year, month)
        self._everyone_can_get(url)

    def test_get_public_event(self):
        """Public event, everyone can see"""
        evt = self.pub_event
        url = "/calendar/{}".format(evt.id)
        self._everyone_can_get(url)

    def test_get_reponse_event(self):
        # XXX: this view sucks
        chef, _ = self.client_matrix[0]
        codereps = ["oui", "non", "pe"]
        for coderep in codereps:
            url = "/calendar/rep/{}/{}/{}".format(
                chef.profile.slug, self.priv_event.slug, coderep
            )
            self._everyone_can_get(url, redirect_url="/calendar/")

    # Only ossia members can get theses pages

    def _get_restricted_page(self, url, chef_only=False, redirect_url=None):
        """Shorthand for testing wether a page in only accessible by ossia members"""

        def user_allowed(user):
            if user is None:
                return False
            if chef_only:
                return user.profile.is_chef
            return True

        for user, client in self.client_matrix:
            # If user is not None, it is an ossia member
            resp = client.get(url)
            if user_allowed(user):
                self.assertEqual(200, resp.status_code)
            else:
                if redirect_url is None:
                    redirect_url = "/login?next={}".format(urlencode(urlencode(url)))
                self.assertRedirects(resp, redirect_url)

    def test_get_private_event(self):
        """Private event, restricted access"""
        evt = self.priv_event
        url = "/calendar/{}".format(evt.id)
        self._get_restricted_page(url, redirect_url="/calendar/")

    def test_get_private_event_bis(self):
        """Private event, restricted access"""
        url = "/calendar/{}".format(self.priv_event.id)
        self._get_restricted_page(url, redirect_url="/calendar/")

    def test_get_new(self):
        """Only chef can create an event"""
        url = "/calendar/new"
        self._get_restricted_page(url, chef_only=True)

    def test_get_edit(self):
        """Only chef can edit an event"""
        url = "/calendar/edition/{}".format(self.pub_event.id)
        self._get_restricted_page(url, chef_only=True)

    def test_get_delete(self):
        """Only chef can delete an event"""
        url = "/calendar/supprimer/{}".format(self.pub_event.id)
        self._get_restricted_page(url, chef_only=True)

    def test_get_resend(self):
        """Only chef can send event emails"""
        url = "/calendar/resend/{}".format(self.pub_event.id)
        self._get_restricted_page(url, chef_only=True)

    def test_get_changename(self):
        """Only authenticated users can have a doodle name"""
        url = "/calendar/changename"
        self._get_restricted_page(url)

    def test_get_answers(self):
        """Only ossia members can see who attends an event"""
        url = "/calendar/{}/reponse".format(self.priv_event.id)
        self._get_restricted_page(url)
