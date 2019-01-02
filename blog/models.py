from __future__ import unicode_literals

import datetime
from datetime import date

from django.db import models
from django import forms
from django.http import Http404, HttpResponse
from django.utils.dateformat import DateFormat
from django.utils.formats import date_format
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

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
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase, Tag as TaggitTag
from wagtailmd.utils import MarkdownField, MarkdownPanel

# Create your models here.
class BlogIndex(RoutablePageMixin, Page):

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
            all_post = self.get_posts()
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

        return context

   
    def get_posts(self):
        all_post = []
        all_post += PostPage.objects.live()
        all_post += LandingPage.objects.live()
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

  

class PostPage(Page):
    date = models.DateTimeField(verbose_name="Post date", default=datetime.datetime.today)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)

    body = MarkdownField()
    thumbnail = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', blank=True, null=True)
    content_panels = Page.content_panels + [
        ImageChooserPanel('thumbnail'),
        MarkdownPanel('body'),
        FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel('date'),
    ]

    @property
    def blog_index(self):
        return self.get_parent().specific

    def get_context(self, request, *args, **kwargs):
        context = super(PostPage, self).get_context(request, *args, **kwargs)
        context['blog_index'] = self.blog_index
        context['post'] = self
        return context

@register_snippet
class BlogCategory(Orderable, models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=80)

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
    ]

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class LandingPage(Page): # a special type of post page (I intend to use it for game devlog)
    date = models.DateTimeField(verbose_name="Post date", default=datetime.datetime.today)
    project_overview = models.BooleanField(default=False)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)

    thumbnail = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', blank=True, null=True)
    intro = models.CharField(max_length=255, blank=True,)
    body = StreamField([
        ('heading',blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock(icon="image")),
        ('two_columns', TwoColumnBlock()),
        ('embedded_video', EmbedBlock(icon="media")),
    ],null=True,blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ImageChooserPanel('thumbnail'),
        FieldPanel('intro'),
        StreamFieldPanel('body')
    ]
    settings_panels = Page.settings_panels + [
        FieldPanel('date'),FieldPanel('project_overview'),
    ]



        