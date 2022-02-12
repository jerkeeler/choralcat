# Generated by Django 4.0.1 on 2022-02-12 21:56

from django.db import migrations

import choralcat.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0005_composition_title_unidecode"),
    ]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="slug",
            field=choralcat.core.fields.AutoSlugField(
                blank=True,
                null=True,
                populated_from=["first_name", "last_name"],
                unique=True,
            ),
        ),
    ]
