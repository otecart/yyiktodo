from django.urls import path

from .views import (
    EntryCreateView,
    EntryDeleteView,
    EntryEditView,
    MyToDoListView,
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
    path("<int:pk>/", ToDoDetailView.as_view(), name="todo-detail"),
    path("<int:pk>/edit/", ToDoEditView.as_view(), name="todo-edit"),
    path("<int:pk>/delete/", ToDoDeleteView.as_view(), name="todo-delete"),
    path("<int:pk>/create_entry/", EntryCreateView.as_view(), name="entry-create"),
    path("entries/<int:pk>/edit/", EntryEditView.as_view(), name="entry-edit"),
    path("entries/<int:pk>/delete/", EntryDeleteView.as_view(), name="entry-delete"),
    path("users/<str:username>/", UserProfileView.as_view(), name="profile"),
]
