from django.contrib import admin
from .models import Post, Comment 

# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("publish", "title", "author", "status")
    list_filter = ("publish", "status")
    search_fields = ["title", "author__username"]
    prepopulated_fields = { "slug": ("title",)}
    date_hierarchy = "publish"
    raw_id_fields = ('author',)
    ordering = ('-publish', 'status')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author")
    list_filter = ("active", "created")
    search_fields = ("body", "author__username")
    date_hierarchy = "created"
