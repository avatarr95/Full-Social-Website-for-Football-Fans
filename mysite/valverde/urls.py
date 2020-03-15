from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'valverde'

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/<slug:post>/", views.post_detail, name="post_detail"),
    path("<int:pk>/<slug:post>/edit/", views.post_detail, name="post_detail"),
    path("contact/", views.contact, name='contact'),    
    path("register/", views.register, name="register"),
    path("comments_like/", views.comments_like, name="comments_like"),
    path('new-post/', views.add_a_new_post, name="add_post"),
    path("account/", include("django.contrib.auth.urls")),
    

]

