from __future__ import unicode_literals

import datetime
from datetime import date

from django.db import models
from django import forms
from django.http import Http404, HttpResponse
from django.utils.dateformat import DateFormat
from django.utils.formats import date_format
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from colorfield.fields import ColorField

from wagtail.core import blocks
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import (FieldPanel, FieldRowPanel,
                                         InlinePanel, MultiFieldPanel,
                                         PageChooserPanel, StreamFieldPanel)
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.snippets.models import register_snippet


from blog.blocks import TwoColumnBlock

from modelcluster.fields import ParentalKey, ParentalManyToManyField
# from modelcluster.tags import ClusterTaggableManager
# from taggit.models import TaggedItemBase, Tag as TaggitTag
from wagtailmd.utils import MarkdownField, MarkdownPanel

from wagtailtrans.models import TranslatablePage

# Create your models here.

@register_snippet
class BlogCategory(Orderable, models.Model):
    name = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(unique=True, max_length=80)
    shown_order = models.IntegerField(blank=True, unique=True,null=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('name_en'),
        FieldPanel('slug'),
        FieldPanel('shown_order'),
    ]

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

@register_snippet
class Series( models.Model):
    name = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(unique=True, max_length=80)
    shown_order = models.IntegerField(blank=True, unique=True,null=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('name_en'),
        FieldPanel('slug'),
        FieldPanel('shown_order'),
    ]

    class Meta:
        verbose_name = "Series"

    def __str__(self):
        return self.name


class BlogIndex(RoutablePageMixin, TranslatablePage):
    Page = TranslatablePage
    title_caption = models.CharField(max_length=250,blank=True,)
    description = models.CharField(max_length=255, blank=True,)
    banner = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, related_name='+',null=True,blank=True,
    )
    content_panels = Page.content_panels + [
        FieldPanel('title_caption'),
        FieldPanel('description'),
        ImageChooserPanel('banner'),
    ]

    '''
    finally figured out someway to control it:
        when request url pattern match with route decorator,
        just do some thing to change self.attrs, and then read
        them in get_context.
    The logic in https://blog.michaelyin.info/wagtail-tutorials-routable-page/
    realy makes no sense. His code should not work based on my understanding, but it just works!!
    '''
    posts_this_page = []
    p = []
    help_text = ''
    present_method = 0 # 0 for recent posts, 1 for categories, 2 for title keyword search
    searched_categories = []
    keyword = ''

    def get_context(self, request, *args, **kwargs):
        print('main get_context is called!')
        context = super().get_context(request, *args, **kwargs)
        if request.method == 'POST':
            self.help_text = '分類搜索：'
            self.present_method = 1
            self.posts_this_page = []
            all_post = self.get_posts(sibling = True)
            cats = []
            for cat in BlogCategory.objects.all():
                if request.POST.get(cat.name):
                    cats.append(cat.name)
            
            self.searched_categories = BlogCategory.objects.filter(name__in=cats)        
            for post in all_post:
                for c in post.categories.all():
                    if c.name in cats:
                        self.posts_this_page.append(post)
                        break
                        
        context['posts_this_page'] = self.posts_this_page
        context['p'] = self.p
        context['blog_index'] = self
        context['help_text'] = self.help_text
        context['present_method'] = self.present_method
        context['searched_categories'] = self.searched_categories
        context['keyword'] = self.keyword
        context['categories'] = BlogCategory.objects.all()
        context['n_category_left'] = len(BlogCategory.objects.all()) % 3
        print(self.language.code)
        return context

   
    def get_posts(self, sibling = False):
        all_post = []
        if sibling:
            all_post += PostPage.objects.sibling_of(self).live()
            all_post += LandingPage.objects.sibling_of(self).live()
        else:
            all_post += PostPage.objects.descendant_of(self).live()
            all_post += LandingPage.objects.descendant_of(self).live()
        return all_post

    def get_recent_posts(self, n = 10):
        '''
        reorder all_post in decending date order
        '''
        all_post = self.get_posts()

        dates = [post.date for post in all_post]
        dates.sort(reverse = True)
        reordered_all_post = []
        for d in dates:
            for p in all_post:
                if p.date == d:
                    reordered_all_post.append(p)
                    break
        return reordered_all_post[0:10]

    @route(r'^category/(?P<category>[-\w]+)/$')
    # @route(r'^category$')
    def post_by_category(self, request, category, *args, **kwargs):
        print('route post_by_category is called!!')
        self.help_text = '分類搜索：'
        self.present_method = 1
        self.searched_categories = BlogCategory.objects.filter(slug=category)
        self.posts_this_page = [post for post in self.get_recent_posts(50) if category in [c.slug for c in post.categories.all()]]
        return Page.serve(self, request, *args, **kwargs)


    @route(r'^search_post/$')
    def post_search(self,request, *args, **kwargs):
        print('route post_search is called!!')
        self.help_text = '關鍵字搜索：'
        self.present_method = 2
        search_query = request.GET.get('q', None)
        self.keyword = search_query
        all_posts = self.get_posts()
        if search_query:
            self.posts_this_page = [p for p in all_posts if search_query in p.title]
        return Page.serve(self, request, *args, **kwargs)
    
    @route(r'^$')
    def post_list(self, request, *args, **kwargs):
        '''
        pagination for posts
        '''
        print('route post list is called!!')
        self.help_text = '近期文章：'
        all_post = self.get_recent_posts(999)
        paginator = Paginator(all_post, 20)
        p = request.GET.get('p')
        if not p:
            p = 1
        try:
            posts_this_page = paginator.page(p)
        except PageNotAnInteger:
            p = 1
            posts_this_page = paginator.page(p)
        except EmptyPage:
            p = paginator.num_pages
            posts_this_page = paginator.page(p)

        self.posts_this_page = posts_this_page
        self.p = p
        return Page.serve(self, request, *args, **kwargs)

# The abstract model for related links, complete with panels
class RelatedLink(models.Model):
    related_page = models.ForeignKey(
        TranslatablePage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    panels = [PageChooserPanel('related_page', ['blog.PostPage', 'blog.LandingPage'])]

    class Meta:
        abstract = True

class PostPageRelatedLinks(Orderable, RelatedLink):
    page = ParentalKey('blog.PostPage', on_delete=models.CASCADE, related_name='related_links')  

class PostPage(TranslatablePage):
    Page = TranslatablePage
    
    date = models.DateTimeField(verbose_name="Post date", default=datetime.datetime.today)
    is_series = models.BooleanField(default=False)
    series_name = models.ForeignKey(Series, on_delete=models.SET_NULL, related_name='+', blank=True, null=True)
    series_id = models.IntegerField(blank=True, unique=False,null=True)

    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)
    
    body = MarkdownField()
    thumbnail = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', blank=True, null=True)
    
    content_panels = Page.content_panels + [
        ImageChooserPanel('thumbnail'),
        MarkdownPanel('body'),
        FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        InlinePanel('related_links', label="Related Links"),
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel('date'),
        MultiFieldPanel([
            FieldPanel('is_series'),
            FieldPanel('series_name'),
            FieldPanel('series_id')],
        heading='SeriesSetting',classname="collapsible collapsed"),
    ]

    @property
    def blog_index(self):
        return self.get_parent().specific

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['blog_index'] = self.blog_index
        if self.is_series:
            all_post = []
            all_post += PostPage.objects.live()
            all_post += LandingPage.objects.live()
            context['Series'] = [p for p in all_post if (p.language == self.language) and (p.series_name == self.series_name)]
            if self.language.code == 'zh':
                context['Series_name'] = self.series_name
            else:
                context['Series_name'] = self.series_name.name_en
        return context


class LandingPageRelatedLinks(Orderable, RelatedLink):
    page = ParentalKey('blog.LandingPage', on_delete=models.CASCADE, related_name='related_links')  


class LandingPage(TranslatablePage): # a special type of post page (I intend to use it for game devlog)
    Page = TranslatablePage

    date = models.DateTimeField(verbose_name="Post date", default=datetime.datetime.today)
    project_overview = models.BooleanField(default=False)
    thumbnail = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', blank=True, null=True)
    is_series = models.BooleanField(default=False)
    series_name = models.ForeignKey(Series, on_delete=models.SET_NULL, related_name='+', blank=True, null=True)
    series_id = models.IntegerField(blank=True, unique=False,null=True)

    banner = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', blank=True, null=True)
    title_color = ColorField(default='#FF0000') 
    tilable_banner = models.BooleanField(default=False)

    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)
    intro = models.CharField(max_length=255, blank=True,)
    body = StreamField([
        ('heading',blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock(icon="image")),
        ('two_columns', TwoColumnBlock()),
        ('embedded_video', EmbedBlock(icon="media")),
    ],null=True,blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            ImageChooserPanel('banner'),
            FieldPanel('tilable_banner'),
            FieldPanel('title_color')],
        heading='Banner'),
        FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        FieldPanel('intro'),
        StreamFieldPanel('body'),
        InlinePanel('related_links', label="Related Links"),
    ]
    settings_panels = Page.settings_panels + [
        FieldPanel('date'),FieldPanel('project_overview'),
        ImageChooserPanel('thumbnail'),
        MultiFieldPanel([
            FieldPanel('is_series'),
            FieldPanel('series_name'),
            FieldPanel('series_id')],
        heading='SeriesSetting',classname="collapsible collapsed"),
    ]        

