# Generated by Django 2.1.4 on 2019-01-06 12:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0001_squashed_0021'),
        ('blog', '0008_auto_20190106_1945'),
    ]

    operations = [
        migrations.RenameField(
            model_name='landingpage',
            old_name='banner_color',
            new_name='title_color',
        ),
        migrations.AddField(
            model_name='landingpage',
            name='banner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
    ]