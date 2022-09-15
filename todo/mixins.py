from functools import reduce
from operator import or_
from typing import Callable

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, QuerySet
from django.shortcuts import redirect
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


class FilteredBaseMixin:
    """Base mixin for filtering querysets."""

    filters: list[Q]
    filter_chainer: Callable[[Q, Q], Q]

    def get_filters(self):
        return self.filters


class OrFilteredMixin(FilteredBaseMixin):
    """Semi-base mixin for filtering querysets with `|`."""

    filter_chainer = or_


class FilteredSingleMixin(FilteredBaseMixin, SingleObjectMixin):
    """Add queryset filtering for single object."""

    def get_queryset(self):
        queryset = super().get_queryset()
        total_filter = reduce(self.filter_chainer, self.get_filters())
        return queryset.filter(total_filter)


class OrFilteredSingleMixin(OrFilteredMixin, FilteredSingleMixin):
    """Add queryset filtering with `|` for single object."""


class FilteredMultipleMixin(FilteredBaseMixin, MultipleObjectMixin):
    """Add queryset filtering for multiple object."""

    def get_queryset(self):
        queryset: QuerySet = super().get_queryset()  # type: ignore
        total_filter = reduce(self.filter_chainer, self.get_filters())
        return queryset.filter(total_filter)


class OrFilteredMultipleMixin(OrFilteredMixin, FilteredMultipleMixin):
    """Add queryset filtering with `|` for multiple object."""
