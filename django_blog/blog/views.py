# blog/views.py

from django.views.generic import ListView
from .models import Post

# Use Django's built-in ListView to fetch and display multiple objects
class PostListView(ListView):
    # Tell the view what model to query
    model = Post
    
    # Specify the template file to use for rendering
    # The default would be blog/post_list.html, but we name it home.html
    template_name = 'blog/home.html'
    
    # The name of the context variable used in the template (default is object_list)
    context_object_name = 'posts'
    
    # Order the posts by published_date, newest first (the minus sign)
    ordering = ['-published_date']from django.shortcuts import render

# Create your views here.
