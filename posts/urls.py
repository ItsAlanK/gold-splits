from django.urls import path
from . import views


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('posts', views.AllPosts.as_view(), name='posts'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_page'),
    path('like/<slug:slug>', views.AddLike.as_view(), name='add_like'),
    path('create', views.CreatePost.as_view(), name='create_post'),
    path('edit/<slug:slug>/', views.EditPost.as_view(), name='edit_post'),
    path('delete/<slug:slug>/', views.DeletePost.as_view(), name='delete_post'),
    path('category/<str:name>/', views.category, name='category_page'),
    path('search-results', views.search_results, name='search_results'),
]
