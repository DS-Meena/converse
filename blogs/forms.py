from django import forms

from .models import Post

# creating a form
class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = "__all__"