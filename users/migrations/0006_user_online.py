# Generated by Django 4.1.3 on 2022-11-18 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_alter_user_email_alter_user_username"),
    ]

    operations = [
        migrations.AddField(
            model_name="user", name="online", field=models.BooleanField(default=False),
        ),
    ]
