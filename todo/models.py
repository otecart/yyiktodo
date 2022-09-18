from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

User = get_user_model()


class ToDo(models.Model):
    title = models.CharField(max_length=200, default="To-Do List")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todo_list")
    public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class ToDoEntry(models.Model):
    todo = models.ForeignKey(ToDo, on_delete=models.CASCADE, related_name="entries")
    text = models.CharField(max_length=200, validators=[MinLengthValidator(2)])
    completed = models.BooleanField(default=False)

    def save(self):
        self.todo.save()
        return super().save()

    def delete(self):
        self.todo.save()
        return super().delete()

    def __str__(self) -> str:
        return self.text
