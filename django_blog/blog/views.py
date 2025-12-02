# blog/views.py

from django.views.generic import ListView
from .models import Post

# Use Django's built-in ListView to fetch and display multiple object
# blog/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # <-- NEW IMPORTS
from django.views.generic import ( # <-- UPDATED IMPORTS
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm # Still needed for profile view
from .forms import UserRegisterForm
from .models import Post, User 

# --- Authentication Views (Keep these as they were) ---
# ... register(request) function ...
# ... profile(request) function ...
# ------------------------------------------------------


# --- Blog Post Views (CRUD) ---

class PostListView(ListView):
    # R - READ (List)
    model = Post
    template_name = 'blog/home.html'  # Use the existing home template
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 5 # Optional: Add pagination

class PostDetailView(DetailView):
    # R - READ (Detail)
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    # C - CREATE
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content'] # We only ask for these two fields

    def form_valid(self, form):
        # Automatically set the author to the logged-in user
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    # U - UPDATE
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        # Automatically set the author to the logged-in user (though it shouldn't change)
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        # REQUIRED BY UserPassesTestMixin: Ensures only the author can update
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    # D - DELETE
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/' # Redirect to the homepage after successful deletion

    def test_func(self):
        # REQUIRED BY UserPassesTestMixin: Ensures only the author can delete
        post = self.get_object()
        return self.request.user == post.author

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form, 'title': 'Register'})

@login_required
def profile(request):
    if request.method == 'POST':
        # Simple profile update using built-in form
        form = UserChangeForm(request.POST, instance=request.user)
        # Note: UserChangeForm needs to be subclassed to remove password fields
        # but for simplicity now, we use the base form.
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile')
    else:
        form = UserChangeForm(instance=request.user)

    # We need to remove the password fields from the form for a proper UI
    form.fields.pop('password') 
    
    return render(request, 'blog/profile.html', {'form': form, 'title': 'Profile'})
# blog/views.py (ADDITIONS)

from .forms import UserRegisterForm, CommentForm # <-- UPDATED IMPORT
from .models import Post, User, Comment         # <-- UPDATED IMPORT

# ... (Keep existing Post, register, and profile views) ...

# ------------------------------------------------------------------
# Comment Views (CRUD)
# ------------------------------------------------------------------

@login_required
def add_comment_to_post(request, pk):
    """Handles adding a new comment directly from the post detail page."""
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment was posted successfully!')
            return redirect('post-detail', pk=post.pk)
    else:
        # If accessing via GET, the form will be displayed on the detail page
        return redirect('post-detail', pk=post.pk)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    # U - UPDATE Comment
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    # We don't need to specify success_url here because the model's get_absolute_url
    # method will redirect to the post detail page automatically.
    
    def test_func(self):
        # Only the author can update the comment
        comment = self.get_object()
        return self.request.user == comment.author


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    # D - DELETE Comment
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    
    def get_success_url(self):
        # Redirect to the post detail page after deletion
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        # Only the author can delete the comment
        comment = self.get_object()
        return self.request.user == comment.author

# Ensure you keep your existing PostListView, DetailView, etc. below this
# blog/views.py (UPDATED)

# ... (Keep all imports) ...

class PostDetailView(DetailView):
    # R - READ (Detail)
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs): # <-- ADD THIS METHOD
        context = super().get_context_data(**kwargs)
        # Add the CommentForm to the context for use in the template
        context['form'] = CommentForm() 
        return context
