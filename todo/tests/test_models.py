import time

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from django.utils import timezone

from ..models import Entry, ToDo

User = get_user_model()


class ToDoTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="U_S_E_R",
            password="123",
        )

    def test_todo_create(self):
        todo: ToDo = ToDo.objects.create(
            title="ToDoList",
            owner=self.user,
        )
        self.assertEqual(todo.title, "ToDoList")
        self.assertFalse(todo.public)
        self.assertEqual(todo.owner.username, "U_S_E_R")
        self.assertEqual(self.user.todo_list.first(), todo)

    def test_todo_create_public(self):
        todo: ToDo = ToDo.objects.create(
            title="123",
            owner=self.user,
            public=True,
        )
        self.assertTrue(todo.public)

    def test_todo_create_max_len_title(self):
        todo: ToDo = ToDo.objects.create(
            title="w" * 200,
            owner=self.user,
        )
        self.assertEqual(todo.title, "w" * 200)

    # def test_todo_create_too_long_title_fails(self):
    #     """It should fail but it's not."""
    #     ToDo.objects.create(
    #         title="w" * 201,
    #         owner=self.user,
    #     )

    def test_todo_create_anonymous_fails(self):
        self.assertRaises(
            ValueError,
            ToDo.objects.create,
            title="123123",
            owner=AnonymousUser,
        )

    def test_todo_str_returns_title(self):
        todo: ToDo = ToDo.objects.create(
            title="SomeTitle",
            owner=self.user,
        )
        self.assertEqual(str(todo), "SomeTitle")


class EntryTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="U_S_E_R",
            password="123",
        )
        self.todo: ToDo = ToDo.objects.create(
            title="Title",
            owner=self.user,
        )

    def test_entry_create(self):
        entry: Entry = Entry.objects.create(
            todo=self.todo,
            text="some text",
        )
        self.assertEqual(entry.text, "some text")
        self.assertEqual(entry.todo, self.todo)
        self.assertEqual(entry.todo.owner, self.user)

    # def test_entry_create_short_text_fails(self):
    #     """It should fail but it's not."""
    #     ToDoEntry.objects.create(todo=self.todo, text="")

    def test_entry_create_max_len_text(self):
        entry = Entry.objects.create(
            todo=self.todo,
            text="a" * 200,
        )
        self.assertEqual(entry.text, "a" * 200)

    # def test_entry_create_too_long_text_fails(self):
    #     """It should fail but it's not."""
    #     ToDoEntry.objects.create(
    #         todo=self.todo,
    #         text="a" * 251,
    #     )

    def test_entry_create_updates_todo(self):
        now = timezone.now().timestamp()
        self.assertAlmostEqual(self.todo.created_at.timestamp(), now, 2)
        self.assertAlmostEqual(self.todo.modified_at.timestamp(), now, 2)
        time.sleep(0.1)

        Entry.objects.create(
            todo=self.todo,
            text="awewa",
        )
        now = timezone.now().timestamp()
        self.assertNotAlmostEqual(self.todo.created_at.timestamp(), now, 2)
        self.assertAlmostEqual(self.todo.modified_at.timestamp(), now, 2)

    def test_entry_delete_updates_todo(self):
        entry: Entry = Entry.objects.create(
            todo=self.todo,
            text="awewa",
        )
        now = timezone.now().timestamp()
        self.assertAlmostEqual(self.todo.modified_at.timestamp(), now, 2)
        time.sleep(0.1)

        entry.delete()
        now = timezone.now().timestamp()
        self.assertAlmostEqual(self.todo.modified_at.timestamp(), now, 2)

    def test_entry_str_returns_text(self):
        entry: Entry = Entry.objects.create(
            todo=self.todo,
            text="texttext",
        )
        self.assertEqual(str(entry), "texttext")
