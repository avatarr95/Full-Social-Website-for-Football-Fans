from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import datetime
from django.conf import settings
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from bs4 import BeautifulSoup
import random

# Create your models here.

class Post(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published")
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    body = RichTextField()
    publish = models.DateTimeField(default=timezone.now())
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="published")
    slug = models.SlugField(max_length=50)
    image = models.ImageField(upload_to="images/", blank=True)
    description = models.CharField(max_length=160, default="", blank=True)
    pic_nr = models.IntegerField(default=random.randint(1, 10), blank=True)
    

    class Meta:
        ordering = ("-publish",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        #return reverse("strona:post_detail", args=[self.publish.year, self.publish.strftime("%m"), self.publish.strftime("%d"), self.slug])
        return reverse("valverde:post_detail", args=[self.pk, self.slug])

    def was_published_recently(self):
        return timezone.now() - datetime.timedelta(days=1) <= self.publish <= timezone.now()

    

    def save(self, *args, **kwargs):
        pic_nr= self.pic_nr
        if not self.image:
            self.image = u'images/{}.jpg'.format(pic_nr)

        html_text = self.body
        soup = BeautifulSoup(html_text, features="lxml")
        cleaned_text = soup.get_text(separator=" ")
        self.description = cleaned_text[0:79]

        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    udpated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    description = models.CharField(max_length=50, default='', blank=True)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="comments_liked", blank=True)

    class Meta:
        ordering = ('-created',)

    def children(self):
        return Comment.objects.filter(parent=self)
    
    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True

    def save(self, *args, **kwargs):
        html_text = self.body
        soup = BeautifulSoup(html_text)
        txt = soup.get_text()
        self.description = txt[:49]
        super(Comment, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.description
    
