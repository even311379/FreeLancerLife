# Generated by Django 2.1.5 on 2019-01-10 03:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailtrans', '0007_auto_20180327_1127'),
        ('apps', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppPost',
            fields=[
                ('translatablepage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailtrans.TranslatablePage')),
                ('app_name', models.CharField(blank=True, max_length=80)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailtrans.translatablepage',),
        ),
    ]