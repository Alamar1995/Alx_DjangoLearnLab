# blog/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Extends the default form to require/include the email field
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
# blog/forms.py (ADDITIONS)

from .models import Comment # <-- NEW IMPORT

# ... (Keep existing UserRegisterForm definition) ...

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Join the discussion...'}),
        }
