from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from blogs.models import Blog, Category
from .forms import AddUserForm, BlogPostForm, CategoryForm, EditUserForm
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# =============== CUSTOM DECORATOR ===============
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_staff:
            messages.error(request, "Access denied. Admin privileges required.")
            return redirect('home')  # REDIRECT TO HOME PAGE
        return view_func(request, *args, **kwargs)
    return wrapper

# =============== PROTECTED VIEWS ===============

@admin_required
@login_required(login_url='login')
def dashboard(request):
    category_count = Category.objects.all().count()
    blogs_count = Blog.objects.all().count()
    user_count = User.objects.all().count()

    context = {
        'category_count': category_count,
        'blogs_count': blogs_count,
        'user_count': user_count,
    }
    return render(request, 'dashboard/dashboard.html', context)

@admin_required
@login_required(login_url='login')
def categories(request):
    categories = Category.objects.all().order_by('-created_at')
    context = {'categories': categories}
    return render(request, 'dashboard/categories.html', context)

@admin_required
@login_required(login_url='login')
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('categories')
    form = CategoryForm()
    context = {'form': form}
    return render(request, 'dashboard/add_category.html', context)

@admin_required
@login_required(login_url='login')
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('categories')
    form = CategoryForm(instance=category)
    context = {'form': form, 'category': category}
    return render(request, 'dashboard/edit_category.html', context)

@admin_required
@login_required(login_url='login')
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category deleted successfully!')
    return redirect('categories')

@admin_required
@login_required(login_url='login')
def posts(request):
    posts = Blog.objects.all()
    context = {'posts': posts}
    return render(request, 'dashboard/posts.html', context)

@admin_required
@login_required(login_url='login')
def add_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            title = form.cleaned_data['title']
            post.slug = slugify(title) + '-'+str(post.id)
            post.save()
            messages.success(request, 'Post published successfully!')
            return redirect('posts')
    form = BlogPostForm()
    context = {'form': form}
    return render(request, 'dashboard/add_post.html', context)

@admin_required
@login_required(login_url='login')
def edit_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            title = form.cleaned_data['title']
            post.slug = slugify(title) + '-'+str(post.id)
            post.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('posts')
    form = BlogPostForm(instance=post)
    context = {'form': form, 'post': post}
    return render(request, 'dashboard/edit_post.html', context)

@admin_required
@login_required(login_url='login')
def delete_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    post.delete()
    messages.success(request, 'Post deleted successfully!')
    return redirect('posts')

@admin_required
@login_required(login_url='login')
def users(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'dashboard/users.html', context)

@admin_required
@login_required(login_url='login')
def add_user(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User added successfully!')
            return redirect('users')
    form = AddUserForm()
    context = {'form': form}
    return render(request, 'dashboard/add_user.html', context)

@admin_required
@login_required(login_url='login')
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully!')
            return redirect('users')
    form = EditUserForm(instance=user)
    context = {'form': form}
    return render(request, 'dashboard/edit_user.html', context)

@admin_required
@login_required(login_url='login')
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    messages.success(request, 'User deleted successfully!')
    return redirect('users')