# Generated by Django 2.1.5 on 2019-01-11 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0004_appindex_banner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apppost',
            name='app_custom_htmlcode',
        ),
        migrations.AddField(
            model_name='apppost',
            name='component_name',
            field=models.CharField(blank=True, max_length=80),
        ),
    ]