# Generated by Django 4.0.1 on 2022-01-22 21:29

import choralcat_core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('choralcat_web', '0007_alter_category_options_alter_program_ordering'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='non_male_identifying',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='person',
            name='poc',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(blank=True, max_length=256, null=True, unique=True)),
                ('value', models.CharField(blank=True, max_length=256, null=True, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, choralcat_core.models.TimeStampMixin, choralcat_core.models.CreatedByMixin),
        ),
        migrations.AddField(
            model_name='composition',
            name='topics',
            field=models.ManyToManyField(blank=True, to='choralcat_web.Topic'),
        ),
        migrations.AddField(
            model_name='program',
            name='topics',
            field=models.ManyToManyField(blank=True, to='choralcat_web.Topic'),
        ),
    ]