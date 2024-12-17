from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('posts/create/', views.create_post, name='create_post'),
    path('posts/edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('posts/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('posts/like/<int:post_id>/', views.toggle_like, name='toggle_like'),
    path('register/', views.register, name='register'),
]
