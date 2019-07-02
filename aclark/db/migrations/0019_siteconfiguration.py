# Generated by Django 2.1.9 on 2019-07-01 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("db", "0018_auto_20190701_2255")]

    operations = [
        migrations.CreateModel(
            name="SiteConfiguration",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("site_name", models.CharField(default="Site Name", max_length=255)),
                ("maintenance_mode", models.BooleanField(default=False)),
            ],
            options={"verbose_name": "Site Configuration"},
        )
    ]