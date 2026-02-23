from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .context_processors import get_categories, get_social_links
from .forms import RegistrationForm
from .models import Blog, Bookmark, Category, Comment



def posts_by_category(request, category_id):
    # Fetch the posts that belongs to the category with the id category_id
    posts = Blog.objects.filter(status='Published', category=category_id)
    # Use try/except when we want to do some custom action if the category does not exists
    # try:
    #     category = Category.objects.get(pk=category_id)
    # except:
    #     # redirect the user to homepage
    #     return redirect('home')
    
    # Use get_object_or_404 when you want to show 404 error page if the category does not exist
    category = get_object_or_404(Category, pk=category_id)
    
    context = {
        'posts': posts,
        'category': category,
    }
    return render(request, 'posts_by_category.html', context)



def blogs(request, slug):
    single_blog = get_object_or_404(Blog, slug=slug, status='Published')
    if request.method == 'POST':
        if not request.user.is_authenticated:
            from django.contrib import messages
            messages.error(request, 'You must be logged in to comment.')
            return HttpResponseRedirect(request.path_info)
        comment = Comment()
        comment.user = request.user
        comment.blog = single_blog
        comment.comment = request.POST['comment']
        comment.save()
        return HttpResponseRedirect(request.path_info)

    # Comments
    comments = Comment.objects.filter(blog=single_blog).order_by('-created_at')
    comment_count = comments.count()

    # Related posts — same category, exclude current
    related_posts = Blog.objects.filter(
        status='Published',
        category=single_blog.category
    ).exclude(pk=single_blog.pk).order_by('-created_at')[:4]

    # If fewer than 2 related in same category, fill from other categories
    if related_posts.count() < 2:
        related_posts = Blog.objects.filter(
            status='Published'
        ).exclude(pk=single_blog.pk).order_by('-created_at')[:4]

    context = {
        'single_blog': single_blog,
        'comments': comments,
        'comment_count': comment_count,
        'related_posts': related_posts,
    }
    return render(request, 'blogs.html', context)

def search(request):
    keyword = request.GET.get('keyword')
    
    blogs = Blog.objects.filter(Q(title__icontains=keyword) | Q(short_description__icontains=keyword) | Q(blog_body__icontains=keyword), status='Published')
  
    context = {
        'blogs': blogs,
        'keyword': keyword,
    }
    return render(request, 'search.html', context)




def custom_404(request, exception=None): 
    """
    Custom 404 handler that passes all required context
    """
    print(f"404 Error: {request.path}")  # Debug
    
    # Get categories using your context processor
    categories = get_categories(request).get('categories', [])
    
    # Get social links using your context processor
    social_links = get_social_links(request).get('social_links', {})
    
    context = {
        'categories': categories,
        'social_links': social_links,
        'exception': str(exception) if exception else "Page not found",
    }
    
    return render(request, '404.html', context, status=404)

@login_required(login_url='login')
def toggle_bookmark(request, blog_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    blog = get_object_or_404(Blog, id=blog_id, status='Published')
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, blog=blog)
    if not created:
        bookmark.delete()
        return JsonResponse({'status': 'removed', 'count': blog.bookmarks.count()})
    return JsonResponse({'status': 'added', 'count': blog.bookmarks.count()})


@login_required(login_url='login')
def my_bookmarks(request):
    bookmarks = Bookmark.objects.filter(
        user=request.user
    ).select_related('blog', 'blog__category', 'blog__author').order_by('-created_at')
    return render(request, 'bookmarks.html', {'bookmarks': bookmarks})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            plain_message = (
                f'Hi {user.name},\n\n'
                f'Welcome to Inspiring Blogs! You have successfully subscribed.\n\n'
                f'You will now receive email notifications whenever a new article is published.\n\n'
                f'Visit us at: http://127.0.0.1:8000/\n\n'
                f'Thank you,\nInspiring Blogs Team'
            )
            html_message = f"""
            <html>
            <body style="font-family:Arial,sans-serif; background:#f8f9fa; padding:20px; margin:0;">
              <div style="max-width:580px; margin:0 auto; background:white; border-radius:16px;
                          box-shadow:0 4px 20px rgba(0,0,0,0.1); overflow:hidden;">
                <div style="background:linear-gradient(135deg,#ffc107,#ff9800); padding:36px 30px; text-align:center;">
                  <div style="font-size:48px; margin-bottom:12px;">🎉</div>
                  <h1 style="color:white; margin:0; font-size:26px; font-weight:700;">
                    You're Subscribed!
                  </h1>
                  <p style="color:rgba(255,255,255,0.9); margin:8px 0 0; font-size:15px;">
                    Welcome to Inspiring Blogs
                  </p>
                </div>
                <div style="padding:32px 30px;">
                  <p style="font-size:16px; color:#333; margin-bottom:8px;">
                    Hi <strong>{user.name}</strong>,
                  </p>
                  <p style="color:#555; line-height:1.7; font-size:15px;">
                    Thank you for subscribing! You are now part of our growing community of readers.
                    We'll send you an email every time a new article goes live — so you never miss a post.
                  </p>
                  <div style="background:#fff8e1; border-left:4px solid #ffc107; padding:14px 18px;
                              border-radius:8px; margin:24px 0;">
                    <p style="margin:0; color:#856404; font-size:14px;">
                      <strong>📬 What to expect:</strong><br>
                      Notifications for every new published article, straight to this inbox.
                    </p>
                  </div>
                  <div style="text-align:center; margin-top:28px;">
                    <a href="http://127.0.0.1:8000/"
                       style="background:linear-gradient(135deg,#ffc107,#ff9800); color:#212529;
                              padding:13px 30px; border-radius:25px; text-decoration:none;
                              font-weight:bold; font-size:15px; display:inline-block;">
                      Read Latest Articles →
                    </a>
                  </div>
                </div>
                <div style="background:#f8f9fa; padding:16px 30px; text-align:center;
                            font-size:12px; color:#999;">
                  You received this because you subscribed at Inspiring Blogs.
                </div>
              </div>
            </body>
            </html>
            """

            send_mail(
                subject='Welcome to Inspiring Blogs! 🎉',
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )

            return render(request, 'successful.html')

    else:
        form = RegistrationForm()

    return render(request, 'subscribe.html', {'form': form})