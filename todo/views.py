from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .mixins import AddOwnerMixin
from .models import ToDo, ToDoEntry


class ToDoListView(ListView):
    model = ToDo


class ToDoDetailView(DetailView):
    model = ToDo


class ToDoCreateView(AddOwnerMixin, CreateView):
    model = ToDo
    fields = ["title"]
    success_url = reverse_lazy("todo:todo-list")


class ToDoEditView(UpdateView):
    model = ToDo
    fields = ["title"]

    def get_success_url(self) -> str:
        return reverse("todo:todo-detail", args=(self.object.pk,))


class ToDoDeleteView(DeleteView):
    model = ToDo
    success_url = reverse_lazy("todo:todo-list")
