from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("todo", "0005_todo_public"),
    ]

    operations = [
        migrations.RenameModel("todoentry", "entry"),
    ]
