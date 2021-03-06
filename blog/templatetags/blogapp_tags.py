# -*- coding: utf-8 -*-
import six
from django.template import Library, loader
from django.urls import resolve
from ..models import BlogCategory as Category

register = Library()

@register.simple_tag()
def post_date_url(post, blog_index):
    post_date = post.date
    url = blog_index.url + blog_index.reverse_subpage(
        'post_by_date_slug',
        args=(
            post_date.year,
            '{0:02}'.format(post_date.month),
            '{0:02}'.format(post_date.day),
            post.slug,
        )
    )
    return url

@register.inclusion_tag('blog/comments/disqus.html', takes_context=True)
def show_comments(context):
    post = context['self']
    path = post.url

    raw_url = context['request'].get_raw_uri()
    parse_result = six.moves.urllib.parse.urlparse(raw_url)
    abs_path = six.moves.urllib.parse.urlunparse([
        parse_result.scheme,
        parse_result.netloc,
        path,
        "",
        "",
        ""
    ])

    return {'disqus_url': abs_path,'disqus_identifier': post.pk, 'request':context['request']}


# @register.inclusion_tag('blog/components/tags_list.html',
#                         takes_context=True)
# def tags_list(context, limit=None):
#     blog_page = context['blog_page']
#     tags = Tag.objects.all()
#     if limit:
#         tags = tags[:limit]
#     return {
#         'blog_page': blog_page, 'request': context['request'], 'tags': tags}

# @register.inclusion_tag('blog/components/categories_list.html',
#                         takes_context=True)
# def categories_list(context):
#     blog_page = context['blog_page']
#     categories = Category.objects.all()
#     return {
#         'blog_page': blog_page, 'request': context['request'], 
#         'categories': categories}


