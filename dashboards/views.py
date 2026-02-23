from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from blogs.models import Blog, Category, RegisteredUser
from .forms import AddUserForm, BlogPostForm, CategoryForm, EditUserForm
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


def notify_subscribers_new_post(post):
    """Send email notification to all subscribers when a new blog is published."""
    subscribers = RegisteredUser.objects.all()
    recipient_list = [sub.email for sub in subscribers]
    if not recipient_list:
        return

    subject = f'New Post: {post.title}'
    plain_message = (
        f'Hi there!\n\n'
        f'A new blog post has been published on Inspiring Blogs:\n\n'
        f'Title: {post.title}\n'
        f'Category: {post.category.category_name}\n\n'
        f'{post.short_description}\n\n'
        f'Read the full article at: http://127.0.0.1:8000/blogs/{post.slug}/\n\n'
        f'Thank you for subscribing!\n'
        f'— Inspiring Blogs Team'
    )
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background:#f8f9fa; padding:20px;">
      <div style="max-width:600px; margin:0 auto; background:white; border-radius:12px;
                  box-shadow:0 4px 20px rgba(0,0,0,0.1); overflow:hidden;">
        <div style="background:linear-gradient(135deg,#ffc107,#ff9800); padding:30px; text-align:center;">
          <h1 style="color:white; margin:0; font-size:24px;">📰 New Blog Post!</h1>
          <p style="color:rgba(255,255,255,0.9); margin:8px 0 0;">Inspiring Blogs</p>
        </div>
        <div style="padding:30px;">
          <h2 style="color:#333; font-size:22px; margin-bottom:10px;">{post.title}</h2>
          <p style="display:inline-block; background:#fff3cd; color:#856404; padding:4px 12px;
                    border-radius:20px; font-size:13px; margin-bottom:16px;">
            📁 {post.category.category_name}
          </p>
          <p style="color:#555; line-height:1.7; font-size:15px;">{post.short_description}</p>
          <div style="text-align:center; margin-top:24px;">
            <a href="http://127.0.0.1:8000/blogs/{post.slug}/"
               style="background:linear-gradient(135deg,#ffc107,#ff9800); color:#212529;
                      padding:12px 28px; border-radius:25px; text-decoration:none;
                      font-weight:bold; font-size:15px;">
              Read Full Article →
            </a>
          </div>
        </div>
        <div style="background:#f8f9fa; padding:16px; text-align:center;
                    font-size:12px; color:#888;">
          You're receiving this because you subscribed to Inspiring Blogs.
        </div>
      </div>
    </body>
    </html>
    """

    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        html_message=html_message,
        fail_silently=True,
    )

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
    subscriber_count = RegisteredUser.objects.all().count()
    published_count = Blog.objects.filter(status='Published').count()
    recent_subscribers = RegisteredUser.objects.order_by('-created_at')[:5]

    context = {
        'category_count': category_count,
        'blogs_count': blogs_count,
        'user_count': user_count,
        'subscriber_count': subscriber_count,
        'published_count': published_count,
        'recent_subscribers': recent_subscribers,
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
            post.slug = slugify(title) + '-' + str(post.id)
            post.save()
            if post.status == 'Published':
                notify_subscribers_new_post(post)
            messages.success(request, 'Post published successfully!')
            return redirect('posts')
    form = BlogPostForm()
    context = {'form': form}
    return render(request, 'dashboard/add_post.html', context)

@admin_required
@login_required(login_url='login')
def edit_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    old_status = post.status
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            title = form.cleaned_data['title']
            post.slug = slugify(title) + '-' + str(post.id)
            post.save()
            if post.status == 'Published' and old_status != 'Published':
                notify_subscribers_new_post(post)
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


@admin_required
@login_required(login_url='login')
def subscribers(request):
    subscriber_list = RegisteredUser.objects.all().order_by('-created_at')
    context = {'subscribers': subscriber_list, 'count': subscriber_list.count()}
    return render(request, 'dashboard/subscribers.html', context)


@admin_required
@login_required(login_url='login')
def delete_subscriber(request, pk):
    subscriber = get_object_or_404(RegisteredUser, pk=pk)
    subscriber.delete()
    messages.success(request, 'Subscriber removed successfully!')
    return redirect('subscribers')