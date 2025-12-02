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
