from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class ToDo(models.Model):
    title = models.CharField(max_length=200, default="To-Do List")
    owner = models.ForeignKey(
        User, null=True, on_delete=models.CASCADE, related_name="todo_lists"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class ToDoEntry(models.Model):
    list = models.ForeignKey(ToDo, on_delete=models.CASCADE, related_name="entries")
    text = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.text
