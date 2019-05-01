# Generated by Django 2.2 on 2019-05-01 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0008_remove_estimate_estimate_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('hidden', models.BooleanField(default=False)),
                ('icon_name', models.CharField(blank=True, max_length=25, null=True, verbose_name='Font Awesome Icon')),
                ('icon_size', models.CharField(blank=True, choices=[('1x', 'Small'), ('2x', 'Medium'), ('3x', 'Large'), ('4x', 'XL'), ('5x', 'XXL')], max_length=255, null=True)),
                ('icon_color', models.CharField(blank=True, choices=[('primary', 'Primary'), ('secondary', 'Secondary'), ('success', 'Success'), ('danger', 'Danger'), ('warning', 'Warning'), ('info', 'Info'), ('light', 'Light'), ('dark', 'Dark'), ('muted', 'Muted'), ('white', 'White')], max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
