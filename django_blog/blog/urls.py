# blog/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Maps the base URL (e.g., /blog/) to the PostListView defined in views.py
    path('', views.PostListView.as_view(), name='blog-home'),
]
