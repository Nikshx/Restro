# Generated by Django 5.2.4 on 2025-07-26 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0004_remove_menuitem_image_url_menuitem_is_special_today"),
    ]

    operations = [
        migrations.AddField(
            model_name="menuitem",
            name="image_url",
            field=models.URLField(blank=True, null=True),
        ),
    ]
