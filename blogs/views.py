from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.views import generic
from .models import Post
from .forms import PostForm


# Create your views here.
class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 5

# To see a particular post
class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'


# Function to slugify for the url
def slugify(title):
    t = '-'.join(title.split())
    #check it the same title post already exists
    postCheck = Post.objects.filter(slug=t).count()
    print(postCheck)
    print(title)
    if postCheck==0:
        return t
    else:
        return (t+'-%s'% postCheck)

# Function to add post
def add_post(request):
    # Username in user var
    user = request.user

    context = {}
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.slug = slugify(post.title)
        post.author = user
        post.save()
        return render(request, 'add_post.html', context)
    context['form'] = form
    return render(request, 'add_post.html', context)