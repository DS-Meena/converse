from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from django.views import generic
from .models import Post
from .forms import PostForm, CommentForm
from account.models import Account


# Create your views here.
class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 5

# To see a particular post
# class PostDetail(generic.DetailView):
#     model = Post
#     template_name = 'post_detail.html'


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
        # this should go to all blogs page after adding post
        return redirect('/blogs')
        # return render(request, 'add_post.html', context)
        
    context['form'] = form
    return render(request, 'add_post.html', context)



def post_detail(request, slug):
    user = request.user
    template_name = "post_detail.html"
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True).order_by("-created_on")
    new_comment = None
    # Comment posted
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Assign username of commenter
            new_comment.name = user
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(
        request,
        template_name,
        {
            "post": post,
            "comments": comments,
            "new_comment": new_comment,
            "comment_form": comment_form,
        },
    )


def blog_list_view(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        user_id = kwargs.get("user_id")
        if user_id:
            try:
                this_user = Account.objects.get(pk=user_id)
                context['this_user'] = this_user
            except Account.DoesNotExist:
                return HttpResponse("That user does not exist.")
            try:
                blog_list = Post.objects.filter(author=this_user)
               # print(blog_list)
            except Post.DoesNotExist:
                return HttpResponse(f"Could not find any posts for {this_user.username}")

            blogs = []  # [(friend1, True), (friend2, False), ...]
            # get the authenticated users friend list
            auth_user_friend_list = Post.objects.filter(author=this_user)
            for blog in blog_list.all():
                blogs.append((blog))
            context['blogs'] = blogs
    else:
        return HttpResponse("You must be logged in to view the blog list.")
    return render(request, "blog_list.html", context)

def updateStatus(request, slug):
    post = Post.objects.get(slug=slug)
    post.status = not post.status
    print(post.status)
    post.save()
    blogs = []
    user = request.user
    blog_list = Post.objects.filter(author=user)
    for blog in blog_list.all():
        blogs.append((blog))
    context = {'blogs':blogs}
    
    return render(request, 'blog_list.html', context)
  