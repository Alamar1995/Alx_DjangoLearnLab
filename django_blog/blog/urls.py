# blog/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Blog Homepage
    path('', views.PostListView.as_view(), name='blog-home'),
    
    # Custom Authentication URLs
    path('register/', views.register, name='register'), # <-- ADD THIS
    path('profile/', views.profile, name='profile'),   # <-- ADD THIS
]
