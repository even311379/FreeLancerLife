# Generated by Django 2.1.5 on 2019-01-11 13:39

from django.db import migrations, models
import django.db.models.deletion
import wagtailmd.utils


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0001_squashed_0021'),
        ('apps', '0002_apppost'),
    ]

    operations = [
        migrations.AddField(
            model_name='appindex',
            name='title_caption',
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name='apppost',
            name='app_custom_htmlcode',
            field=wagtailmd.utils.MarkdownField(blank=True),
        ),
        migrations.AddField(
            model_name='apppost',
            name='app_description',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AddField(
            model_name='apppost',
            name='app_thumbnail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='apppost',
            name='is_dash_app',
            field=models.BooleanField(default=False),
        ),
    ]