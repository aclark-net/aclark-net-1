# Generated by Django 3.0.7 on 2020-07-13 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0050_auto_20200710_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='doc_type',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]