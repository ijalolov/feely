# Generated by Django 4.1.3 on 2022-11-18 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("doctor", "0005_videocoursecategory_videocourse_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="doctor",
            name="company",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
