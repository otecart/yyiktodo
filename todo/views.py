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

from todo.forms import EntryForm

from .mixins import AddOwnerMixin
from .models import ToDo, ToDoEntry


class ToDoListView(ListView):
    model = ToDo


class ToDoDetailView(DetailView):
    model = ToDo
    extra_context = {"form": EntryForm()}


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


class EntryCreateView(View):
    def post(self, request, pk: int):
        todo = get_object_or_404(ToDo, pk=pk)
        entry = ToDoEntry(todo=todo, text=request.POST["text"])
        entry.save()
        return redirect(reverse("todo:todo-detail", args=(todo.pk,)))


class EntryEditView(UpdateView):
    model = ToDoEntry
    fields = ["text", "completed"]
    template_name = "todo/entry_form.html"
    context_object_name = "entry"

    def get_success_url(self) -> str:
        return reverse("todo:todo-detail", args=(self.object.todo.pk,))


class EntryDeleteView(DeleteView):
    model = ToDoEntry
    template_name = "todo/entry_confirm_delete.html"
    context_object_name = "entry"

    def get_success_url(self) -> str:
        return reverse("todo:todo-detail", args=(self.object.todo.pk,))
