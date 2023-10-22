from django.urls import path
from django.views.decorators.cache import cache_page

# from django.views.decorators.cache import cache_page
from blog.views import (
    BlogListView,
    BlogCreateView,
    BlogDetailView,
    BlogUpdateView,
    BlogDeleteView,
    HomeListView
)

app_name = 'blog'


urlpatterns = [
    path('', HomeListView.as_view(), name='blog_home'),
    path('blog/', cache_page(60)(BlogListView.as_view()), name='blog'),
    path('create/', BlogCreateView.as_view(), name='blog_create'),
    path('<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('<int:pk>/update/', BlogUpdateView.as_view(), name='blog_update'),
    path('<int:pk>/delete/', BlogDeleteView.as_view(), name='blog_delete'),
]