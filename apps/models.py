from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from blog import models as blog_model

from wagtailtrans.models import TranslatablePage
from wagtailmd.utils import MarkdownField, MarkdownPanel
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
    app_description = MarkdownField(blank=True)
    component_name = models.CharField(max_length=80,blank=True)
    # app_custom_htmlcode = MarkdownField(blank=True)

    is_dash_app = models.BooleanField(default=False)

    content_panels = Page.content_panels + [
        FieldPanel('app_name'),
        ImageChooserPanel('app_thumbnail'),
        MarkdownPanel('app_description'),
        FieldPanel('component_name'),
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel('is_dash_app')
    ]