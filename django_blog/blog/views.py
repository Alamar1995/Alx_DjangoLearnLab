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
# blog/views.py (ADDITIONS)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.forms import UserChangeForm # We'll use this for now

# ... (Keep the existing PostListView definition) ...

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
