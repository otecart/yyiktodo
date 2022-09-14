from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import ModelFormMixin
from django.views.generic.list import MultipleObjectMixin


class AddOwnerMixin(LoginRequiredMixin, ModelFormMixin):
    """Add current user as owner of created object."""

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user  # type: ignore
        self.object.save()
        return redirect(self.get_success_url())


class OwnedOnlyListMixin(MultipleObjectMixin, View):
    """Returns only user owned list of objects."""

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.model._default_manager.filter(owner=self.request.user)  # type: ignore
        return self.model._default_manager.none()  # type: ignore


class OwnedOnlyDetailMixin(LoginRequiredMixin, SingleObjectMixin, View):
    """Returns only user owned object."""

    def get_queryset(self):
        return self.model._default_manager.filter(owner=self.request.user)
