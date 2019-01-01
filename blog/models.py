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

    description = models.CharField(max_length=255, blank=True,)

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full")
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


    def get_context(self, request, *args, **kwargs):
        print('secrets in get_context')
        context = super().get_context(request, *args, **kwargs)
        context['posts_this_page'] = self.posts_this_page
        # if self.p:
        context['p'] = self.p
        context['blog_index'] = self

        context['search_type'] = getattr(self, 'search_type', "")
        context['search_term'] = getattr(self, 'search_term', "")

        context['categories'] = BlogCategory.objects.all()
        if len(BlogCategory.objects.all()) % 2 == 1:
            context['n_category_odd'] = True

        return context

    @route(r'^$')
    def post_list(self, request, *args, **kwargs):
        '''
        pagination for posts
        '''
        print('secrets in postlist')
        all_post = self.get_recent_posts(999)
        paginator = Paginator(all_post, 2)
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

    def get_posts(self):
        all_post = []
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
    def post_by_category(self, request, category, *args, **kwargs):
        self.search_type = 'category'
        self.search_term = category
        print(category)
        for p in self.get_recent_posts(50):
            print([i.slug for i in p.categories.all()])
            print(category in [i.slug for i in p.categories.all()])
        print([post for post in self.get_recent_posts(50) if category in [c.slug for c in post.categories.all()]])
        self.posts_this_page = [post for post in self.get_recent_posts(50) if category in [c.slug for c in post.categories.all()]]
        return Page.serve(self, request, *args, **kwargs)


    @route(r'^search/$')
    def post_search(self,request, *args, **kwargs):
        search_query = request.GET.get('q', None)
        self.posts = self.get_posts()
        if search_query:
            self.posts = self.posts.filter(body__contains=search_query)
            self.search_term = search_query
            self.search_type = 'search'
        return Page.serve(self, request, *args, **kwargs)

'''
I should use a new page class to present search by category results,
since the templates will differ a lot than blog index
'''    

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



        