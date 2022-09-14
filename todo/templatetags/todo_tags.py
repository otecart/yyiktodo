from django.template import Library
from django.urls import reverse

from ..models import ToDo

register = Library()


@register.simple_tag
def get_back_url(todo: ToDo | str) -> str:
    if not (isinstance(todo, ToDo) or todo == ""):
        raise ValueError(f"{type(todo)} is not of type ToDo or None")
    if isinstance(todo, ToDo):
        return reverse("todo:todo-detail", args=(todo.id,))  # type: ignore
    return reverse("todo:todo-list")
