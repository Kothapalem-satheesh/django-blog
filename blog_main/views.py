# from django.shortcuts import redirect, render
# from django.contrib import messages  # ADD THIS IMPORT
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib import auth

# from blogs.models import Blog, Category
# from assignments.models import About
# from .forms import RegistrationForm

# def home(request):
#     featured_posts = Blog.objects.filter(is_featured=True, status='Published').order_by('updated_at')
#     posts = Blog.objects.filter(is_featured=False, status='Published')
    
#     # Fetch about us
#     try:
#         about = About.objects.get()
#     except:
#         about = None
#     context = {
#         'featured_posts': featured_posts,
#         'posts': posts,
#         'about': about,
#     }
#     return render(request, 'home.html', context)


# def register(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
            
#             # ADD SUCCESS MESSAGE
#             messages.success(request, 'Account created successfully! Please login with your credentials.')
            
#             # REDIRECT TO LOGIN PAGE (NOT REGISTER PAGE)
#             return redirect('login')  # CHANGED FROM 'register' TO 'login'
#         else:
#             # SHOW FORM ERRORS AS MESSAGES
#             for field, errors in form.errors.items():
#                 for error in errors:
#                     messages.error(request, f"{field}: {error}")
#     else:
#         form = RegistrationForm()
    
#     context = {
#         'form': form,
#     }
#     return render(request, 'register.html', context)


# def login(request):
#     # IF USER IS ALREADY LOGGED IN, REDIRECT THEM
#     if request.user.is_authenticated:
#         if request.user.is_staff:
#             return redirect('dashboard')
#         else:
#             return redirect('home')
    
#     if request.method == 'POST':
#         form = AuthenticationForm(request, request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']

#             user = auth.authenticate(username=username, password=password)
#             if user is not None:
#                 auth.login(request, user)
#                 messages.success(request, f'Welcome back, {username}!')
                
#                 # REDIRECT BASED ON USER TYPE
#                 if user.is_staff:
#                     return redirect('dashboard')
#                 else:
#                     return redirect('home')
#         else:
#             messages.error(request, 'Invalid username or password.')
    
#     form = AuthenticationForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'login.html', context)


# def logout(request):
#     auth.logout(request)
#     messages.success(request, 'You have been logged out successfully.')
#     return redirect('home')




from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.http import Http404

from blogs.models import Blog, Category
from assignments.models import About, SocialLink
from .forms import RegistrationForm

def home(request):
    featured_posts = Blog.objects.filter(is_featured=True, status='Published').order_by('-updated_at')
    posts = Blog.objects.filter(is_featured=False, status='Published').order_by('-created_at')
    recent_posts = Blog.objects.filter(status='Published').order_by('-created_at')[:5]
    all_posts_count = Blog.objects.filter(status='Published').count()

    try:
        about = About.objects.get()
    except Exception:
        about = None

    try:
        social_links = SocialLink.objects.all()
    except Exception:
        social_links = []

    try:
        categories = Category.objects.all()
    except Exception:
        categories = []

    context = {
        'featured_posts': featured_posts,
        'posts': posts,
        'recent_posts': recent_posts,
        'all_posts_count': all_posts_count,
        'about': about,
        'social_links': social_links,
        'categories': categories,
    }
    return render(request, 'home.html', context)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Account created successfully! Please login with your credentials.')
            
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RegistrationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'register.html', context)


def login(request):
    # IF USER IS ALREADY LOGGED IN, REDIRECT THEM
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('dashboard')
        else:
            return redirect('home')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                
                if user.is_staff:
                    return redirect('dashboard')
                else:
                    return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'login.html', context)


def logout(request):
    auth.logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

# ===========================================
# CUSTOM ERROR PAGES
# ===========================================

def custom_404(request, exception=None):
    """
    Custom 404 page handler — works from handler404 and catch-all URL.
    """
    # Get data for the 404 page
    try:
        categories = Category.objects.all()[:8]  # Limit to 8 for mobile
    except:
        categories = []
    
    try:
        about = About.objects.first()
    except:
        about = None
    
    try:
        social_links = SocialLink.objects.all()
    except:
        social_links = []
    
    context = {
        'categories': categories,
        'about': about,
        'social_links': social_links,
        'request': request,  # Pass request to template
    }
    
    return render(request, '404.html', context, status=404)


def custom_500(request):
    """
    Custom 500 page handler
    """
    context = {
        'message': 'Something went wrong on our server. Please try again later.',
    }
    return render(request, '500.html', context, status=500)


def custom_403(request, exception):
    """
    Custom 403 page handler
    """
    context = {
        'message': 'You do not have permission to access this page.',
    }
    return render(request, '403.html', context, status=403)


def custom_400(request, exception):
    """
    Custom 400 page handler
    """
    context = {
        'message': 'Bad request. Please check your input and try again.',
    }
    return render(request, '400.html', context, status=400)



