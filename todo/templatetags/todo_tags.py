from django.template import Library
from django.urls import reverse
from django.utils.html import format_html

from ..models import ToDo

register = Library()


@register.simple_tag
def get_back_url(todo: ToDo | str) -> str:
    if not (isinstance(todo, ToDo) or todo == ""):
        raise ValueError(f"{type(todo)} is not of type ToDo or None")
    if isinstance(todo, ToDo):
        return reverse("todo:todo-detail", args=(todo.id,))  # type: ignore
    return reverse("todo:todo-list")


@register.simple_tag
def toggle_list(path: str) -> str:
    public_list_url = reverse("todo:todo-list")
    my_list_url = reverse("todo:todo-list-my")
    if path == public_list_url:
        return format_html('<a href="{}">Show my lists only</a>', my_list_url)
    if path == my_list_url:
        return format_html('<a href="{}">Show public lists</a>', public_list_url)
    raise ValueError(f"Argument must be either public or user own list url")


@register.simple_tag
def row(classes=""):
    if not classes:
        return format_html('<div class="row">')
    return format_html('<div class="{}">', classes)


@register.simple_tag
def endrow():
    return format_html("</div>")

@register.simple_tag
def col(classes=""):
    if not classes:
        return format_html('<div class="col">')
    return format_html('<div class="{}">', classes)


@register.simple_tag
def endcol():
    return format_html("</div>")
