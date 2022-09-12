from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import ModelFormMixin


# class AddOwnerMixin(LoginRequiredMixin, ModelFormMixin):
class AddOwnerMixin(ModelFormMixin):
    """Add current user as owner of created object."""

    def form_valid(self, form):
        obj = form.save(commit=False)
        user = self.request.user
        if user.is_authenticated:
            obj.owner = user
        else:
            obj.owner = None
        obj.save()
        return super().form_valid(form)
