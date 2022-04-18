# Generated by Django 4.0.1 on 2022-02-12 20:53

from django.db import migrations

import choralcat.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0004_person_nationality"),
    ]

    operations = [
        migrations.AddField(
            model_name="composition",
            name="title_unidecode",
            field=choralcat.core.fields.UnidecodeField(blank=True, max_length=256, null=True, populated_from="title"),
        ),
    ]
