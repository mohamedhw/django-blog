from datetime import date
from django import forms
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from .models import Post, PostComments
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CommentsFrom
from django.contrib.auth.decorators import login_required, user_passes_test 
from django.http import JsonResponse
from django.core import serializers

class HomeView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'post/post_list_temp.html'
    ordering = ('-date',)
    paginate_by = 5


class UserPostsView(ListView):
    model = Post
    template_name = 'post/user_post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date')




# class PostDetailview(DetailView):
#     model = Post


def aj_comments(request, pk):
    form = CommentsFrom(request.POST or None)
    data = {}

    if request.is_ajax():
        if form.is_valid():
            form.save()
        return JsonResponse(data)

    context = {
        'form': form
    }
    return render(request, )

@login_required
def detailview(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # comments = PostComments.objects.all().filter(post=post)
    form = CommentsFrom(request.POST or None)
    instance_ = None
    # if request.is_ajax():
    #     if form.is_valid():
    #         data = form.save(commit=False)
    #         data.author = request.user
    #         data.post = post
    #         data.save()
    #         return JsonResponse(data)
    if request.method == 'POST':
        form = CommentsFrom(request.POST)
        if form.is_valid():
            instance_ = form.save(commit=False)
            instance_.author = request.user
            instance_.post = post
            instance_.save()
            return JsonResponse({
                "comment" : instance_.comment
            })

        else:
            form = CommentsFrom()
    else:
        form = CommentsFrom()

    context = {
        'post': post,
        'comments': instance_,
        # 'comments': comments,
        'form': form,
    }
    return render(request, 'post/post_detail.html', context)

@login_required
def saved_posts(request):
    user = request.user
    posts = user.save_post.all()
    context = {
        'posts': posts,
    }
    return render(request, "post/saved_posts.html", context)


@login_required
def save_button(request, pk):
    if request.POST.get('action') == 'post':
        data = {}
        post = Post.objects.get(pk=pk)
        if request.user in post.save_post.all():
            post.save_post.remove(request.user)
        else:
            post.save_post.add(request.user)
    return JsonResponse({'data': data})


def aj_get_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = PostComments.objects.all().filter(post=post)
    data = []
    for obj in comments:
        item = {
            "comment": obj.comment,
            "date": obj.date,
            "author": obj.author.username,
            "img": obj.author.profile.image.url,
        }
        data.append(item)
    return JsonResponse({"data":data})


def add_comment(request, pk):
        post = get_object_or_404(Post, pk=pk)
        comments = PostComments.objects.all().filter(post=post)
        instance_ = None
        if request.method == 'POST' and request.is_ajax():
            form = CommentsFrom(request.POST)
            if form.is_valid():
                instance_ = form.save(commit=False)
                instance_.author = request.user
                instance_.post = post
                comment_instance = instance_.save()
                ser_comment = serializers.serialize("json", [comment_instance,])
                return JsonResponse({'comment_instance': ser_comment}, status=200)
        else:
            if request.is_ajax():
                return JsonResponse({'error': forms.errors}, status=400)
            else:
                return JsonResponse({'error': "Invalid request"}, status=400)

        return JsonResponse({"error": ""}, status=400)


@login_required
def like_button(request, pk):
    if request.POST.get('action') == 'post':
        result = ''
        post = Post.objects.get(pk=pk)
        if request.user in post.like.all():
            post.like.remove(request.user)
            post.like_count -= 1
            result = post.like_count
            post.save()
        else:
            post.like.add(request.user)
            post.like_count += 1
            result = post.like_count
            post.save()
    return JsonResponse({'result': result})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url ="/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False    

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = [
        'body',
        'image',
    ]

    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)



class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['body', 'image']
    template_name = "post/post_update.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

@login_required
def searchpost(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        posts = Post.objects.filter(body__contains=searched)
        context = {
            'searched' : searched,
            'posts' : posts,
        }
        return render(request, 'post/search_temp.html', context)
    else:
        return render(request, 'post/search_temp.html',{})


# def createcomment(request, pk):
#     instance_ = None
#     if request.method == 'POST':
#         form = CommentsFrom(request.POST)
#         if form.is_valid():
#             instance_ = form.save(commit=False)
#             instance_.author = User
#             instance_.post = post
#             instance_.save()
#     else:
#         form = CommentsFrom()
#     context = {
#         'form': form
#     }
#     return render(request, 'post/commenttemp.html', context)

# class CommentCreateView(LoginRequiredMixin, CreateView):
#     model = PostComments
#     template_name = 'post/commenttemp.html'
#     fields = ['content']
#     success_url = "/"
#     print(date)


# class CommentView(ListView):
#     model = PostComments
#     template_name = 'post/comment_temp.html'
#     ordering = ['-date']


# def add_comment_to_post(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = CommentForm()
#     return render(request, 'post/commenttemp.html', {'form': form})