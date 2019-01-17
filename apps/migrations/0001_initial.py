# Generated by Django 2.1.5 on 2019-01-15 14:20

from django.db import migrations, models
import django.db.models.deletion
import wagtailmd.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailtrans', '0007_auto_20180327_1127'),
        ('wagtailimages', '0001_squashed_0021'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppIndex',
            fields=[
                ('translatablepage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailtrans.TranslatablePage')),
                ('title_caption', models.CharField(blank=True, max_length=80)),
                ('banner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailtrans.translatablepage',),
        ),
        migrations.CreateModel(
            name='AppPost',
            fields=[
                ('translatablepage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailtrans.TranslatablePage')),
                ('app_name', models.CharField(blank=True, max_length=80)),
                ('app_description', wagtailmd.utils.MarkdownField(blank=True)),
                ('component_name', models.CharField(blank=True, max_length=80)),
                ('is_dash_app', models.BooleanField(default=False)),
                ('app_thumbnail', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailtrans.translatablepage',),
        ),
    ]
