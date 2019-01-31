# Generated by Django 2.1.5 on 2019-01-31 12:57

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_auto_20190129_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landingpage',
            name='body',
            field=wagtail.core.fields.StreamField([('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('code', wagtail.core.blocks.TextBlock()), ('code_output', wagtail.core.blocks.TextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image')), ('two_columns', wagtail.core.blocks.StructBlock([('left_column', wagtail.core.blocks.StreamBlock([('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())], icon='arrow-right', label='Left column content')), ('right_column', wagtail.core.blocks.StreamBlock([('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())], icon='arrow-right', label='Right column content'))])), ('embedded_video', wagtail.embeds.blocks.EmbedBlock(icon='media')), ('custom_html', wagtail.core.blocks.TextBlock(icon='plus-inverse'))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='landingpost',
            name='body',
            field=wagtail.core.fields.StreamField([('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('code', wagtail.core.blocks.StructBlock([('language', wagtail.core.blocks.ChoiceBlock(choices=[('python', 'Python'), ('bash', 'Bash'), ('brainfuck', 'Brainfuck'), ('csharp', 'C#'), ('cpp', 'C++'), ('css', 'CSS'), ('django', 'Django/Jinja2'), ('http', 'HTTP'), ('java', 'Java'), ('javascript', 'JavaScript'), ('json', 'JSON')], help_text='Coding language', label='Language')), ('code', wagtail.core.blocks.TextBlock(label='Code'))], label='Code')), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image')), ('custom_html', wagtail.core.blocks.TextBlock(icon='plus-inverse'))], blank=True, null=True),
        ),
    ]
