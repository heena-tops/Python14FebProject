# Generated by Django 4.2 on 2023-04-11 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("myapp", "0002_delete_user"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("fname", models.CharField(max_length=100)),
                ("lname", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                ("pswd", models.CharField(max_length=100)),
                ("contact", models.IntegerField()),
                ("address", models.TextField()),
            ],
        ),
    ]
