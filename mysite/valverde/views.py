from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Post, Comment
from .forms import CommentForm, RegisterForm, NewPostForm
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


class IndexView(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status="published")
    context_object_name = "posts"
    template_name = "valverde/index.html"


def post_detail(request, pk, post):
    post = get_object_or_404(Post, status="published", pk=pk, slug=post)
    comments = post.comments.filter(active=True)

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

    return render(request, 'valverde/post_detail.html', {'post': post, 'comment_form': comment_form, 'comments': comments})




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


@login_required
@require_POST
def post_like(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    if post_id and action:
        try:
            post = Post.objects.get(id=post_id)
            if action == 'like':
                post.users_like.add(request.user)
            else:
                post.users_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'ok'})


def add_a_new_post(request):
    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.status = "draft"
            new_post.save()
            return HttpResponseRedirect(request.path)
    else:
        form = NewPostForm()

    return render(request, 'valverde/add_a_post.html', {'form': form})