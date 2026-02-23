from .models import Category, Bookmark
from assignments.models import SocialLink


def get_categories(request):
    categories = Category.objects.all()
    return dict(categories=categories)


def get_social_links(request):
    social_links = SocialLink.objects.all()
    return dict(social_links=social_links)


def get_user_bookmarks(request):
    """Return the set of blog IDs the current user has bookmarked."""
    if request.user.is_authenticated:
        try:
            bookmarked_ids = set(
                Bookmark.objects.filter(user=request.user).values_list('blog_id', flat=True)
            )
        except Exception:
            bookmarked_ids = set()
        return {'bookmarked_ids': bookmarked_ids}
    return {'bookmarked_ids': set()}
