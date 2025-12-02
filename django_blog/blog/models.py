# blog/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# Existing Post Model (Ensure this is still present)
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # Used by CreateView/UpdateView to redirect after success
        return reverse('post-detail', kwargs={'pk': self.pk})

# NEW COMMENT MODEL
class Comment(models.Model):
    # Foreign Key to the Post it belongs to
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    
    # Foreign Key to the User who wrote the comment
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # The actual text content
    content = models.TextField()
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at'] # Display newest comments last
        verbose_name_plural = "Comments"

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    
    def get_absolute_url(self):
        # Redirect back to the post detail page after a successful action (edit/delete)
        return reverse('post-detail', kwargs={'pk': self.post.pk})
