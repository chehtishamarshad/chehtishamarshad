from django.shortcuts import render,redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth import logout
from django.db.models import Q
from .models import Post
from .models import Post
from .forms import PostForm

# Create your views here.


def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts': posts})

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post-detail', id=post.id)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_update(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post-detail', id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})


@login_required
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        post.delete()
        return redirect('blog-home')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'You are now logged in as {username}.')
                return redirect('blog-home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})



def logout_view(request):
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('login')

@login_required
def profile(request):
    return render(request, 'blog/profile.html')

def search(request):
    query = request.GET.get('q')
    results = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
    return render(request, 'blog/search_results.html', {'results': results})



# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import login, authenticate, logout
# from django.contrib import messages
# from django.db.models import Q
# from .models import Post, Comment, Profile
# from .forms import PostForm, UserRegisterForm




# def home(request):
#     posts = Post.objects.all()
#     return render(request, 'blog/home.html', {'posts': posts})

# def post_detail(request, id):
#     post = get_object_or_404(Post, id=id)
#     comments = post.comments.all()
#     if request.method == 'POST':
#         content = request.POST.get('content')
#         comment = Comment.objects.create(post=post, author=request.user, content=content)
#         comment.save()
#         return redirect('post-detail', id=post.id)
#     return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments})

# @login_required
# def post_create(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             return redirect('post-detail', id=post.id)
#     else:
#         form = PostForm()
#     return render(request, 'blog/post_form.html', {'form': form})

# @login_required
# def post_update(request, id):
#     post = get_object_or_404(Post, id=id)
#     if request.method == 'POST':
#         form = PostForm(request.POST, instance=post)
#         if form.is_valid():
#             form.save()
#             return redirect('post-detail', id=post.id)
#     else:
#         form = PostForm(instance=post)
#     return render(request, 'blog/post_form.html', {'form': form})

# @login_required
# def post_delete(request, id):
#     post = get_object_or_404(Post, id=id)
#     if request.method == 'POST':
#         post.delete()
#         return redirect('blog-home')
#     return render(request, 'blog/post_confirm_delete.html', {'post': post})

# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, f'Account created for {username}!')
#             return redirect('login')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'blog/register.html', {'form': form})

# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 messages.info(request, f'You are now logged in as {username}.')
#                 return redirect('blog-home')
#             else:
#                 messages.error(request, 'Invalid username or password.')
#         else:
#             messages.error(request, 'Invalid username or password.')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'blog/login.html', {'form': form})

# def logout_view(request):
#     logout(request)
#     messages.info(request, 'You have successfully logged out.')
#     return redirect('login')

# @login_required
# def profile(request):
#     return render(request, 'blog/profile.html')

# def search(request):
#     query = request.GET.get('q')
#     results = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
#     return render(request, 'blog/search_results.html', {'results': results})
