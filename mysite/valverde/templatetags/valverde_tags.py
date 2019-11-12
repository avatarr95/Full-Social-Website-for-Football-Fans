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



@register.simple_tag
def get_last_post():
    return Post.objects.filter(status="published").order_by("-publish")[0]
    
@register.simple_tag
def get_2nd_last_post():
    return Post.objects.filter(status="published").order_by("-publish")[1]

@register.simple_tag
def get_3rd_last_post():
    return Post.objects.filter(status="published").order_by("-publish")[2]



"""
@register.simple_tag
def top_post():
    return Post.objects.filter(status="published", publish__lte=timezone.now(), publish__gte=timezone.now()-datetime.timedelta(days=1)).annotate(total_comments=Count("comments")).order_by("-comments")[0]


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.objects.filter(status="published", publish__lte=timezone.now(), publish__gte=timezone.now()-datetime.timedelta(days=1)).annotate(total_comments=Count("comments")).order_by("-comments")[1:count]


# markdown używamy, gdy jesteśmy pewni, że kod jest bezpieczny... lepiej nie ufać nikomu
# @register.filter(name="markdown")
# def markdown_format(text):
#     return mark_safe(markdown.markdown(text))

"""