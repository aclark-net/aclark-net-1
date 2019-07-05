# Generated by Django 2.1.10 on 2019-07-05 23:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("db", "0022_remove_project_user_hours")]

    operations = [
        migrations.RemoveField(model_name="client", name="icon_color"),
        migrations.RemoveField(model_name="client", name="icon_name"),
        migrations.RemoveField(model_name="client", name="icon_size"),
        migrations.RemoveField(model_name="contact", name="icon_color"),
        migrations.RemoveField(model_name="contact", name="icon_name"),
        migrations.RemoveField(model_name="contact", name="icon_size"),
        migrations.RemoveField(model_name="estimate", name="estimate_type"),
        migrations.RemoveField(model_name="estimate", name="icon_color"),
        migrations.RemoveField(model_name="estimate", name="icon_name"),
        migrations.RemoveField(model_name="estimate", name="icon_size"),
        migrations.RemoveField(model_name="invoice", name="icon_color"),
        migrations.RemoveField(model_name="invoice", name="icon_name"),
        migrations.RemoveField(model_name="invoice", name="icon_size"),
        migrations.RemoveField(model_name="note", name="icon_color"),
        migrations.RemoveField(model_name="note", name="icon_name"),
        migrations.RemoveField(model_name="note", name="icon_size"),
        migrations.RemoveField(model_name="profile", name="app_admin"),
        migrations.RemoveField(model_name="profile", name="dashboard_items"),
        migrations.RemoveField(model_name="profile", name="editor"),
        migrations.RemoveField(model_name="profile", name="icon_color"),
        migrations.RemoveField(model_name="profile", name="icon_name"),
        migrations.RemoveField(model_name="profile", name="icon_size"),
        migrations.RemoveField(model_name="profile", name="is_contact"),
        migrations.RemoveField(model_name="profile", name="notify"),
        migrations.RemoveField(model_name="profile", name="payment_method"),
        migrations.RemoveField(model_name="profile", name="preferred_username"),
        migrations.RemoveField(model_name="project", name="icon_color"),
        migrations.RemoveField(model_name="project", name="icon_name"),
        migrations.RemoveField(model_name="project", name="icon_size"),
        migrations.RemoveField(model_name="report", name="icon_color"),
        migrations.RemoveField(model_name="report", name="icon_name"),
        migrations.RemoveField(model_name="report", name="icon_size"),
        migrations.RemoveField(model_name="task", name="color"),
        migrations.RemoveField(model_name="task", name="icon_color"),
        migrations.RemoveField(model_name="task", name="icon_name"),
        migrations.RemoveField(model_name="task", name="icon_size"),
        migrations.RemoveField(model_name="testimonial", name="icon_color"),
        migrations.RemoveField(model_name="testimonial", name="icon_name"),
        migrations.RemoveField(model_name="testimonial", name="icon_size"),
        migrations.RemoveField(model_name="time", name="icon_color"),
        migrations.RemoveField(model_name="time", name="icon_name"),
        migrations.RemoveField(model_name="time", name="icon_size"),
    ]
