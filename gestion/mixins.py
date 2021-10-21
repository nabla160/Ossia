from django.contrib.auth.mixins import UserPassesTestMixin


class ChefRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return (user is not None) and hasattr(user, "profile") and user.profile.is_chef
