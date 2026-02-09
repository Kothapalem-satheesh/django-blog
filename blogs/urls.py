from django.urls import path
from . import views


urlpatterns = [
    path('<int:category_id>/', views.posts_by_category, name='posts_by_category'),
    path('test-404/', views.custom_404, name='test_404'),
    # path('<path:unknown>/', views.custom_404, name='custom_404'),
]

# IMPORTANT: Catch-all pattern MUST BE LAST
urlpatterns.append(path('<path:unknown>/', views.custom_404))