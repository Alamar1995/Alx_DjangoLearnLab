
# blog/urls.py (UPDATED)

from django.urls import path
from . import views
from .views import ( # <-- IMPORT THE CBVs
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)

urlpatterns = [
    # Blog Homepage (uses PostListView)
    path('', PostListView.as_view(), name='blog-home'),
    
    # R - READ (Detail)
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    
    # C - CREATE
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    
    # U - UPDATE
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    
    # D - DELETE
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    
    # Custom Authentication URLs (Keep these)
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]
# blog/urls.py (UPDATED with Comment URLs)

# ... existing imports ...

urlpatterns = [
    # ... existing Post and Auth URLs ...

    # Comment URLs
    # C - CREATE Comment (Uses function-based view for simplicity)
    path('post/<int:pk>/comment/new/', views.add_comment_to_post, name='add-comment'),
    
    # U - UPDATE Comment (Note: uses <int:pk> for the Comment ID, not the Post ID)
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment-update'),
    
    # D - DELETE Comment
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),
    
    # ... existing register/profile URLs ...
]
# blog/urls.py (UPDATED)

# ... existing imports ...

urlpatterns = [
    # ... existing Post and Auth URLs ...
    
    # SEARCH URL
    path('search/', views.post_search, name='post-search'), # <-- ADD THIS
    
    # TAG URL (Shows posts with a specific tag)
    path('tags/<slug:tag_slug>/', views.PostListView.as_view(), name='posts-by-tag'), # <-- ADD THIS

    # ... existing register/profile URLs ...
]
