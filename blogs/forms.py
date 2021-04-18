from django import forms

from .models import Post, Comment

# creating a form
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('slug', 'author',)

    def clean(self):
        cleaned_data = super(PostForm, self).clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        if not title or not content:
            raise forms.ValidationError('You have to write something!')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('name', 'post', 'active')
