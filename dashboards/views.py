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

    subject = f'✨ New Article: {post.title} | Inspiring Blogs'
    plain_message = (
        f'Hello!\n\n'
        f'A brand new article has just been published on Inspiring Blogs!\n\n'
        f'Title    : {post.title}\n'
        f'Category : {post.category.category_name}\n'
        f'Summary  : {post.short_description}\n\n'
        f'Read the full article here:\n'
        f'http://127.0.0.1:8000/blogs/{post.slug}/\n\n'
        f'Thanks for being part of our community!\n'
        f'— Satheesh Yadav\n'
        f'  Inspiring Blogs | satheeshyadav85@gmail.com'
    )
    html_message = f"""
    <html>
    <body style="margin:0; padding:0; background:#f0f2f5; font-family:'Segoe UI',Arial,sans-serif;">
      <div style="max-width:620px; margin:30px auto; background:white;
                  border-radius:18px; overflow:hidden;
                  box-shadow:0 8px 32px rgba(0,0,0,0.10);">

        <!-- Header -->
        <div style="background:linear-gradient(135deg,#1a1a2e 0%,#16213e 100%);
                    padding:36px 30px; text-align:center; position:relative;">
          <div style="font-size:42px; margin-bottom:10px;">📰</div>
          <h1 style="color:#ffc107; margin:0; font-size:26px; font-weight:800;
                     letter-spacing:0.5px;">New Article Published!</h1>
          <p style="color:rgba(255,255,255,0.7); margin:8px 0 0; font-size:14px;">
            Inspiring Blogs &nbsp;•&nbsp; satheeshyadav85@gmail.com
          </p>
        </div>

        <!-- Category badge -->
        <div style="padding:20px 30px 0; text-align:center;">
          <span style="background:linear-gradient(135deg,#ffc107,#ff9800);
                       color:#212529; font-size:12px; font-weight:700;
                       padding:5px 16px; border-radius:20px;
                       text-transform:uppercase; letter-spacing:0.8px;">
            📁 {post.category.category_name}
          </span>
        </div>

        <!-- Article info -->
        <div style="padding:24px 30px;">
          <h2 style="color:#1a1a2e; font-size:22px; font-weight:800;
                     margin:0 0 14px; line-height:1.35;">{post.title}</h2>
          <p style="color:#555; line-height:1.8; font-size:15px;
                    margin:0 0 24px; border-left:4px solid #ffc107;
                    padding-left:14px; background:#fffdf0;
                    border-radius:0 8px 8px 0; padding:12px 14px;">
            {post.short_description}
          </p>

          <!-- CTA Button -->
          <div style="text-align:center; margin:28px 0 10px;">
            <a href="http://127.0.0.1:8000/blogs/{post.slug}/"
               style="background:linear-gradient(135deg,#ffc107,#ff9800);
                      color:#212529; padding:14px 36px; border-radius:30px;
                      text-decoration:none; font-weight:800; font-size:15px;
                      display:inline-block; box-shadow:0 4px 15px rgba(255,193,7,0.4);">
              Read Full Article &rarr;
            </a>
          </div>
        </div>

        <!-- Divider -->
        <div style="height:1px; background:linear-gradient(to right,transparent,#e0e0e0,transparent);
                    margin:0 30px;"></div>

        <!-- Footer -->
        <div style="padding:20px 30px; text-align:center; background:#fafafa;">
          <p style="margin:0 0 6px; font-size:13px; color:#444; font-weight:600;">
            Satheesh Yadav &nbsp;|&nbsp; Inspiring Blogs
          </p>
          <p style="margin:0; font-size:12px; color:#999;">
            You received this because you subscribed at Inspiring Blogs.
          </p>
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