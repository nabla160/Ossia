from django.contrib.auth import get_user_model
from django.core.files import File
from django.template.defaultfilters import urlencode
from django.test import Client, TestCase

from gestion.models import OssiaUser

from ..models import Category, Partition, PartitionSet

User = get_user_model()


def new_user(username, ossia=False, chef=False):
    u = User.objects.create_user(username=username)
    OssiaUser.objects.create(user=u, slug=username, is_chef=chef, is_ossia=ossia)
    return u


class TestViews(TestCase):
    # TODO: add tests for upload/deletions
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
        # A Partition set with 1 partition
        self.pset = PartitionSet.objects.create(
            category=Category.objects.first(), nom="My PSet", auteur="PSet author"
        )
        file = File(open("partitions/tests/test_file.txt"), "test file")
        Partition.objects.create(nom="part1", part=file, morceau=self.pset)

    def tearDown(self):
        """Remove dummy files from media/partitions/"""
        for partition in self.pset.partition_set.all():
            partition.delete()

    def _get_restricted_page(self, url):
        """
        Shorthand for testing wether a page in only accessible by ossia
        members
        """
        for user, client in self.client_matrix:
            # If user is not None, it is an ossia member
            resp = client.get(url)
            if user:
                self.assertEqual(200, resp.status_code)
            else:
                encoded_url = urlencode(urlencode(url))
                redirection_url = "/login?next={}".format(encoded_url)
                self.assertRedirects(resp, redirection_url)

    def test_get_partition_sets(self):
        """The list of all partition sets can be fetched by everyone"""
        for _, client in self.client_matrix:
            resp = client.get("/partitions/")
            self.assertEqual(200, resp.status_code)

    def test_get_partitions(self):
        """
        Only ossia members can see the partitions inside of a partition set
        """
        url = "/partitions/{}/{}".format(self.pset.nom, self.pset.auteur)
        self._get_restricted_page(url)

    def test_see(self):
        """Only ossia members can see partitions"""
        part = self.pset.partition_set.first()
        url = "/partitions/{}/{}/see/{}".format(
            self.pset.nom, self.pset.auteur, part.id
        )
        self._get_restricted_page(url)

    def test_download(self):
        """Only ossia members can download partitions"""
        part = self.pset.partition_set.first()
        url = "/partitions/{}/{}/{}".format(self.pset.nom, self.pset.auteur, part.id)
        self._get_restricted_page(url)

    def test_new(self):
        """Only ossia members can create partiton sets"""
        url = "/partitions/new"
        self._get_restricted_page(url)
