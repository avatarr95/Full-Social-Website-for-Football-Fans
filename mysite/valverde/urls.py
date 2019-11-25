from django.urls import path, include
from . import views

app_name = 'valverde'

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/<slug:post>/", views.post_detail, name="post_detail"),
    path("contact/", views.contact, name='contact'),    
    path("register/", views.register, name="register"),
    path('like/', views.post_like, name='like'),
]

