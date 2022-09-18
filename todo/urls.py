from django.urls import path

from .views import (
    EntryCreateView,
    EntryDeleteView,
    EntryEditView,
    MyToDoListView,
    RegisterView,
    ToDoCreateView,
    ToDoDeleteView,
    ToDoDetailView,
    ToDoEditView,
    ToDoListView,
    UserProfileView,
)

app_name = "todo"

urlpatterns = [
    path("", ToDoListView.as_view(), name="todo-list"),
    path("my/", MyToDoListView.as_view(), name="todo-list-my"),
    path("create/", ToDoCreateView.as_view(), name="todo-create"),
    path("todos/<int:pk>/", ToDoDetailView.as_view(), name="todo-detail"),
    path("todos/<int:pk>/edit/", ToDoEditView.as_view(), name="todo-edit"),
    path("todos/<int:pk>/delete/", ToDoDeleteView.as_view(), name="todo-delete"),
    path(
        "todos/<int:pk>/create_entry/", EntryCreateView.as_view(), name="entry-create"
    ),
    path("entries/<int:pk>/edit/", EntryEditView.as_view(), name="entry-edit"),
    path("entries/<int:pk>/delete/", EntryDeleteView.as_view(), name="entry-delete"),
    path("users/register/", RegisterView.as_view(), name="register"),
    path("users/<str:username>/", UserProfileView.as_view(), name="profile"),
]
