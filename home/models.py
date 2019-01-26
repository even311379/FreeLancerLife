from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet

from blog import models as blog_model
from wagtailtrans.models import TranslatablePage
from wagtailmd.utils import MarkdownField, MarkdownPanel

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
        all_LandingPage = [p for p in blog_model.LandingPage.objects.live() if p.language==self.language]
        context['recent_projects'] = [page for page in all_LandingPage if page.project_overview]
        return context

@register_snippet
class task_type(models.Model):    
    name = models.CharField(max_length=30)
    name_en = models.CharField(max_length=30,blank=True)

    def __str__(self):
        return self.name
    # consult, data, web, tutorial, 

@register_snippet
class plan_type(models.Model):
    name = models.CharField(max_length=30)
    name_en = models.CharField(max_length=30,blank=True)

    def __str__(self):
        return self.name
    # remote , short-term, long-term, 

class ContactMeData(models.Model):
    '''
    I can add it in wagtailadmin through wagtail_hooks,
    and it works so good!
    '''
    name = models.CharField(max_length=30)
    organization = models.CharField(max_length=100)
    task = models.ForeignKey(task_type, on_delete=models.SET_NULL, related_name='+', null=True)
    plan = models.ForeignKey(plan_type, on_delete=models.SET_NULL, related_name='+', null=True)
    due_date = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    receive_time = models.DateTimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.name


class SubscriberEmail(models.Model):
    subsciber_email = models.EmailField(max_length=50)
    receive_time = models.DateTimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.subsciber_email


class ContactMe(TranslatablePage):

    Page = TranslatablePage
    head = models.CharField(max_length=30,blank=True)
    head_intro = models.CharField(max_length=80,blank=True)

    name_intro0 = models.CharField(max_length=80,blank=True)
    name_intro1 = models.CharField(max_length=80,blank=True)
    assist = models.CharField(max_length=80,blank=True)
    due = models.CharField(max_length=80,blank=True)
    plan_intro = models.CharField(max_length=80,blank=True)
    mail_intro = models.CharField(max_length=80,blank=True)
    thanks = models.CharField(max_length=80,blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('head'),
            FieldPanel('head_intro'),
        ], heading="head"),
        MultiFieldPanel([
            FieldPanel('name_intro0'),
            FieldPanel('name_intro1'),
            FieldPanel('assist'),
            FieldPanel('due'),
            FieldPanel('plan_intro'),
            FieldPanel('mail_intro'),
            FieldPanel('thanks'),
        ], heading="ContactMeText"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        if self.language.code == 'en':
            context['task_type'] = [i.name_en for i in task_type.objects.all()]
            context['plan_type'] = [i.name_en for i in plan_type.objects.all()]
        else:
            context['task_type'] = [i.name for i in task_type.objects.all()]
            context['plan_type'] = [i.name for i in plan_type.objects.all()]
        return context



class HireMe(TranslatablePage):
    Page = TranslatablePage
    banner = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', blank=True, null=True)
    title_caption = models.CharField(max_length=80,blank=True)
    Flow = MarkdownField(blank=True) 
    Task = MarkdownField(blank=True)
    Plan = MarkdownField(blank=True)
    Charge = MarkdownField(blank=True)

    content_panels = Page.content_panels + [
        ImageChooserPanel('banner'),
        FieldPanel('title_caption'),
        MarkdownPanel('Flow'),
        MarkdownPanel('Task'),
        MarkdownPanel('Plan'),
        MarkdownPanel('Charge'),
    ]


