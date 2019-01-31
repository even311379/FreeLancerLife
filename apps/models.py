from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from blog import models as blog_model

from wagtailtrans.models import TranslatablePage
from wagtailmd.utils import MarkdownField, MarkdownPanel

from wagtail.core import blocks
# Create your models here.

class AppIndex(TranslatablePage):
    Page = TranslatablePage
    banner = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', blank=True, null=True)
    title_caption =models.CharField(max_length=80, blank=True)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['app_posts'] = [p for p in AppPost.objects.live() if p.language == self.language]
        return context

    content_panels = Page.content_panels + [
        FieldPanel('title_caption'),
        ImageChooserPanel('banner'),
    ]

class AppPost(TranslatablePage):
    Page = TranslatablePage
    app_name = models.CharField(max_length=80,blank=True)
    app_thumbnail = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', blank=True, null=True)
    body_before_app = StreamField([
        ('heading',blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock(icon="image")),
        ('custom_html', blocks.TextBlock(icon='plus-inverse')),
    ],null=True,blank=True)
    body_after_app = StreamField([
        ('heading',blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock(icon="image")),
        ('custom_html', blocks.TextBlock(icon='plus-inverse')),
    ],null=True,blank=True)

    is_dash_app = models.BooleanField(default=False)
    dash_ratio = models.FloatField(default=0.5, 
    help_text = 'The ratio of height to width.  Will inherit its width as 100\% of its parent, then set height')

    content_panels = Page.content_panels + [
        FieldPanel('app_name'),
        ImageChooserPanel('app_thumbnail'),
        StreamFieldPanel('body_before_app'),
        StreamFieldPanel('body_after_app'),
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel('is_dash_app'),
        FieldPanel('dash_ratio')
    ]