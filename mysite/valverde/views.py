from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Post, Comment
from .forms import CommentForm, RegisterForm
from django.http import HttpResponseRedirect


class IndexView(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status="published")
    context_object_name = "posts"
    template_name = "valverde/index.html"


def post_detail(request, pk, post):
    post = get_object_or_404(Post, status="published", pk=pk, slug=post)

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            return HttpResponseRedirect(request.path_info)
    else:
        comment_form = CommentForm()

    return render(request, 'valverde/post_detail.html', {'post': post, 'comment_form': comment_form})




def register(request):
    if request.method == "POST":
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, "valverde/register_done.html", {'new_user': new_user})
    else:
        user_form = RegisterForm()
    return render (request, "valverde/register.html", {'user_form': user_form})


def contact(request):
    return render(request, 'valverde/contact.html', {})