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


class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'


def add_post(request):
    context = {}

    # we know there is a form, 
    # we have to just render it on the html file
    form = PostForm(request.POST)
    print("you form looks like this",form)

    # if form is filled
    if form.is_valid():
        form.save()
        context['form'] = form
        return redirect('home')
            # try:
            #     form.save()
            #     context['form'] = form
            #     return redirect('home')
            # except:
            #     pass
    
    # if form is unfilled, then render it on page
    context['form'] = form
    return render(request, 'add_post.html', context)

    # if request.method == 'POST':
    #     if form.is_valid():
    #         try:
    #             form.save()
    #             context['form'] = form
    #             return redirect('home')
    #         except:
    #             pass
    #     else:
    #         return render(request, 'add_post.html', context)
    # else:
    #     return render(request, 'add_post.html', context)
