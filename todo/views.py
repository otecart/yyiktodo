from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)

from .forms import EntryForm
from .mixins import AddOwnerMixin, OrFilteredMultipleMixin, OrFilteredSingleMixin
from .models import ToDo, ToDoEntry


class ToDoListView(OrFilteredMultipleMixin, ListView):
    model = ToDo

    def get_filters(self):
        filters = [Q(public=True)]
        if self.request.user.is_authenticated:
            filters.append(Q(owner=self.request.user))
        return filters


class MyToDoListView(LoginRequiredMixin, OrFilteredMultipleMixin, ListView):
    model = ToDo

    def get_filters(self):
        return [Q(owner=self.request.user)]


class ToDoDetailView(OrFilteredSingleMixin, DetailView):
    model = ToDo
    extra_context = {"entry_form": EntryForm()}

    def get_filters(self):
        filters = [Q(public=True)]
        if self.request.user.is_authenticated:
            filters.append(Q(owner=self.request.user))
        return filters


class ToDoCreateView(AddOwnerMixin, CreateView):
    model = ToDo
    fields = ["title", "public"]
    success_url = reverse_lazy("todo:todo-list")


class ToDoEditView(LoginRequiredMixin, OrFilteredSingleMixin, UpdateView):
    model = ToDo
    fields = ["title", "public"]

    def get_filters(self):
        return [Q(owner=self.request.user)]

    def get_success_url(self) -> str:
        return reverse("todo:todo-detail", args=(self.object.pk,))


class ToDoDeleteView(LoginRequiredMixin, OrFilteredSingleMixin, DeleteView):
    model = ToDo
    success_url = reverse_lazy("todo:todo-list")

    def get_filters(self):
        return [Q(owner=self.request.user)]


class EntryCreateView(LoginRequiredMixin, View):
    def post(self, request, pk: int):
        todo = get_object_or_404(ToDo, pk=pk, owner=self.request.user)
        entry = ToDoEntry(todo=todo, text=request.POST["text"])
        entry.save()
        return redirect(reverse("todo:todo-detail", args=(todo.pk,)))


class EntryEditView(LoginRequiredMixin, OrFilteredSingleMixin, UpdateView):
    model = ToDoEntry
    fields = ["text", "completed"]
    template_name = "todo/entry_form.html"
    context_object_name = "entry"

    def get_filters(self):
        return [Q(todo__owner=self.request.user)]

    def get_success_url(self) -> str:
        return reverse("todo:todo-detail", args=(self.object.todo.pk,))


class EntryDeleteView(LoginRequiredMixin, OrFilteredSingleMixin, DeleteView):
    model = ToDoEntry
    template_name = "todo/entry_confirm_delete.html"
    context_object_name = "entry"

    def get_filters(self):
        return [Q(todo__owner=self.request.user)]

    def get_success_url(self) -> str:
        return reverse("todo:todo-detail", args=(self.object.todo.pk,))
