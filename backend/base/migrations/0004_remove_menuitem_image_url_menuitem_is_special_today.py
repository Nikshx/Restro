# Generated by Django 5.2.4 on 2025-07-26 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0003_menuitem_image_url"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="menuitem",
            name="image_url",
        ),
        migrations.AddField(
            model_name="menuitem",
            name="is_special_today",
            field=models.BooleanField(default=False),
        ),
    ]
