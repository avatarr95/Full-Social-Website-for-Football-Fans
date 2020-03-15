from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from .models import Post, Comment
from .forms import CommentForm, RegisterForm, NewPostForm
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from bs4 import BeautifulSoup
from django.contrib import messages


# Getting all Posts with "published" status. This will be displayed on main domain.
class IndexView(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status="published")
    context_object_name = "posts"
    template_name = "valverde/index.html"


def post_detail(request, pk, post):
    post = get_object_or_404(Post, status="published", pk=pk, slug=post) # Only posts with "published" status will be visible for the user
    comments = post.comments.filter(active=True) # All comments with active status, as we can delete or make inactive those, which are inapproppriate 
    can_edit = False # Only post's author will be able to edit his/her post.
    edit_link = "" # This will be the link, where post's author will be able to edit his content
    if request.user == post.author:
        can_edit = True
        edit_link = str(post.get_absolute_url()+"/edit")
    else: 
        pass

    if request.method == "POST":
        comment_form = CommentForm(request.POST) # Assigning a form with the data entered by a user to a variable
        if comment_form.is_valid(): # Checking, whether the form has been filled correctly
            new_comment = comment_form.save(commit=False)
            new_comment.post = post # Before adding to database, we will attach the comment to the post
            try:
                parent_id = request.POST.get("parent_id") # Comments without parent_ids will be parent comments, comments with parent_ids will be replies
            except:
                parent_id = None

            # Assigning parent_id (if exists)  and author to a comment
            new_comment.parent_id = parent_id
            new_comment.author = request.user
            new_comment.save()
            return HttpResponseRedirect(request.path_info)
    else:
        comment_form = CommentForm()

    return render(request, 'valverde/post_detail.html', {'post': post, 'comment_form': comment_form, 'comments': comments, "can_edit": can_edit, "edit_link": edit_link})

# Creating a new user and adding him/her to a database
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


# Contact details
def contact(request):
    return render(request, 'valverde/contact.html', {})


# The procedure of liking comments and comment replies
@login_required
@require_POST
def comments_like(request):
    comment_id = request.POST.get("id")
    action = request.POST.get("action")
    if comment_id and action:
        try:
            comment = Comment.objects.get(id=comment_id)
            if action == 'like':
                comment.users_like.add(request.user)
            else: 
                comment.users_like.remove(request.user)
        except:
            pass
    return JsonResponse({"status": "ok"})



# Users can add new posts, which then will be reviewed by a staff member
def add_a_new_post(request):
    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.status = "draft"
            new_post.save()
            messages.success(request, "Your post has been added succesfully and will be revieved by our team")
            return HttpResponseRedirect(request.path)
    else:
        form = NewPostForm()

    return render(request, 'valverde/add_a_post.html', {'form': form})

# Here the author can edit his post. After making a changes and submitting, post will be reviewed by a staff member
def post_edit(request, pk=None, post=None):
    post = get_object_or_404(Post, pk=pk, slug=post)
    form = NewPostForm(request.POST or None, instance=post)
    if request.user != post.author:
        return HttpResponseForbidden()
    if form.is_valid():
        post = form.save(commit=False)
        post.status = "draft"
        post.save()
        messages.success(request, "Your post has been edited succesfully and will be reviewed by our team")

    context = {
        'title': post.title,
        'post': post,
        "form": form,
    }
    return render(request, "valverde/post_edit.html", context)


    