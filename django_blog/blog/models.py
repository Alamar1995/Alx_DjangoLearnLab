
# blog/models.py
from django.db import models
from django.contrib.auth.models import User  # Import Django's built-in User model

class Post(models.Model):
    # Field to store the title of the post
    title = models.CharField(max_length=200)

    # Field for the main, long-form content of the post
    content = models.TextField()

    # Automatically sets the date/time when the object is first created
    published_date = models.DateTimeField(auto_now_add=True)

    # ForeignKey creates a one-to-many relationship (one author, many posts)
    # models.CASCADE ensures all posts are deleted if the author is deleted
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        # This determines the readable representation of a Post object (e.g., in the Admin site)
        return self.title
