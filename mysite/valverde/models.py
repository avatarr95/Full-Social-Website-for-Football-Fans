from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import datetime

# Create your models here.

class Post(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published")
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now())
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="published")
    slug = models.SlugField(max_length=50)
    image = models.ImageField(upload_to="images/")

    class Meta:
        ordering = ("-publish",)

    def __str__(self):
        return self.title



    def get_absolute_url(self):
        #return reverse("strona:post_detail", args=[self.publish.year, self.publish.strftime("%m"), self.publish.strftime("%d"), self.slug])
        return reverse("valverde:post_detail", args=[self.pk, self.slug])

    def was_published_recently(self):
        return timezone.now() - datetime.timedelta(days=1) <= self.publish <= timezone.now()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    udpated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.post.title