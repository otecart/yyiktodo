from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Entry, ToDo

User = get_user_model()


class ViewsTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.user1 = User.objects.create(
            username="user1",
            password="pass1",
        )
        self.user2 = User.objects.create(
            username="user2",
            password="pass2",
        )

        ToDo.objects.bulk_create(
            [
                ToDo(
                    title="User1 public list",
                    owner=self.user1,
                    public=True,
                ),
                ToDo(
                    title="User1 private list",
                    owner=self.user1,
                ),
                ToDo(
                    title="User2 public list 1",
                    owner=self.user2,
                    public=True,
                ),
                ToDo(
                    title="User2 private list",
                    owner=self.user2,
                ),
                ToDo(
                    title="User2 public list 2",
                    owner=self.user2,
                    public=True,
                ),
            ]
        )
        Entry.objects.bulk_create(
            [
                Entry(
                    todo=get_todo(1),
                    text="1.1.Text",
                    completed=True,
                ),
                Entry(
                    todo=get_todo(1),
                    text="1.2.Text",
                ),
                Entry(
                    todo=get_todo(2),
                    text="2.1.Text",
                ),
                Entry(
                    todo=get_todo(3),
                    text="3.1.Text",
                    completed=True,
                ),
                Entry(
                    todo=get_todo(3),
                    text="3.2.Text",
                    completed=True,
                ),
            ]
        )

        self.list_path = reverse("todo:todo-list")
        self.my_list_path = reverse("todo:todo-list-my")
        self.profile = lambda username: reverse("todo:profile", args=(username,))
        self.todo_detail = lambda pk: reverse("todo:todo-detail", args=(pk,))
        self.todo_create = reverse("todo:todo-create")
        self.todo_edit = lambda pk: reverse("todo:todo-edit", args=(pk,))
        self.todo_delete = lambda pk: reverse("todo:todo-delete", args=(pk,))
        self.entry_create = lambda todo_id: reverse(
            "todo:entry-create", args=(todo_id,)
        )
        self.entry_edit = lambda pk: reverse("todo:entry-edit", args=(pk,))
        self.entry_delete = lambda pk: reverse("todo:entry-delete", args=(pk,))

    def test_todo_list_template(self):
        response = self.client.get(self.list_path)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todo/todo_list.html")  # type: ignore

    def test_todo_list_anonymous_shows_public(self):
        response = self.client.get(self.list_path)

        self.assertContains(response, "User1 public list")
        self.assertContains(response, "User2 public list 1")
        self.assertContains(response, "User2 public list 2")

    def test_todo_list_hides_anonymous_hides_private(self):
        response = self.client.get(self.list_path)

        self.assertNotContains(response, "User1 private list")  # type: ignore
        self.assertNotContains(response, "User2 private list")  # type: ignore

    def test_todo_list_user_shows_public_and_own(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.list_path)

        self.assertContains(response, "User1 public list")
        self.assertContains(response, "User1 private list")
        self.assertContains(response, "User2 public list 1")
        self.assertContains(response, "User2 public list 2")

    def test_todo_list_user_hides_not_own_private(self):
        self.client.force_login(self.user2)
        response = self.client.get(self.list_path)

        self.assertNotContains(response, "User1 private list")  # type: ignore

    def test_my_todo_list_template(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.my_list_path)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todo/todo_list.html")  # type: ignore

    def test_my_todo_list_anonymous_redirects(self):
        response = self.client.get(self.my_list_path, follow=True)

        url = login_plus_next(self.my_list_path)
        self.assertRedirects(response, url)  # type: ignore

    def test_my_todo_shows_own(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.my_list_path)

        self.assertContains(response, "User1 public list")
        self.assertContains(response, "User1 private list")

    def test_my_todo_hides_not_own(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.my_list_path)

        self.assertNotContains(response, "User2 public list 1")  # type: ignore
        self.assertNotContains(response, "User2 public list 2")  # type: ignore
        self.assertNotContains(response, "User2 private list")  # type: ignore

    def test_profile_template(self):
        response = self.client.get(self.profile("user1"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todo/profile.html")  # type: ignore

    def test_profile_404(self):
        response = self.client.get(self.profile("user3"))

        self.assertEqual(response.status_code, 404)

    def test_profile_shows_user_public(self):
        response = self.client.get(self.profile("user1"))

        self.assertContains(response, "User1 public list")

    def test_profile_hides_user_private(self):
        response = self.client.get(self.profile("user1"))

        self.assertNotContains(response, "User1 private list")  # type: ignore

    def test_profile_hides_another(self):
        response = self.client.get(self.profile("user2"))

        self.assertNotContains(response, "User1 public list")  # type: ignore
        self.assertNotContains(response, "User1 private list")  # type: ignore

    def test_todo_detail_template(self):
        response = self.client.get(self.todo_detail(1))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todo/todo_detail.html")  # type: ignore

    def test_todo_detail_404(self):
        response = self.client.get(self.todo_detail(10))

        self.assertEqual(response.status_code, 404)

    def test_todo_detail_private_anonymous_returns_404(self):
        response = self.client.get(self.todo_detail(2))

        self.assertEqual(response.status_code, 404)

    def test_todo_detail_private_not_owner_returns_404(self):
        self.client.force_login(self.user2)
        response = self.client.get(self.todo_detail(2))

        self.assertEqual(response.status_code, 404)

    def test_todo_detail_private_owner_shows_entries(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.todo_detail(2))

        self.assertContains(response, "User1 private list")
        self.assertContains(response, "2.1.Text")

    def test_todo_detail_public_shows_its_entries(self):
        response = self.client.get(self.todo_detail(1))

        self.assertContains(response, "User1 public list")
        self.assertContains(response, "1.1.Text")
        self.assertContains(response, "1.2.Text")

    def test_todo_detail_public_hides_another_entries(self):
        response = self.client.get(self.todo_detail(1))

        self.assertNotContains(response, "2.1.Text")  # type: ignore
        self.assertNotContains(response, "3.1.Text")  # type: ignore
        self.assertNotContains(response, "3.2.Text")  # type: ignore

    def test_todo_detail_public_anonymous_hides_editing(self):
        response = self.client.get(self.todo_detail(1))

        self.assertNotContains(response, reverse("todo:todo-edit", args=(1,)))  # type: ignore
        self.assertNotContains(response, reverse("todo:todo-delete", args=(1,)))  # type: ignore
        self.assertNotContains(response, reverse("todo:entry-edit", args=(1,)))  # type: ignore
        self.assertNotContains(response, reverse("todo:entry-delete", args=(1,)))  # type: ignore
        self.assertNotContains(response, reverse("todo:entry-edit", args=(2,)))  # type: ignore
        self.assertNotContains(response, reverse("todo:entry-delete", args=(2,)))  # type: ignore

    def test_todo_detail_public_not_owner_hides_editing(self):
        self.client.force_login(self.user2)
        response = self.client.get(self.todo_detail(1))

        self.assertNotContains(response, reverse("todo:todo-edit", args=(1,)))  # type: ignore
        self.assertNotContains(response, reverse("todo:todo-delete", args=(1,)))  # type: ignore
        self.assertNotContains(response, reverse("todo:entry-edit", args=(1,)))  # type: ignore
        self.assertNotContains(response, reverse("todo:entry-delete", args=(1,)))  # type: ignore
        self.assertNotContains(response, reverse("todo:entry-edit", args=(2,)))  # type: ignore
        self.assertNotContains(response, reverse("todo:entry-delete", args=(2,)))  # type: ignore
        self.assertNotContains(response, reverse("todo:entry-create", args=(1,)))  # type: ignore

    def test_todo_detail_owner_shows_editing(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.todo_detail(1))

        self.assertContains(response, reverse("todo:todo-edit", args=(1,)))
        self.assertContains(response, reverse("todo:todo-delete", args=(1,)))
        self.assertContains(response, reverse("todo:entry-edit", args=(1,)))
        self.assertContains(response, reverse("todo:entry-delete", args=(1,)))
        self.assertContains(response, reverse("todo:entry-edit", args=(2,)))
        self.assertContains(response, reverse("todo:entry-delete", args=(2,)))
        self.assertContains(response, reverse("todo:entry-create", args=(1,)))

    def test_todo_create_anonymous_redirects(self):
        response = self.client.get(self.todo_create, follow=True)

        url = login_plus_next(self.todo_create)
        self.assertRedirects(response, url)  # type: ignore

    def test_todo_create_user_template(self):
        self.client.force_login(self.user2)
        response = self.client.get(self.todo_create)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todo/todo_form.html")  # type: ignore

    def test_todo_create_POST_anonymous_fails(self):
        data = {"title": "QWERTY"}
        self.client.post(self.todo_create, data)

        self.assertFalse(ToDo.objects.filter(title="QWERTY").exists())

    def test_todo_create_POST_implicit_public(self):
        self.client.force_login(self.user1)
        data = {"title": "QWERTY"}
        self.client.post(self.todo_create, data)

        self.assertTrue(ToDo.objects.filter(title="QWERTY").exists())
        todo = ToDo.objects.get(title="QWERTY")
        self.assertEqual(todo.owner, self.user1)
        self.assertIs(todo.public, False)

    def test_todo_create_POST(self):
        self.client.force_login(self.user1)
        data = {"title": "QWERTY", "public": True}
        self.client.post(self.todo_create, data)

        self.assertTrue(ToDo.objects.filter(title="QWERTY").exists())
        todo = ToDo.objects.get(title="QWERTY")
        self.assertEqual(todo.owner, self.user1)
        self.assertIs(todo.public, True)

    # def test_todo_create_user_has_form(self):
    #     self.client.force_login(self.user2)
    #     response = self.client.get(self.todo_create)

    #     self.assertContains(
    #         response,
    #         '<form method="POST">',
    #         html=True,
    #     )
    #     self.assertContains(
    #         response,
    #         '<input name="title">',
    #         html=True,
    #     )
    #     self.assertContains(
    #         response,
    #         '<input name="public">',
    #         html=True,
    #     )

    def test_todo_edit_anonymous_redirects(self):
        response = self.client.get(self.todo_edit(3), follow=True)

        url = login_plus_next(self.todo_edit(3))
        self.assertRedirects(response, url)  # type: ignore

    def test_todo_edit_non_owner_returns_404(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.todo_edit(3), follow=True)

        self.assertEqual(response.status_code, 404)

    def test_todo_edit_owner_template(self):
        self.client.force_login(self.user2)
        response = self.client.get(self.todo_edit(3), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todo/todo_form.html")  # type: ignore

    def test_todo_edit_POST_anonymous_fails(self):
        data = {"title": "QWERTY", "public": False}
        self.client.post(self.todo_edit(3), data)

        self.assertFalse(ToDo.objects.filter(title="QWERTY").exists())
        self.assertIsNot(get_todo(3).public, False)

    def test_todo_edit_POST_non_owner_fails(self):
        self.client.force_login(self.user1)
        data = {"title": "QWERTY", "public": False}
        self.client.post(self.todo_edit(3), data)

        self.assertFalse(ToDo.objects.filter(title="QWERTY").exists())
        self.assertIsNot(get_todo(3).public, False)

    def test_todo_edit_POST_owner(self):
        self.client.force_login(self.user2)
        data = {"title": "QWERTY", "public": False}
        self.client.post(self.todo_edit(3), data)

        self.assertTrue(ToDo.objects.filter(title="QWERTY").exists())
        self.assertIs(get_todo(3).public, False)

    def test_todo_delete_anonymous_redirects(self):
        response = self.client.get(self.todo_delete(3), follow=True)

        url = login_plus_next(self.todo_delete(3))
        self.assertRedirects(response, url)  # type: ignore

    def test_todo_delete_non_onwer_returns_404(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.todo_delete(3))

        self.assertEqual(response.status_code, 404)

    def test_todo_delete_owner_template(self):
        self.client.force_login(self.user2)
        response = self.client.get(self.todo_delete(3))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todo/todo_confirm_delete.html")  # type: ignore

    def test_todo_delete_POST_anonymous_fails(self):
        self.client.post(self.todo_delete(3))

        self.assertTrue(ToDo.objects.filter(pk=3).exists())

    def test_todo_delete_POST_non_owner_fails(self):
        self.client.force_login(self.user1)
        self.client.post(self.todo_delete(3))

        self.assertTrue(ToDo.objects.filter(pk=3).exists())

    def test_todo_delete_POST_owner(self):
        self.client.force_login(self.user2)
        self.client.post(self.todo_delete(3))

        self.assertFalse(ToDo.objects.filter(pk=3).exists())

    def test_entry_create_anonymous_redirects(self):
        response = self.client.get(self.entry_create(3), follow=True)

        url = login_plus_next(self.entry_create(3))
        self.assertRedirects(response, url)  # type: ignore

    def test_entry_create_private_non_owner_redirects_and_404(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.entry_create(4), follow=True)

        url = self.todo_detail(4)
        self.assertRedirects(response, url, target_status_code=404)  # type: ignore

    def test_entry_create_owner_redirects(self):
        self.client.force_login(self.user2)
        response = self.client.get(self.entry_create(4), follow=True)

        url = self.todo_detail(4)
        self.assertRedirects(response, url)  # type: ignore

    def test_entry_create_POST_anonymous_fails(self):
        data = {"text": "la-la-la"}
        self.client.post(self.entry_create(3), data)

        self.assertFalse(Entry.objects.filter(text="la-la-la").exists())

    def test_entry_create_POST_non_owner_fails(self):
        self.client.force_login(self.user1)
        data = {"text": "la-la-la"}
        self.client.post(self.entry_create(3), data)

        self.assertFalse(Entry.objects.filter(text="la-la-la").exists())

    def test_entry_create_POST_owner(self):
        self.client.force_login(self.user2)
        data = {"text": "la-la-la"}
        self.client.post(self.entry_create(3), data)

        self.assertTrue(Entry.objects.filter(text="la-la-la").exists())

    def test_entry_edit_anonymous_redirects(self):
        response = self.client.get(self.entry_edit(4), follow=True)

        url = login_plus_next(self.entry_edit(4))
        self.assertRedirects(response, url)  # type: ignore

    def test_entry_edit_non_owner_returns_404(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.entry_edit(4))

        self.assertEqual(response.status_code, 404)

    def test_entry_edit_owner_template(self):
        self.client.force_login(self.user2)
        response = self.client.get(self.entry_edit(4))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todo/entry_form.html")  # type: ignore

    def test_entry_edit_POST_anonymous_fails(self):
        data = {"text": "la-la-la", "completed": False}
        self.client.post(self.entry_edit(4), data)

        entry = get_entry(4)
        self.assertFalse(Entry.objects.filter(text="la-la-la").exists())
        self.assertIs(entry.completed, True)

    def test_entry_edit_POST_non_owner_fails(self):
        self.client.force_login(self.user1)
        data = {"text": "la-la-la", "completed": False}
        self.client.post(self.entry_edit(4), data)

        entry = get_entry(4)
        self.assertFalse(Entry.objects.filter(text="la-la-la").exists())
        self.assertIs(entry.completed, True)

    def test_entry_edit_POST_owner(self):
        self.client.force_login(self.user2)
        data = {"text": "la-la-la", "completed": False}
        self.client.post(self.entry_edit(4), data)

        entry = get_entry(4)
        self.assertTrue(Entry.objects.filter(text="la-la-la").exists())
        self.assertIs(entry.completed, False)

    def test_entry_delete_anonymous_redirects(self):
        response = self.client.get(self.entry_delete(4), follow=True)

        url = login_plus_next(self.entry_delete(4))
        self.assertRedirects(response, url)  # type: ignore

    def test_entry_delete_non_owner_returns_404(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.entry_delete(4))

        self.assertEqual(response.status_code, 404)

    def test_entry_delete_owner_template(self):
        self.client.force_login(self.user2)
        response = self.client.get(self.entry_delete(4))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todo/entry_confirm_delete.html")  # type: ignore

    def test_entry_delete_POST_anonymous_fails(self):
        self.client.post(self.entry_delete(4))

        self.assertTrue(Entry.objects.filter(pk=4).exists())

    def test_entry_delete_POST_non_owner_fails(self):
        self.client.force_login(self.user1)
        self.client.post(self.entry_delete(4))

        self.assertTrue(Entry.objects.filter(pk=4).exists())

    def test_entry_delete_POST_owner(self):
        self.client.force_login(self.user2)
        self.client.post(self.entry_delete(4))

        self.assertFalse(Entry.objects.filter(pk=4).exists())


def url_plus_next(url: str, next: str) -> str:
    return f"{url}?next={next}"


def login_plus_next(next: str) -> str:
    return url_plus_next(reverse("auth:login"), next)


def get_todo(pk: int) -> ToDo:
    return ToDo.objects.get(pk=pk)


def get_entry(pk: int) -> Entry:
    return Entry.objects.get(pk=pk)
