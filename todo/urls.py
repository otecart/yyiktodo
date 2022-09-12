from django.urls import path

from .views import (ToDoCreateView, ToDoDeleteView, ToDoDetailView,
                    ToDoEditView, ToDoListView)

app_name = "todo"

urlpatterns = [
    path("", ToDoListView.as_view(), name="todo-list"),
    path("create/", ToDoCreateView.as_view(), name="todo-create"),
    path("<int:pk>/", ToDoDetailView.as_view(), name="todo-detail"),
    path("<int:pk>/edit/", ToDoEditView.as_view(), name="todo-edit"),
    path("<int:pk>/delete/", ToDoDeleteView.as_view(), name="todo-delete"),
]
