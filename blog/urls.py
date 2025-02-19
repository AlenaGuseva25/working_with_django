from django.urls import path
from blog.views import BlogListView, BlogCreateView, BlogDetailView, BlogDeleteView, BlogUpdateView



app_name = 'blog'



urlpatterns = [
    path('', BlogListView.as_view(), name='blogpost_list'),
    path('post/<int:pk>/', BlogDetailView.as_view(), name='blogpost_detail'),
    path('post/new/', BlogCreateView.as_view(), name='blogpost_create'),
    path('post/<int:pk>/edit/', BlogUpdateView.as_view(), name='blogpost_update'),
    path('post/<int:pk>/delete/', BlogDeleteView.as_view(), name='blogpost_delete'),
]
