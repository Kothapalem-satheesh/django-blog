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
        return JsonResponse({'status': 'removed', 'count': blog.bookmarks.count()}) # type: ignore
    return JsonResponse({'status': 'added', 'count': blog.bookmarks.count()}) # type: ignore


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
                f'Welcome to Inspiring Blogs! Your subscription is confirmed.\n\n'
                f'You will now receive an email every time a new article is published.\n\n'
                f'Visit us: http://127.0.0.1:8000/\n\n'
                f'Thank you for joining our community!\n'
                f'— Satheesh Yadav\n'
                f'  Inspiring Blogs | satheeshyadav85@gmail.com'
            )
            html_message = f"""
            <html>
            <body style="margin:0; padding:0; background:#f0f2f5;
                         font-family:'Segoe UI',Arial,sans-serif;">
              <div style="max-width:600px; margin:30px auto; background:white;
                          border-radius:18px; overflow:hidden;
                          box-shadow:0 8px 32px rgba(0,0,0,0.10);">

                <!-- Header -->
                <div style="background:linear-gradient(135deg,#1a1a2e 0%,#16213e 100%);
                            padding:40px 30px; text-align:center;">
                  <div style="width:72px; height:72px; margin:0 auto 16px;
                              background:linear-gradient(135deg,#ffc107,#ff9800);
                              border-radius:50%; display:flex; align-items:center;
                              justify-content:center; font-size:32px;
                              line-height:72px; text-align:center;">
                    🎉
                  </div>
                  <h1 style="color:#ffc107; margin:0; font-size:28px; font-weight:800;">
                    Welcome Aboard!
                  </h1>
                  <p style="color:rgba(255,255,255,0.75); margin:8px 0 0; font-size:14px;">
                    Inspiring Blogs &nbsp;•&nbsp; satheeshyadav85@gmail.com
                  </p>
                </div>

                <!-- Body -->
                <div style="padding:32px 30px;">
                  <p style="font-size:18px; color:#1a1a2e; font-weight:700; margin:0 0 8px;">
                    Hi {user.name}! 👋
                  </p>
                  <p style="color:#555; line-height:1.8; font-size:15px; margin:0 0 20px;">
                    You have successfully subscribed to <strong>Inspiring Blogs</strong>.
                    You are now part of a growing community of curious readers passionate
                    about Technology, Programming, Web Development, and AI.
                  </p>

                  <!-- What to expect box -->
                  <div style="background:#f8f9ff; border:1px solid #e0e7ff;
                              border-radius:12px; padding:18px 20px; margin-bottom:24px;">
                    <p style="margin:0 0 10px; font-weight:700; color:#1a1a2e; font-size:14px;">
                      📬 What happens next?
                    </p>
                    <ul style="margin:0; padding-left:18px; color:#555; font-size:14px;
                               line-height:2;">
                      <li>You'll get an email every time a new article is published</li>
                      <li>Fresh content on Technology, Programming, Web Dev &amp; AI</li>
                      <li>No spam — only real articles, straight to your inbox</li>
                    </ul>
                  </div>

                  <!-- CTA -->
                  <div style="text-align:center; margin-top:10px;">
                    <a href="http://127.0.0.1:8000/"
                       style="background:linear-gradient(135deg,#ffc107,#ff9800);
                              color:#212529; padding:14px 36px; border-radius:30px;
                              text-decoration:none; font-weight:800; font-size:15px;
                              display:inline-block;
                              box-shadow:0 4px 15px rgba(255,193,7,0.4);">
                      Explore Latest Articles &rarr;
                    </a>
                  </div>
                </div>

                <!-- Divider -->
                <div style="height:1px;
                            background:linear-gradient(to right,transparent,#e0e0e0,transparent);
                            margin:0 30px;"></div>

                <!-- Footer -->
                <div style="padding:20px 30px; text-align:center; background:#fafafa;">
                  <p style="margin:0 0 4px; font-size:13px; color:#444; font-weight:600;">
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