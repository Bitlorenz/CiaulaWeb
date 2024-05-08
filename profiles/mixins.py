from django.contrib.auth.mixins import LoginRequiredMixin
from profiles.models import UserProfileModel


# mixin per controllare che l'utente che fa la richiesta sia lo stesso che deve essere modificato (dettagli)
class IsSameUserMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        affected_user = UserProfileModel.objects.get(pk=kwargs['pk'])
        if not request.user == affected_user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
