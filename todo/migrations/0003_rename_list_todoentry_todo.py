# Generated by Django 4.1.1 on 2022-09-13 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("todo", "0002_alter_todo_owner"),
    ]

    operations = [
        migrations.RenameField(
            model_name="todoentry",
            old_name="list",
            new_name="todo",
        ),
    ]