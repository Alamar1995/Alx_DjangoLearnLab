
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
