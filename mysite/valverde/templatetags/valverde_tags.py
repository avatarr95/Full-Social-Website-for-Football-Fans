from django import template
from ..models import Post
from django.utils import timezone
import datetime
from django.db.models import Count 
from django.utils.safestring import mark_safe
import markdown



register = template.Library()


# @register.inclusion_tag('strona/latest_posts.html')
# def show_latest_posts(count=5):
#     latest_posts =  Post.objects.filter(status="published", publish__lte=timezone.now(), publish__gte=timezone.now()-datetime.timedelta(days=1)).order_by("-publish")[:count]
#     return {'latest_posts': latest_posts}


#LAST POSTS TAGS

@register.simple_tag
def get_last_post():
    return Post.objects.filter(status="published").order_by("-publish")[0]
    
@register.simple_tag
def get_2nd_last_post():
    return Post.objects.filter(status="published").order_by("-publish")[1]

@register.simple_tag
def get_3rd_last_post():
    return Post.objects.filter(status="published").order_by("-publish")[2]

@register.simple_tag
def get_4_to_24_last_posts():
    return Post.objects.filter(status="published").order_by('-publish')[1:24]


#MOST COMMENTED POSTS TAGS


@register.simple_tag
def get_first_most_commented_post():
    most_commented_post = Post.objects.filter(status="published", publish__lte=timezone.now(), publish__gte=timezone.now()-datetime.timedelta(days=1)).annotate(total_comments=Count("comments")).order_by("-total_comments").first()
    most_commented_post_from_last_week = Post.objects.filter(status="published", publish__lte=timezone.now(), publish__gte=timezone.now()-datetime.timedelta(days=7)).annotate(total_comments=Count("comments")).order_by("-total_comments").first()
    most_commented_post_from_last_month = Post.objects.filter(status="published", publish__lte=timezone.now(), publish__gte=timezone.now()-datetime.timedelta(days=30)).annotate(total_comments=Count("comments")).order_by("-total_comments").first()
    if most_commented_post:
        return most_commented_post
    else:
        if most_commented_post_from_last_week:
            return most_commented_post_from_last_week
        else:
            return most_commented_post_from_last_month

@register.simple_tag
def get_second_most_commented_post():
    
    most_commented_posts = Post.objects.filter(status="published", publish__lte=timezone.now(), publish__gte=timezone.now()-datetime.timedelta(days=1)).annotate(total_comments=Count("comments")).order_by("-total_comments")
    most_commented_posts_from_last_week = Post.objects.filter(status="published", publish__lte=timezone.now(), publish__gte=timezone.now()-datetime.timedelta(days=7)).annotate(total_comments=Count("comments")).order_by("-total_comments")
    most_commented_posts_from_last_month = Post.objects.filter(status="published", publish__lte=timezone.now(), publish__gte=timezone.now()-datetime.timedelta(days=30)).annotate(total_comments=Count("comments")).order_by("-total_comments")
    if len(most_commented_posts) > 1:
        return most_commented_posts[1]
    else:
        if len(most_commented_posts_from_last_week) > 1:
            return most_commented_posts_from_last_week[1]
        else: 
            return most_commented_posts_from_last_month[1]




@register.simple_tag
def most_commented_posts(count=5):
    return Post.objects.filter(status="published", publish__lte=timezone.now(), publish__gte=timezone.now()-datetime.timedelta(days=1)).annotate(total_comments=Count("comments")).order_by("-total_comments")[:count]







#markdown używamy, gdy jesteśmy pewni, że kod jest bezpieczny... lepiej nie ufać nikomu
@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
