from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class EngilorianRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and getattr(user, 'is_engilorian', False)

    def handle_no_permission(self):
        raise PermissionDenied("You must be an Engilorian to perform this action.")



class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and getattr(user, 'is_admin', False)

    def handle_no_permission(self):
        raise PermissionDenied("You must be an Admin to perform this action.")
