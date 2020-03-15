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

# A function, which will return us the newest post.
# Ex. get_post(0) will return us the newest post 
def get_post(table_index):
    return Post.objects.filter(status="published").order_by("-publish")[table_index]

@register.simple_tag
def get_last_post():
    return get_post(0)
    
@register.simple_tag
def get_2nd_last_post():
    return get_post(1)

@register.simple_tag
def get_3rd_last_post():
    return get_post(2)

@register.simple_tag
def get_4_to_24_last_posts():
    return Post.objects.filter(status="published").order_by("-publish")[1:24]



#MOST COMMENTED POSTS
def getMostCommentedPosts(nr_of_days):
    return Post.objects.filter(status="published", publish__lte=timezone.now(), publish__gte=timezone.now()-datetime.timedelta(days=nr_of_days)).annotate(total_comments=Count("comments")).order_by("-total_comments")


# Useful variables to get most commented posts from last x days
most_commented_posts = getMostCommentedPosts(1)
most_commented_posts_from_last_week = getMostCommentedPosts(7)
most_commented_posts_from_last_month = getMostCommentedPosts(31)

@register.simple_tag
def get_first_most_commented_post():
    if most_commented_posts:
        return most_commented_posts[0]
    else:
        if most_commented_posts_from_last_week:
            return most_commented_posts_from_last_week[0]
        else:
            return most_commented_posts_from_last_month[0]

# Could have been done with a function not to repeat the code, but we had to use the len method, otherwise it would not work
@register.simple_tag
def get_second_most_commented_post():
    if len(most_commented_posts) > 1:
        return most_commented_posts[1]
    else:
        if len(most_commented_posts_from_last_week) > 1:
            return most_commented_posts_from_last_week[1]
        else: 
            return most_commented_posts_from_last_month[1]



# Getting 5 most commented posts
@register.simple_tag
def most_commented_posts(count=5):
    return Post.objects.filter(status="published", publish__lte=timezone.now(), publish__gte=timezone.now()-datetime.timedelta(days=1)).annotate(total_comments=Count("comments")).order_by("-total_comments")[:count]


@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
