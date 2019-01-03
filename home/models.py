from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from blog import models as blog_model

from wagtailtrans.models import TranslatablePage

class HomePage(TranslatablePage):
    title_caption = models.CharField(max_length=250,blank=True)

    intro = RichTextField(blank=True)
    banner = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, related_name='+',null=True,blank=True,
    )

    about_caption = models.CharField(max_length=250,blank=True)
    about_content = RichTextField(blank=True)

    data_title = models.CharField(max_length=50,blank=True)
    data_content = RichTextField(blank=True)

    web_title = models.CharField(max_length=50,blank=True)
    web_content = RichTextField(blank=True)

    game_title = models.CharField(max_length=50,blank=True)
    game_content = RichTextField(blank=True)

    tutorial_title = models.CharField(max_length=50,blank=True)
    tutorial_content = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('title_caption'),
            FieldPanel('intro'),
            ImageChooserPanel('banner'),
        ], heading="Title"),
        MultiFieldPanel([
            FieldPanel('about_caption'),
            FieldPanel('about_content'),
        ], heading="about"),
        MultiFieldPanel([
            FieldPanel('data_title'),
            FieldPanel('data_content'),
            FieldPanel('web_title'),
            FieldPanel('web_content'),
            FieldPanel('game_title'),
            FieldPanel('game_content'),
            FieldPanel('tutorial_title'),
            FieldPanel('tutorial_content'),
        ], heading="service"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(HomePage, self).get_context(request, *args, **kwargs)
        all_LandingPage = blog_model.LandingPage.objects.live()
        context['recent_projects'] = [page for page in all_LandingPage if page.project_overview]
        return context




