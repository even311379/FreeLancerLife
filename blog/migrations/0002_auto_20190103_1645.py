# Generated by Django 2.1.4 on 2019-01-03 08:45

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailforms', '0003_capitalizeverbose'),
        ('wagtailmenus', '0022_auto_20170913_2125'),
        ('wagtailimages', '0001_squashed_0021'),
        ('wagtailtrans', '0007_auto_20180327_1127'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='transLandingPage',
            new_name='LandingPage',
        ),
        migrations.RenameModel(
            old_name='transPostPage',
            new_name='PostPage',
        ),
    ]
