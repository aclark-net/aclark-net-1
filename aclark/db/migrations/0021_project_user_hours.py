# Generated by Django 2.1.9 on 2019-07-02 18:29

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("db", "0020_auto_20190701_2342")]

    operations = [
        migrations.AddField(
            model_name="project",
            name="user_hours",
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        )
    ]
